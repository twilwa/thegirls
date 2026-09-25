# 11: FrankenSearch - Progressive Two-Tier Hybrid Search with Graceful Degradation

**Source:** FrankenSearch Rust Library (github.com/frankensearch/frankensearch, active development 2025-2026)

**FrankenSearch is a production-grade Rust library implementing a progressive two-tier hybrid search pipeline. Its architecture directly informs the girls' retrieval system design, particularly the mapping between fast lexical+semantic recall (Phase 1) and quality-optimized reranking (Phase 2).**

---

## Architecture Overview: 11 Focused Crates

FrankenSearch's modular design separates concerns across focused components:

### Core Layer
- **frankensearch-types:** Type definitions and trait abstractions for extensibility
- **frankensearch-traits:** Pluggable interfaces (embedder, indexer, search, reranker)

### Embedding & Vector Processing
- **frankensearch-embed:** Progressive embedding stack: hash fallback → model2vec → fastembed (potion-128M default, MiniLM-L6-v2 for quality phase)
- **frankensearch-index:** FSVI vector format (custom on-disk format) with f16 quantization, mmap reads, CRC32 checksums; SIMD dot products for efficient similarity

### Search Pipeline
- **frankensearch-lexical:** Tantivy BM25 integration for keyword search
- **frankensearch-fusion:** RRF (Reciprocal Rank Fusion) combining keyword + semantic results; orchestration of two-tier pipeline

### Optional Quality & Reranking
- **frankensearch-rerank:** Cross-encoder reranking (optional, skipped if unavailable or timeout)

### Storage & Persistence
- **frankensearch-storage:** FrankenSQLite for metadata and indexing; persistent job queue with state machine (Pending → Processing → Completed/Failed/Skipped); content-hash deduplication
- **frankensearch-durability:** Write-ahead logging, consistency guarantees for long-running operation

### Operations & Interface
- **frankensearch-tui:** Terminal UI for monitoring, debugging search performance
- **frankensearch-cli:** Command-line tools for indexing, querying, bulk operations
- **frankensearch-ops:** Telemetry, metrics collection, health checks

### Async Runtime
- **frankensearch-async:** asupersync integration (NOT Tokio) — structured concurrency via Cx capability context, cancel-correct semantics, deterministic testing with LabRuntime + virtual time

---

## Two-Tier Search Pipeline

### Phase 1: Fast Recall (~15ms latency)

Executes in parallel:
1. **Fast embedding:** Hash-based fallback (deterministic, <1ms) or lightweight model2vec (<5ms) produces 128D vectors
2. **Lexical search:** Tantivy BM25 retrieves keyword-matching documents
3. **Vector search:** SIMD dot products against fast embedding space (FSVI index)
4. **RRF fusion:** Combines keyword and semantic scores using Reciprocal Rank Fusion (K=60 default)

**Output:** Top 60 candidates ranked by fused score

**Guarantees:**
- Always returns something (lexical-only fallback if embedding fails)
- Deterministic and reproducible
- Sub-20ms p99 latency even on cold disk reads

### Phase 2: Quality Refinement (~150ms latency)

Executes conditionally on Phase 1 results:
1. **Quality embedding:** MiniLM-L6-v2 (384D) re-encodes top 60 candidates from Phase 1
2. **Re-scoring:** Computes high-quality similarity scores
3. **Blending:** Combines Phase 1 and Phase 2 scores: `final_score = alpha * quality_score + (1-alpha) * phase1_score` (alpha = 0.7 default)
4. **Optional cross-encoder:** Re-ranks top K candidates using cross-encoder if available (adds 50-100ms)

**Output:** Top N candidates with refined ranking

**Graceful degradation:**
- If quality timeout: returns Phase 1 results without penalty
- If quality embedder missing: skip Phase 2, use Phase 1 as final
- If cross-encoder unavailable: proceed without it
- If Phase 2 takes longer than timeout: interrupt and use best-effort current ranking

---

## Graceful Degradation Philosophy

FrankenSearch's core principle: **Always deliver something useful, optionally deliver something better.**

### Failure Modes with Handling

| Scenario | Behavior |
|----------|----------|
| Fast embedder unavailable | Use hash fallback (deterministic, no learned semantics) |
| Lexical index corrupt | Vector search only (semantic fallback) |
| Fast index missing | Lexical search only (keyword fallback) |
| Quality embedder timeout | Return Phase 1 results immediately |
| Quality embedder missing | Skip Phase 2, use Phase 1 ranking |
| Cross-encoder unavailable | Use blended Phase 1+2 score (no cross-encoder) |
| Storage I/O slow | Use in-memory cache, degrade gracefully as cache fills |

**No single component failure blocks retrieval.** This is crucial for the girls' always-on architecture: even if the KAN scorer (quality phase) is unavailable or slow, they get fast results from energy-based scoring.

---

## Configuration Knobs

```yaml
Quality Phase Configuration:
  quality_weight: 0.7           # Blending weight (0-1)
  rrf_k: 60                     # RRF fusion parameter
  candidate_multiplier: 1.5     # How many candidates to keep for Phase 2
  quality_timeout_ms: 150       # Max time before returning Phase 1 results
  fast_only_flag: false         # Force Phase 1 only (debugging/budget)

Storage Configuration:
  hnsw_threshold: 1000          # When to use HNSW vs. brute-force search
  quantization_bits: 16         # f16 for vectors
  mmap_enabled: true            # Memory-map index reads
  dedup_by_content_hash: true   # Prevent duplicate indexing
```

---

## Storage & Durability

### Vector Index (FSVI Format)

Custom on-disk format optimized for:
- **f16 quantization:** 2x memory savings vs. f32, minimal recall loss
- **mmap reads:** Load vectors without copying to memory
- **CRC32 checksums:** Detect corruption on disk
- **SIMD dot products:** Hardware-accelerated similarity computation

**Result:** Fast, memory-efficient vector search suitable for long-running services.

### Metadata Storage (FrankenSQLite)

- Metadata indexed in SQLite (faster than JSON files)
- Persistent job queue with state machine
- Content-hash deduplication (prevent re-indexing same content)
- Transactional consistency across metadata and index updates

### Job Queue State Machine

```
Pending → Processing → Completed
              ↓
         Failed (with retry)
              ↓
         Skipped (if cancelled)
```

Enables:
- Resumable indexing (if server crashes mid-reindex, resume from Pending)
- Deduplication (same content hash → skip processing)
- Bulk reranking (bulk Operation queues candidates for Phase 2 re-scoring)

---

## Async Runtime: asupersync, Not Tokio

FrankenSearch deliberately uses **asupersync** (structured concurrency framework) instead of Tokio:

### Why This Matters

**Tokio characteristics:**
- Task cancellation is fire-and-forget (can leak resources)
- Deterministic testing requires extensive mocking
- Implicit dependencies between spawned tasks

**asupersync characteristics:**
- Structured concurrency: all spawned tasks must complete/cancel deterministically
- Cx capability context: tracks task lifetime and cancellation
- LabRuntime: virtual time for deterministic testing (no flaky timeouts)
- Cancel-correct: cancellation propagates correctly without leaks

### Implication for Girls' Enzyme Workers

The girls' PRD v2 describes an "enzyme worker" architecture where specialized agents handle different memory transformations in parallel. asupersync's structured concurrency model is better suited than Tokio for this:
- Ensures all workers complete or cancel together (no orphaned processes)
- Virtual time enables deterministic replay and debugging
- Capability context tracks which worker has what permissions

---

## Two-Tier Pattern Maps to EBM Retrieval

### Current EBM System (PRD v5)

The girls' Episodic/Belief/Model three-tier system answers: "Given a context, retrieve relevant memories with weights."

Current challenge: EBM recall must hit <50ms for voice pipeline, requiring efficient ranked retrieval across three memory types.

### FrankenSearch Phase 1 as EBM Phase 1

**Fast lexical + semantic fusion directly maps to EBM's first pass:**
- Phase 1a (Lexical): Keyword BM25 over episodic memory index (recent memories, explicit keywords)
- Phase 1b (Semantic): Vector search using precomputed energy scores (episodic salience, belief relevance weights)
- Phase 1c (RRF fusion): Combine keyword + energy scores

**Output:** Top 60 candidate memories ranked by fast approximation

### FrankenSearch Phase 2 as EBM Phase 2

**Quality embedding + cross-encoder reranking maps to EBM's refinement:**
- Phase 2a (Quality embedding): MiniLM-L6-v2 re-encodes memory context using full semantic understanding
- Phase 2b (Blending): `alpha * quality_score + (1-alpha) * energy_score` combines learned quality with precomputed salience
- Phase 2c (Cross-encoder): Optional KAN-based reranking specifically for query-context relevance

**Output:** Top 20 memories with refined ranking

### Graceful Degradation in EBM

If KAN scorer unavailable → use Phase 1 results (energy-based ranking)

If quality embedder fails → use precomputed energy scores alone

If lexical search slow → vector search provides fallback candidates

**Result:** Girls always get some meaningful memories, never block on retrieval.

---

## RRF Fusion: Reconciling Keyword and Semantic

FrankenSearch's RRF (Reciprocal Rank Fusion) approach:

```
For each result in top-K (lexical U semantic):
  rrf_score = sum of (1 / (K + rank_in_list))
```

This is exactly what IronClaw and NullClaw use for memory search in the girls' current design, but FrankenSearch formalizes it and optimizes the computation.

**Key insight:** RRF doesn't require the keyword and semantic scores to be on the same scale — it only uses ranks. This allows mixing:
- BM25 (keyword relevance)
- Energy scores (episodic salience)
- Belief weights (semantic relevance)

All in one unified ranking without score normalization gymnastics.

---

## Architectural Implications for the Girls

### 1. Two-Tier Matches EBM's Cognitive Architecture

The girls' memory retrieval shouldn't be instant (unrealistic) but shouldn't be slow (blocks interaction). Two-tier hybrid search provides:

**Phase 1 (15ms):** Fast, approximate recall using energy-based scoring
**Phase 2 (150ms total):** Optional quality refinement for conversation depth

The girls can:
- Respond immediately with Phase 1 memories for quick confirmations ("What did I do yesterday?")
- Spend more time refining for complex reasoning ("What patterns do I see in my recent beliefs?")

### 2. Progressive Delivery Enables Always-On Architecture

Phase 1 results are immediately returned. Phase 2 refines them in background if there's time before response generation.

For the girls' 24/7 operation: even when the system is under load, basic retrieval never blocks. Optional quality refinement completes when it can.

### 3. Graceful Degradation Matches PRD v5 Philosophy

PRD v5 Section 5 ("Failure with Grace"):
> "When any component degrades, the system should degrade gracefully rather than fail catastrophically."

FrankenSearch embodies this:
- Missing quality embedder? Use fast results.
- Slow cross-encoder? Return blended ranking.
- Corrupt vector index? Use lexical fallback.

The girls' retrieval system should adopt the same principle.

### 4. Content-Hash Dedup Prevents Duplicate Memory Processing

The job queue's deduplication by content hash is crucial for memory ingestion:

When new daily notes arrive, FrankenSearch's approach prevents:
- Re-indexing identical episodic memories
- Duplicate belief derivations
- Wasted compute on duplicate synthesis

The girls' memory processor can leverage this to skip redundant EBM updates.

### 5. asupersync for Structured Concurrency

The enzyme worker architecture (PRD v2) requires:
- All workers complete or cancel together
- Deterministic behavior for debugging
- No orphaned processes

asupersync is better suited than Tokio for this design.

---

## Cross-References and Integration Points

### Paper 09: Energy-Based Models for Episodic Memory
EBM describes precomputed salience/relevance scores for fast recall. FrankenSearch's Phase 1 energy-based fusion (combining BM25 + energy scores) is a practical implementation of EBM principles.

**Integration:** Energy scores from EBM become Phase 1 semantic scores in FrankenSearch pipeline.

### Brief 05: Memgraph Atomic GraphRAG
Memgraph provides unified storage for graph structure + embeddings. FrankenSearch provides efficient retrieval from that store.

**Integration:** FrankenSearch indexes episodic/belief/model nodes from Memgraph; Atomic GraphRAG provides single-query context assembly; two-tier hybrid search refines results.

**Combined:** Single query to Memgraph returns candidate memories + structure, FrankenSearch ranks them with Phase 1/2.

### PRD v2: Enzyme Worker Architecture
Enzyme workers transform memories (extraction, synthesis, abstraction). asupersync's structured concurrency is better suited than Tokio for coordinating workers.

**Integration:** Job queue in FrankenSearch storage coordinates enzyme worker jobs with state machine (Pending → Processing → Completed).

### PRD v5: Async Environment-Native, Graceful Degradation
FrankenSearch embodies both principles:
- Async runtime via asupersync (structured concurrency, not Tokio)
- Graceful degradation (Phase 1 fallback, optional Phase 2, multiple search modes)

### Context-Engineering Brief 01: Gold Panning
Gold Panning describes iterative search with progressive refinement. FrankenSearch's two-tier pipeline is the technical realization: Phase 1 prospecting (broad recall), Phase 2 refinement (deep reranking).

**Integration:** Gold Panning's iterative questioning maps to two-tier phases: initial search (Phase 1), question refinement based on Phase 1 results (leads to Phase 2).

---

## Recommendation: Adopt FrankenSearch Pattern for EBM Retrieval

**Scope:** Implement two-tier hybrid search for episodic/belief/model memory retrieval.

**Phase 1 Implementation:**
- Index episodic memories with BM25 (Tantivy) + energy scores (vector search)
- RRF fusion combining keyword + energy rankings
- Target: <20ms p95 latency

**Phase 2 Implementation:**
- Quality embedder (MiniLM-L6-v2) re-encodes top candidates
- Blends Phase 1 + Phase 2 scores (alpha = 0.7)
- Optional KAN-based cross-encoder when available
- Target: <150ms total latency

**Graceful Degradation:**
- If quality embedder slow/missing: return Phase 1 results
- If cross-encoder unavailable: use blended score (no cross-encoder)
- If energy scores missing: use BM25 alone
- If lexical index fails: use vector search only

**Storage Integration:**
- Use FrankenSearch's FSVI format for episodic memory vectors
- FrankenSQLite for metadata, job queue, deduplication
- asupersync for coordinating Phase 1 + Phase 2 execution

**Timeline:** Post-MVP, as part of retrieval system hardening (PRD v5 Section 6).

**Risk level:** Low-medium. FrankenSearch is well-tested in production. Main work: (a) integrating with Memgraph indexing pipeline, (b) tuning Phase 1/2 latency targets for voice interaction, (c) calibrating alpha blend weight for the girls' specific memories.

**Benefit:** <50ms EBM recall latency, graceful degradation under load, deterministic testing with LabRuntime, structured concurrency for enzyme workers.

---

## Metrics to Validate Post-Implementation

| Metric | Target | Notes |
|--------|--------|-------|
| Phase 1 latency (p95) | <20ms | Fast recall for immediate responses |
| Phase 2 latency (p95) | <150ms total | Quality refinement still interactive |
| Recall@20 (Phase 1 + 2) | >0.85 | Ensure quality refinement improves ranking |
| Graceful degradation coverage | 100% | Every failure mode has fallback |
| Memory footprint (f16 quantization) | 50% of f32 | Vector storage efficiency |
| Content-hash dedup effectiveness | >90% | Prevent re-processing duplicate memories |
| LabRuntime deterministic test pass rate | 100% | No flaky timeout tests |

---

## Open Questions

1. **Energy score computation:** How should Phase 1 energy scores be precomputed? Running a full EBM model before indexing, or learned from user behavior (click-through rates, conversation depth)?

2. **Quality embedder selection:** Is MiniLM-L6-v2 (384D) the right tradeoff between quality and Phase 2 latency? Should we explore other embedders (ONNX-optimized versions)?

3. **Cross-encoder integration:** When should the KAN-based cross-encoder be available? How do we handle the 50-100ms addition without violating voice pipeline latency?

4. **Alpha blending:** How should alpha be tuned for the girls' specific memories? User study to find the right blend between fast approximation and quality refinement?

5. **Memgraph integration:** How does FrankenSearch's FSVI vector index interact with Memgraph's Vector Single Store? Can we bypass FrankenSearch's storage and use Memgraph as the canonical store?

These should be answered during proof-of-concept phase before full EBM retrieval system implementation.
