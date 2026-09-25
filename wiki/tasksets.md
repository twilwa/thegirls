# Tasksets: Task Distribution and Orchestration for RLM Agents

## Overview

**Tasksets** is a PyPI package (`v0.1.0`) designed to provide utilities for working with task sets in distributed agent frameworks. While the current implementation is a minimal scaffold, the package is positioned as foundational infrastructure for the RLM (Recursive Language Model) paradigm, particularly within the OpenClaw ecosystem and the broader CICADA-71 agent network.

### Purpose

Tasksets serves as:

1. **Task decomposition layer** — Breaking large problems into tractable subtasks for LLM processing
2. **Distribution mechanism** — Assigning tasks to specialized agents in parallel or sequential patterns
3. **RLM enabler** — Supporting the recursive processing patterns that allow agents to handle inputs beyond their context limits
4. **State management** — Tracking task completion, dependencies, and results across distributed execution

### Current Status

The package is in **early development** (v0.1.0) and consists of:
- A basic Python module scaffold
- Version and export declarations in `__init__.py`
- Packaged via PyPI using the `uv` build system
- Dependencies: Python >=3.10

### Key Use Cases

In the RLM paradigm, tasksets would support:
- Chunking large documents/datasets for divide-and-conquer processing
- Managing task dependencies in orchestration patterns (Captain's Chair, Gas Town)
- Distributing work across agent pools with fault tolerance
- Tracking progress and aggregating results from parallel task execution
- Implementing filter-then-recurse patterns for needle-in-haystack problems

---

## Key Classes and Functions

As of v0.1.0, the package exports:

### Current API

```python
from tasksets import __version__

print(__version__)  # "0.1.0"
```

### Planned Architecture (Inferred from Context)

Based on the RLM patterns in OpenProse and CICADA-71 bot task documentation, tasksets is likely to provide:

#### Task Representations

```python
# Hypothetical - following RLM decomposition patterns
class Task:
    """Represents a single unit of work"""
    id: str
    prompt: str              # The instruction for an LLM
    context: Dict[str, Any] # Input data
    status: str             # pending, running, completed, failed
    result: Optional[Any]   # Output after execution

class TaskSet:
    """Collection of related tasks with dependencies"""
    name: str
    tasks: List[Task]
    dependencies: Dict[str, List[str]]  # task_id -> [dependency_ids]
    execution_strategy: str  # "sequential", "parallel", "divide_conquer"

class TaskResult:
    """Aggregated results from task execution"""
    task_id: str
    output: str  # LLM response
    tokens_used: int
    execution_time: float
    success: bool
```

#### Core Functions

```python
# Hypothetical - matching RLM patterns
def decompose(problem: str, agent: Agent) -> TaskSet:
    """Break a problem into subtasks using an LLM"""
    pass

def distribute(taskset: TaskSet, agents: List[Agent]) -> TaskSet:
    """Assign tasks to agents and execute"""
    pass

def aggregate(results: List[TaskResult]) -> str:
    """Synthesize partial results into final output"""
    pass

def recurse(taskset: TaskSet, depth_limit: int) -> TaskSet:
    """Support recursive task decomposition (core RLM pattern)"""
    pass
```

### Integration Points

The actual implementation would likely expose:

1. **State backend** — SQLite, PostgreSQL, or in-memory storage for task graphs
2. **Agent binding** — Integration with OpenProse agents and Anthropic SDK
3. **Async execution** — Support for concurrent task processing
4. **Retry logic** — Built-in backoff and resilience patterns
5. **Monitoring hooks** — Progress tracking and error reporting

---

## How Tasksets Fits into the RLM Paradigm

### Recursive Language Models: The Problem They Solve

RLMs address a fundamental constraint in working with LLMs: **context limits**.

Standard approaches fail on large inputs:
- **Base LLM on 100K token input**: Gets <0.1% accuracy on complex tasks (quadratic-complexity problems)
- **Base LLM on their context limit**: Exhibits "context rot" — performance degrades as you approach the limit

**RLMs achieve 58% accuracy** on the same quadratic-complexity tasks by treating the problem as an **external environment** the LLM can interact with, query, and decompose.

### The RLM Pattern

```
INPUT (arbitrarily large)
    ↓
[CHUNK] ← Agent asks: "What are the logical divisions?"
    ↓
[PARALLEL RECURSIVE PROCESSING]
    For each chunk:
      - Send to LLM (fits in context)
      - Get partial result
      - Optionally: recurse deeper (chunk the chunk)
    ↓
[AGGREGATE] ← Agent asks: "How do I synthesize these results?"
    ↓
OUTPUT
```

### Where Tasksets Fits

Tasksets would be the **task graph execution engine** for this pattern:

1. **Input decomposition** — Taking "process 500K tokens" and converting it to "process 50 chunks of 10K tokens each"
2. **Recursive chunking** — Supporting multi-level recursion where each chunk can be further decomposed
3. **Parallel execution** — Managing the concurrent LLM calls across agents
4. **Aggregation** — Coordinating the synthesis step
5. **State tracking** — Maintaining the call tree so agents know where to aggregate results

### Examples from the Ecosystem

#### Gas Town (Multi-Agent Orchestration)

In the Gas Town orchestration system (OpenProse example 28), tasksets would:
- Decompose a convoy operation into worker roles (dispatcher, scout, driver, guard, medic)
- Distribute these roles to specialized agents
- Track completion of each task
- Aggregate results into convoy status

#### CICADA-71 Bot Network

In the distributed bot challenge (BOT_TASKS.md), tasksets would:
- Distribute 109 flakes across 108 bots using modulo arithmetic
- Track task completion (test, build, document, ZK proof, report)
- Aggregate results for dashboard reporting
- Support recursive phases (shard processing, special flake handling, verification)

#### Captain's Chair Pattern

The captain's chair orchestration pattern (OpenProse example 29) relies on tasksets for:
- Breaking a problem into research subtasks, execution subtasks, and critic subtasks
- Assigning these in parallel to executor and critic agents
- Waiting for all to complete before the captain synthesizes
- Supporting multi-round cycles of planning → execution → criticism → refinement

---

## Example Usage Patterns

### Pattern 1: Simple Decomposition

```python
from tasksets import TaskSet, Task, decompose

# Define a large problem
problem = """
Analyze all 500 research papers on adversarial robustness,
identify the 5 most impactful trends, and synthesize findings.
"""

# RLM agent decomposes into subtasks
decomposer = Agent(model="claude-opus", system_prompt="Break problems into subtasks")
taskset = decompose(problem, decomposer)
# → Creates 10 subtasks: "Analyze papers 1-50 on theme A", "Analyze papers 51-100 on theme A", etc.

# Execute in parallel
results = execute_parallel(taskset)

# Aggregate
synthesizer = Agent(model="claude-opus")
final = synthesizer.synthesize(results)
```

### Pattern 2: Recursive Divide-and-Conquer

```python
from tasksets import recurse, distribute

# Process a huge dataset recursively
data = load_large_dataset()  # 10M records

# Recursive decomposition
# Level 1: Divide into 1000 chunks
# Level 2: Send each chunk to LLM (if still too large, divide further)
# Level 3: For chunks that remain, process directly

taskset = recurse(
    data,
    decomposer_agent,
    depth_limit=3,
    chunk_strategy="log-linear"  # Logarithmic fanout
)

results = distribute(taskset, agent_pool)
aggregated = aggregate_tree(results)  # Tree aggregation, not linear
```

### Pattern 3: Filter-Then-Recurse (Needle-in-Haystack)

```python
from tasksets import filter_tasks, recurse

# Find anomalies in 1M records
records = load_records()

# Stage 1: Cheap filtering (parallelizable, no LLM needed)
candidates = fast_filter(records, criteria="suspicious")  # 500 candidates

# Stage 2: Deep analysis on candidates only
taskset = decompose_for_analysis(candidates, agent)
results = execute(taskset)

# Only "expensive" LLM calls on promising candidates
```

### Pattern 4: Pairwise Aggregation (O(n²) Tasks)

```python
from tasksets import pairwise_tasks, aggregate_pairwise

# Compare 1000 research papers in a semantic graph
papers = load_papers()

# Instead of O(n²) = 1M comparisons all at once,
# decompose into hierarchical batches

# Batch 1: Compare papers [0-100] all to each other (100 pairs)
# Batch 2: Compare papers [101-200] all to each other (100 pairs)
# ...
# Batch 2: Cross-compare batch results hierarchically

taskset = pairwise_tasks(papers, batch_size=100, agent=compare_agent)
results = execute(taskset)
graph = aggregate_pairwise(results)  # O(n log n) aggregation
```

### Pattern 5: Integration with OpenProse Orchestration

```prose
# In an OpenProse script, tasksets enable RLM patterns

agent decomposer:
  model: opus
  prompt: "Break problems into logical chunks"

agent processor:
  model: sonnet
  prompt: "Process a chunk deeply"

agent synthesizer:
  model: opus
  prompt: "Synthesize partial results"

# Define the task graph
let taskset = session: decomposer
  prompt: "Break this large input into 10 logical chunks"

# Execute in parallel
parallel for chunk in taskset.chunks:
  let result = session: processor
    context: chunk

# Synthesize
output final = session: synthesizer
  context: results
  prompt: "Synthesize all partial results"
```

---

## Dependencies and Integration Points

### Current Dependencies

From `tasksets-0.1.0.dist-info/METADATA`:
```
Name: tasksets
Version: 0.1.0
Requires-Python: >=3.10
Summary: Utilities for working with task sets
```

**No external dependencies listed** in the current scaffold.

### Planned Dependencies (Inferred)

Based on RLM integration with the ecosystem, tasksets would likely depend on:

#### Core Dependencies

1. **Anthropic SDK** (`anthropic`)
   - Direct LLM calls for decomposition and aggregation
   - Token counting for context awareness
   - Streaming support for real-time task updates

2. **OpenProse Integration** (`openprose`)
   - Tasksets as a native skill in the OpenProse language
   - Syntactic sugar for task decomposition in `.prose` files
   - Direct execution within OpenProse's session context

3. **State Management**
   - `sqlalchemy` — Support for PostgreSQL/SQLite backends
   - `pydantic` — Type-safe task representations
   - `redis` — Optional: distributed task queue

#### Integration Dependencies

4. **Async Runtime**
   - `asyncio` (stdlib) for async execution
   - `anyio` (optional) for unified async abstraction

5. **Error Handling & Monitoring**
   - Custom retry logic with exponential backoff
   - Integration with observability stacks (Datadog, Sentry)
   - Structured logging (`structlog` or similar)

6. **Agent Frameworks**
   - Compatible with CrewAI agent definitions
   - Integration with ElizaOS task patterns
   - LangChain tool use for skill binding

### Integration with Existing Systems

#### OpenClaw Ecosystem

Tasksets would be:
- A **core skill** in the OpenClaw agent framework
- Available in all agent contexts (OpenProse, REST API, Discord agents)
- Bound to agent permissions (read/write constraints per task)
- Cacheable (memoization of task decompositions)

#### CICADA-71 Bot Network

For the distributed bot challenge:
- **Bot task assignment** via tasksets decomposition
- **Shard distribution** following `bot_id % 71 == shard` patterns
- **ZK proof generation** after taskset completion
- **BBS reporting** of task status (success/failure/proofs)

#### Lightshell Voice Agent

Tasksets would support:
- Breaking long user requests into decomposable voice commands
- Managing multi-turn task execution across voice channel sessions
- Aggregating results for TTS output synthesis

#### Letta Memory System

Integration points:
- Storing task contexts in Letta's long-term memory
- Using task execution history for retrospective learning
- Inferring user intent from patterns in task decompositions

---

## Architecture & Data Flow

### Conceptual Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (OpenProse, Agent, User)                 │
│         Input: "Process 500K tokens"                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ TASKSETS DECOMPOSITION LAYER                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Input → Decomposer Agent → Task Graph              │  │
│  │ (LLM decides: how many chunks? what strategy?)     │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                          │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │ Task Representation:                                │  │
│  │ - Task ID, Prompt, Context, Status, Result         │  │
│  │ - Dependencies (for DAG execution)                  │  │
│  │ - Recursion metadata (depth, parent, aggregation)  │  │
│  └──────────────┬──────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ EXECUTION LAYER                                             │
│                                                             │
│  ┌──────────────┬──────────────┬──────────────────────┐   │
│  │              │              │                      │   │
│  ▼              ▼              ▼                      ▼   │
│ Task 1→ Task 2→ Task 3→ ... Task N [PARALLEL]       │   │
│  │              │              │                      │   │
│  └──────────────┴──────────────┴──────────────────────┘   │
│         ↓                ↓                ↓                │
│      Agent 1         Agent 2          Agent N             │
│  (Process chunks,  (Refine,        (Lookup,             │
│   aggregate,       verify,         format)              │
│   recurse)         synthesize)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ STATE LAYER                                                 │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Task Graph Storage:                                  │  │
│  │ - SQLite/PostgreSQL with call tree structure         │  │
│  │ - Task status, results, timing, errors              │  │
│  │ - Enables retries, debugging, observability         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ AGGREGATION LAYER                                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Synthesizer Agent: Combines partial results         │  │
│  │ - May be recursive (aggregate-then-aggregate)       │  │
│  │ - May require multiple passes (refinement)          │  │
│  │ Output: Final result fitting in context             │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ APPLICATION OUTPUT                                          │
│         Result: "The 5 key findings are..."               │
└─────────────────────────────────────────────────────────────┘
```

### Task Execution Graph

For a recursive divide-and-conquer task:

```
INPUT (1M records)
    │
    ├─ Decomposer: "Split into 100 chunks"
    │
    ├─ [Chunk 1] ─┬─ [Rechunk 1.1] → Process → Result 1.1
    │             ├─ [Rechunk 1.2] → Process → Result 1.2
    │             └─ [Rechunk 1.3] → Process → Result 1.3
    │                                    ↓
    │                            Aggregate → Result 1
    │
    ├─ [Chunk 2] → Process → Result 2
    ├─ [Chunk 3] → Process → Result 3
    ...
    └─ [Chunk 100] → Process → Result 100
                                    ↓
                        Synthesizer: Combine all
                                    ↓
                              OUTPUT
```

### State Tracking Example

In the database (SQLite/PostgreSQL):

```sql
-- Task graph table
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  parent_id TEXT,  -- For recursion
  depth INT,
  prompt TEXT,
  context JSONB,
  status ENUM('pending', 'running', 'completed', 'failed'),
  result TEXT,
  tokens_used INT,
  execution_time FLOAT,
  agent_id TEXT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);

-- Example execution:
-- Task root: decompose 1M records
--   ├─ root.1: process chunk 1 (recursive)
--   │   ├─ root.1.1: process subchunk 1.1
--   │   └─ root.1.2: process subchunk 1.2
--   ├─ root.2: process chunk 2
--   ...
```

---

## Current State & Future Roadmap

### Version 0.1.0 (Current)

- Minimal PyPI package scaffold
- Core module and version declaration
- Packaged via `uv` build system
- No implemented functionality yet

### Projected Development Path

Based on the RLM ecosystem and CICADA-71 infrastructure:

#### Phase 1 (0.2.0)
- Core task representations (Task, TaskSet, TaskResult)
- Basic sequential execution
- SQLite state backend
- Integration with Anthropic SDK

#### Phase 2 (0.3.0)
- Parallel execution with asyncio
- Recursive decomposition support
- PostgreSQL backend
- OpenProse skill binding

#### Phase 3 (0.4.0)
- Filter-then-recurse patterns
- Pairwise aggregation for O(n²) problems
- Integration with bot networks
- ZK proof generation hooks

#### Phase 4 (1.0.0)
- Production monitoring and observability
- Distributed task queues (Redis, RabbitMQ)
- Multi-agent coordination frameworks
- Comprehensive documentation and examples

---

## Relationship to Related Packages

### OpenProse (`openprose`)

**OpenProse** is the high-level workflow orchestration language. **Tasksets** is the low-level execution engine that OpenProse uses for task decomposition and distribution.

- **OpenProse**: "What should happen?" (declarative)
- **Tasksets**: "How do we make it happen efficiently?" (imperative)

### Anthropic SDK (`anthropic`)

**Tasksets** would wrap the SDK to:
- Batch API calls for task execution
- Handle token counting for context-aware decomposition
- Support streaming for real-time progress

### Letta (`letta`)

**Letta** provides long-term memory. **Tasksets** would:
- Store task contexts in Letta memory for inter-session learning
- Use Letta's core memory for agent state during task execution
- Learn task decomposition patterns from history

---

## Conclusion

Tasksets is foundational infrastructure for enabling RLM patterns in distributed agent systems. While currently a minimal scaffold, it positions itself as the task graph execution engine that unlocks:

1. **Scalable LLM processing** beyond context limits
2. **Distributed agent coordination** in frameworks like CICADA-71
3. **Recursive decomposition** for hierarchical problem-solving
4. **State management** for observable, debuggable agent systems

The package is designed to integrate seamlessly with:
- OpenProse orchestration language
- OpenClaw agent framework
- Discord voice and text agents (Lightshell)
- Distributed bot networks (CICADA-71)
- Anthropic SDK and Claude models

### Key Takeaways

- **RLMs solve context limits** by treating inputs as external environments
- **Tasksets enables RLMs** through task decomposition, parallel execution, and aggregation
- **The pattern is recursive**: chunks can be further chunked, results can be further synthesized
- **State tracking is critical**: Full call tree visibility enables debugging, retries, and learning
- **Integration is broad**: Works with orchestration languages, agent frameworks, memory systems, and bot networks

---

*Article compiled from tasksets v0.1.0 source, OpenProse RLM documentation, CICADA-71 bot task patterns, and RLM paradigm research.*

*Last updated: 2026-02-09*
