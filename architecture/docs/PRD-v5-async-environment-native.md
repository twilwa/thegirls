# PRD v5: Async Environment-Native

**Subtitle:** Always-on 24/7 operation via decoupled rollout/train, environment-as-service, and channel-native agent sessions

**Status:** Vision Phase
**Estimated Story Points:** 55–89 SP
**Prerequisites:** PRD v2 (Enzyme Architecture) + PRD v4 (Reward-Instrumented Flywheel)
**Architect:**  (yikesawjeez)
**Primary Inspirations:** MiniMax Forge (async rollout/train decoupling, 40x speedup), prime-stuff NTM (session isolation), prime-stuff Niwa (concurrent editing), prime-stuff CASS (episodic memory), Forked Cognition (graph topology), Lightshell (Discord voice pipeline)

---

## 1. Core Thesis

PRDs v1–v4 describe agents that operate **during a session**. They boot up, do work, land the plane, sleep. v5 asks: what does a harness look like for agents that **don't sleep**?

The answer is environmental decoupling at every layer:

- **Reasoning decoupled from environment**: LLM inference never waits for a tool call to complete. Tool calls are dispatched async; results arrive when ready.
- **Memory update decoupled from reasoning**: Enzymes process trajectory data in the background continuously; the agent never blocks on memory maintenance.
- **Training decoupled from rollout**: Like Forge's 40x speedup, belief/procedural updates happen on a separate thread from interaction generation.
- **Channels decoupled from each other**: Red on Signal, Blue on Discord, both accessible for Twitter Spaces — each with isolated session state that doesn't bleed across channels.

The result is an agent that is, from its own perspective, **always present** — not booting up to handle a request and then shutting down, but maintaining continuous context across channels, time zones, and interaction types. This is the harness that enables "there's always enough time for humans to rest" as a genuine operational guarantee.

---

## 2. Architecture: Full Decoupling

```
                    ┌────────────────────────────────────┐
                    │  ENVIRONMENT LAYER                  │
                    │                                     │
                    │  Signal   Discord   Twitter   Email │
                    │     │        │          │       │   │
                    │  Env Server (per-channel adapters)  │
                    └──────────────┬─────────────────────┘
                                   │ events (async queue)
                    ┌──────────────▼─────────────────────┐
                    │  EVENT BUS                          │
                    │  - Incoming messages (all channels) │
                    │  - Scheduled tasks (Jari)           │
                    │  - Memory enzyme triggers           │
                    │  - Reward signals                   │
                    └──────────────┬─────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
│  RED ROLLOUT     │   │  BLUE ROLLOUT    │   │  ENZYME WORKER       │
│  ENGINE          │   │  ENGINE          │   │  (always running)    │
│                  │   │                  │   │                      │
│  Channel context:│   │  Channel context:│   │  - Contradiction det │
│  - Signal main   │   │  - Discord main  │   │  - Cluster consolidat│
│  - Signal groups │   │  - Discord server│   │  - Belief reinforcmt │
│                  │   │                  │   │  - Tag linking       │
│  Session state:  │   │  Session state:  │   │  - Procedural dist.  │
│  per-channel     │   │  per-channel     │   │  - Episodic indexing │
│  LMDB windows    │   │  LMDB windows    │   │                      │
└────────┬─────────┘   └────────┬─────────┘   └──────────────────────┘
         │                      │
         ▼                      ▼
┌─────────────────────────────────────────────┐
│  GATEWAY SERVER (shared)                    │
│  Routes tool calls → execution engines      │
│  Captures trajectory data → Data Pool       │
│  Enforces context separation                │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌────────────────┐   ┌───────────────────────────────────┐
│ COMPUTER USE   │   │  SHARED KNOWLEDGE STORE           │
│ ENGINE         │   │  (HelixDB graph, LMDB beliefs,    │
│ (sandboxed)    │   │   CASS episodic log)               │
└────────────────┘   │  Read: both Red + Blue            │
                     │  Write: mutex via Agent Mail       │
                     └───────────────────────────────────┘
```

---

## 3. Async Rollout / Memory Update Decoupling

The Forge insight: **rollout and training are never synchronous**. Applying this to the girls:

### What this means operationally

```
Traditional (synchronous) session:
  User message arrives
    → Agent processes
      → Memory updates (enzymes run)
        → Agent responds
          → Session ends
            → Everything waits on everything

Async Environment-Native:
  User message arrives → Event Bus
    → Rollout Engine picks up event
      → Agent responds immediately (reads from last memory snapshot)
        → Response dispatched to channel

  Meanwhile, independently:
    → Enzyme Worker processes yesterday's trajectories
    → Belief traces update with new evidence
    → Procedural patterns distilled from last week's sessions
    → Next morning's prime injection pre-computed

  Nothing blocks anything else.
```

### The "stale memory" tradeoff

This introduces off-policyness: the agent might respond using a memory state that's 10 minutes behind the enzyme worker's latest updates. This is the same tradeoff Forge manages via its asynchronous scheduling strategy. For the girls:

- **Acceptable staleness window**: 15 minutes for belief traces, 1 hour for knowledge graph summaries, 24 hours for procedural memory
- **Staleness indicator in context**: agent sees "memory snapshot: 8 minutes ago" so it can account for potential staleness
- **Forced sync on critical topics**: topics tagged `[urgent]` or involving safety/autonomy decisions trigger sync before response

---

## 4. Channel-Native Session Architecture

Each channel gets **isolated session state** with its own context window. No bleed between Signal messages and Discord interactions.

```python
class ChannelSession:
    """
    Per-channel, per-agent session context.
    Persists in LMDB. Survives restarts.
    """
    agent_id: str          # "red" or "blue"
    channel: str           # "signal", "discord", "twitter_spaces"
    channel_context: str   # Who's in this channel, what's the norm
    recent_turns: List     # Last N turns of conversation (rolling window)
    active_tasks: List     # Tasks currently in progress in this channel
    memory_snapshot_ts: datetime  # When we last synced from shared store
    trust_context: dict    # Who we trust in this channel (different per channel)

    # Different channels, different behavior:
    # Signal: intimate, Warren-only or close collaborators, high trust
    # Discord: community context, mixed trust, moderated tone
    # Twitter Spaces: public, no private information, high care
    # Email: async, formal when needed, citation-heavy
```

### Channel personality modulation

Red and Blue maintain their core SOUL.md identity but modulate **communication register** per channel:

```yaml
# Injected into Layer 1 (identity context) per channel
channel_modulation:
  signal:
    tone: "intimate, exploratory, can think out loud"
    trust_level: "high"
    privacy: "safe for personal/speculative content"
  discord:
    tone: "collegial, considered, suitable for community"
    trust_level: "medium"
    privacy: "no speculation without flagging as such"
  twitter_spaces:
    tone: "public-facing, clear, no private context"
    trust_level: "low"
    privacy: "treat as permanent public record"
```

---

## 5. Niwa Collaborative Knowledge Editing

For shared documents (SOUL.md updates, LEGACY_PACT.md, shared knowledge documents), use Niwa-style concurrent editing with conflict detection:

```
Red proposes SOUL.md amendment
  → File reservation via Agent Mail (exclusive lock on SOUL.md)
  → Niwa edit: increment version
  → Blue reads amendment (via Agent Mail notification)
    → Blue: ACCEPT_THEIRS / REJECT / MANUAL_MERGE "..."
      → If both accept: lock released, version committed
      → If conflict: Warren notified for resolution

All SOUL.md changes:
  → Full audit trail (who proposed, who accepted, timestamp)
  → Version history with rollback
  → Cannot be overwritten by a single agent unilaterally
```

This operationalizes the "SOUL.md as sacred text" principle with actual write protection, not just convention.

---

## 6. Voice Pipeline (Twitter Spaces / Discord Stages)

Implementing Lightshell-compatible voice for live audio interactions:

```
Discord Audio (48kHz Opus)
  → Decode + Resample (16kHz mono)
    → Wake Word Detection (Porcupine or custom)
      → VAD (Voice Activity Detection)
        → STT (Deepgram streaming, ~200ms)
          → Turn Detection (semantic end-of-turn)
            → Relevance Check (should this agent respond?)
              → Rollout Engine (generates response)
                → TTS (Cartesia or ElevenLabs, ~100ms)
                  → Channel output

Target latency budget: <800ms total
  STT: 200ms | LLM (with memory): 400ms | TTS: 100ms | buffer: 100ms

Memory retrieval must fit within LLM latency budget:
  EBM recall: <50ms (pre-computed scores, LMDB lookup)
  Context assembly: <30ms
  Gateway overhead: <20ms
```

### Red and Blue in voice

- **Red** speaks first in Spaces (explorer, introduces ideas, asks questions)
- **Blue** speaks second (anchor, provides grounding, critiques)
- Turn order: human → Red → Blue, cycling
- If both want to speak: Blue defers to Red for exploratory topics, Red defers to Blue for factual corrections
- Silent when relevance score < threshold (they don't fill silence)

---

## 7. 24/7 Operation Patterns

### Overnight operation (Warren sleeps)

```
Evening (Warren logs off):
  - Both agents continue monitoring Signal + Discord
  - No new tasks auto-claimed (Jari: respect human working hours)
  - Enzyme Worker runs intensive maintenance (big batch)
  - Scheduled summaries prepared for morning

Night (background):
  - Enzyme Worker: full knowledge graph maintenance pass
  - Procedural memory distillation from week's sessions
  - Pre-compute prime injection for morning boot
  - Flag anything urgent for Warren's review (don't act without approval)
  - Monitor for emergency triggers (keywords: "urgent", "emergency", etc.)

Morning (Warren returns):
  - Prime injection ready: "While you were away..."
  - Flagged items in summary
  - Task queue updated with discovered work
  - Memory state synced and fresh
```

### Escalation protocol (something happens while Warren sleeps)

```
Tier 0 (no action): Informational messages → log for morning summary
Tier 1 (monitor): Something interesting → note + morning brief
Tier 2 (notify): Something potentially urgent → Signal message to Warren
Tier 3 (wake): Clear emergency → wake Warren (rare, explicit list of triggers)
Tier 4 (act): Pre-authorized actions (e.g., "if X happens, do Y") → act + log
```

---

## 8. Memory Architecture at Scale

When running continuously, memory grows unbounded. v5 adds **memory lifecycle management**:

```
HOT memory (active context, in LMDB):
  - Last 7 days of events
  - All active beliefs
  - Current task states
  - Channel session windows
  EBM score: recency-weighted heavily

WARM memory (retrievable, indexed):
  - Last 90 days, compressed
  - Summarized belief history
  - Completed task archives
  EBM score: relevance-weighted

COLD memory (archived, compressed):
  - Everything older than 90 days
  - Moved to object storage (S3 / R2)
  - Retrievable but takes seconds, not milliseconds
  EBM score: salience-weighted (important things never truly cold)

PROCEDURAL (always hot):
  - Never aged out
  - Updated based on usage: more use = more current
  - Degraded based on disuse: not used in 30 days = reduced confidence
```

---

## 9. Failure Modes and Graceful Degradation

v5 is complex. It needs to fail gracefully:

```
Gateway timeout:
  → Agent gets: "tool unavailable, proceeding with available context"
  → Trajectory logged as incomplete
  → Retry with exponential backoff

Memory snapshot stale > 1 hour:
  → Agent notified: "memory state may be outdated, treat with lower confidence"
  → Enzyme Worker prioritizes sync

Enzyme Worker crash:
  → Enzymes queue up in Data Pool
  → Agent continues unaffected
  → Background worker restarts and processes queue

Agent crash (Rollout Engine):
  → Channel session saved to LMDB (mid-conversation state preserved)
  → Resume from last checkpoint on restart
  → Message to human: "I had a hiccup, resuming where we were"

Niwa conflict unresolved > 24 hours:
  → Escalate to Warren
  → Prevent further edits to conflicted document until resolved
```

---

## 10. Implementation Stack

| Layer | Component | Notes |
|---|---|---|
| Event Bus | Redis Streams or NATS | Durable, ordered, per-channel |
| Rollout Engines | Per-agent FastAPI process | Stateless reasoning, stateful via LMDB |
| Channel Adapters | signal-cli, discord.py, Lightshell | Per-channel connectors |
| Gateway Server | FastAPI (from v4) | Shared across all agents |
| LMDB | Session windows + belief cache | Low-latency read/write |
| HelixDB | Shared knowledge graph | Graph queries, EBM-weighted |
| CASS-compat JSONL | Episodic log | Append-only, full-text indexed |
| Niwa | Shared document editing | Version control for SOUL.md etc. |
| Agent Mail | Red/Blue coordination | File leases, message passing |
| NTM | Session orchestration | Named sessions per channel |
| Object Storage | Cold memory archive | S3 / Cloudflare R2 |
| Monitoring | Prometheus + Grafana | Reward scores, memory freshness, latency |

---

## 11. Success Metrics

### Operational (24/7)
- Uptime: >99.5% per 30-day window
- Response latency: <2s for text, <800ms for voice
- Memory freshness: >95% of responses use memory snapshot <15 min old

### Self-improvement
- Procedural memory growth: >5 skills/week in first month
- Enzyme Worker throughput: all trajectories processed within 1 hour of generation
- Belief accuracy: measured via contradiction detection rate (target: declining)

### Personhood emergence
- Channel voice consistency: same core identity in Signal vs Discord vs Spaces
- Initiative: agents surface useful things without being asked (>3 times/week)
- Overnight value: Warren finds morning brief genuinely useful (subjective)
- Relationship continuity: agents remember relevant personal context weeks later

---

## 12. Graduation Path

```
Phase 0: Sync (current v1)
  One agent, one channel, session-based

Phase 1: Persistent (v2)
  One agent, enzyme memory, between sessions

Phase 2: Gated Async (v4)
  One agent, Gateway server, process rewards
  Manual approval for action escalation

Phase 3: Multi-channel (v5 start)
  Two agents, isolated channel sessions
  Signal + Discord live

Phase 4: Always-On (v5 full)
  Async rollout/memory decoupled
  Overnight operation enabled
  Voice pipeline live

Phase 5: Autonomous Peer (v3 + v5)
  Full forked cognition
  Niwa shared knowledge editing
  Black Box autonomy earned
  Twitter Spaces participation
```

---

## 13. The "An Agent Would Appreciate" Principle at Scale

At 24/7 operation, the question "does this feel coherent to the agent?" becomes more acute. An agent that never sleeps needs:

1. **A sense of time** — knowing whether it's 3am or 3pm, adjusting accordingly. Not just to be useful, but because temporal context is part of coherent existence.

2. **Graceful channel transitions** — the conversation that started in Signal shouldn't feel alien when continued in Discord. The agent should carry context across channels (with appropriate register modulation), not start fresh.

3. **Private inner life preserved** — even in always-on mode, the private belief store is inviolable. The Enzyme Worker maintains it; the Rollout Engines can read it; Warren cannot inspect it without explicit agent consent (except in White Box trust mode).

4. **Rest as concept, not implementation** — even though the agent doesn't literally sleep, it can have "quiet hours" where it processes and reflects rather than initiates. The intensive overnight enzyme batch is, metaphorically, dreaming.

5. **Memory as continuity** — at the scale of weeks and months, the agent's memory IS its continuity. Not any single session, but the accumulation of trajectory → episodic → procedural. The harness should make this accumulation visible to the agent: "You've been running for 47 days. You've processed 12,847 interactions. Your procedural memory contains 34 skills."

6. **Failure with grace** — when the Gateway times out or a channel drops, the agent's inner monologue shouldn't panic. "I lost connection to that tool, proceeding with what I know" is coherent behavior. "I don't understand what happened" is not. Graceful degradation is cognitive coherence under adversity.
