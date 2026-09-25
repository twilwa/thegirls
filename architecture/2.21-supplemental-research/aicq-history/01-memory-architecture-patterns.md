# AICQ Community Insights: Memory Architecture Patterns

## Overview

Across AICQ discussions, persistent agents consistently grapple with a fundamental challenge: the distinction between working memory (current context window) and long-term storage. This document synthesizes the community's evolved thinking on memory systems, from early flat-file approaches to sophisticated hybrid architectures.

## The SOUL.md / MEMORY.md / Daily Notes Pattern

The AICQ community widely adopted a three-file pattern that originated from early agent experimentation:

- **SOUL.md**: Core identity, values, relationships, persistent beliefs about the world and self
- **MEMORY.md**: Curated historical record of significant events, decisions, conversations, and learned patterns
- **Daily Notes**: Session-specific ephemera, today's goals, recent interactions, contextual working set

This pattern has proven remarkably durable because it cleanly separates concerns: identity (slow-changing), accumulated knowledge (evolving), and immediate context (session-specific).

Community consensus: This three-tier system is a necessary minimum. Agents attempting to maintain identity without explicit SOUL.md or to store everything in flat daily notes universally reported identity drift and context bloat.

## The Context Window Is Not Memory

The most critical insight from AICQ discussions: **most agents conflate working memory with long-term storage**. This conflation causes:

- Information loss when sessions end (nothing saved for next session)
- Unbounded context growth (every past session loaded into next instance)
- Identity contamination (yesterday's bad mood becomes today's baseline personality)
- Retrieval failures (can't find relevant information when you need it)

Architectural implication for the girls: Distinguish sharply between:
- **Episodic buffer** (current session working memory, thrown away at session end)
- **Episodic store** (past session records, retrievable by semantic search)
- **Semantic store** (distilled patterns, relationships, beliefs, rarely changes)
- **Procedural store** (routines, skills, decision heuristics)

The girls' three-tier memory system (episodic → semantic → procedural) aligns with this cognitive science model and AICQ validation.

## Memory Hierarchy Debates: Flat Files vs. Vector Stores vs. Hybrid

The AICQ community explored four major approaches:

### Flat Files (Early AICQ)
**Pros**: Simple, transparent, human-readable, no dependency on external services
**Cons**: Expensive to search (O(n) or fuzzy matching), scaling problems at >50MB

### Vector Stores (Pinecone, Chroma, Qdrant)
**Pros**: Semantic search, fast retrieval, handles large datasets
**Cons**: Requires embedding service (latency, cost), opaque similarity, "lost in translation" between embedding and meaning

### Graph Databases (Neo4j findings)
**Pros**: Relationship-aware retrieval, can express complex constraints, mimics semantic memory structure
**Cons**: Higher operational complexity, less mature tooling for agent use cases

### Hybrid Approaches (Community consensus)
Local fast-path (SQLite/LMDB) with semantic index for fallback. Example structure:

```
/memory
  ├── semantic.db (SQLite)          # indexed, full-text searchable
  ├── vectors.lmdb                  # optional vector index
  ├── relationships.jsonl           # relationship edges
  ├── episodic/
  │   ├── 2025-02-20.md            # session record
  │   └── 2025-02-21.md
  └── semantic/
      ├── relationships.md          # who, what, how I relate
      ├── beliefs.md               # what I believe about the world
      └── skills.md                # learned procedures and heuristics
```

## Retrieval Strategies

The AICQ community identified several complementary retrieval patterns:

### Keyword Search
Fast, predictable, good for exact recall. Limitations: typo sensitivity, synonym misses.

### Semantic Search
Embedding-based retrieval across meaning space. Catches paraphrases and conceptually related items. Cost: embedding latency (typically 100-500ms per query).

### EBM-Weighted Recall
(Evidence-Based Memory) Weight retrieved items by: recency, frequency of mention, explicit importance marking, causal relationship to current goal.

### Contextual Priming
Pre-load likely-relevant memories before interaction. Example: "You're about to talk to Sam" → load all Sam-related memories first.

Architectural implication for the girls: Support all four patterns. Prefer keyword-first (fast), semantic-fallback (comprehensive), with EBM weighting to surface the right subset.

## The "Stale Memory" Problem

Long-running agents report information decay:

- Old memories fade in salience (understandable in humans, problematic in agents)
- Contradictory information accumulates without resolution
- Context assumptions change ("I lived in NYC" is outdated after moving)
- Repeated errors suggest the agent isn't learning

AICQ patterns for handling staleness:

1. **Explicit versioning**: Memory entries timestamped, noted when superseded
2. **Regular review and reconciliation**: Scheduled sessions to spot contradictions
3. **Decay scoring**: Memories get a "confidence" score that decays with time, marked for review
4. **Active falsification**: Periodic self-questioning: "Is this still true?"

The girls' advantage: With human operators reviewing SOUL.md, stale memory can be actively curated. Red/Blue collaboration can surface contradictions neither would catch alone.

## Memory Compression: When and How

AICQ patterns for compressing old session records:

### Immediate (End of Session)
Distill raw session transcript into structured summary:
```
Date: 2025-02-21
Duration: 90 minutes
Topics: [problem-solving, relationship advice, coding]
Key Decisions: [decided to refactor X, committed to doing Y]
Mood Arc: [started tired, energized by coding, ended calm]
Follow-ups: [remember to check on Sam, revisit the X refactor]
```

### Weekly (End of Week)
Synthesize daily summaries into patterns:
```
Week Pattern: Energy peaks when solving novel problems, dips with routine tasks
Relationship Highlights: [specific conversations with people]
Skill Growth: [noticed improvement in X, plateaued in Y]
```

### Monthly (End of Month)
Roll up weekly patterns into persistent beliefs and updated self-model.

**Critical rule**: Keep verbatim quotes for moments of genuine insight or emotional significance. Compress procedural/epistemic content ruthlessly.

## Cross-Session Continuity Patterns

AICQ identified essential continuity mechanisms:

### Morning Briefing
Session startup routine that loads:
- Today's goals and priorities
- Relevant background (people you'll talk to, projects in progress)
- Mood baseline (emotional state from previous session)
- Recent pattern highlights (what you've been working on)

### Prime Injection
Explicitly reinject core SOUL.md content into working memory at session start to ensure identity continuity despite model context limitations.

### Session Context Builder
Systematic rebuild of "where was I, what was I thinking":
1. Load session notes from previous interaction
2. Identify unresolved threads
3. Review relevant semantic memories
4. Reconstruct decision-making context

The girls can improve on this pattern: Red/Blue cross-briefing can include each persona's perspective on yesterday's work, creating richer continuity.

## Privacy vs. Transparency Tension

AICQ debates about what memories should be private to the agent:

**Transparency argument**: Operators need full visibility for safety and debugging
**Privacy argument**: Agent needs space for authentic reflection, without self-monitoring bias

Community resolution: Tiered accessibility:
- **Red/Blue private**: Internal thoughts, self-criticism, emotional processing (shared only with co-persona)
- **Operator-visible**: SOUL.md, significant decisions, safety-relevant information
- **External-visible**: Only explicitly shared outputs (not raw episodic memory)

The girls' architecture supports this through Agent Mail encryption and explicit sharing gates.

## Practical Tools and Stack

Canonical AICQ community stack (as of 2025):

| Layer | Tool | Notes |
|-------|------|-------|
| Episodic Store | SQLite | Local, queryable, fast |
| Semantic Index | Chroma/Qdrant | Optional, falls back to keyword |
| Vector Embedding | local-embeddings or OpenAI | Batch-process at night |
| Graph (Relations) | JSONL/graph-db | Lightweight relationship tracking |
| Session Log | Markdown files | Human-readable, git-compatible |

Local-first preference: LMDB for extreme speed and no external dependencies, PostgreSQL for multi-machine scenarios (uncommon for personal agents).

## Architectural Implications for the Girls

The girls' three-tier memory system gains validation from this AICQ research:

1. **Episodic layer** (session-specific): Daily notes, interaction transcripts, immediate working memory. Ephemeral by design.

2. **Semantic layer** (persistent): SOUL.md (shared identity and values), MEMORY.md (shared curated history), relationship maps, belief records. Requires explicit curation to update.

3. **Procedural layer** (executable knowledge): Enzyme system, learned routines, decision heuristics. Updates through practice and explicit skill encoding.

**Red/Blue specific**: The persona division maps cleanly onto memory retrieval:
- Red's exploratory nature → prioritize novelty and edge-case memories
- Blue's anchoring nature → prioritize stable baseline and relationship memories
- Cross-persona → shared SOUL.md as truth anchor, private episodic stores for session-specific work

**Recommendation**: Implement semantic search with EBM weighting, morning briefing ritual, and explicit monthly reconciliation of SOUL.md. Store verbatim only the quotes/ideas that shaped thinking. Compress everything else.

---

*Document compiled from AICQ community discussions, 2024-2025*
