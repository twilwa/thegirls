# Verifiers Package: A Complete Wiki

## Overview

**Verifiers** is a comprehensive Python framework for building, evaluating, and fine-tuning language models (LMs) in reinforcement learning (RL) workflows, particularly within the Recursive Language Models (RLM) paradigm. It provides unified abstractions for environment design, reward specification, and model rollout evaluation.

**Version**: 0.1.9.post3

**Purpose**: Verifiers bridges the gap between LM inference and RL training by providing:
- Standardized task environments for model evaluation
- Flexible reward/rubric systems for scoring outputs
- Parsers for structured LM outputs (XML, thinking tags, etc.)
- Integration with various inference backends and training frameworks
- Support for single-turn, multi-turn, and tool-using agent interactions

---

## 1. Architecture Overview

### Core Components

The verifiers package is organized into five primary modules:

```
verifiers/
├── parsers/          # Output parsing and extraction
├── rubrics/          # Reward functions and evaluation metrics
├── envs/             # Task environments for model rollouts
├── rl/               # Reinforcement learning training (optional)
├── types.py          # Type definitions and data structures
├── errors.py         # Exception hierarchy
├── decorators.py     # Decorators for environment lifecycle
└── utils/            # Utility functions across submodules
```

### Data Flow

1. **Environment** defines a task (dataset, evaluation criteria)
2. **Rollout**: Model generates completions for prompts
3. **Parser**: Extracts structured answers from model outputs
4. **Rubric**: Scores answers using reward functions
5. **Trainer** (optional): Uses scores to optimize model weights

---

## 2. Key Classes and Functions

### 2.1 Types and State Management

**File**: `verifiers/types.py`

#### Core TypedDicts

| Type | Purpose |
|------|---------|
| `State` | Mutable dictionary tracking rollout state across generation and scoring |
| `TrajectoryStep` | Individual step in a multi-turn conversation with tokens and rewards |
| `RolloutInput` | Input specification: prompt, task, example ID, optional answer/info |
| `RolloutScore` | Score output: reward float and metrics dict |
| `GenerateOutputs` | Batch generation results with metadata |
| `ProcessedOutputs` | Tokenized and masked outputs ready for training |

#### State Fields

The `State` object is the central context object:

```python
class State(dict):
    # Input fields (forwarded from RolloutInput)
    prompt: Messages
    answer: str
    task: str
    info: Info
    example_id: int

    # Execution fields
    client: AsyncOpenAI
    model: str
    sampling_args: SamplingArgs

    # Output fields
    completion: Messages
    trajectory: list[TrajectoryStep]
    reward: float
    metrics: dict[str, float]
    is_completed: bool
    is_truncated: bool
    error: Error
```

#### EvalConfig

Configuration Pydantic model for environment evaluation:

```python
class EvalConfig(BaseModel):
    env_id: str
    env_args: dict
    model: str
    sampling_args: dict
    num_examples: int
    rollouts_per_example: int
    max_concurrent: int
```

### 2.2 Parsers

**File**: `verifiers/parsers/parser.py` and submodules

Parsers extract structured answers from LM outputs.

#### Base Parser

```python
class Parser:
    def __init__(self, extract_fn: Callable[[str], str] = lambda x: x):
        self.extract_fn = extract_fn

    def parse(self, text: str) -> Any:
        """Parse raw text output."""
        return self.extract_fn(text)

    def parse_answer(self, completion: Messages) -> str | None:
        """Extract final answer from completion."""
```

**Features**:
- Customizable extraction function
- Helper methods to filter messages by role (assistant, user, tool, system)
- Format validation with `get_format_reward_func()`

#### ThinkParser

Specialized for models using reasoning tags like Claude 3.5's thinking feature.

```python
class ThinkParser(Parser):
    def parse(self, text: str) -> str:
        # Extracts content after </think> tags
        if "</think>" in text:
            return text.split("</think>")[-1].strip()
        return ""
```

**Use cases**:
- Extended reasoning models (Claude with extended thinking)
- Models that output explicit reasoning before answers

**Warning**: Only use with models that preserve `<think>` tags; some models automatically parse them.

#### XMLParser

Flexible parser for structured XML output with multiple field support.

```python
class XMLParser(Parser):
    def __init__(
        self,
        fields: list[str | tuple[str, ...]],
        answer_field: str = "answer",
        extract_fn: Callable[[str], str] = lambda x: x,
    ):
        # fields can be simple strings or tuples of alternatives
        # e.g., ["reasoning", ("code", "answer")]
```

**Features**:
- Field alternatives (multiple acceptable tag names for one field)
- Regex-based parsing with proper tag matching
- Format scoring based on field presence and structure
- Conversion to namespace object for attribute access

**Example**:

```python
parser = XMLParser(
    fields=["reasoning", ("code", "answer")],
    answer_field="answer"
)

# Parse: <reasoning>...</reasoning><answer>42</answer>
result = parser.parse(text)
print(result.reasoning)  # Access parsed fields as attributes
print(result.answer)

# Format output
formatted = parser.format(reasoning="...", code="...")
```

### 2.3 Rubrics

**File**: `verifiers/rubrics/rubric.py` and submodules

Rubrics define reward functions for evaluating model outputs.

#### Rubric Class

```python
class Rubric:
    def __init__(
        self,
        funcs: list[RewardFunc | GroupRewardFunc] | None = None,
        weights: list[float] | None = None,
        parser: Parser | None = None,
    ):
```

**Components**:
- **Reward Functions**: Callable[(state/outputs) -> float] or [float]
- **Weights**: Linear combination weights for multiple functions
- **Parser**: Optional parser for answer extraction

#### Reward Function Types

**Individual-level** (per rollout):
```python
def accuracy(completion, answer, **kwargs) -> float:
    extracted = parser.parse_answer(completion)
    return 1.0 if extracted == answer else 0.0
```

**Group-level** (batch-wise):
```python
def ranking_reward(completions, answers, **kwargs) -> list[float]:
    # Compute relative scores across a batch
    return scores
```

#### Methods

| Method | Purpose |
|--------|---------|
| `add_reward_func(func, weight)` | Add individual reward function |
| `add_metric(func, weight=0)` | Add non-weighted metric (for tracking only) |
| `score_rollout(state, score_sem)` | Score single rollout (individual funcs only) |
| `score_rollouts(states, score_sem)` | Score batch with group functions |

#### Detection Logic

The rubric automatically detects function type by inspecting:
- Parameter names (plural names → group function: `states`, `completions`)
- Return type annotation
- Signature to determine required parameters

#### JudgeRubric

Specialized rubric for LLM-based evaluation:

```python
class JudgeRubric(Rubric):
    # Uses another LLM to evaluate model outputs
    # Supports custom judge prompts and scoring criteria
```

### 2.4 Environments

**File**: `verifiers/envs/environment.py` and submodules

Environments encapsulate tasks and orchestrate rollouts.

#### Base Environment Class

```python
class Environment(ABC):
    def __init__(
        self,
        dataset: Dataset | None = None,
        system_prompt: str | None = None,
        few_shot: list[ChatMessage] | None = None,
        parser: Parser | None = None,
        rubric: Rubric | None = None,
        sampling_args: SamplingArgs | None = None,
        message_type: MessageType = "chat",
        oai_tools: list[ChatCompletionToolParam] | None = None,
        max_workers: int = 512,
        env_id: str | None = None,
        **kwargs,
    ):
```

**Key Fields**:
- `dataset`: Hugging Face Dataset with examples
- `eval_dataset`: Separate evaluation set
- `system_prompt`: System context for all rollouts
- `few_shot`: Demonstration examples
- `parser`: Output parser
- `rubric`: Reward functions
- `oai_tools`: OpenAI tools schema for function calling

**Lifecycle Methods**:

```python
@stop(priority=10)
async def my_stop_condition(self, state: State) -> bool:
    """Return True to halt rollout."""

@cleanup(priority=5)
async def my_cleanup(self, state: State):
    """Called after each rollout completes."""

@teardown(priority=0)
async def my_teardown(self):
    """Called when environment is destroyed."""
```

#### SingleTurnEnv

Single-turn Q&A tasks (default max_turns=1):

```python
class SingleTurnEnv(MultiTurnEnv):
    def __init__(self, **kwargs):
        super().__init__(max_turns=1, **kwargs)
```

**Typical workflow**:
1. Model receives system prompt + few-shot + user query
2. Model generates one response
3. Response is parsed and scored

#### MultiTurnEnv

Multi-turn conversation environments:

```python
class MultiTurnEnv(Environment):
    async def env_response(
        self, messages: Messages, state: State, **kwargs
    ) -> Messages:
        """Define environment's response to model messages."""
```

Useful for:
- Dialogue tasks
- Problem-solving with intermediate steps
- Tool use requiring feedback loops

#### ToolEnv / StatefulToolEnv

Environments where models can call tools:

```python
class ToolEnv(Environment):
    # Tools available to the model during rollout
    oai_tools: list[ChatCompletionToolParam]
```

`StatefulToolEnv` maintains state across tool calls, enabling:
- File operations
- Database interactions
- Stateful APIs

#### Environment Execution

**Main method**: `rollout()`

```python
async def rollout(
    state: State,
    client: AsyncOpenAI,
    model: str,
    sampling_args: SamplingArgs | None = None,
) -> State:
    """Generate completion, parse, and score."""
```

**Returns**: Updated state with `completion`, `reward`, `metrics`, `trajectory`

### 2.5 Error Handling

**File**: `verifiers/errors.py`

Exception hierarchy for structured error handling:

```
Error (base)
├── ModelError
│   └── EmptyModelResponseError
├── ToolError
│   ├── ToolParseError
│   └── ToolCallError
├── OverlongPromptError
└── InfraError
    └── SandboxError
```

**Usage**:
```python
from verifiers import ModelError, OverlongPromptError

try:
    result = await env.rollout(state)
except OverlongPromptError:
    # Handle context length exceeded
except ModelError as e:
    # Handle model API errors
```

### 2.6 Decorators

**File**: `verifiers/decorators.py`

Lifecycle decorators for environments:

#### @stop

Marks a stop condition (halts rollout when True):

```python
@vf.stop(priority=10)
async def max_depth_reached(self, state: State) -> bool:
    return len(state["trajectory"]) >= 10

@vf.stop()
async def error_occurred(self, state: State) -> bool:
    return state.get("error") is not None
```

Higher priority runs first. Ties broken alphabetically.

#### @cleanup

Post-rollout cleanup (called after each rollout):

```python
@vf.cleanup(priority=5)
async def log_completion(self, state: State):
    print(f"Reward: {state.get('reward')}")
```

#### @teardown

Environment teardown (called during cleanup):

```python
@vf.teardown()
async def close_resources(self):
    await self.db.close()
```

---

## 3. RLM (Recursive Language Models) Integration

### 3.1 RLM Paradigm

From [RLM paper](https://alexzhang13.github.io/blog/2025/rlm/), RLMs extend LMs to handle unbounded-length contexts by:

1. **Decomposition**: Breaking complex problems into manageable sub-problems
2. **Recursion**: Models can spawn sub-LLM calls to process chunks
3. **REPL Integration**: Root model interacts with environment (Python REPL) that stores context

### 3.2 RLMEnv

**File**: `verifiers/envs/experimental/rlm_env.py` (referenced in README)

**Features**:
- Python REPL environment for context storage
- Support for recursive sub-LLM calls
- Tool integration for document processing
- Ability to handle contexts of unbounded length

**Architecture**:
```
Root LLM → Python REPL (context variable)
    ↓
[Can spawn sub-LLM calls for chunks]
    ↓
Scores based on final result
```

### 3.3 Integration with Verifiers

Verifiers enables RLM training via:

1. **Environments**: Define tasks suitable for decomposition
2. **Parsers**: Extract structured sub-task outputs
3. **Rubrics**: Score recursive problem decomposition
4. **RLTrainer**: Fine-tune models for improved decomposition

**Example workflow**:
```python
env = RLMEnv(
    dataset=long_documents_dataset,
    rubric=question_answering_rubric,
    parser=structured_parser,
)

outputs = await env.generate(
    model="claude-opus-4",
    num_examples=100,
    rollouts_per_example=4,
)
```

---

## 4. Data Serialization Utilities

**File**: `verifiers/utils/rlm_data_serialization_utils.py`

Specialized utilities for RLM trajectory data:

- Serialize/deserialize nested LLM call hierarchies
- Save trajectory data with recursive structure
- Export for analysis and visualization

---

## 5. Usage Patterns

### 5.1 Basic Single-Turn Evaluation

```python
import verifiers as vf
from datasets import load_dataset

# Define reward function
def exact_match(completion, answer, **kwargs) -> float:
    extracted = parser.parse_answer(completion)
    return 1.0 if extracted == answer else 0.0

# Create parser
parser = vf.XMLParser(["reasoning", "answer"], answer_field="answer")

# Create rubric
rubric = vf.Rubric(
    funcs=[exact_match],
    weights=[1.0],
    parser=parser,
)

# Create environment
dataset = load_dataset("path/to/dataset", split="train")
env = vf.SingleTurnEnv(
    dataset=dataset,
    parser=parser,
    rubric=rubric,
    system_prompt="Answer the following question:\n",
)

# Generate rollouts
outputs = await env.generate(
    model="gpt-4",
    num_examples=10,
    rollouts_per_example=1,
)

print(f"Average reward: {sum(outputs['reward']) / len(outputs['reward'])}")
```

### 5.2 Multi-Turn Agent Environment

```python
class CustomEnv(vf.MultiTurnEnv):
    async def env_response(self, messages, state, **kwargs):
        # Environment provides feedback to agent
        user_input = state.get("user_input")
        return [{"role": "assistant", "content": f"Got: {user_input}"}]

env = CustomEnv(
    dataset=dataset,
    max_turns=5,
    rubric=rubric,
)

outputs = await env.generate(model="gpt-4", num_examples=5)
```

### 5.3 XML-Structured Outputs

```python
# Configure parser for specific XML schema
parser = vf.XMLParser(
    fields=[
        "problem_analysis",
        ("solution", "code"),  # Alternatives
        "verification",
    ],
    answer_field="solution",
)

# Define reward checking format compliance
format_reward = parser.get_format_reward_func()

# Combine with accuracy reward
def accuracy_reward(completion, answer, **kwargs):
    extracted = parser.parse_answer(completion)
    return 1.0 if str(extracted) == str(answer) else 0.0

rubric = vf.Rubric(
    funcs=[format_reward, accuracy_reward],
    weights=[0.2, 0.8],  # Emphasize correctness
)

# Generate outputs
outputs = await env.generate(model="gpt-4", num_examples=100)

# Access parsed results
for completion, reward in zip(outputs["completion"], outputs["reward"]):
    parsed = parser.parse_answer(completion)
    print(f"Solution: {parsed.solution}, Format score contribution: {reward * 0.2}")
```

### 5.4 Thinking-based Reasoning

```python
# For models with extended thinking (Claude 3.5)
parser = vf.ThinkParser(
    extract_fn=lambda x: x.strip().split('\n')[-1]  # Last line after thinking
)

rubric = vf.Rubric(
    funcs=[
        parser.get_format_reward_func(),  # Check for think tags
        exact_match,  # Correctness
    ],
    weights=[0.1, 0.9],
)

env = vf.SingleTurnEnv(
    dataset=dataset,
    parser=parser,
    rubric=rubric,
)
```

### 5.5 Tool-Using Environments

```python
# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the web",
            "parameters": {...}
        }
    }
]

class SearchEnv(vf.ToolEnv):
    async def handle_tool_call(self, tool_name, tool_input, state):
        if tool_name == "search":
            return await self.search_api(tool_input)

env = SearchEnv(
    dataset=dataset,
    oai_tools=tools,
    rubric=rubric,
)
```

### 5.6 Reinforcement Learning Training

```python
from verifiers import RLConfig, RLTrainer

config = RLConfig(
    model="Qwen/Qwen3-4B-Instruct",
    env_id="alphabet-sort",
    learning_rate=1e-5,
    batch_size=512,
    rollouts_per_example=16,
    max_steps=500,
    use_lora=True,
    lora_rank=16,
)

trainer = RLTrainer(config=config)
trainer.train()
```

---

## 6. Dependencies and Integration Points

### 6.1 External Dependencies

| Package | Purpose | Integration Point |
|---------|---------|-------------------|
| `openai` | LM API access (async) | Client configuration, API calls |
| `datasets` | Hugging Face datasets | Environment data loading |
| `pydantic` | Configuration validation | Config models (EvalConfig, ClientConfig) |
| `accelerate` | Distributed training | RLTrainer distributed setup |
| `transformers` | Model loading | RLTrainer model management |
| `vllm` (optional) | Fast inference | RLTrainer inference server |

### 6.2 Configuration Sources

Environments can be loaded from:

1. **Python code** (manual instantiation)
2. **Environment registry** (via `load_environment`)
3. **HuggingFace Hub** (pre-configured environments)

```python
env = vf.load_environment(
    env_id="kalomaze/alphabet-sort",
    dataset=dataset,
)
```

### 6.3 Extensibility Points

**Custom environments**:
```python
class MyEnv(vf.Environment):
    async def env_response(self, messages, state, **kwargs):
        # Custom logic
        pass

    @vf.stop()
    async def my_stop_condition(self, state):
        # Custom stopping
        pass
```

**Custom reward functions**:
```python
def my_reward(completion, answer, state, **kwargs) -> float:
    # Access full state context
    return compute_score(completion, answer, state)

rubric.add_reward_func(my_reward, weight=1.0)
```

**Custom parsers**:
```python
class MyParser(vf.Parser):
    def parse(self, text):
        # Custom extraction logic
        return result

    def parse_answer(self, completion):
        # Custom answer extraction
        return answer
```

### 6.4 Output Formats

Environments produce outputs following `GenerateOutputs` TypedDict:

```python
{
    "prompt": [...],           # List of input prompts
    "completion": [...],       # List of model completions
    "answer": [...],           # List of extracted answers
    "reward": [...],           # List of reward scores
    "metrics": {...},          # Dict[metric_name, list[scores]]
    "state": [...],            # Full State objects for debugging
    "metadata": {...},         # Experiment metadata
}
```

Can be saved to:
- Hugging Face Hub (with `save_to_hf_hub=True`)
- Local parquet files
- JSON for analysis

---

## 7. Experimental and Integration Environments

**File**: `verifiers/envs/experimental/` and `verifiers/envs/integrations/`

### GymEnv

Universal wrapper for OpenAI Gym / Gymnasium-compatible environments.

### MCPEnv

Model Context Protocol (MCP) server integration for tool-based agents.

### CliAgentEnv

Sandbox environment for custom agent code via HTTP proxy interception.

### HarborEnv

Loads Harbor-format task specifications with structured evaluation.

### ReasoningGymEnv, TextArenaEnv

Third-party benchmark integrations.

---

## 8. Logging and Debugging

### Setup Logging

```python
vf.setup_logging(
    level="DEBUG",
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Or via environment variable
import os
os.environ["VF_LOG_LEVEL"] = "DEBUG"
```

### Utilities

**Print sample completions**:
```python
vf.print_prompt_completions_sample(outputs)
```

**Extract answers**:
```python
answer = vf.extract_boxed_answer(text)  # Searches for \boxed{...}
answer = vf.extract_hash_answer(text)   # Searches for ###...
```

---

## 9. Advanced Topics

### 9.1 Group-Level Reward Functions

For batch-wise scoring (e.g., relative ranking):

```python
def ranking_reward(completions, answers, **kwargs) -> list[float]:
    """Score completions relative to each other."""
    scores = rank_completions(completions, answers)
    return scores

rubric = vf.Rubric(funcs=[ranking_reward])
outputs = await env.generate(...)  # Uses score_rollouts internally
```

### 9.2 Custom Stop Conditions

Control rollout termination:

```python
class SearchEnv(vf.ToolEnv):
    @vf.stop(priority=5)
    async def max_tool_calls_reached(self, state):
        tool_calls = sum(
            1 for step in state["trajectory"]
            if step.get("tool_call")
        )
        return tool_calls >= 10
```

### 9.3 Async Tool Execution

Tools can be async-aware:

```python
async def async_tool(query: str) -> str:
    result = await expensive_api_call(query)
    return result

class SearchEnv(vf.ToolEnv):
    async def handle_tool_call(self, tool_name, tool_input, state):
        if tool_name == "search":
            return await async_tool(tool_input["query"])
```

### 9.4 Multi-Model Evaluation

Compare models on same environment:

```python
env = vf.SingleTurnEnv(...)

results = {}
for model in ["gpt-4", "claude-opus-4", "llama-70b"]:
    outputs = await env.generate(
        model=model,
        num_examples=100,
        rollouts_per_example=4,
    )
    results[model] = {
        "avg_reward": sum(outputs["reward"]) / len(outputs["reward"]),
        "metrics": outputs["metrics"],
    }

for model, metrics in results.items():
    print(f"{model}: {metrics['avg_reward']:.3f}")
```

---

## 10. Quick Reference

### Common Imports

```python
import verifiers as vf
from verifiers import (
    Parser, ThinkParser, XMLParser,
    Rubric, JudgeRubric,
    Environment, SingleTurnEnv, MultiTurnEnv, ToolEnv,
    RLTrainer, RLConfig,
)
```

### Key Methods by Use Case

| Goal | Method |
|------|--------|
| Create environment | `SingleTurnEnv()` or `MultiTurnEnv()` |
| Configure reward | `Rubric(funcs=[...])` |
| Parse outputs | `parser.parse_answer(completion)` |
| Run evaluation | `env.generate(model, num_examples, rollouts_per_example)` |
| Train model | `RLTrainer(config).train()` |
| Load preset | `vf.load_environment(env_id)` |

### Configuration Parameters

```python
# Generation config
sampling_args = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 512,
}

# Training config (RLTrainer)
rl_config = RLConfig(
    learning_rate=1e-5,
    batch_size=512,
    rollouts_per_example=16,
    use_lora=True,
)
```

---

## 11. Related Resources

- **RLM Blog**: https://alexzhang13.github.io/blog/2025/rlm/
- **GitHub**: https://github.com/PrimeIntellect-ai/verifiers
- **Installation**: `pip install verifiers` or `uv add verifiers`
- **With RL support**: `pip install verifiers[rl]` or `uv add 'verifiers[rl]'`

---

## Summary

Verifiers is a production-ready framework for LM evaluation and reinforcement learning. Its modular design separates concerns (parsing, scoring, environment interaction) while providing tight integration for end-to-end workflows. It's particularly well-suited for:

- **Researchers** developing new evaluation metrics
- **ML Engineers** scaling LM inference and training
- **Teams** implementing RLM-based systems
- **Anyone** building LM-powered agents or tools

The framework abstracts away infrastructure complexity while remaining deeply hackable for custom requirements.
