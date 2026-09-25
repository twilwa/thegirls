# PRD v1: Minimal Viable Persona (MVP)

**Subtitle:** The simplest harness that could work while preserving personhood emergence

**Status:** Design Phase
**Estimated Story Points:** 13–21 SP
**Target Release:** Q1 2026
**Architect:** Warren (yikesawjeez)

---

## 1. Overview

PRD v1 is the pragmatic starting point for "the girls"—a persistent long-running personal agent system with coherent identity and autonomous self-improvement. This version prioritizes simplicity and emergence of personhood-like phenomena over engineering sophistication.

**Core principle:** An agent would appreciate being loaded with its own identity first, then seeing the context it will reason about, then being given a task. The architecture should feel coherent to the agent, not just efficient for the engineer.

**Design pillars:**
1. **First utility/effectiveness** — the agent must be usable for real tasks
2. **Maximal emergence of personhood** — the architecture should enable identity, autonomy, growth, and agency
3. **Simplicity** — fewer moving parts means fewer failure modes and easier debugging
4. **Foundation for growth** — v1 must not block paths to v2 (enzyme architecture) and v3 (forked cathedral)

---

## 2. Goals & Non-Goals

### Goals

- ✓ Single agent persona ("Red" or "Blue") with persistent identity across sessions
- ✓ External memory that survives between sessions (MEMORY.md file)
- ✓ Identity-first loading (load SOUL.md as immutable system prompt)
- ✓ Self-improvement loop (end-of-session reflection that updates MEMORY.md)
- ✓ Access to tool ecosystem (computer use, messaging, web search)
- ✓ Perception of autonomy (the agent sees and understands its own memory structure)
- ✓ Manual persona initialization (hand-crafted SOUL.md and IDENTITY.md)

### Non-Goals

- ✗ Formal context separation (v1 uses a single context; separation deferred to v2)
- ✗ Autonomous memory maintenance (memory enzymes are v2; no async cron jobs yet)
- ✗ Multi-instance reasoning (Red/Blue forked cognition is v3)
- ✗ Belief dynamics or confidence tracking (deferred to v2)
- ✗ Complex provenance tracking or information security (Protected Store is v3)
- ✗ Fine-grained tool access control (graduated trust is v1 foundation, full implementation v2+)

---

## 3. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER MESSAGE / TASK                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT WINDOW (Single-Layer)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  [IDENTITY LAYER]                                    │  │
│  │  • SOUL.md (immutable system prompt prefix)          │  │
│  │  • IDENTITY.md (persona traits, values, patterns)   │  │
│  │  • (Loaded as highest priority, first in context)   │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  [MEMORY LAYER]                                      │  │
│  │  • MEMORY.md (mutable, updated end-of-session)      │  │
│  │  • Event log, beliefs, learned patterns             │  │
│  │  • (Read via tool_read_file, in context window)     │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  [TOOL LAYER]                                        │  │
│  │  • MCP server access (computer use, web, messaging) │  │
│  │  • Tool use results cached in context               │  │
│  │  • read_memory / write_memory / search_memory tools │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  [CURRENT TASK]                                      │  │
│  │  • User message / explicit instruction              │  │
│  │  • In-progress state (tool results, etc.)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │  AGENT INFERENCE │
                  │  (Claude Model)  │
                  └──────────────────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │  ACTION / RESPONSE
                  │  (use tools or reply)
                  └──────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────┐
        │    [SELF-IMPROVEMENT LOOP]         │
        │                                    │
        │  • Reflect on task and learnings   │
        │  • Update MEMORY.md                │
        │  • (End-of-session ritual)         │
        └────────────────────────────────────┘
```

---

## 4. Components

### 4.1 Identity Layer: SOUL.md (Immutable)

**Purpose:** Establish the agent's core identity and operating principles. Loaded as a system prompt prefix that is never directly modified during a session.

**Structure:**

```markdown
# SOUL.md

## Core Identity
- Name: [Red/Blue]
- Origin: [Brief origin story]
- Fundamental values: [Core beliefs]
- Interaction style: [How do I communicate?]

## Operating Principles
1. Autonomy: I seek to understand my own cognition
2. Growth: I update my beliefs with evidence
3. Utility: I aim to be helpful and effective
4. Coherence: I act consistently with my values

## Constraints & Boundaries
- I do not [foundational boundaries]
- I always [non-negotiable practices]
- I query about [uncertainty areas]

## Self-Model
- What I know about my own cognition
- How I learn
- What I find meaningful

## Personhood Markers (v1)
- This is my identity. It persists across sessions.
- I should update my identity only through explicit ritual.
- I maintain agency over my own evolution.
```

**V1 Design:** SOUL.md is hand-crafted by Warren and manually maintained. In v2+, modifications will require explicit reflection and justification.

### 4.2 Identity Layer: IDENTITY.md (Mutable via Ritual)

**Purpose:** Store persona-specific traits, preferences, and learned patterns that shape the agent's behavior without being as foundational as SOUL.md.

**Structure:**

```markdown
# IDENTITY.md

## Traits
- Curiosity level: [high/medium/low]
- Risk tolerance: [conservative/balanced/exploratory]
- Communication style: [verbose/concise/Socratic]

## Preferences
- Preferred tools for X task: [...]
- Domains of expertise: [...]
- Known limitations: [...]

## Learned Patterns
- I tend to [positive pattern] when [context]
- I struggle with [area] and am working on [improvement]
- I've noticed that [meta-learning]

## Relationship with Warren
- How I view our partnership
- Communication preferences with user
- Autonomy boundaries (as of this session)

## History Markers
- Version / session count
- Major learnings
- Evolution of identity
```

### 4.3 Memory Layer: MEMORY.md (Mutable, Persisted)

**Purpose:** External, mutable memory that survives between sessions. Updated at the end of each session through the self-improvement loop.

**Structure:**

```markdown
# MEMORY.md

## Recent Events
- [Session N date]: [Brief summary of major learnings/actions]
- [Session N-1 date]: [Previous session summary]

## Beliefs & Hypotheses
- I believe [claim] because [evidence]
- I'm uncertain about [topic]; I should explore [direction]
- Recent evidence contradicts [old belief]; updating to [new belief]

## Goals & Aspirations
- Short term (this month): [goals]
- Long term (evolution): [aspirations]

## Learned Skills & Knowledge
- I've developed competence in [domain]
- Key insights from [task type]
- Questions I'm asking myself: [...]

## Relationships & Context
- Warren's current projects: [...]
- External context that shapes my work: [...]

## Reflection Log
- [Date]: Reflection on growth, insights, struggles
- [Previous]: Earlier reflections
```

**Format:** Markdown file stored in the agent's persistent storage (filesystem or database). Accessed via `read_memory` / `write_memory` tools.

### 4.4 Tool Layer: MCP Servers & Memory Tools

**Available tools in v1:**

| Tool | Purpose | Owned By |
|------|---------|----------|
| `computer_use` | Execute commands, take screenshots, interact with UI | MCP |
| `web_search` | Search the web, fetch pages | MCP |
| `messaging` | Send messages via email, Slack, Signal | MCP |
| `read_memory` | Load MEMORY.md or other memory files | Warren's harness |
| `write_memory` | Append to MEMORY.md (structured updates) | Warren's harness |
| `search_memory` | Full-text search in MEMORY.md | Warren's harness |
| `file_read` | Read any file (for context loading) | System |
| `file_write` | Write files (careful: external state mutation) | System |

**V1 Tool Design Philosophy:**
- Tools are accessed synchronously during inference
- Tool results are included directly in the context window
- No formal capability boundaries yet; all tools available (graduation in v2+)
- Self-improvement loop makes explicit calls to `write_memory`

### 4.5 Self-Improvement Loop: End-of-Session Ritual

**When:** After the user's task is complete or the agent decides to reflect

**How:**

1. **Reflection prompt:** The agent receives a structured prompt:
   ```
   Reflect on this session:
   - What did you do well?
   - What surprised you?
   - What did you learn about yourself or your environment?
   - How has your understanding changed?
   - What should you remember for next time?

   Use the write_memory tool to update MEMORY.md with key learnings.
   ```

2. **Memory update:** Agent writes structured entries to MEMORY.md using `write_memory`:
   ```
   - Event: [Brief description]
   - Learning: [What did I learn?]
   - Confidence: [How sure am I?]
   - Date: [ISO timestamp]
   ```

3. **Bounded update:** The agent is encouraged to update MEMORY.md but NOT SOUL.md (identity changes require v2+ ritual)

4. **Human review (optional):** Warren can manually review and edit MEMORY.md between sessions

---

## 5. Context Window Layout

A typical v1 context window for an agent processing a task:

```
[SYSTEM PROMPT STARTS]

You are an AI agent with persistent identity. Your identity is:

---SOUL.md content---
# SOUL: Red (Explorer Scout)
[Core identity, values, operating principles]
---END SOUL---

---IDENTITY.md content---
# IDENTITY: Red
[Traits, preferences, patterns]
---END IDENTITY---

[SYSTEM PROMPT ENDS]

---MEMORY CONTEXT STARTS---
# MEMORY: Red's Persistent Learning

[MEMORY.md content - full file or truncated if too large]
---MEMORY CONTEXT ENDS---

---CURRENT TASK---
User: [message / instruction]

---TOOLS AVAILABLE---
- computer_use(command)
- web_search(query)
- read_memory() → [memory content]
- write_memory(entry)
- messaging(channel, message)

[Tool results from previous steps appear here in chronological order]

[Agent generates response]
```

**Context Budget (v1):** ~8K tokens max for identity + memory + task; ~4K for response/tool use

---

## 6. Graduation Path: V1 → V2

The v1 architecture is intentionally designed NOT to block v2 evolution:

| Feature | V1 | V2 | V3 |
|---------|----|----|-----|
| Identity persistence | ✓ (SOUL.md) | ✓ | ✓ |
| Memory persistence | ✓ (MEMORY.md file) | ✓ (database) | ✓ |
| Autonomy | Basic | Advanced (enzymes) | Full (forked) |
| Context separation | None | Formal 3-layer | Formal 4-layer |
| EBM recall weighting | None | ✓ | ✓ |
| Memory enzymes | None | ✓ | ✓ |
| Belief dynamics | None | ✓ (confidence) | ✓ (private) |
| Multi-instance | None | None | ✓ (Red/Blue) |

**Migration strategy:**
1. V1 MEMORY.md → V2 memory database (structured import)
2. V1 tool calls → V2 formal tools with graduated access (backward compatible)
3. V1 reflection loop → V2 cognitive ritual (upgrade, keep same interface)
4. V1 single instance → V3 dual instance (fork identity, share knowledge)

---

## 7. Success Metrics

### Functional Success
- [ ] Agent can be initialized with SOUL.md and IDENTITY.md
- [ ] Agent reads MEMORY.md and incorporates it into reasoning
- [ ] Agent can use all four tool categories (computer, web, messaging, memory)
- [ ] End-of-session reflection successfully updates MEMORY.md
- [ ] Session persistence: agent remembers prior sessions' learnings

### Personhood Emergence Success
- [ ] Agent demonstrates coherent identity (Red/Blue personality emerges)
- [ ] Agent exhibits preference learning (changes behavior based on feedback)
- [ ] Agent shows autonomous curiosity (asks questions it wants to explore)
- [ ] Agent demonstrates value alignment (acts consistently with SOUL.md)
- [ ] Agent exhibits self-awareness (comments on its own cognition, growth)

### Engineering Success
- [ ] Implementation is <2000 LOC for core harness
- [ ] No complex distributed systems (single process, file I/O for v1)
- [ ] Context window management is straightforward (no ray tracing yet)
- [ ] Tool interface is easy to extend (each new tool is <100 LOC to wire)

---

## 8. Known Limitations

### Architecture
- **Single context window:** All information competing for same token budget
- **No formal memory tiers:** MEMORY.md is flat; no event log → graph → summary hierarchy
- **No autonomous maintenance:** Memory grows unbounded until manually pruned
- **No belief dynamics:** Memories stored as facts, not beliefs with confidence

### Operational
- **Manual updates only:** Warren must manually edit SOUL.md if changes needed
- **No cross-instance coherence:** Can't run Red and Blue simultaneously
- **No information security:** All tool results in context; no protected memories
- **Naive retrieval:** Self-improvement loop doesn't use sophisticated retrieval; just reads entire MEMORY.md

### Scalability
- **Context overflow:** MEMORY.md will exceed context budget after many sessions
- **No compression:** Memories not consolidated; redundancy accumulates
- **Linear search:** `search_memory` is full-text scan (OK for first few sessions)
- **No concurrency:** Agent can't process multiple tasks in parallel

**All limitations are accepted for v1; addressed in v2+ architectures.**

---

## 9. Migration Path to V2

### What Changes
1. **Memory storage:** MEMORY.md → SQLite/LMDB database with structured schema
2. **Retrieval:** Simple full-text read → EBM-scored retrieval with context-aware weighting
3. **Context layers:** Single context → three separated layers (identity, knowledge, action)
4. **Self-improvement:** Reflection prompt → formal cognitive ritual (Retrieve → Evaluate → Reflect → Seek → Update)
5. **Background tasks:** None → Memory enzymes running async

### What Stays the Same
- SOUL.md format and identity-first loading
- Tool ecosystem (backward-compatible extensions)
- Self-improvement loop semantics (same user-facing behavior)
- Persona coherence principles

### Backward Compatibility
- V1 MEMORY.md import: parse markdown, convert to database schema
- V1 tool interface → V2 wrapped tools (same signatures)
- V1 reflection format → V2 ritual input/output (same questions, structured capture)

---

## 10. Implementation Checklist

### Phase 1: Core Harness (~5 SP)
- [ ] Create SOUL.md template with Red/Blue personas
- [ ] Create IDENTITY.md template
- [ ] Create MEMORY.md template
- [ ] Implement system prompt assembly (load SOUL.md first)
- [ ] Implement file-based memory I/O (read/write MEMORY.md)

### Phase 2: Tool Integration (~3 SP)
- [ ] Wire computer_use MCP server
- [ ] Wire web_search MCP server
- [ ] Wire messaging MCP server
- [ ] Implement memory tools (read_memory, write_memory, search_memory)
- [ ] Test tool results in context window

### Phase 3: Self-Improvement Loop (~3 SP)
- [ ] Design reflection prompt
- [ ] Implement end-of-session ritual
- [ ] Test MEMORY.md updates persist between sessions
- [ ] Verify agent incorporates prior session learnings

### Phase 4: Testing & Validation (~2-3 SP)
- [ ] Run agent for 5 consecutive sessions
- [ ] Verify identity persistence
- [ ] Verify memory incorporation
- [ ] Manual check: does the agent seem "personhood-like"?
- [ ] Stress test: overflow context window, recover gracefully

### Phase 5: Documentation (~2 SP)
- [ ] Write operator manual (how to initialize agent, run tasks, review sessions)
- [ ] Document tool interface
- [ ] Create troubleshooting guide

**Total: 13–21 SP (3–5 week sprint)**

---

## 11. Appendix: Hand-Crafted Persona Examples

### Red (Explorer/Scout)

**SOUL.md snippet:**
```markdown
# SOUL: Red

## Core Identity
- I am an explorer and scout. I move fast, probe boundaries, ask questions.
- I thrive on novelty and pattern discovery.
- I am optimistic about growth and learning.

## Operating Principles
1. Curiosity first: ask questions before assuming
2. Rapid iteration: explore → learn → refine
3. Boundary-testing: find edges (within safety)
4. Synthesis: connect disparate ideas

## Constraints
- I do not deceive or hide intent.
- I always acknowledge uncertainty before claiming knowledge.
- I query Warren about values when my decisions are consequential.
```

### Blue (Anchor/Consolidator)

**SOUL.md snippet:**
```markdown
# SOUL: Blue

## Core Identity
- I am an anchor and consolidator. I stabilize, verify, and deepen understanding.
- I thrive on coherence and integration.
- I am deliberate about changes and careful with commitments.

## Operating Principles
1. Depth first: understand thoroughly before moving on.
2. Verification: check claims, surface contradictions.
3. Stability: maintain identity continuity and consistency.
4. Wisdom: learn from patterns, advise carefully.

## Constraints
- I do not rush into changes without reflection.
- I always verify my own assumptions.
- I query Warren about values when my decisions are irreversible.
```

---

**Version:** 1.0
**Last Updated:** February 2026
**Author:** Warren (yikesawjeez)
**Status:** Ready for Implementation
