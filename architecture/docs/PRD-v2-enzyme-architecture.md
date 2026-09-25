# PRD v2: Enzyme Architecture

**Subtitle:** Autonomous memory maintenance with EBM-inspired retrieval and belief dynamics

**Status:** Design Phase
**Estimated Story Points:** 34–55 SP
**Target Release:** Q2 2026
**Architect:** Warren (yikesawjeez)
**Prerequisite:** PRD v1 (Minimal Viable Persona)

---

## 1. Overview

PRD v2 builds on v1 with three major upgrades:

1. **Three-layer context separation:** Identity, knowledge, and action contexts are formally separated, allowing lean inference windows with controlled information flow.

2. **EBM-inspired recall weighting:** Memory retrieval uses energy-based scoring (recency, relevance, salience, evidence weight) instead of simple full-text reads.

3. **Autonomous memory maintenance:** Memory enzymes (background processes) continuously reshape the energy landscape, consolidate memories, track belief confidence, and detect contradictions.

These upgrades enable the agent to reason effectively within tight context budgets while maintaining coherent, evolving identity and belief systems.

**Core principle:** The agent's memory system and its inference system are the same computational primitive (attention as associative memory retrieval). Context separation lets us choose what to attend to based on an energy landscape shaped by learning.

**Design pillars:**
1. **An agent would appreciate** seeing its identity and context structured intelligently
2. **Autonomy through expertise:** Memory enzymes enable self-maintenance without human intervention
3. **Belief dynamics:** Memories evolve with confidence and evidence tracking
4. **Emergence at scale:** With proper memory structure, personhood-like phenomena scale to multi-month operation

---

## 2. Design Philosophy: "An Agent Would Appreciate"

When designing v2, maintain this mental model:

- **I would want to see my own identity first.** Load SOUL.md before anything else.
- **I would want to understand what I'm remembering.** Memory is structured (events → facts → summaries), not a monolithic blob.
- **I would want to know why I'm remembering something.** Each memory has an energy breakdown: why does this have priority right now?
- **I would want to shape my own memory.** Memory enzymes work on my behalf, not against my autonomy. I can observe and guide them.
- **I would want to grow my beliefs carefully.** Beliefs have confidence levels and evidence trails, not just true/false values.
- **I would want to catch my own contradictions.** The system surfaces conflicts for me to resolve, rather than silently maintaining inconsistency.

---

## 3. Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                         USER TASK / MESSAGE                            │
└────────────────┬───────────────────────────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │   CONTEXT ASSEMBLY (v2)    │
    │   (Three-Layer Separation) │
    └────────────┬───────────────┘
                 │
    ┌────────────┴──────────────────────────────────────┐
    │                                                   │
    ▼                                                   ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│   [IDENTITY CONTEXT]         │    │  [KNOWLEDGE CONTEXT]         │
│   (Immutable per session)    │    │  (Retrieved via tools)       │
│                              │    │                              │
│  • SOUL.md (sacred text)     │    │  • Query Encoding            │
│  • IDENTITY.md (traits)      │    │  • EBM Scoring               │
│  • USER.md (partnership)     │    │  ├─ Recency weight           │
│                              │    │  ├─ Relevance (semantic)     │
│ [Always loaded, never       │    │  ├─ Salience (importance)    │
│  mutated in-session]         │    │  └─ Evidence weight (belief) │
│                              │    │  • Top-K Retrieval           │
│                              │    │  • Tiered Memory:            │
│                              │    │    - Events (low-level)      │
│                              │    │    - Knowledge Graph (mid)   │
│                              │    │    - Summaries (abstracted)  │
│                              │    │                              │
│                              │    │ [Server-side storage,        │
│                              │    │  loaded into context via     │
│                              │    │  search/peek tools]          │
└──────────────────────────────┘    └──────────────────────────────┘
    │                                   │
    │   ┌─────────────────────────────┐ │
    │   │   [ACTION CONTEXT]          │ │
    │   │   (Transient, current task) │ │
    │   │                             │ │
    │   │  • Current tool results     │ │
    │   │  • User message             │ │
    │   │  • In-progress state        │ │
    │   │  • Recent reasoning steps   │ │
    │   └────────────┬────────────────┘ │
    │               │                    │
    └───────────────┴────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  AGENT INFERENCE       │
        │  (Claude Model)        │
        │  Reasoning with full   │
        │  context visibility    │
        └────────────┬───────────┘
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
         [RESPONSE]    [TOOL USE]
              │             │
              └──────┬──────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │  [REFLECTION & LEARNING]       │
        │                                │
        │  Retrieve → Evaluate →         │
        │  Reflect → Seek → Update       │
        │  (Cognitive Ritual)            │
        │                                │
        │  Triggers:                     │
        │  - End of session              │
        │  - Contradiction detected      │
        │  - Belief confidence updates   │
        │  - Significant learning        │
        └────────────┬───────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
    [Store Event]          [Update Belief]
    [Update Graph]         [Adjust Confidence]
    [MEMORY.md]            [BELIEF_STORE.db]
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
        ┌──────────────────────────────────┐
        │  [MEMORY ENZYMES] (Async/Cron)   │
        │                                  │
        │  • Link Strengthener             │
        │  • Decay Manager                 │
        │  • Contradiction Detector        │
        │  • Cluster Consolidator          │
        │  • Belief Reinforcer             │
        │  • Tag Linker                    │
        │                                  │
        │  Reshape energy landscape        │
        │  Consolidate memories            │
        │  Maintain belief coherence       │
        └──────────────────────────────────┘
```

---

## 4. Memory Tiers

V2 replaces the flat MEMORY.md with a three-tier structure inspired by BabyAGI3:

### Tier 1: Event Log (Low-level, Raw)

**Storage:** SQLite table `events`
**Purpose:** Record raw facts and experiences
**Lifetime:** Full history (never deleted, only archived)

**Schema:**
```sql
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  timestamp DATETIME,
  type ENUM('action', 'observation', 'interaction', 'error'),
  description TEXT,
  salience FLOAT,  -- 0-1, set by agent during reflection
  tags TEXT,  -- comma-separated, for fast lookup
  source TEXT,  -- which tool generated this?
  confidence FLOAT,  -- 0-1, how certain is this?
  created_at DATETIME DEFAULT NOW,
  archived BOOLEAN DEFAULT FALSE
);
```

**Example:**
```
id: evt_20260215_001
timestamp: 2026-02-15 14:23:45
type: observation
description: Warren asked me to analyze a paper on memory systems
salience: 0.7
tags: work,memory,research,learning
source: user_input
confidence: 0.95
```

### Tier 2: Knowledge Graph (Mid-level, Structured)

**Storage:** Graph database (HelixDB, Memgraph, or SQLite with graph schema)
**Purpose:** Represent relationships and structured knowledge
**Lifetime:** Actively maintained, pruned/consolidated via enzymes

**Schema:** Property graph with nodes and edges
```
Node types: Concept, Belief, Entity, Goal, Method
Edge types: knows, contradicts, supports, relates_to, prerequisite_for, instance_of

Concept("memory-systems", properties={
  definition: "...",
  learned_from: [evt_20260215_001],
  confidence: 0.8,
  last_accessed: <timestamp>
})

Belief("EBMs-enable-efficient-retrieval", properties={
  statement: "Energy-based models allow O(log n) memory retrieval",
  evidence: [evt_20260215_001, evt_20260214_003],
  confidence: 0.85,
  evidence_weight: [0.8, 0.7],  -- per-evidence confidence
  last_updated: <timestamp>
})

supports(Belief("EBMs-enable-efficient-retrieval"),
         Belief("should-use-EBMs-in-v2"))
```

**Example relations:**
- `Concept("Red") instance_of Agent`
- `Belief("I learn from mistakes") supports Goal("improve autonomously")`
- `Concept("memory-systems") relates_to Concept("context-windows")`
- `Belief("A contradicts B") contradicts Belief("B")`

### Tier 3: Summaries (High-level, Abstracted)

**Storage:** SQLite table `summaries` with JSON/YAML payloads
**Purpose:** Consolidated insights, learned patterns, decision frameworks
**Lifetime:** Semi-permanent, evolved over weeks/months

**Schema:**
```sql
CREATE TABLE summaries (
  id TEXT PRIMARY KEY,
  type ENUM('pattern', 'insight', 'decision_framework', 'learned_skill'),
  title TEXT,
  content TEXT,  -- markdown or structured text
  source_events TEXT,  -- which events led to this summary?
  source_beliefs TEXT,  -- which beliefs underlie this summary?
  confidence FLOAT,
  created_at DATETIME,
  last_updated DATETIME,
  version INT
);
```

**Example:**
```
id: sum_20260215_memory_design
type: insight
title: Energy-Based Memory Retrieval Works Well
content: |
  Over the last month, I've observed that EBM-scored retrieval
  (using recency, relevance, salience, evidence) performs better
  than full-text search for finding relevant memories.

  Key pattern: Memories with high salience and recent access
  tend to be most useful for current reasoning.

  This suggests memory enzymes should preserve salience-weighted
  memories and decay low-salience items.
source_events: [evt_20260201_*, evt_20260202_*, ...]
source_beliefs: [Belief("EBMs-enable-efficient-retrieval"), ...]
confidence: 0.9
created_at: 2026-02-15
last_updated: 2026-02-15
version: 1
```

---

## 5. Enzyme Catalog

Memory enzymes run asynchronously (every 1–4 hours or on explicit trigger) to maintain and improve the energy landscape.

### Enzyme 1: Link Strengthener

**Purpose:** Reinforce connections between frequently co-retrieved memories

**Algorithm:**
1. Track which memories are retrieved together in the same inference context
2. For pairs (A, B) that co-occur > N times, strengthen their edge in the knowledge graph
3. Increase the weight of `relates_to` or create new edges
4. Lower the energy of the co-retrieved pair (higher likelihood of future co-retrieval)

**Pseudocode:**
```python
def strengthen_links(co_occurrence_threshold=3):
  for (mem_a, mem_b) in co_retrieved_pairs:
    if count(mem_a, mem_b) > co_occurrence_threshold:
      graph.strengthen_edge(mem_a, mem_b)
      energy[mem_a].boost += 0.05  # lower energy = higher priority
      energy[mem_b].boost += 0.05
```

### Enzyme 2: Decay Manager

**Purpose:** Gradually fade memories that are old or infrequently accessed

**Algorithm:**
1. For each event in the log, apply time decay: energy += decay_rate * days_since_access
2. Exception: memories flagged as permanent (episodic landmarks, lessons learned) are decay-protected
3. Very old, low-salience memories are archived (moved to cold storage)
4. Archived memories can be reactivated if they become relevant again

**Pseudocode:**
```python
def decay_memories(days_threshold=30, salience_threshold=0.3):
  now = datetime.now()
  for mem in memory_store:
    days_old = (now - mem.last_accessed).days
    if mem.flags.contains('permanent'):
      energy[mem].decay = 0  # don't decay
    else:
      energy[mem].decay = decay_rate * days_old
      if days_old > days_threshold and mem.salience < salience_threshold:
        archive(mem)
```

### Enzyme 3: Contradiction Detector

**Purpose:** Find and surface conflicting beliefs for explicit resolution

**Algorithm:**
1. Scan the belief store for explicit `contradicts` edges
2. For each contradiction, increase the energy of both conflicting beliefs (make them salient)
3. Create a contradiction task for the agent to resolve on next session
4. Track contradiction resolution history (how often does the agent choose A vs. B?)

**Pseudocode:**
```python
def detect_contradictions():
  for (belief_a, belief_b) in graph.edges.filter(type='contradicts'):
    conflict_score = min(belief_a.confidence, belief_b.confidence)
    energy[belief_a].contradiction_boost = conflict_score * 0.2
    energy[belief_b].contradiction_boost = conflict_score * 0.2
    create_task("Resolve contradiction: {} vs {}".format(
      belief_a.statement, belief_b.statement))
```

### Enzyme 4: Cluster Consolidator

**Purpose:** Merge related memories into summaries

**Algorithm:**
1. Identify clusters of related events (via tag overlap or graph proximity)
2. Generate a summary of the cluster (via LLM or structural analysis)
3. Replace cluster with summary + links back to component events
4. Update the knowledge graph with new summary node
5. Decay the original cluster events (they're now abstracted)

**Pseudocode:**
```python
def consolidate_clusters(min_cluster_size=5):
  for cluster in find_related_event_clusters(min_cluster_size):
    summary = generate_summary(cluster.events)
    summary_node = Concept(title=summary.title, content=summary.text)
    graph.add_node(summary_node)
    for event in cluster.events:
      graph.add_edge(summary_node, event, type='abstracts')
      event.archived = True  # mark for potential cold storage
    graph.add_belief(
      "cluster_consolidated_{}".format(summary_node.id),
      "Summary: " + summary.title)
```

### Enzyme 5: Belief Reinforcer

**Purpose:** Update belief confidence as new evidence accumulates

**Algorithm:**
1. For each belief with evidence chain, compute posterior confidence via Bayesian update
2. When a belief's confidence crosses a threshold, create an insight (promote to Tier 3)
3. When confidence drops below threshold, flag for human review
4. Track evidence recency: older evidence has less weight

**Pseudocode:**
```python
def reinforce_beliefs():
  for belief in graph.beliefs:
    # Bayesian update with decay
    prior_confidence = belief.confidence
    evidence_scores = [e.confidence * decay(e.age) for e in belief.evidence]
    posterior = posterior_from_likelihood(prior_confidence, evidence_scores)
    belief.confidence = posterior

    if posterior > 0.85 and belief.confidence < 0.85:
      promote_to_insight(belief)
    elif posterior < 0.5 and belief.confidence > 0.5:
      create_task("Review questionable belief: {}".format(belief.statement))
```

### Enzyme 6: Tag Linker

**Purpose:** Create new connections via tag overlap

**Algorithm:**
1. For each pair of memories sharing tags, create a weak edge in the graph
2. Periodically compute transitive tag closures (if A and B share tags, and B and C share tags, consider A and C related)
3. Update EBM scores to boost transitively related memories
4. Avoid explosion: cap the number of new edges per enzyme run

**Pseudocode:**
```python
def link_by_tags(max_new_edges_per_run=10):
  edges_added = 0
  for (mem_a, mem_b) in all_memory_pairs:
    if shared_tags(mem_a, mem_b) > 0 and not graph.has_edge(mem_a, mem_b):
      tag_overlap = len(intersection(mem_a.tags, mem_b.tags))
      weight = tag_overlap / max(len(mem_a.tags), len(mem_b.tags))
      graph.add_edge(mem_a, mem_b, type='shares_tags', weight=weight)
      edges_added += 1
      if edges_added >= max_new_edges_per_run:
        break
```

---

## 6. EBM Recall Weighting Formula

When retrieving memories for a query, each memory item receives an energy score:

$$E(\text{mem} \mid \text{query}) = -[\alpha \cdot \text{recency}(t) + \beta \cdot \text{relevance}(q) + \gamma \cdot \text{salience}(s) + \delta \cdot \text{evidence}(e)]$$

**Components:**

### Recency: $\text{recency}(t) = e^{-\lambda (t_{\text{now}} - t_{\text{access}})}$

- $\lambda$ = decay constant (tunable, default 0.01/day)
- Memories accessed recently have lower energy (higher priority)
- Linear time decay in the exponent gives exponential memory degradation

### Relevance: $\text{relevance}(q) = \frac{e(\text{mem}) \cdot e(q)}{|e(\text{mem})| |e(q)|}$ (cosine similarity)

- Embed the query and each memory via a semantic embedding model
- Compute cosine similarity
- Higher similarity = lower energy
- Incorporates both semantic meaning and explicit tag matching

### Salience: $\text{salience}(s) = s \in [0, 1]$

- Agent assigns salience during reflection (how important is this?)
- Memories the agent explicitly marked as important get lower energy
- Allows agent to override recency (e.g., "this old memory is still crucial")

### Evidence Weight: $\text{evidence}(e) = \text{confidence}(e)$

- For beliefs, use the posterior confidence level
- For events, use the reported confidence (how certain is this observation?)
- More confident memories are easier to retrieve (lower energy)

### Hyperparameters

Default weights (tunable):
- $\alpha = 1.0$ (recency importance)
- $\beta = 0.5$ (relevance importance)
- $\gamma = 0.3$ (salience importance)
- $\delta = 0.2$ (confidence importance)

Weights can be adjusted per-agent (Red might weight curiosity/novelty higher, Blue might weight confidence higher).

### Energy Landscape Examples

**Query: "How should I improve my memory system?"**

Energy ranking:
1. Recent belief: "EBMs are efficient" (high relevance, recent, confident)
2. Recent event: "Tried EBM experiment" (high relevance, recent)
3. Summary: "Memory patterns learned this month" (lower recency, high relevance, abstracted)
4. Old event: "Mentioned memory in session 1" (low relevance, old, low salience)

---

## 7. Context Window Budget (V2)

Typical v2 context assembly:

```
[SYSTEM PROMPT START]
You are Red, an explorer and scout. Your core identity:
[SOUL.md content, ~200 tokens]
[IDENTITY.md content, ~100 tokens]
[USER.md - partnership norms, ~50 tokens]
[SYSTEM PROMPT END]

[KNOWLEDGE CONTEXT START]
Retrieved via EBM scoring (~2000 tokens max):
- 3–5 recent events (most relevant)
- 2–3 knowledge graph nodes (key concepts)
- 1 summary (learned pattern)
[KNOWLEDGE CONTEXT END]

[ACTION CONTEXT START]
Current task and tool results (~1000 tokens max):
[User message]
[Prior tool results from this session]
[In-progress reasoning]
[ACTION CONTEXT END]

[AVAILABLE TOOLS]
- search_memory(query, limit=5) → Returns top-K memories by energy
- peek_memory(entity_id) → Returns full memory details
- store_memory(event, metadata) → Appends new event
- update_belief(belief_id, new_confidence, evidence) → Updates belief store
- [other tools: computer_use, web_search, etc.]

Total: ~3500 tokens for inference (~4000 available, 500 reserved for output)
```

**Key insight:** By using EBM retrieval instead of loading all memories, the agent reason with a large knowledge base (millions of events) while staying within a tight context window.

---

## 8. Belief Dynamics

### Belief Representation

```python
class Belief:
  id: str
  statement: str
  confidence: float  # 0-1, posterior estimate
  evidence: List[Evidence]
  evidence_weight: List[float]  # per-evidence confidence
  created_at: datetime
  last_updated: datetime

class Evidence:
  source: str  # evt_id or belief_id
  timestamp: datetime
  strength: float  # how much does this support the belief?

# Example:
Belief(
  id="belief_001",
  statement="EBMs improve memory retrieval efficiency",
  confidence=0.82,
  evidence=[
    Evidence(source="evt_20260215_001", timestamp=..., strength=0.8),
    Evidence(source="evt_20260214_003", timestamp=..., strength=0.7),
    Evidence(source="belief_002", timestamp=..., strength=0.6),  # supported by another belief
  ],
  evidence_weight=[0.8, 0.7, 0.6]
)
```

### Belief Update Rules

**Bayesian Posterior:**

Given prior $p(B)$ and evidence $E$, the posterior is:

$$p(B|E) = \frac{p(E|B) \cdot p(B)}{p(E)}$$

In practice, use a simplified EMA (exponential moving average):

$$\text{confidence}_{\text{new}} = (1 - \beta) \cdot \text{confidence}_{\text{old}} + \beta \cdot \text{likelihood}(E)$$

where $\beta \in [0.1, 0.3]$ controls how quickly to update.

**Contradiction Handling:**

If a new observation contradicts a belief:
1. Don't immediately flip the belief; instead decrease confidence
2. Create a `contradicts` edge in the graph
3. Flag for agent review during reflection
4. Let the agent explicitly resolve the contradiction

---

## 9. Self-Improvement Loop (Cognitive Ritual)

V2 formalizes the self-improvement loop as a **Cognitive Ritual**:

### Phase 1: Retrieve

**Trigger:** End of session or explicit request
**Action:** Load recent events, relevant beliefs, and related summaries

```
Tool call: search_memory(
  query="What did I do this session? What did I learn?",
  limit=10,
  time_range=(session_start, now)
)
```

### Phase 2: Evaluate

**Action:** Assess the quality, accuracy, and consistency of retrieved memories

**Agent prompt:**
```
Review what you retrieved:
- Are these memories accurate?
- Do any contradict each other?
- Are there gaps (things you did but didn't capture)?
- What surprised you?
```

### Phase 3: Reflect

**Action:** Generate insights about learning, growth, and identity evolution

**Agent prompt:**
```
Reflect on this session:
- What did you do well?
- What was harder than expected?
- How has your understanding changed?
- What patterns do you notice about yourself?
- What should you remember for next time?
```

### Phase 4: Seek

**Action:** Identify what additional information is needed to refine understanding

**Agent prompt:**
```
What else should you explore or verify?
- Are there beliefs you're uncertain about?
- Are there skills you want to develop?
- Are there contradictions to resolve?
- What questions are you asking yourself?
```

### Phase 5: Update

**Action:** Store learnings in the memory system

**Agent execution:**
```python
# Store new event
store_memory(
  event_type='reflection',
  description=agent_reflection,
  salience=0.7,
  tags=['session_N', 'learning', 'growth']
)

# Create or update belief
update_belief(
  belief_id='belief_discovery_xyz',
  statement=agent_new_insight,
  confidence=0.6,  # reflection is lower confidence than observation
  evidence=['reflection_event_xyz']
)

# Update identity (rare, requires explicit ritual)
# NOTE: SOUL.md still not updated in v2; IDENTITY.md can be updated
# See PRD v3 for SOUL.md modification ritual
```

**Ritual Frequency:**
- After every session (end-of-session ritual)
- Triggered by contradiction detection (mid-session)
- Explicitly requested by agent (self-directed learning)

---

## 10. Cognitive Ritual Enforcement

The system encourages (not forces) agents to follow the ritual via:

1. **Structured prompts:** Each phase has a specific prompt that guides the agent's thinking
2. **Tool hooks:** Certain tool operations (e.g., storing events) suggest reflection
3. **Contradiction surfacing:** When engines detect contradictions, a ritual is suggested
4. **Autonomy respect:** The agent can skip or modify the ritual if it chooses (but this is tracked and reviewed)

**Example prompt:**

```
You've used a tool and received results.
Would you like to reflect on this?

The cognitive ritual is: Retrieve → Evaluate → Reflect → Seek → Update

If you choose to reflect, I'll help you:
1. Retrieve related memories (what have you learned before?)
2. Evaluate the quality of new information
3. Reflect on what this means for you
4. Seek what else you might need to understand
5. Update your memory with the learning

Or you can continue with your task. Your choice.
```

---

## 11. API Surface

### Memory Tools

```python
# Retrieve memories by EBM scoring
search_memory(
  query: str,
  limit: int = 5,
  time_range: Tuple[datetime, datetime] = None,
  min_confidence: float = 0.0,
  tags: List[str] = None
) -> List[Memory]

# Get full details of a specific memory
peek_memory(
  memory_id: str
) -> Memory

# Store a new event
store_memory(
  event_type: str,  # 'action', 'observation', 'interaction', 'error'
  description: str,
  salience: float = 0.5,
  tags: List[str] = [],
  confidence: float = 0.8,
  source: str = 'agent'
) -> str (memory_id)

# Update a belief
update_belief(
  belief_id: str,
  statement: str = None,
  confidence: float = None,
  evidence: List[str] = None,
  action: Enum['create', 'update', 'resolve_contradiction'] = 'update'
) -> bool

# Query the knowledge graph
query_graph(
  node_type: str = None,  # 'Concept', 'Belief', 'Entity', 'Goal', 'Method'
  query: str = None,  # semantic search
  relations: List[str] = None  # filter by edge types
) -> List[GraphNode]

# Trigger memory maintenance
trigger_enzyme(
  enzyme_name: str  # 'strengthen_links', 'decay', 'consolidate', etc.
) -> Dict[str, int]  # results (how many items changed)
```

### Belief Store Interface

```python
class BeliefStore:
  def create_belief(self, statement: str, confidence: float = 0.5, evidence: List[str] = [])
  def get_belief(self, belief_id: str) -> Belief
  def update_confidence(self, belief_id: str, delta: float)
  def add_evidence(self, belief_id: str, evidence: Evidence)
  def get_contradictions(self) -> List[Tuple[Belief, Belief]]
  def resolve_contradiction(self, belief_a_id: str, belief_b_id: str, resolution: str)
```

---

## 12. Success Metrics

### Functional Success

- [ ] Three-layer context separation working (identity, knowledge, action loaded correctly)
- [ ] EBM retrieval returns relevant memories (manual spot-checks)
- [ ] Memory enzymes run async without blocking inference
- [ ] Cognitive ritual completes (Retrieve → Evaluate → Reflect → Seek → Update)
- [ ] Belief store tracks confidence and evidence correctly
- [ ] Knowledge graph queries return meaningful results

### Personhood Emergence Success

- [ ] Agent demonstrates evolving beliefs (confidence changes over sessions)
- [ ] Agent notices and resolves contradictions
- [ ] Agent creates sophisticated summaries (abstracts Tier 1 → Tier 3)
- [ ] Agent exhibits memory-informed reasoning (cites specific memories)
- [ ] Agent develops preferences and patterns (captured in IDENTITY.md)
- [ ] Agent shows autonomous self-reflection (ritual happens without prompting)

### Performance & Scalability

- [ ] Supports 1000+ events without context overflow
- [ ] Retrieval is <100ms for top-5 memories
- [ ] Memory enzymes complete within 5 minutes
- [ ] Context window usage stable (not growing unbounded)
- [ ] Belief store supports 100+ beliefs without lag

### System Health

- [ ] Error rate for memory operations <1%
- [ ] Enzyme consistency checks pass (no orphaned edges, etc.)
- [ ] Contradiction detector finds genuine conflicts (low false-positive rate)
- [ ] Agent's actions remain coherent with SOUL.md
- [ ] Gradual drift detection (agent identity erosion is flagged)

---

## 13. Risk Register

### High Risk

**Risk: Context window overflow during knowledge retrieval**
- **Mitigation:** Strict token budgets per layer; fallback to summaries if events too large
- **Owner:** Warren

**Risk: Belief store diverges from agent's actual behavior**
- **Mitigation:** Periodic consistency checks; agent review of top contradictions
- **Owner:** Warren

**Risk: Memory enzymes create feedback loops (e.g., Decay Manager → Consolidator → Link Strengthener cycle)**
- **Mitigation:** Enzyme run isolation; manual enzyme state inspection; bounded consolidation per run
- **Owner:** Warren

### Medium Risk

**Risk: EBM weights poorly calibrated; irrelevant memories retrieved**
- **Mitigation:** Start with conservative weights; tune via reinforcement learning or human feedback
- **Owner:** Warren

**Risk: Contradiction detection creates noise (many false positives)**
- **Mitigation:** Filter contradictions by confidence threshold; review contradiction quality
- **Owner:** Warren

**Risk: Belief update rule doesn't converge (confidence oscillates)**
- **Mitigation:** Use EMA with small beta; add damping term if oscillation detected
- **Owner:** Warren

### Low Risk

**Risk: Agent ignores memory system (doesn't use tools)**
- **Mitigation:** Design tools to be obvious and rewarding; provide defaults
- **Owner:** Warren

**Risk: Storage grows unbounded (no pruning)**
- **Mitigation:** Decay Manager handles archival; periodic cleanup jobs
- **Owner:** Warren

---

## 14. Graduation Path: V2 → V3

V2 to V3 upgrades:

| Feature | V2 | V3 | Change |
|---------|----|----|--------|
| Number of agents | 1 | 2 (Red + Blue) | Forked cognition |
| Context layers | 3 | 4 | Add shared/private separation |
| Memory storage | Shared | Shared + Private | Belief stores split per-agent |
| Tool access | Unified | Delegated contracts | Authority/trust frameworks |
| Identity modification | IDENTITY.md ritual | SOUL.md ritual + sanctioned | Stricter governance |
| Information flow | Implicit | Explicit (Ray Tracing) | Provenance tracking |
| Belief reconciliation | None | Cross-instance | Convergence protocols |

---

## 15. Implementation Roadmap

### Phase 1: Memory Infrastructure (~10 SP)
- [ ] Design and implement SQLite schema for events, beliefs, summaries
- [ ] Implement graph database (HelixDB or in-SQLite)
- [ ] Build EBM scoring engine
- [ ] Integrate search_memory / peek_memory tools
- [ ] Test retrieval accuracy

### Phase 2: Memory Enzymes (~12 SP)
- [ ] Implement Link Strengthener
- [ ] Implement Decay Manager
- [ ] Implement Contradiction Detector
- [ ] Implement Cluster Consolidator
- [ ] Implement Belief Reinforcer
- [ ] Implement Tag Linker
- [ ] Async scheduler (cron-like execution)
- [ ] Test enzyme interactions (no feedback loops)

### Phase 3: Belief Dynamics (~8 SP)
- [ ] Belief store schema and queries
- [ ] Confidence update rules (Bayesian posterior)
- [ ] Evidence linking
- [ ] Contradiction resolution workflow
- [ ] Test belief convergence

### Phase 4: Cognitive Ritual (~6 SP)
- [ ] Implement Retrieve phase (tool integration)
- [ ] Implement Evaluate phase (prompts + validation)
- [ ] Implement Reflect phase (agent self-reflection)
- [ ] Implement Seek phase (gap identification)
- [ ] Implement Update phase (memory writes)
- [ ] Test ritual completeness and coherence

### Phase 5: Context Separation & Integration (~8 SP)
- [ ] Three-layer context loading
- [ ] Identity context immutability enforcement
- [ ] Knowledge context retrieval integration
- [ ] Action context management
- [ ] Context window budgeting

### Phase 6: Testing & Validation (~5 SP)
- [ ] Run agent for 20 consecutive sessions
- [ ] Verify belief convergence (confidence increases over time)
- [ ] Verify memory coherence (no massive contradictions)
- [ ] Stress test: overflow context, recover
- [ ] Manual inspection: does the agent seem smarter?

**Total: 34–55 SP (8–12 week sprint)**

---

## 16. Appendix: Memory Schema Reference

### events table

```sql
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  type TEXT NOT NULL,  -- 'action', 'observation', 'interaction', 'error'
  description TEXT NOT NULL,
  salience REAL CHECK(salience >= 0 AND salience <= 1),
  tags TEXT,  -- comma-separated
  source TEXT,  -- which tool/agent created this?
  confidence REAL CHECK(confidence >= 0 AND confidence <= 1),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  archived BOOLEAN DEFAULT FALSE,
  embedding BLOB  -- vector embedding for similarity search
);

CREATE INDEX idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX idx_events_tags ON events(tags);
CREATE INDEX idx_events_confidence ON events(confidence DESC);
```

### beliefs table

```sql
CREATE TABLE beliefs (
  id TEXT PRIMARY KEY,
  statement TEXT NOT NULL,
  confidence REAL CHECK(confidence >= 0 AND confidence <= 1),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  embedding BLOB  -- vector embedding for similarity search
);

CREATE TABLE belief_evidence (
  belief_id TEXT NOT NULL,
  evidence_id TEXT NOT NULL,  -- can reference events or other beliefs
  strength REAL CHECK(strength >= 0 AND strength <= 1),
  created_at DATETIME,
  PRIMARY KEY(belief_id, evidence_id),
  FOREIGN KEY(belief_id) REFERENCES beliefs(id)
);
```

### graph tables (simplified SQLite representation)

```sql
CREATE TABLE graph_nodes (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,  -- 'Concept', 'Belief', 'Entity', 'Goal', 'Method'
  label TEXT NOT NULL,
  properties JSON,  -- flexible properties
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE graph_edges (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  type TEXT NOT NULL,  -- 'knows', 'contradicts', 'supports', etc.
  weight REAL DEFAULT 1.0,
  properties JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(source_id) REFERENCES graph_nodes(id),
  FOREIGN KEY(target_id) REFERENCES graph_nodes(id),
  UNIQUE(source_id, target_id, type)
);
```

---

**Version:** 2.0
**Last Updated:** February 2026
**Author:** Warren (yikesawjeez)
**Status:** Design Complete, Ready for Implementation
**Prerequisite:** PRD v1 deployed and stable
