# Harnesses: Runtime Orchestration for Recursive Language Models

## Overview

**Harnesses** is a Python package designed to provide runtime orchestration and execution frameworks for Recursive Language Model (RLM) workflows. It serves as an infrastructure layer that enables structured multi-agent coordination and complex AI task decomposition patterns.

The harnesses package acts as a scaffold system—a foundation upon which complex agent-based workflows can be built, particularly those involving:

- Recursive problem decomposition and synthesis
- Multi-agent orchestration with persistent memory
- Parallel execution and fan-out/fan-in patterns
- Context management for arbitrarily large data flows
- Session isolation and state management

### Key Philosophy

Harnesses enables AI systems to act as "virtual machines" that coordinate and execute complex programs. Rather than a single agent handling an entire task, harnesses allows breaking work into logical sessions managed by a coordination layer, each potentially using specialized agents with different capabilities and memory contexts.

## Core Concepts

### Sessions as Function Calls

In the harnesses/RLM paradigm, a **session** is a unit of work that:

- Spawns a subagent to handle a specific task
- Operates within a defined context and scope
- Returns structured outputs to the coordinator
- May be stateless or persistent across invocations

Sessions are analogous to function calls in traditional programming—they receive inputs, perform computation, and return results.

### Recursive Language Models (RLM)

RLMs are a pattern for solving problems that exceed traditional LLM context limits or require complex multi-step reasoning. The core insight is that language models can orchestrate their own decomposition and synthesis:

**RLM Pattern Structure:**

```
Input (Problem) → Decompose → Parallel Analysis → Synthesize → Output (Solution)
```

Key characteristics:

- **Recursive depth control** — Stop recursion when subproblems fit in context
- **Parallel execution** — Fan out work to multiple agents simultaneously
- **Intelligent synthesis** — Combine partial results while managing conflicts
- **Reference-based context** — Pass pointers to data, not full copies

### Persistent Agents

Agents can maintain state across multiple invocations:

- **Stateless agents** — Fresh session each time (default)
- **Execution-scoped** — Memory dies with the run
- **Project-scoped** — Memory survives across runs in a project
- **User-scoped** — Cross-project memory on the same machine
- **Custom-scoped** — Arbitrary storage location

Example: A "captain" agent that reviews work across multiple steps can remember all prior reviews and maintain coherent architectural decisions.

## Integration with OpenProse

Harnesses is foundational to the **OpenProse VM**, a structured programming environment for LLM orchestration. OpenProse provides a high-level language (`.prose` format) that compiles to harness-based execution patterns.

### OpenProse Language Examples

**Self-Refinement RLM Pattern:**

```prose
agent evaluator:
  model: sonnet
  prompt: "Score 0-100 against criteria. List specific issues."

agent refiner:
  model: opus
  prompt: "Make targeted improvements. Preserve what works."

block refine(content, depth):
  if depth <= 0:
    output content

  let eval = session: evaluator
    prompt: "Evaluate against: {criteria}"
    context: content

  if **score >= 85**:
    output content

  let improved = session: refiner
    prompt: "Fix the identified issues"
    context: { artifact: content, evaluation: eval }

  output do refine(improved, depth - 1)

output result = do refine(artifact, 5)
```

**Divide-and-Conquer for Large Corpus Analysis:**

```prose
block process(data, depth):
  if **data under 50k characters** or depth <= 0:
    output session: analyzer
      prompt: "{query}"
      context: data

  let chunks = session: chunker
    prompt: "Split this corpus"
    context: data

  let partials = []
  parallel for chunk in chunks:
    let result = do process(chunk, depth - 1)
    partials = partials + [result]

  output session: synthesizer
    prompt: "Synthesize for: {query}"
    context: partials

output answer = do process(corpus, 4)
```

**Pairwise Analysis (O(n²) relationships):**

```prose
block analyze(items, rel, depth):
  let all_pairs = do pairs(items)

  if **fewer than 100 pairs** or depth <= 0:
    output all_pairs | pmap:
      session: comparator
        prompt: "Analyze {rel}"
        context: item

  let batches = session "Split into batches of ~25 pairs"
    context: all_pairs

  let results = []
  parallel for batch in batches:
    let batch_results = batch | pmap:
      session: comparator
        prompt: "Analyze {rel}"
        context: item
    results = results + batch_results

  output results
```

## Key Classes and Functions

While the installed harnesses package is currently minimal (v0.0.0), the logical architecture includes these core abstractions:

### Agent Registry

**Purpose:** Track available agents and their configurations.

**Attributes:**
- `name` — Agent identifier
- `model` — Model choice (haiku, sonnet, opus)
- `prompt` — System prompt/instructions
- `persist` — Persistence scope (none, execution, project, user, custom path)
- `context` — Initial context bindings
- `retry_policy` — Failure handling (count, backoff strategy)
- `skills` — Available tool integrations

### Session Coordinator

**Purpose:** Orchestrate execution of sessions and manage their lifecycle.

**Operations:**
- `spawn(agent_config, prompt, context)` — Launch a subagent session
- `resume(agent_name, memory, prompt, context)` — Resume persistent agent with prior memory
- `wait_for_completion()` — Block until session finishes
- `collect_output()` — Retrieve session result
- `propagate_error()` — Handle failures with retry/backoff

### Binding Store

**Purpose:** Hold variable bindings and context references.

**Storage Backends:**
- **Filesystem** — Files in `.prose/runs/{id}/bindings/`
- **In-context** — Narration protocol within conversation
- **SQLite** — Local database (experimental)
- **PostgreSQL** — Networked database (experimental)

**Key Principle:** The VM tracks *references* to bindings, not full values. This enables arbitrarily large context without VM bottleneck.

### Execution State Machine

**Purpose:** Maintain VM state across sessions.

**State Includes:**
- Current statement position
- Active call stack (for nested blocks)
- All variable bindings and their storage locations
- Agent memory references
- Error context and retry state

**State File Format:** Markdown with code blocks for embedding program fragments and execution traces.

### Block Invocation Manager

**Purpose:** Handle block definitions, invocation, recursion, and scope isolation.

**Features:**
- Lexical scoping with shadowing
- Execution ID generation for collision-free variable binding
- Maximum recursion depth enforcement
- Call stack tracking for debugging

## How It Fits into the RLM Paradigm

### Decomposition Without Bottleneck

Traditional approaches have a single LLM orchestrate all work, creating a context bottleneck. Harnesses inverts this:

1. **Coordinator (small context)** — Maintains orchestration logic
2. **Specialist agents (full context)** — Handle actual work
3. **Binding store (external)** — Holds large intermediate values

The coordinator passes *references* to data, not copies, enabling work on problems 100x beyond any single context limit.

### Bounded Recursion

RLM patterns rely on knowing when to stop recursion. Harnesses provides:

- **Discretion conditions** (`**stop when quality is good enough**`) — AI-evaluated termination
- **Depth limits** — Maximum recursion bound to prevent infinite loops
- **Size checks** — Automatic terminal condition when problem fits in one context

### Parallel Execution Coordination

Harnesses orchestrates fan-out/fan-in patterns:

```
Single Large Problem
    ↓
[Decompose] → Chunks A, B, C, D, E
    ↓
[Parallel] → Process A  Process B  Process C  Process D  Process E
    ↓
[Collect] → Results: [RA, RB, RC, RD, RE]
    ↓
[Synthesize] → Final Output
```

Each parallel branch runs independently with full context, then results combine at the synthesis stage.

### Benchmark Performance

RLM patterns significantly outperform base LLMs on complex reasoning:

- **Pairwise Analysis** — Base LLM: <1% accuracy → RLM (OOLONG-Pairs): 58%
- **Complex Decomposition** — Base LLM: token limits hit → RLM: Handles arbitrarily large input
- **Multi-step Refinement** — Base LLM: single pass → RLM: Iterative improvement until quality threshold

## Example Usage Patterns

### 1. Iterative Refinement

Repeatedly improve output until quality threshold:

```python
# Pseudocode concept
refine_harness = Harness("refinement")
content = initial_artifact

for depth in range(5):
    evaluation = refine_harness.spawn_session(
        agent="evaluator",
        prompt=f"Score against: {criteria}",
        context=content
    )

    if evaluation.score >= 85:
        return content

    content = refine_harness.spawn_session(
        agent="refiner",
        prompt="Fix identified issues",
        context={
            "artifact": content,
            "evaluation": evaluation
        }
    )

return content
```

### 2. Divide-and-Conquer Analysis

Analyze corpus too large for single context:

```python
# Pseudocode concept
def analyze(data, depth=0):
    if len(data) < CONTEXT_LIMIT or depth >= MAX_DEPTH:
        return harness.spawn_session(
            agent="analyzer",
            prompt=f"Extract: {query}",
            context=data
        )

    chunks = harness.spawn_session(
        agent="chunker",
        prompt="Split at semantic boundaries",
        context=data
    )

    # Parallel: analyze each chunk recursively
    results = harness.parallel([
        analyze(chunk, depth + 1)
        for chunk in chunks
    ])

    return harness.spawn_session(
        agent="synthesizer",
        prompt=f"Combine for: {query}",
        context=results
    )
```

### 3. Persistent Agent Coordination

Maintain coherent architectural decisions across multiple review cycles:

```python
# Pseudocode concept
captain = PersistentAgent(
    name="captain",
    model="opus",
    scope="project",
    prompt="Coordinate reviews and maintain consistency"
)

# First review
review_1 = captain.resume(
    prompt="Review architecture decisions",
    context=design_doc_v1
)

# Later, in different run, captain remembers prior context
review_2 = captain.resume(
    prompt="Review updated implementation",
    context=code_changes
)
# captain's memory includes review_1, ensuring consistency
```

### 4. Pairwise Relationship Analysis

Identify O(n²) relationships efficiently:

```python
# Pseudocode concept
def analyze_relationships(items, relation_type):
    pairs = generate_pairs(items)

    if len(pairs) < 100:
        # Single pass for small sets
        return harness.parallel([
            harness.spawn_session(
                agent="comparator",
                prompt=f"Analyze {relation_type}",
                context=pair
            )
            for pair in pairs
        ])

    # Batch for larger sets
    batches = batch_pairs(pairs, batch_size=25)

    results = []
    for batch in batches:
        batch_results = harness.parallel([
            harness.spawn_session(
                agent="comparator",
                prompt=f"Analyze {relation_type}",
                context=pair
            )
            for pair in batch
        ])
        results.extend(batch_results)

    return harness.spawn_session(
        agent="mapper",
        prompt=f"Build {relation_type} map",
        context={"items": items, "relationships": results}
    )
```

## Dependencies and Integration Points

### Runtime Dependencies

- **Python >= 3.11** — Minimum version requirement
- **Task Tool** — Spawns subagent sessions (core execution mechanism)
- **Binding Store Backend** — One of:
  - Filesystem (default) — No external deps
  - SQLite — Built-in Python support
  - PostgreSQL — Requires `psycopg2` or async equivalent
  - In-context narration — Text-based state protocol

### Integration Points

#### 1. AI Model Access

Harnesses abstracts model selection:

```python
agent.model = "haiku"   # Fast, cheap, limited reasoning
agent.model = "sonnet"  # Balanced capability/cost
agent.model = "opus"    # Full reasoning, expensive
```

Each session can override the agent's model for specialized work.

#### 2. Tool/Skill Integration

Agents can declare available tools:

```prose
agent researcher:
  model: opus
  skills:
    - web_search
    - database_query
    - file_io
  prompt: "You have access to these tools for research"
```

#### 3. State Persistence Backends

**Filesystem** (default):
```
.prose/runs/{run_id}/
├── state.md
├── bindings/
│   ├── research.md
│   └── analysis.md
└── agents/
    └── captain/
        ├── memory.md
        └── captain-001.md
```

**PostgreSQL** (for networked teams):
```sql
openprose.bindings (
  id, name, run_id, content, storage_path, execution_id, created_at
)
openprose.agents (
  id, agent_name, scope, memory_content, run_id, updated_at
)
```

**In-Context** (for conversation-based state):
```
[Frame+] execution_id: 1, block: "process", depth: 2
[Let] result = ...
[Frame-]
```

#### 4. Error Handling

Integrated retry/backoff mechanisms:

```prose
session "Flaky API"
  retry: 3
  backoff: "exponential"
```

Built-in strategies:
- `none` — Fail immediately
- `linear` — Wait 1s, 2s, 3s, ...
- `exponential` — Wait 1s, 2s, 4s, 8s, ...

#### 5. Context Passing

Reference-based context flow:

```python
# Coordinator doesn't hold full value
context_ref = binding_store.get_location("research_output")
# Passes location, not content
session.run(context=context_ref)
# Subagent reads from storage as needed
```

## Performance Characteristics

### Advantages

1. **Scalability** — Handle problems 100x larger than context limit via recursive decomposition
2. **Parallelism** — Fan out to multiple agents; synthesize results
3. **Cost Efficiency** — Use cheaper models (haiku) for simple steps; reserve expensive models (opus) for complex reasoning
4. **Robustness** — Persistent agents maintain coherence across multiple invocations
5. **Modularity** — Reusable blocks and imported programs reduce duplication

### Tradeoffs

1. **Latency** — Multiple sequential stages add wall-clock time
2. **Context Overhead** — Storing/retrieving bindings has I/O cost (mitigated by reference-based passing)
3. **Coordination Complexity** — More moving parts than single-agent approach
4. **Error Propagation** — Failures in parallel branches require thoughtful handling

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          OpenProse VM (Coordinator)                 │
│  - Parse .prose program                             │
│  - Manage execution state                           │
│  - Evaluate discretion conditions                   │
│  - Spawn and coordinate sessions                    │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    [Session A]   [Session B]   [Session C]
     (Haiku)       (Sonnet)      (Opus)
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │    Binding Store (External) │
        │  - Filesystem              │
        │  - SQLite/PostgreSQL       │
        │  - In-Context Narration    │
        └─────────────────────────────┘
```

## Current State and Future

### Version 0.0.0

The installed harnesses package is currently a minimal scaffold (just version marker and metadata). This is intentional:

- **Design-first approach** — Semantics defined through OpenProse and execution patterns
- **VM as specification** — The execution semantics are described in OpenProse documentation
- **Progressive implementation** — Core functionality emerging through OpenProse runtime

### Evolution

Harnesses is expected to evolve as:

1. **Reference implementation** — Python library with concrete session coordination
2. **Multi-language support** — Adapters for JavaScript, Go, Rust, etc.
3. **Distribution frameworks** — Kubernetes/serverless integration for scaling
4. **Observability layer** — Metrics, traces, debugging tools for RLM workflows

## Related Concepts

- **OpenProse** — High-level language for harness-based orchestration
- **Agent Memory** — Persistent state across invocations
- **Binding Store** — External storage for large intermediate values
- **Discretion** — AI-evaluated conditions (marked with `**...**`)
- **Recursive Language Models (RLM)** — The computational pattern harnesses enables

## References

- OpenProse VM specification: `.prose/skills/prose/prose.md`
- RLM examples:
  - Self-Refinement: `40-rlm-self-refine.prose`
  - Divide-and-Conquer: `41-rlm-divide-conquer.prose`
  - Pairwise Analysis: `43-rlm-pairwise.prose`
- Package repository: https://github.com/willccbb/harnesses
- Author: Will Brown

## Summary

Harnesses provides the runtime foundation for Recursive Language Model orchestration. It enables:

- **Decomposition** of large problems into parallel subproblems
- **Coordination** of multiple AI agents with different capabilities
- **Memory** that persists across agent invocations
- **Scaling** beyond single-context limits through recursive patterns
- **Efficiency** by matching model capability to task difficulty

By inverting the control flow—making the coordinator lightweight and agents specialist—harnesses enables AI systems to tackle problems of unprecedented complexity.
