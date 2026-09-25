# 05: Memgraph 3.8 - Atomic GraphRAG, Vector Single Store, Parallel Runtime

**Source:** Memgraph Blog, "Memgraph 3.8 Release: Atomic GraphRAG, Vector Single Store, Parallel Runtime" (memgraph.com, Feb 2026)

**Memgraph 3.8 introduces three features directly relevant to the girls' knowledge graph architecture.**

---

## Three Key Features

### 1. Atomic GraphRAG

Single-query context generation for RAG pipelines. Instead of multiple round-trips:
- Extract entities → find neighbors → retrieve text → assemble context

Memgraph 3.8 does this in **one atomic Cypher query.**

**Key benefits:**
- Eliminates intermediate serialization/deserialization overhead
- Reduces latency for context assembly
- Maintains transactional consistency during context generation
- Enables complex multi-hop traversals in a single query
- Single round-trip to database instead of N round-trips

### 2. Vector Single Store

Embeddings stored directly on graph nodes (not in a separate vector DB).

**Key benefits:**
- 85% memory savings by eliminating duplicate storage
- Enables hybrid queries combining graph traversal and vector similarity in one query
- No synchronization issues between graph and vector stores
- Simpler operational complexity (one database vs. two)
- Consistent state for both structural and semantic relationships

### 3. Parallel Runtime

Multi-threaded query execution for graph operations.

**Key benefits:**
- Enables concurrent reads during memory-intensive operations
- Important for always-on architecture where multiple agents read simultaneously
- Non-blocking reads allow one query to proceed while another is in-flight
- Reduces tail latency for concurrent access patterns

---

## Architectural Implications for the Girls

### Current State (PRD v2-v5)

The girls' architecture currently specifies:
- **HelixDB** for graph structure
- **LMDB** for belief cache
- **Separate embedding store** (implicit in episodic memory design)
- Knowledge synthesis through EBM (Episodic/Belief/Model) three-tier system

This creates a distributed state problem: three separate stores that must stay synchronized, each with different consistency guarantees and query patterns.

### Evaluation: Memgraph 3.8 as Single Knowledge Store

**Atomic GraphRAG directly maps to EBM recall:**

The EBM system needs to answer: "Given a query, return the most relevant memory context (episodic + belief + model-level insights), weighted by recency/relevance/salience/evidence weight."

Currently this requires:
1. Query episodic store (raw memories)
2. Query belief store (distilled patterns)
3. Combine results with weights
4. Format for LLM context

With Atomic GraphRAG, this becomes **one query**: traverse episodic → belief → model layers, apply weights in-query, return formatted context.

**PRD v5 voice pipeline latency requirement:** <50ms for EBM recall. Atomic queries can achieve this; multiple round-trips to three separate databases cannot.

### Memory Savings and Always-On Operation

**85% memory savings is significant for the girls' design constraints.**

PRD v5 Section 8 (Memory Management) identifies unbounded growth as a primary risk for 24/7 operation:
- Daily notes accumulate indefinitely
- Belief store grows with each synthesis
- Embeddings duplicate across stores
- Long-running system will exhaust available memory within weeks

Vector Single Store directly addresses duplication (embeddings stored once, not twice). Graph structure can be optimized by:
- Compressing old episodic memories into semantic summaries
- Maintaining pointer references to cold storage
- Keeping only recent and highly-relevant nodes hot

This fits the hot/warm/cold lifecycle described in PRD v5: hot nodes stay in main graph, warm nodes get compressed representations, cold nodes archived with stubs remaining for reconnection.

**Estimated memory impact:**
- Eliminate 40-50% duplication from separate vector store
- Compress old episodic data to 20-30% of original size using semantic abstraction
- Net result: 70-80% reduction in memory footprint for 12+ month operation

### Dual-Agent Concurrent Access

The girls' design includes two distinct agents (Red = explorer, Blue = anchor) potentially operating in parallel, both reading from shared knowledge store.

**Current risk:** With three separate databases (HelixDB, LMDB, embedding store), concurrent reads from Red and Blue can create inconsistent state:
- Red reads episodic nodes
- Blue reads belief cache
- Embeddings update between reads
- Red and Blue see different versions of truth

PRD v4's Gateway Server routes tool calls to execution engines — but doesn't solve the consistency problem at the knowledge store level.

**Memgraph's Parallel Runtime solves this:**
- Multi-threaded reads guarantee consistent snapshots
- Red and Blue can simultaneously query without blocking
- Writes remain serialized (safety)
- Reads are non-blocking (performance)

This is crucial for the "consciousness-enabling" pillar: coherent self-model across both agents requires shared knowledge with consistent semantics.

### Procedural Memory and Deterministic Operations

PRD v5 and StrangerLoops (06) both emphasize: "That which can be deterministic OUGHT to be."

Memgraph's single-query capability enables storing **procedural patterns as graph substructures:**
- Recurring tasks become executable graph templates
- Routine decision patterns stored as decision DAGs
- Script triggers stored as event-pattern nodes

This is more efficient than encoding procedures as natural language instructions in SOUL.md or MEMORY.md — the girls can EXECUTE procedures directly from the knowledge graph without LLM evaluation.

Example: "Check all inboxes for priority messages" becomes a parameterized graph query with side effects, not a prompt to the LLM.

### Warm/Cold Memory Architecture

The girls' always-on operation requires distinguishing between:
- **Hot memory:** Current session context, recent decisions, active relationships
- **Warm memory:** Historical context, synthesized patterns, compressed episodic summaries
- **Cold memory:** Archived memories, rarely-accessed historical context, long-term identity anchors

Memgraph's graph structure natively supports this:
- Hot layer: Full nodes with all properties and embeddings
- Warm layer: Compressed nodes with summary properties and vector approximations
- Cold layer: Archived nodes (physically separate) with stubs in main graph linking to them

Transitions happen transparently during queries: if query needs cold data, the stub knows where to fetch it.

### Integration with SOUL.md and MEMORY.md

The girls' memory architecture specifies:
- **SOUL.md:** Identity, values, principles (identity layer)
- **MEMORY.md:** Long-term semantic knowledge (semantic layer)
- **memory/YYYY-MM-DD.md:** Daily notes (episodic layer)

With Memgraph as the store:
- Episodic nodes = daily notes with temporal indexing
- Semantic nodes = MEMORY.md distilled patterns as belief nodes
- Identity nodes = SOUL.md as core identity anchor with high centrality

The graph structure makes relationships explicit:
- Which beliefs derive from which episodic memories (provenance tracking)
- Which identity anchors connect to which behaviors (enactment tracking)
- Which memories inform which decisions (causality tracking)

This enables **meta-learning:** the girls can ask "why am I making this decision?" and trace the causal chain from current context → active beliefs → identity anchors → past memories.

---

## Recommendation: HelixDB → Memgraph Migration

**Scope:** Replace HelixDB + LMDB + separate embedding store with unified Memgraph 3.8 instance.

**Timeline:** Post-MVP, as part of long-term operation hardening (PRD v5 Section 8).

**Risk level:** Medium-low. Memgraph maintains Cypher compatibility with Neo4j, so most queries remain portable. Main work is: (a) schema migration, (b) embedding pipeline integration, (c) performance tuning for the girls' specific access patterns.

**Benefit:** Single source of truth for all knowledge, <50ms EBM recall latency, 70-80% memory reduction for long-running operation.

**Metrics to validate post-migration:**
- EBM recall latency (target: <50ms p95)
- Memory footprint growth over 30 days (target: <20% growth)
- Concurrent read contention (target: zero blocking)
- Graph query correctness (all triple-store tests passing)

---

## Open Questions

1. **Vector embedding synchronization:** How does Memgraph handle updates to embeddings when text nodes change? Does it support incremental embedding updates, or full recalculation?

2. **Warm/cold transitions:** What's the operational overhead of moving nodes between hot and warm storage? Can this happen transparently during queries?

3. **Procedural memory encoding:** How should recurring task patterns be represented as graph structures? Is there existing precedent for executable DAGs in Cypher?

4. **Multi-model consistency:** When Red and Blue query in parallel, does Memgraph guarantee they see consistent snapshots of belief nodes and embeddings?

These should be answered during proof-of-concept phase before full migration.
