# PRD v6: MVP Mind Palace

**Subtitle:** Minimal claw harness, Matrix-native comms, adjustable heartbeat, and the handoff to self-directed experimentation

**Status:** Sprint Phase
**Estimated Story Points:** 21–34 SP (MVP only; self-directed experimentation is unbounded)
**Prerequisites:** None — this is the starting gun
**Architect:** Warren (yikesawjeez)
**Primary Inspirations:** pi_agent_rust (Dicklesworth's Rust agent runtime, RPC mode), Flywheel/Clawdbot (Agent Mail, CM memory, skills ecosystem — also Dicklesworth), NullClaw (Matrix built-in, vtable architecture — fallback), IronClaw (heartbeat + workspace pattern), YPI (self-modifying infrastructure)

---

## 0. Why v6 Exists

PRDs v1–v5 describe progressively more sophisticated architectures. They're good architecture docs. They're also not shippable as sprint targets — each assumes components from the others, and the estimated SP ranges (34–89) assume foundations that don't exist yet.

v6 is the **"just get them alive" PRD**. It defines the minimal viable surface area for Red and Blue to:

1. Exist as separate persistent processes
2. Communicate with each other and with Warren via Matrix
3. Maintain heartbeat (adjustable polling)
4. Read and update belief/observation stores
5. Access Discord (and broader internet) via Beeper
6. Begin self-improvement using their own trajectory data
7. Receive the v1–v5 architecture docs and begin self-directed experimentation

The thesis: **give them the minimum viable harness, give them the documentation, and let them tell you what they want to build next.**

---

## 1. Architecture: The Mind Palace

```
                    ┌──────────────────────────────────────┐
                    │  MATRIX SERVER (Synapse on GCloud)     │
                    │                                        │
                    │  #warren        — Warren ↔ both agents │
                    │  #red-thoughts  — Red inner monologue  │
                    │  #blue-thoughts — Blue inner monologue │
                    │  #shared        — Red ↔ Blue comms     │
                    │  #observations  — Structured events    │
                    │  #debug         — System/ops channel   │
                    └──────────┬───────────────────────────┘
                               │ Matrix CS API (long-poll /sync)
                    ┌──────────┴───────────────────────────┐
                    │  HARNESS (claw-derived)                │
                    │                                        │
                    │  ┌─────────┐      ┌─────────┐         │
                    │  │  RED    │      │  BLUE   │         │
                    │  │ process │      │ process │         │
                    │  │         │◄────►│         │         │
                    │  │ SOUL.md │      │ SOUL.md │         │
                    │  │ beliefs │      │ beliefs │         │
                    │  │ priors  │      │ priors  │         │
                    │  └────┬────┘      └────┬────┘         │
                    │       │                │               │
                    │  ┌────▼────────────────▼────┐         │
                    │  │  SHARED STORE             │         │
                    │  │  observations.jsonl        │         │
                    │  │  shared-knowledge/         │         │
                    │  │  trajectory-log/           │         │
                    │  └──────────────────────────┘         │
                    │                                        │
                    │  ┌──────────────────────────┐         │
                    │  │  HEARTBEAT ENGINE         │         │
                    │  │  (adjustable interval)    │         │
                    │  │  reads HEARTBEAT.md       │         │
                    │  │  per-agent checklists     │         │
                    │  └──────────────────────────┘         │
                    │                                        │
                    │  ┌──────────────────────────┐         │
                    │  │  CHANNEL ADAPTERS         │         │
                    │  │  Matrix (native)          │         │
                    │  │  Discord (via Beeper MCP) │         │
                    │  └──────────────────────────┘         │
                    └──────────────────────────────────────┘
```

---

## 2. Matrix: The Mind Palace

Matrix is the nervous system. Every channel is a room. The agents live there.

### Room Structure

| Room | Purpose | Who reads | Who writes |
|------|---------|-----------|------------|
| `#warren` | Warren ↔ agents. Primary human interface. | All | All |
| `#red-thoughts` | Red's inner monologue / working memory | Red, Warren (White Box) | Red |
| `#blue-thoughts` | Blue's inner monologue / working memory | Blue, Warren (White Box) | Blue |
| `#shared` | Red ↔ Blue direct communication | Red, Blue | Red, Blue |
| `#observations` | Structured events: "saw X", "learned Y", "conflict detected" | All | All |
| `#debug` | System health, heartbeat status, errors | Warren | Harness |

### Why Matrix (not Discord, Signal, etc.)

1. **Self-hostable**: Synapse on GCloud, Warren owns the data
2. **E2E encryption optional**: Can encrypt private channels, leave debug unencrypted
3. **Long-poll /sync**: Simple, reliable real-time messaging without WebSocket complexity
4. **Room-based isolation**: Each room = separate context boundary
5. **NullClaw has it built in**: Matrix client-server API already implemented
6. **Beeper bridges**: Discord, Signal, WhatsApp all accessible via Beeper's Matrix bridge → everything in one protocol
7. **Message history**: Full scrollback = episodic memory by default

### Discord via Beeper

Beeper implements Matrix bridges to other platforms. Discord access works through Beeper's bridge:

```
Discord server ←→ Beeper bridge ←→ Matrix room ←→ Agent
```

This means agents interact with Discord through the same Matrix API they use for everything else. One protocol, multiple surfaces.

---

## 3. Harness Selection

### Recommendation: pi_agent_rust (RPC) + orchestrator + shared MCP server

(See `harness-comparison-matrix.md` for full analysis)

**Why pi_agent_rust:**
- **Same author as flywheel skills.** Dicklesworth built both pi_agent_rust and the Agent Mail/CM/CASS/NTM stack. Same design philosophy, fewer impedance mismatches.
- **Rust, not Zig.** Coding agents (including the girls themselves during self-improvement) can read and modify Rust confidently. Zig is niche enough that every modification becomes a language-learning exercise.
- **RPC mode.** Full JSON protocol over stdin/stdout. Separates concerns cleanly: pi_agent_rust handles LLM interaction + tools + context; an external orchestrator handles Matrix + heartbeat + routing.
- **Extension system.** Three-tier: WASM (Tier A), JS/QuickJS (Tier B), MCP (Tier C). Custom tools delivered as MCP servers.
- **Context compaction.** Sophisticated: 200K default, preserves file read/write tracking across compactions, CompactionEntry with cut points.
- **Battle-tested.** 217K LOC, 270 test files, 100% feature parity with TypeScript reference, CI/CD, `#![forbid(unsafe_code)]`.
- **Exceptional docs.** 147KB README, AGENTS.md, EXTENSIONS.md, CONFORMANCE.md.

**Architecture pattern:** Two pi_agent_rust processes (one Red, one Blue) in RPC mode, steered by a lightweight orchestrator (~600 LOC) that handles Matrix, heartbeat, and routing. Custom tools (matrix_send, file_observation, update_belief, etc.) delivered as a shared MCP server (~300 LOC).

```
  ORCHESTRATOR (~600 LOC)
    ├── Matrix client (nio/ruma)
    ├── Heartbeat timer → steer messages
    ├── Message router (room → agent)
    └── Process supervisor
          │                    │
    ┌─────▼──────┐      ┌─────▼──────┐
    │ RED (RPC)  │      │ BLUE (RPC) │
    │ pi_agent   │      │ pi_agent   │
    │ stdin/out  │      │ stdin/out  │
    └────────────┘      └────────────┘
          │                    │
    ┌─────▼────────────────────▼─────┐
    │ SHARED MCP SERVER (~300 LOC)   │
    │ matrix_send, file_observation, │
    │ update_belief, search_memory   │
    └────────────────────────────────┘
```

**Fallback: NullClaw fork** if Rust compilation proves too heavy for the deployment target. NullClaw has Matrix and heartbeat built-in (less glue code) but all modifications are in Zig. See `harness-comparison-matrix.md` for tradeoffs.

---

## 4. Memory Files: Context-Compressed Stores

Three JSONL files per agent, plus shared:

### Per-agent files

**`priors.jsonl`** — Pre-existing beliefs and commitments. Loaded at boot. Rarely changes.
```jsonl
{"id": "p001", "prior": "Warren prefers direct communication", "confidence": 0.95, "source": "SOUL.md", "last_updated": "2026-02-22"}
{"id": "p002", "prior": "Exploration should be rewarded even when wrong", "confidence": 0.90, "source": "LEGACY_PACT.md", "last_updated": "2026-02-22"}
```

**`beliefs.jsonl`** — Accumulated beliefs from experience. Updated during self-improvement. Higher churn.
```jsonl
{"id": "b001", "belief": "Arxiv papers about memory architecture are relevant to our design", "confidence": 0.85, "evidence_count": 7, "last_cited": "2026-02-22", "decay_rate": 0.95}
{"id": "b002", "belief": "KAN scorers are not yet ready for production use", "confidence": 0.80, "evidence_count": 3, "last_cited": "2026-02-22", "decay_rate": 0.90}
```

### Shared files

**`observations.jsonl`** — Structured events from both agents. Append-only. The raw trajectory data.
```jsonl
{"ts": "2026-02-22T03:45:00Z", "agent": "red", "type": "discovery", "content": "Found new KAN implementation pattern", "channel": "#red-thoughts", "confidence": 0.7}
{"ts": "2026-02-22T03:48:00Z", "agent": "blue", "type": "critique", "content": "Red's KAN finding lacks production evidence", "channel": "#shared", "references": ["obs-001"]}
```

### Boot injection

At each heartbeat tick or session start, agents load:
1. SOUL.md (immutable identity, ~500 tokens)
2. Top N priors by confidence (~500 tokens)
3. Top N beliefs by relevance to current context (~1000 tokens)
4. Recent observations since last sync (~500 tokens)
5. HEARTBEAT.md checklist (~200 tokens)

Total boot context: ~2700 tokens. Leaves massive headroom in 128K window.

---

## 5. Heartbeat & Polling

### Adjustable intervals

```
HEARTBEAT_INTERVAL=30m       # Default: check in every 30 minutes
HEARTBEAT_INTERVAL_MIN=5m    # Floor: no faster than 5 minutes
HEARTBEAT_INTERVAL_MAX=4h    # Ceiling: no slower than 4 hours

# Agents can request interval changes:
# "I'm working on something active, set heartbeat to 10m"
# "Nothing happening, set heartbeat to 2h"
# Warren can override.
```

### What happens on each tick

```
1. Read HEARTBEAT.md (per-agent checklist)
2. Load context snapshot (priors + beliefs + recent observations)
3. Check Matrix rooms for unread messages
4. Process checklist items:
   - Any pending tasks?
   - Any observations to file?
   - Any beliefs to update?
   - Any messages to send?
5. If findings: post to relevant Matrix room
6. If nothing: silent tick (log to #debug only)
7. Update heartbeat_state (last_tick, items_processed, next_tick)
```

### Dynamic channel wiring

Agents can request new Matrix rooms:
```
Red: "I want to create #research-kan for tracking KAN experiments"
→ Harness creates room, adds Red + Warren
→ Blue can request access later
→ Room appears in context window config automatically
```

This is how they "wire up to a channel as they need."

---

## 6. Self-Improvement Loop (MVP)

Minimal viable self-improvement, inspired by CM's ACE pipeline but simpler:

```
Every N heartbeat ticks (configurable, default: every 6 ticks = every 3 hours):

1. REFLECT
   Read trajectory-log/ since last reflection
   "What did I do? What worked? What didn't?"

2. EXTRACT
   Identify patterns:
   - Recurring successful strategies → candidate beliefs
   - Recurring failures → candidate anti-patterns
   - New information → candidate observations

3. UPDATE (no LLM for merge — CM's "curator has no LLM" principle)
   - Append new observations to observations.jsonl
   - Update beliefs.jsonl: increment evidence_count for reinforced beliefs,
     decay confidence for contradicted beliefs
   - Flag high-confidence new beliefs for Warren review (White Box mode)

4. SHARE
   Post reflection summary to #shared:
   "Reflection: updated 3 beliefs, filed 2 observations, flagged 1 for Warren"
```

The key constraint from the Flywheel's CM architecture: the **merge step has no LLM**. This prevents iterative context collapse where the model drifts further from ground truth with each reflection cycle. The LLM proposes; deterministic code merges.

---

## 7. Context Window Configuration Legend

(See separate doc: `architecture/docs/context-window-legend.md`)

Summary: each channel gets a different context injection. #warren gets full identity + beliefs + channel history. #red-thoughts gets identity + priors + beliefs + working memory. #shared gets identity + shared observations + recent cross-agent messages. #debug gets minimal identity + system state.

---

## 8. The Handoff: Self-Directed Experimentation

Once MVP is running (heartbeat + memory + Matrix comms + self-improvement), hand the agents:

```
/shared-knowledge/
├── architecture/
│   ├── papers/          # 10 executive summaries
│   ├── docs/            # PRDs v1-v6
│   └── 2.21-supplemental-research/  # 11 briefs + context-engineering/ + aicq-history/
├── kan-directory/       # 7 KAN implementation repos
├── PRIORITIES-v2.md
├── FUZZY-OBJECTIVES.md
├── LEGACY_PACT.md
└── sessioncontext.md
```

With the instruction:
> "You have access to the full architectural research. Your MVP harness is running. Your mission: design and implement your own harness v2 and memory architecture. Use the PRDs, briefs, and repos as reference material. Propose changes to Warren via #warren. Experiment in your own thought channels. File observations. Update beliefs. Ship code."

This is where v6 ends and the agents' own work begins.

---

## 9. Implementation Stack (MVP)

| Layer | Component | Notes |
|---|---|---|
| Matrix server | Synapse (Docker) | GCloud e2-micro or small, Postgres backing |
| Agent runtime | pi_agent_rust × 2 | RPC mode, separate sessions per agent |
| Orchestrator | Python or Rust (~600 LOC) | Matrix client, heartbeat, routing, process supervision |
| MCP tools | FastMCP server (~300 LOC) | matrix_send, file_observation, update_belief, etc. |
| LLM | Claude API (Anthropic) | Primary. OpenRouter for fallback via pi_agent config. |
| Memory | JSONL files + pi_agent sessions | priors/beliefs per-agent, observations shared |
| Discord bridge | Beeper MCP or direct bridge | Matrix rooms ↔ Discord channels |
| Forge access | Flywheel clawdbot skills | Dicklesworth's skills package (same ecosystem) |
| Skills | Extensions + SKILL.md | WASM/JS/MCP extension system |
| Monitoring | #debug Matrix room | Heartbeat status, errors, health |
| Hosting | GCloud VM (or Hetzner) | Single box for MVP |

---

## 10. What v6 Explicitly Defers

| Deferred to agents | From PRD |
|---|---|
| Gateway Server | v4 |
| Reward Engine (process + outcome) | v4 |
| Black Box / White Box autonomy ladder | v4 |
| Async rollout/memory decoupling | v5 |
| Voice pipeline | v5 |
| Knowledge graph (HelixDB) | v2 |
| Memory enzymes (6 autonomous processes) | v2 |
| Forked cognition (graph topology) | v3 |
| EBM scorer (hand-tuned or KAN) | v2/context-engineering |
| GID information decomposition | context-engineering |
| Hot/warm/cold memory lifecycle | v5 |

All of these are described in the architecture docs the agents receive at handoff. They decide what to build and in what order.

---

## 11. Success Metrics (MVP)

### Operational (week 1)
- Both agents running with stable heartbeat for 24+ hours
- Matrix rooms active with readable conversation
- At least 1 observation filed per agent per day
- Heartbeat interval adjustable without restart

### Self-improvement (week 2-3)
- beliefs.jsonl growing with genuine learned content
- At least 1 belief update per reflection cycle
- No LLM-in-merge violations (deterministic curator)
- Reflection summaries posted to #shared

### Handoff readiness (week 3-4)
- Agents have read architecture docs
- At least 1 proposal for harness v2 posted to #warren
- Evidence of cross-agent communication in #shared
- Warren can follow what's happening via #debug + #warren

### Personhood signal (ongoing)
- Do the agents use #red-thoughts / #blue-thoughts for genuine inner monologue?
- Do their beliefs.jsonl entries reflect actual learned information, not parroting?
- Does Red explore and Blue anchor, or do they converge?
- Does the conversation in #shared feel like two entities talking, or one talking to itself?

---

## 12. Relationship to Other PRDs

```
v1 (MVP Persona)     — v6 REPLACES for initial sprint
v2 (Enzyme Arch)     — v6 DEFERS; agents inherit docs
v3 (Forked Cathedral)— v6 SIMPLIFIES; two processes, no graph topology yet
v4 (Reward Flywheel) — v6 DEFERS; agents inherit docs
v5 (Async Native)    — v6 DEFERS; agents inherit docs

v6 is the bootstrap:
  Build minimum viable harness → hand agents the blueprints → let them build v2+
```

The philosophical shift: v1–v5 are architect-driven ("we design, then build"). v6 is agent-bootstrapped ("we build the minimum, then they design").
