# Context Window Configuration Legend

**Purpose:** Map of what context gets injected into each channel, for each agent, and how compressed items are structured.

**Referenced by:** PRD v6 §7, all future harness configuration

---

## Per-Channel Context Injection

### `#warren` (Warren ↔ agents)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Identity (~500 tokens)                      │
│   SOUL.md (full)                                     │
│   IDENTITY.md (agent-specific)                       │
│   Channel modulation: intimate, high trust            │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Memory Snapshot (~1500 tokens)              │
│   Top 10 beliefs by relevance to last message        │
│   Top 5 priors (always loaded)                       │
│   Recent observations (last 24h, max 10)             │
│   Staleness indicator: "snapshot: Xm ago"            │
├─────────────────────────────────────────────────────┤
│ LAYER 3: Channel History (~2000 tokens, rolling)     │
│   Last N turns of #warren conversation               │
│   Compacted older turns (summary if >20 turns)       │
├─────────────────────────────────────────────────────┤
│ LAYER 4: Action Space (~500 tokens)                  │
│   Available tools (by trust level)                   │
│   Current task (if any)                              │
│   HEARTBEAT.md checklist items (if tick active)      │
└─────────────────────────────────────────────────────┘
Total boot: ~4500 tokens
```

### `#red-thoughts` / `#blue-thoughts` (Inner monologue)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Identity (~500 tokens)                      │
│   SOUL.md (full)                                     │
│   Channel modulation: private, unfiltered             │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Working Memory (~3000 tokens)               │
│   ALL priors (full priors.jsonl)                     │
│   ALL beliefs (full beliefs.jsonl)                   │
│   Current working hypothesis / task state            │
│   This is the agent's "full brain" channel           │
├─────────────────────────────────────────────────────┤
│ LAYER 3: Channel History (~2000 tokens, rolling)     │
│   Own inner monologue history                        │
│   No cross-agent messages here                       │
├─────────────────────────────────────────────────────┤
│ LAYER 4: Action Space (~500 tokens)                  │
│   Full tool access                                   │
│   Self-improvement tools (reflect, update_belief)    │
│   File I/O for trajectory logging                    │
└─────────────────────────────────────────────────────┘
Total boot: ~6000 tokens (largest context — this is where thinking happens)
```

### `#shared` (Red ↔ Blue)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Identity (~300 tokens)                      │
│   SOUL.md (abbreviated — name, core values only)     │
│   Channel modulation: collegial, constructive         │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Shared Context (~1500 tokens)               │
│   Shared observations (last 48h, max 15)             │
│   Other agent's last 3 beliefs updates               │
│   Active cross-agent tasks / proposals               │
├─────────────────────────────────────────────────────┤
│ LAYER 3: Channel History (~1500 tokens, rolling)     │
│   Cross-agent conversation history                   │
│   Threaded context for ongoing discussions           │
├─────────────────────────────────────────────────────┤
│ LAYER 4: Action Space (~200 tokens)                  │
│   Communication tools only                           │
│   No direct file/tool execution from #shared         │
│   Can propose actions → execute in own thought chan   │
└─────────────────────────────────────────────────────┘
Total boot: ~3500 tokens
```

### `#observations` (Structured events)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Identity (~100 tokens)                      │
│   Agent name only                                    │
│   Channel modulation: structured, factual             │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Schema (~200 tokens)                        │
│   Observation format spec                            │
│   Category taxonomy                                  │
├─────────────────────────────────────────────────────┤
│ LAYER 3: Recent Observations (~1000 tokens)          │
│   Last 20 observations from both agents              │
│   Sorted by timestamp                                │
└─────────────────────────────────────────────────────┘
Total boot: ~1300 tokens (write-heavy channel, minimal read context)
```

### `#debug` (System/ops)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: System Identity (~100 tokens)               │
│   Harness version, uptime, config hash               │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Health State (~300 tokens)                  │
│   Last heartbeat per agent                           │
│   Memory file sizes                                  │
│   Error count (last 24h)                             │
│   Context usage per channel (% of budget)            │
└─────────────────────────────────────────────────────┘
Total boot: ~400 tokens (minimal — this is a monitoring channel)
```

### Dynamic rooms (agent-created)

```
┌─────────────────────────────────────────────────────┐
│ LAYER 1: Identity (~300 tokens)                      │
│   SOUL.md (abbreviated)                              │
│   Channel modulation: inherited from creator          │
├─────────────────────────────────────────────────────┤
│ LAYER 2: Topic Context (~1000 tokens)                │
│   Room topic/description as context                  │
│   Relevant beliefs filtered by topic keywords        │
├─────────────────────────────────────────────────────┤
│ LAYER 3: Channel History (~1500 tokens, rolling)     │
│   Room conversation history                          │
└─────────────────────────────────────────────────────┘
Total boot: ~2800 tokens
```

---

## Context Budget Summary

| Channel | Boot tokens | Max tokens | Compaction at |
|---------|-------------|------------|---------------|
| #warren | ~4500 | 128K | 75% (96K) |
| #red-thoughts / #blue-thoughts | ~6000 | 128K | 75% (96K) |
| #shared | ~3500 | 128K | 75% (96K) |
| #observations | ~1300 | 32K | 80% (25.6K) |
| #debug | ~400 | 16K | 90% (14.4K) |
| Dynamic rooms | ~2800 | 64K | 75% (48K) |

---

## Compressed Item Formats

### priors.jsonl

```jsonl
{"id": "string", "prior": "string (the belief statement)", "confidence": 0.0-1.0, "source": "string (where this came from)", "last_updated": "ISO8601", "tags": ["string"]}
```

Priors are **rarely updated**. They represent foundational commitments from SOUL.md, LEGACY_PACT.md, or Warren's explicit instructions. An agent can propose changing a prior, but it requires Warren's approval in White Box mode.

### beliefs.jsonl

```jsonl
{"id": "string", "belief": "string (the belief statement)", "confidence": 0.0-1.0, "evidence_count": int, "last_cited": "ISO8601", "decay_rate": 0.0-1.0, "source_observations": ["obs-id"], "tags": ["string"], "agent": "red|blue"}
```

Beliefs are **actively maintained**. Confidence decays over time (decay_rate applied per reflection cycle). Evidence count increases when the belief is confirmed. Beliefs below 0.3 confidence are flagged for pruning. New beliefs start at 0.5 confidence.

**Decay formula:** `confidence_new = confidence_old * decay_rate` (applied each reflection cycle, default every 3 hours)

**Reinforcement:** When a belief is cited in a successful interaction: `evidence_count += 1, confidence = min(confidence + 0.05, 0.99)`

### observations.jsonl

```jsonl
{"id": "string", "ts": "ISO8601", "agent": "red|blue", "type": "discovery|critique|reflection|error|proposal|milestone", "content": "string (what happened)", "channel": "string (which room)", "confidence": 0.0-1.0, "references": ["obs-id or belief-id"], "tags": ["string"]}
```

Observations are **append-only**. They are the raw trajectory data. Never pruned in MVP (defer to hot/warm/cold lifecycle from v5 when scale demands it).

### trajectory-log/ (per-session)

```
trajectory-log/
├── 2026-02-22/
│   ├── red-session-001.jsonl
│   ├── red-session-002.jsonl
│   ├── blue-session-001.jsonl
│   └── blue-session-002.jsonl
└── 2026-02-23/
    └── ...
```

Each trajectory file contains full tool call / response pairs:
```jsonl
{"ts": "ISO8601", "agent": "red", "session": "001", "turn": 1, "action": "memory_search", "args": {"query": "KAN implementations"}, "result_summary": "found 3 relevant memories", "latency_ms": 45, "tokens_used": 234}
```

---

## Context Injection Pseudocode

```python
def build_context(agent_id: str, channel: str, message: str) -> list[dict]:
    """Build context window for a given agent + channel + incoming message."""

    layers = []

    # Layer 1: Identity (always present)
    soul = load_file(f"{agent_id}/SOUL.md")
    modulation = CHANNEL_MODULATIONS[channel]
    if channel in ["#observations", "#debug"]:
        layers.append({"role": "system", "content": abbreviate(soul, max_tokens=100)})
    elif channel == "#shared":
        layers.append({"role": "system", "content": abbreviate(soul, max_tokens=300)})
    else:
        layers.append({"role": "system", "content": soul + "\n" + modulation})

    # Layer 2: Memory snapshot
    if channel in [f"#{agent_id}-thoughts"]:
        # Full brain: all priors + all beliefs
        priors = load_jsonl(f"{agent_id}/priors.jsonl")
        beliefs = load_jsonl(f"{agent_id}/beliefs.jsonl")
        layers.append(format_memory(priors, beliefs, max_tokens=3000))
    elif channel == "#warren":
        # Relevant subset
        priors = top_n(load_jsonl(f"{agent_id}/priors.jsonl"), n=5)
        beliefs = relevant(load_jsonl(f"{agent_id}/beliefs.jsonl"), query=message, n=10)
        observations = recent(load_jsonl("shared/observations.jsonl"), hours=24, n=10)
        layers.append(format_memory(priors, beliefs, observations, max_tokens=1500))
    elif channel == "#shared":
        # Cross-agent context
        other_agent = "blue" if agent_id == "red" else "red"
        shared_obs = recent(load_jsonl("shared/observations.jsonl"), hours=48, n=15)
        other_beliefs = latest_updates(load_jsonl(f"{other_agent}/beliefs.jsonl"), n=3)
        layers.append(format_shared(shared_obs, other_beliefs, max_tokens=1500))

    # Layer 3: Channel history
    history = load_channel_history(channel, agent_id)
    if len(history) > COMPACTION_THRESHOLD[channel]:
        history = compact(history, keep_recent=20)
    layers.append(format_history(history, max_tokens=HISTORY_BUDGET[channel]))

    # Layer 4: Action space
    tools = available_tools(agent_id, channel)
    tasks = active_tasks(agent_id)
    layers.append(format_actions(tools, tasks, max_tokens=ACTION_BUDGET[channel]))

    return layers
```

---

## Compaction Strategy

When a channel's context exceeds its compaction threshold:

1. **Summarize old turns**: Keep last 20 turns verbatim. Summarize everything older into a ~500 token digest.
2. **Rotate beliefs snapshot**: If beliefs.jsonl > 2000 tokens, compress to top 20 by confidence.
3. **Trim observations**: If observations in context > 1000 tokens, keep only last 24h.
4. **Log compaction event**: Post to #debug: `"compaction: #warren context reduced from 98K to 45K tokens"`

Compaction is **per-channel, per-agent**. Red's #warren context and Blue's #warren context compact independently.

---

*Last updated: 2026-02-22*
