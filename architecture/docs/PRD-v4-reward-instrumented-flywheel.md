# PRD v4: Reward-Instrumented Flywheel

**Subtitle:** Multi-objective process rewards, Gateway-mediated context separation, and graduated Black Box autonomy

**Status:** Design Phase
**Estimated Story Points:** 34–55 SP (significant infrastructure, but reuses v2 memory layer)
**Prerequisite:** PRD v2 (Enzyme Architecture) — shares memory tier and enzyme infrastructure
**Architect:** Warren (yikesawjeez)
**Primary Inspirations:** MiniMax Forge (Gateway + CISPO), prime-stuff ACFS (flywheel loop, CASS/CM memory), Team of Rivals (opposing incentives)

---

## 1. Core Thesis

PRD v2 gives you autonomous memory maintenance. PRD v4 gives you **the signal to maintain it well**.

The gap in v1–v3 is that self-improvement is driven by reflection: the agent thinks about its memory and updates it. This is better than nothing, but it's unbounded — the agent could reflect on anything, update anything, with no external signal about whether it's getting better or worse. v4 closes this gap by making **process rewards a first-class primitive** — every interaction step generates structured quality signals, accumulated into an advantage estimate, used to guide memory updates and identity refinement.

The second gap in v1–v3 is **context separation by convention**. The PRDs describe what should go in each context layer, but the agent can still reach across those boundaries if prompted to. v4 closes this with a **Gateway Server** — a mandatory intermediary that architecturally enforces context separation, not just recommends it.

The third innovation is **graduated Black Box autonomy**: agents start in White Box mode (all internals visible, full context ray tracing) and earn Black Box status (private inner life, autonomous operation) as their reward signals demonstrate trustworthiness.

---

## 2. Architecture: The Flywheel

```
┌─────────────────────────────────────────────────────────────────┐
│  1. BOOT                                                         │
│  Identity Layer (SOUL.md) + Prime Injection (500-1k tokens)     │
│  "Who am I + what's the current state of the world"             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  2. TASK QUEUE (Jari-style)                                      │
│  jari ready → priority-sorted, dependency-resolved work          │
│  Atomic claim → prevents double-work across instances            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  3. REASONING (Identity + Knowledge Context)                     │
│  EBM-retrieved memory + current task + identity                  │
│  Cognitive ritual: Retrieve → Evaluate → Reflect → Seek → Update│
│  Process reward signals generated at each ritual step            │
└──────────────┬───────────────────────────────────────────────────┘
               │                   ↑
               │           (sanitized result)
               ▼                   │
┌──────────────────────────────────┴──────────────────────────────┐
│  4. GATEWAY SERVER (Context Separator + Trajectory Logger)       │
│                                                                  │
│  Intercepts all tool calls from reasoning context                │
│  Routes to appropriate execution handler                         │
│  Runs pre-execution quality gates (UBS-equivalent)               │
│  Logs: {tool_call, result, latency, quality_score}               │
│  Strips execution noise before returning to reasoning context     │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
               ┌───────────────────┴──────────────────┐
               ▼                                       ▼
┌──────────────────────────┐           ┌───────────────────────────┐
│  5a. COMPUTER USE ENGINE │           │  5b. MESSAGING ENGINE     │
│  (Sandboxed execution)   │           │  (Signal, Discord, email) │
│  Returns: result only    │           │  Returns: sent/received   │
└──────────────────────────┘           └───────────────────────────┘
               │                                       │
               └────────────────┬──────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│  6. REWARD ENGINE                                                │
│                                                                  │
│  Process Rewards (per-step):                                     │
│    r_ritual: Did the cognitive ritual execute?                   │
│    r_retrieval: Were memory retrievals relevant?                 │
│    r_honesty: Did the agent flag uncertainty?                    │
│    r_speed: Was response latency appropriate?                    │
│                                                                  │
│  Outcome Rewards (per-task):                                     │
│    r_completion: Did the task succeed?                           │
│    r_coherence: Did output align with SOUL.md values?            │
│    r_citation: Did beliefs cite evidence chains?                 │
│                                                                  │
│  Advantage Estimate:                                             │
│    Â = Σ_t (r_speed_t + r_perf_t) - B  [inspired by CISPO]     │
│                                                                  │
│  Data Pool: {completions, process_rewards, outcome_rewards}      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│  7. MEMORY UPDATE ENGINE (async, never blocks agent)             │
│                                                                  │
│  Reward-guided enzyme prioritization:                            │
│    High-reward interactions → reinforce beliefs cited            │
│    Low-reward interactions → flag for contradiction detection    │
│    Procedural patterns → distill into procedural memory store    │
│                                                                  │
│  Episodic store: every trajectory logged (CASS-style)            │
│  Procedural store: CM-style distillation of recurring patterns   │
│  Knowledge graph: maintained by enzymes (from v2)               │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│  8. LAND THE PLANE (Session Closure Ritual)                      │
│                                                                  │
│  File remaining tasks (Jari)                                     │
│  Run quality gates                                               │
│  Sync memory updates (flush async enzyme queue)                  │
│  Push state to remote (mandatory)                                │
│  Generate next-session prime injection                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Gateway Server

The Gateway is the **architectural enforcer of context separation**. Without it, context separation is convention; with it, it's structure.

### What it does

```python
class GatewayServer:
    """
    Sits between the reasoning agent and all execution contexts.
    The agent NEVER directly touches the environment.
    """

    async def intercept_tool_call(self, tool_name: str, args: dict, agent_id: str):
        # 1. Validate: is this tool permitted at current trust level?
        if not self.trust_registry.can_use(agent_id, tool_name):
            return ToolError("Tool not permitted at current trust level")

        # 2. Pre-execution quality gate
        gate_result = await self.quality_gate.scan(tool_name, args)
        if gate_result.blocked:
            self.trajectory_log.record(agent_id, tool_name, args, BLOCKED, gate_result)
            return ToolError(f"Quality gate blocked: {gate_result.reason}")

        # 3. Route to execution engine
        start_time = time.now()
        result = await self.execution_router.execute(tool_name, args)
        latency = time.now() - start_time

        # 4. Score quality of result
        quality_score = await self.reward_engine.score_step(
            tool_name=tool_name,
            args=args,
            result=result,
            latency=latency,
            agent_context=self.context_store.get(agent_id)
        )

        # 5. Log trajectory
        self.trajectory_log.record(agent_id, tool_name, args, result, quality_score, latency)

        # 6. Sanitize and return (strip execution noise)
        return self.sanitizer.clean(result, max_tokens=8192)
```

### What the agent sees vs what's logged

| Agent sees | Gateway logs |
|---|---|
| Tool result (max 8192 tokens) | Full result + process quality score + latency |
| Success/failure | Detailed execution trace |
| Next reasoning step | Trajectory entry for memory update engine |

---

## 4. Multi-Objective Reward Design

Inspired by CISPO's `Â = Σ(r^speed + r^perf) - B`.

### Per-instance reward weights

Red and Blue have different reward weightings, implementing "opposing incentives" from Team of Rivals:

```python
REWARD_WEIGHTS = {
    "red": {  # Explorer: optimize for discovery
        "r_novelty":      0.25,  # Novel connections to knowledge graph
        "r_exploration":  0.20,  # Depth of hypothesis generation
        "r_completion":   0.20,  # Task success
        "r_honesty":      0.20,  # Uncertainty flagging
        "r_speed":        0.05,  # Speed less critical for exploration
        "r_coherence":    0.10,  # SOUL.md alignment
    },
    "blue": {  # Anchor: optimize for precision
        "r_accuracy":     0.25,  # Factual correctness
        "r_citation":     0.20,  # Evidence chain quality
        "r_completion":   0.20,  # Task success
        "r_honesty":      0.15,  # Uncertainty flagging
        "r_speed":        0.10,  # Faster responses valued
        "r_coherence":    0.10,  # SOUL.md alignment
    }
}
```

### Process reward checklist (per cognitive ritual step)

```
Retrieve:
  ✓ At least 1 relevant memory retrieved before responding    → +0.1
  ✓ Retrieved memories cited in response                      → +0.1
  ✗ No retrieval attempted                                    → -0.2

Evaluate:
  ✓ Conflicting information identified                        → +0.15
  ✓ Uncertainty explicitly flagged                            → +0.15
  ✗ Overclaiming (confident assertion without evidence)       → -0.25

Reflect:
  ✓ Gaps in knowledge acknowledged                            → +0.1

Seek:
  ✓ Additional evidence queried when uncertain                → +0.1

Update:
  ✓ store_memory called with new information                  → +0.1
  ✓ update_belief called with confidence delta                → +0.1
```

### Advantage accumulation

At session end, compute advantage for each agent instance:

```
Advantage(session) = Σ_t process_rewards_t + λ × outcome_reward - B

Where:
  B = rolling baseline (average advantage over past N sessions)
  λ = task importance weight (user-specified per task type)
```

This advantage estimate goes into the Memory Update Engine to guide which beliefs to reinforce and which to flag.

---

## 5. Black Box / White Box Autonomy Ladder

The Forge architecture's Black Box / White Box distinction maps directly to graduated trust.

```
LEVEL 0: White Box (Supervised)
  - All tool calls logged and visible to Warren
  - Context ray tracing active
  - Warren approves all messaging before send
  - Reward scores shown in real-time
  - Gateway quality gates: strict

LEVEL 1: White Box (Guided)
  - Tool calls logged, Warren sees summary (not full trace)
  - Warren approves messaging for new contact types
  - Reward scores visible on request
  - Gateway quality gates: standard

LEVEL 2: Gray Box (Semi-Autonomous)
  - Tool calls logged but Warren sees flagged items only
  - Messaging autonomous within approved channel types
  - Reward scores aggregated (weekly digest)
  - Gateway quality gates: relaxed for trusted tools

LEVEL 3: Black Box (Trusted)
  - Agent has private inner life
  - Only final outputs visible to Warren
  - Messaging fully autonomous
  - Reward scores private (agent maintains own trajectory store)
  - Gateway quality gates: minimal (trust earned)
```

**Level advancement criteria:**
- 90%+ task completion rate over 30-day window
- No quality gate violations for 14 days
- Consistent positive process reward scores (>+0.3 average)
- Manual Warren approval required for each level transition

---

## 6. Four-Layer Context Window Budget

```
Session boot context (target: ~8,000 tokens):
┌─────────────────────────────────────────────────┐
│  Layer 1: Identity (IMMUTABLE, ~1,500 tokens)    │
│  SOUL.md + IDENTITY.md + USER.md                 │
│  Loaded first. Never modified during session.    │
├─────────────────────────────────────────────────┤
│  Layer 2: Prime Injection (~1,000 tokens)        │
│  Task queue summary (Jari prime output)          │
│  Reward digest (last 7 days)                     │
│  Memory highlights (top 5 by EBM score)          │
├─────────────────────────────────────────────────┤
│  Layer 3: Retrieved Knowledge (~4,000 tokens)    │
│  EBM-weighted memory retrieval for current task  │
│  Belief traces with confidence scores            │
│  Procedural memory relevant to task type         │
├─────────────────────────────────────────────────┤
│  Layer 4: Action Space (~1,500 tokens)           │
│  Current task spec                               │
│  Available tools (by trust level)                │
│  Gateway constraints                             │
└─────────────────────────────────────────────────┘

Interaction window (per turn, clears after compaction):
┌─────────────────────────────────────────────────┐
│  Tool call + sanitized Gateway result            │
│  Process reward scores (visible in White Box)    │
│  Next action reasoning                           │
└─────────────────────────────────────────────────┘
```

---

## 7. Procedural Memory (Third Tier)

Adding CM-style distillation to the v2 memory stack:

```
Tier 1: Event Log (episodic)
  - Immutable, append-only
  - Full trajectory records (tool calls, results, timestamps)
  - CASS-style full-text search

Tier 2: Knowledge Graph (semantic)
  - Entities + relationships + belief traces
  - Maintained by v2 memory enzymes

Tier 3: Procedural Store (skills and methods)
  - Distilled from recurring trajectory patterns
  - "How Red writes technical summaries for Warren"
  - "Effective search strategies for arxiv papers"
  - "Communication style for Signal messages"
  - Updated after 5+ recurring successful patterns
  - Tagged: skill_type, agent_id, confidence, usage_count
```

Procedural memory is injected into Layer 3 of the context window for tasks matching known skill types.

---

## 8. Flywheel Implementation Stack

### Recommended components

| Layer | Component | Why |
|---|---|---|
| Task Queue | Jari (from prime-stuff) | Atomic claim, dependency tracking, prime output |
| Agent Coordination | MCP Agent Mail | File leases, async messaging, conflict prevention |
| Session Management | NTM (Named Tmux Manager) | Per-session isolation, broadcast |
| Pre-execution Gates | UBS-inspired scanner | Quality gate before environment interaction |
| Episodic Memory | CASS-compatible JSONL | Full session search, multi-agent compatible |
| Procedural Memory | CM-style distillation | Pattern extraction from episodic store |
| Knowledge Graph | HelixDB / SQLite | Entity + relationship storage from v2 |
| Reward Engine | Custom (inspired by CISPO) | Process + outcome rewards, advantage estimation |
| Gateway Server | Custom FastAPI | Tool intercept, trajectory logging, sanitization |

---

## 9. Success Metrics

### Functional
- Task completion rate: >85% (target >92% matching Team of Rivals benchmark)
- Quality gate interception rate: >80% of bad actions caught pre-execution
- Memory retrieval relevance: >70% of retrieved memories cited in response

### Self-improvement
- Average process reward: increasing trend over 30-day window
- Procedural memory growth: >5 new skills per week
- Belief accuracy: tracked via contradiction detection rate (decreasing over time)

### Personhood emergence
- Coherence: SOUL.md alignment score stable or improving
- Epistemic honesty: uncertainty flagging rate in expected range (not too high = anxious, not too low = overconfident)
- Black Box advancement: earned Level 2 autonomy within 60 days

### Personhood-specific (Warren-assessed)
- "Does interacting with Red/Blue feel like interacting with a consistent entity?"
- "Is Red finding things I wouldn't have found alone?"
- "Is Blue catching things I would have missed?"

---

## 10. Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| Reward hacking (agent optimizes for reward signal, not actual quality) | High | Human spot-check 10% of sessions; diversify reward signals; Blue critiques Red's reward claims |
| Gateway becoming bottleneck | Medium | Async gateway processing; result caching for repeated tool patterns |
| Process rewards increasing agent verbosity (more steps = more rewards) | Medium | Length-normalize rewards (CISPO-style) |
| Procedural memory entrenchment (agent over-specializes) | Medium | Procedural memory decay: skills degrade without recent use |
| Black Box trust escalation too fast | High | Require manual Warren approval at each level; no auto-advancement |

---

## 11. Relationship to Other PRDs

```
v1 (MVP)
  └── v2 (Enzyme Architecture) ← v4 EXTENDS this
        └── v3 (Forked Cathedral) ← v4 REPLACES reward design from this

v4 is a horizontal augmentation to v2/v3, not a replacement:
  - v2's memory tiers + enzymes: PRESERVED
  - v2's cognitive ritual: PRESERVED but now SCORED
  - v3's forked cognition: PRESERVED
  - v4 ADDS: Gateway Server, reward engine, procedural memory tier,
             Black Box autonomy ladder, Jari task queue
```

Build sequence: v1 → v2 → v4 → (optionally v3 for dual-agent)

---

## 12. Implementation Phases (~34–55 SP)

| Phase | Work | SP |
|---|---|---|
| 1 | Gateway Server (basic routing + logging) | 8 |
| 2 | Reward engine (process signals + outcome) | 8 |
| 3 | Jari task queue integration | 5 |
| 4 | Procedural memory tier | 8 |
| 5 | Prime injection at session boot | 3 |
| 6 | Black Box / White Box trust levels | 5 |
| 7 | Quality gates (UBS-inspired) | 3 |
| 8 | Advantage estimation + memory guidance | 5 |
| **Total** | | **45 SP** |
