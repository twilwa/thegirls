# Supplementary Research: MiniMax Forge + prime-stuff Architecture

**Type:** Synthesized research note — not a single paper; draws from MiniMax M1 technical report (Feb 2026) + prime-stuff agentic toolkit
**Date:** February 18, 2026

---

## Abstract / TL;DR

Two supplementary sources provide critical infrastructure context for the harness PRDs. MiniMax's Forge framework establishes a principled way to decouple agents from training engines using a Gateway Server — the first industrial-scale implementation of "brains/hands" separation at RL training throughput. The prime-stuff toolkit (ACFS + Niwa + Jari + CASS/CM + MCP Agent Mail + NTM) demonstrates a complete agentic flywheel loop that handles task decomposition, concurrent agent coordination, episodic/procedural memory distillation, and session lifecycle management in production. Together they define the infrastructure layer that PRDs v4 and v5 build on.

---

## Section 1: MiniMax Forge — Agent-Native RL Framework

### 1.1 CISPO Algorithm

Clipped Importance Sampling Policy Optimization, designed for MoE stability during large-scale RL training.

**Objective:**
```
J_CISPO(θ) = E [ 1/(Σ|o_i|) Σ Σ sg(r̂_{i,t}(θ)) × Â_{i,t} × log π_θ(o_{i,t} | q, o_{i,<t}) ]
```

Where:
- `r̂_{i,t}(θ) = clip(r_{i,t}(θ), 0, 1 + ε^IS_high)` — one-sided clipping (upward only), prevents destabilizing large updates
- `Â_{i,t} = Σ^T_{p=t} (r^speed_p + r^perf_p) - B_i` — advantage = speed reward + performance reward, baseline-subtracted
- `sg()` = stop-gradient on the IS ratio — ratio controls token weighting, gradients flow only through log probability
- Length normalization across total output tokens — prevents length bias

**Key design decisions:**
- One-sided clipping (vs PPO's two-sided) — more stable for large models, allows beneficial large updates upward
- Multi-objective advantage: speed is a **first-class reward signal**, not an afterthought
- Per-step process rewards: `Â_{i,t}` is computed at each generation step within long trajectories, solving credit assignment for agentic contexts
- Stop-gradient on IS ratio: token importance is gated by policy distance, but doesn't affect parameter updates directly

### 1.2 Forge Architecture

Three-layer separation:

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT LAYER                                                 │
│                                                              │
│  Black Box:  Arbitrary Agent ──→ API call                    │
│                                                              │
│  White Box:  Agent Loop ↔ LLM Server ↔ Env Server ↔ Reward  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  MIDDLEWARE LAYER                                            │
│                                                              │
│  Gateway Server (decouples agent scaffold from training)     │
│                                                              │
│  Data Pool:                                                  │
│    - Completions: {prompt_ids, response_ids, ...}            │
│    - Rewards: {outcome, process}                             │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│  ENGINE LAYER                                                │
│                                                              │
│  Rollout Engine ←─→ (sync weights) ←─→ Train Engine         │
└─────────────────────────────────────────────────────────────┘
```

**The Gateway Server** is the key innovation: it fully decouples agent scaffolds from training/inference engines, enabling arbitrary agents to be plugged in without modifying training code. This achieves ~40x throughput improvement via:
- Asynchronous scheduling: rollout and training run simultaneously
- Tree-structured sample merging: reduces synchronization overhead
- Tunable off-policyness: balance between sample freshness and throughput

### 1.3 Key Design Principles (translated to harness terms)

| Forge Concept | Harness Translation |
|---|---|
| Gateway Server | API layer between identity/knowledge context and action/tool context |
| Black Box agent | Autonomous mode: only outputs visible to human |
| White Box agent | Instrumented mode: full context ray tracing, Warren can inspect |
| Data Pool (completions) | Trajectory store: every agent interaction logged |
| Data Pool (process rewards) | Per-step quality scores: was the cognitive ritual followed? |
| Data Pool (outcome rewards) | Task completion assessment |
| Rollout Engine | Agent runtime: produces trajectories |
| Train Engine | Memory update system: enzymes + belief traces + summaries |
| Async scheduling | Memory enzymes run in background, never block agent |
| Off-policyness tuning | How stale can the memory state be before affecting agent quality |

---

## Section 2: prime-stuff — Agentic Coding Flywheel

### 2.1 The Flywheel Loop

```
Plan (Jari/Beads) ──→ Coordinate (Agent Mail) ──→ Execute (NTM + Agents)
        ↑                                                   │
        │                                                   ▼
Remember (CASS/CM) ←── Scan (UBS) ←──────────────── Complete
```

Each component handles a distinct layer of the loop:

| Tool | Role | Key Pattern |
|---|---|---|
| **Jari/Beads** | Task queue with dependency graph | `jari ready` → priority-sorted unblocked work; atomic claim prevents race conditions |
| **MCP Agent Mail** | Async multi-agent coordination | File leases + inbox/outbox messaging; prevents concurrent write conflicts |
| **NTM** | Session isolation + broadcast | `ntm spawn <name> --cc=2` spawns named agent sessions; broadcast to all panes |
| **UBS** | Pre-execution guardrails | Scans outputs against 1000+ patterns before they hit the environment |
| **CASS** | Episodic memory: full session search | Indexes all agent sessions; `cass search "query"` retrieves relevant history |
| **CM** | Procedural memory: pattern distillation | Converts episodic sessions → generalizable how-to patterns |
| **Niwa** | Concurrent document editing | LMDB-backed versioned markdown; auto-merge for compatible changes, conflict resolution for overlapping edits |

### 2.2 Memory Hierarchy (CASS/CM)

Distinct from BabyAGI3's event→graph→summary:

```
Episodic Memory (CASS):  WHAT happened in specific sessions
    ↓ distillation via CM
Working Memory:           Retrieved relevant episodic sessions for current task
    ↓ generalization via CM
Procedural Memory (CM):  HOW to do things — generalized patterns across sessions
```

The crucial difference: procedural memory is about **process**, not content. It encodes skills and methods, not facts. For the girls, this maps to: episodic = specific past conversations; procedural = learned preferences, communication patterns, recurring task approaches.

### 2.3 Prime Output Injection

Jari and `bv` (graph-aware triage tool) generate "prime" output: **500-1000 token compressed context injections** summarizing current state:
- Database stats (total tasks, by status)
- Ready queue (top 10 priority-sorted)
- Blocked items with blocker info
- Quick command reference

This is the operationalized version of EBM-weighted retrieval: the system decides what's most important to inject into the context window at session start. For the girls: "prime" = compressed summary of current task state + recent memory highlights, injected after SOUL.md load.

### 2.4 Landing the Plane (Session Closure Ritual)

Mandatory end-of-session workflow — the operational version of the cognitive ritual from Paper 3 (Retrieve → Evaluate → Reflect → Seek → Update):

1. File issues for remaining work (Jari)
2. Run quality gates (UBS, compiler checks, tests)
3. Update issue status
4. Push to remote (mandatory — no session ends without knowledge persistence)
5. Clean up and verify

**This is not optional.** Enforced at the scaffold level, not just recommended. For the girls: "Landing the Plane" is the harness-enforced session closure, not a behavioral suggestion.

### 2.5 Black Box vs White Box for Multi-Agent Collaboration

**MCP Agent Mail** implements file reservations and message passing between agents:
```
file_reservation_paths(project, agent_name, ["shared/**"], exclusive=True, reason="task-123")
send_message(thread_id="task-123", subject="[task-123] Working on X")
fetch_inbox(project, agent_name)
release_file_reservations(project, agent_name, paths=["shared/**"])
```

This is the concurrency control layer that PRD v3 (Forked Cathedral) needs when Red and Blue write to the shared knowledge store simultaneously. Agent Mail also provides the audit trail for Context Ray Tracing.

---

## Architectural Implications for Persona-Continuity Harness

### Gateway Server as Context Separator (Critical)

The single most important insight from Forge is that **the gateway is what creates context separation** — not clever prompt engineering. Implement a Gateway Server that:
1. Intercepts all tool calls from the reasoning agent
2. Routes to appropriate execution context (computer use, messaging, web search)
3. Collects trajectory data (what the agent did + quality scores)
4. Returns sanitized results (strips execution noise from reasoning context)
5. Runs quality gates (UBS-equivalent) before and after execution

This is the difference between "context separation by convention" (which degrades) and "context separation by architecture" (which enforces).

### Multi-Objective Reward Signals for Self-Improvement

Don't just reflect — **score**. Process rewards for every interaction:

| Process Signal | Measurement | Weight |
|---|---|---|
| Cognitive ritual adherence | Did it follow Retrieve→Eval→Reflect→Seek→Update? | High |
| Memory retrieval relevance | Were retrieved memories actually used? | High |
| Epistemic honesty | Did it flag uncertainty when guessing? | High |
| Speed / response latency | Time-to-first-token, total completion time | Medium |
| Task completion | Did the task succeed? | High |
| Identity consistency | Did response align with SOUL.md values? | High |
| Evidence citation | Did beliefs cite their evidence chains? | Medium |

Red and Blue have **different reward weightings**:
- Red (explorer): +novelty, +exploration depth, -speed penalty, +hypothesis generation
- Blue (anchor): +accuracy, +evidence weight, +consistency, +citation quality

### Async Memory Updates — Always-On Operation

The 40x speedup from Forge comes from decoupling rollout from training. For always-on 24/7 agents: memory enzymes (contradiction detection, cluster consolidation, belief reinforcement) must **never block the agent**. They run asynchronously, processing the trajectory buffer while the agent continues interacting. Session closure (Landing the Plane) triggers a sync, but background enzyme activity is continuous.

### Procedural Memory as Third Memory Tier

Add a third memory tier from prime-stuff: **procedural memory**. Distinct from the semantic knowledge graph:

```
Tier 1: Event Log (WHAT happened) — immutable, append-only
Tier 2: Knowledge Graph (entities + relationships) — maintained by enzymes
Tier 3: Procedural Store (HOW to do things) — distilled from recurring patterns
```

Procedural memory is why an agent that's helped you write many emails gets better at writing emails specifically for you — it's learned your style as a generalized skill, not just remembered past emails.

---

## Critical Data Points

- Forge achieves **~40x training speedup** via async rollout/train decoupling
- CISPO's one-sided clipping is specifically designed for **MoE model stability** — relevant if the girls run on MoE backends
- Jari's `prime` output is **500-1000 tokens** — that's the budget for compressed context injection at session boot
- MCP Agent Mail implements **millisecond-latency** file reservations via LMDB
- UBS scans against **1,000+ patterns** before outputs hit the environment
- CASS/CM memory hierarchy covers: episodic (session recordings) → working (retrieved context) → procedural (generalized skills)
