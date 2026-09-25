# Harness Comparison Matrix: pi_agent_rust vs nullclaw

**Date:** 2026-02-23
**Purpose:** Decide which harness to fork for the girls' MVP

---

## Head-to-Head

| Dimension | pi_agent_rust | nullclaw |
|---|---|---|
| **Language** | Rust (edition 2024, nightly) | Zig 0.15 |
| **Author** | Dicklesworth | Different author |
| **LOC** | ~217K across 78 source files | ~45K across ~110 source files |
| **Binary size** | ~22MB (CI-gated budget) | 678KB (ReleaseSmall) |
| **Startup** | Sub-100ms | <2ms (Apple Silicon), <8ms (edge) |
| **RAM** | Not specified (jemalloc optimized) | ~1MB peak |
| **Tests** | 70+ cases, 270 test files, conformance harness | 2,843 tests, zero-leak verified |
| **Last active** | 2026-02-18 (100% feature parity achieved 2026-02-14) | 2026-02-21 (CalVer, active) |
| **License** | MIT | MIT |

---

## Architecture Comparison

| Feature | pi_agent_rust | nullclaw | Edge |
|---|---|---|---|
| **Agent loop** | Stream-based, tool iteration (max 50), concurrent reads (8 max) | Single-turn, tool iteration (max 25), sequential | pi_agent |
| **Multi-agent** | No. Single-agent per process. RPC mode enables external orchestration. | SessionManager: thread-safe per-session isolation, shared SQLite. `delegate()` tool for sub-agents. | nullclaw |
| **Heartbeat** | No built-in heartbeat or daemon mode | Yes. Parses HEARTBEAT.md, configurable interval, daemon supervisor with exponential backoff | nullclaw |
| **Daemon mode** | No. CLI tool (interactive/print/RPC). Would need external process supervisor. | Yes. Spawns supervised threads: gateway, channel loops, scheduler, heartbeat. Writes daemon_state.json. | nullclaw |
| **Matrix** | No. No channel adapters at all — it's a CLI coding tool. | Yes. Client-Server API, PUT /send. But receive (/sync polling) needs ~200 LOC addition. | nullclaw |
| **Discord** | No | Yes. WebSocket gateway v10, webhook mode. | nullclaw |
| **Other channels** | None (CLI only) | 11 total: Telegram, Discord, Slack, Matrix, iMessage, IRC, WhatsApp, Email, DingTalk, QQ, Lark | nullclaw |
| **Context compaction** | Sophisticated: 200K default, LLM summarization, preserves file read/write tracking across compactions, CompactionEntry with cut points | Simpler: 100K default, LLM summarization, keep-recent-30 + summary, force-compress fallback | pi_agent |
| **Memory** | Session JSONL (tree structure with branching), SQLite index for search | SQLite with FTS5 + vector embeddings, hybrid search (0.7 vector / 0.3 keyword), session-scoped | nullclaw |
| **Tools** | 7 built-in (read/bash/edit/write/grep/find/ls) + extensions | 40+ built-in (shell, file, git, browser, memory, hardware, cron, delegate, web_search, etc.) | nullclaw |
| **Extension system** | Tier A: WASM (wasmtime), Tier B: JS/TS (QuickJS, no Node.js), Tier C: MCP. Capability-gated hostcalls. | MCP subprocess via JSON-RPC. Config-based tool enablement. | pi_agent |
| **LLM providers** | 4: Anthropic, OpenAI, Gemini, Azure | 22+: Anthropic, OpenAI, Ollama, Gemini, OpenRouter, Groq, etc. + `reliable.zig` retry wrapper with fallback chains | nullclaw |
| **Security** | Capability-based hostcalls, WASM sandbox, QuickJS sandbox, MCP process isolation, `#![forbid(unsafe_code)]`, audit logs, risk scoring | Pairing (6-digit code), ChaCha20-Poly1305 encryption, Landlock/Firejail/Bubblewrap/Docker sandbox detection, audit trail, autonomy levels, rate limiting | Tie |
| **Configuration** | `settings.json` + CLI flags + env vars | `config.json` + env vars, multi-agent config, per-channel accounts | nullclaw |
| **Documentation** | Exceptional: 147KB README, AGENTS.md, EXTENSIONS.md, CONFORMANCE.md | Good: CLAUDE.md with AGENTS.md agent guide | pi_agent |
| **RPC/API** | Yes. Full JSON protocol over stdin/stdout: steer, follow-up, get-state, set-model. Real-time event streaming. | Gateway HTTP server: /health, /pair, /webhook. No programmatic agent steering. | pi_agent |
| **Skills** | Package/extension system compatible with Pi ecosystem | SKILL.md + TOML manifests, skill installation | Tie |
| **Streaming** | Full SSE parser, real-time deltas, thinking/tool-call events | Callback-based streaming to caller | pi_agent |
| **Session persistence** | SessionStoreV2 (segmented append log + checksums) or JSONL, tree structure with branching | SQLite messages table + session keys, conversation history per session | pi_agent |

---

## The Critical Question: Flywheel Compatibility

This is where the user's instinct lands.

| Factor | pi_agent_rust | nullclaw |
|---|---|---|
| **Same author as flywheel skills?** | **Yes** — Dicklesworth built both | No |
| **Extension model match?** | WASM/JS/MCP — flywheel skills could be wrapped as MCP servers or extensions | MCP subprocess support — skills loadable as MCP servers |
| **Agent Mail compatibility** | Agent Mail is FastMCP HTTP — would work as MCP extension | Same — MCP server |
| **CM (CASS Memory) compatibility** | Would need adapter but same author's design philosophy | Would need adapter |
| **Ecosystem philosophy** | Same developer, same design values, tested together | Different ecosystem, would be importing foreign patterns |

**Verdict:** pi_agent_rust has a significant ecosystem advantage. When you're already using Dicklesworth's Agent Mail, CM, CASS, NTM — the harness from the same developer will have fewer impedance mismatches. Even if integration isn't drop-in, the assumptions, naming conventions, and architectural patterns align.

---

## The Critical Question: Coding Agent Accessibility

| Factor | pi_agent_rust | nullclaw |
|---|---|---|
| **Language prevalence in training data** | Rust: high (top 15 language, extensive docs, growing) | Zig: low (niche, fewer examples, less tooling knowledge) |
| **Coding agent ability to modify** | Strong. Claude/GPT write good Rust. Cargo ecosystem well-known. | Weak. Zig-specific patterns (allocators, comptime, error unions) less familiar to most models. |
| **Dependency management** | Cargo.toml, crates.io — standard, well-understood | build.zig — less familiar to most coding agents |
| **Error messages** | Rust compiler errors are detailed and googlable | Zig errors are sparse, less community knowledge |
| **Refactoring safety** | Rust type system catches more errors at compile time | Zig catches different things but fewer guarantees at compile time |

**Verdict:** The user is right. Coding agents will be materially more effective modifying Rust than Zig. This compounds over time — every modification, every new feature, every bugfix is easier in the language the agent knows better.

---

## What Each Harness Needs to Become the Girls' MVP

### pi_agent_rust path (~800-1200 LOC new code + orchestrator)

**What it already has:**
- Battle-tested agent loop with streaming + tool execution
- Excellent context compaction with file tracking
- RPC mode for programmatic control
- Extension system (WASM/JS/MCP)
- Same-ecosystem flywheel skills compatibility
- Exceptional documentation

**What needs building:**

1. **External orchestrator** (~400-600 LOC, Python or Rust)
   - Spawns two pi_agent_rust processes in RPC mode (Red, Blue)
   - Matrix client (matrix-nio or ruma)
   - Heartbeat timer (routes heartbeat ticks as RPC steer messages)
   - Message router (Matrix room → correct agent's RPC stdin)
   - Shared memory coordinator (observations.jsonl writes)

2. **MCP tools for Matrix + memory** (~200-300 LOC)
   - `matrix_send`, `matrix_read`, `matrix_create_room`
   - `file_observation`, `update_belief`, `search_memory`
   - `adjust_heartbeat`
   - Packaged as MCP server, loaded by both agents

3. **Per-agent config** (~100 LOC)
   - Separate session directories
   - Separate SOUL.md paths
   - Shared MCP server config

4. **Daemon wrapper** (~100-200 LOC)
   - Process supervision for the orchestrator + two agents
   - Restart on crash
   - Health check endpoint

**Total new code:** ~800-1200 LOC (mostly in the orchestrator, not in pi_agent_rust itself)

**Risk:** The orchestrator is new code outside the battle-tested pi_agent_rust binary. But it's simple glue code — message routing and timers.

### nullclaw path (~400-600 LOC modifications to Zig core)

**What it already has:**
- Matrix send (PUT /send)
- Heartbeat engine with HEARTBEAT.md
- Daemon supervisor with exponential backoff
- SessionManager for multi-session isolation
- SQLite + FTS5 + vector hybrid search
- 40+ tools
- 22+ LLM providers
- Cron scheduler

**What needs building:**

1. **Matrix /sync receiver** (~200 LOC Zig)
   - Long-polling thread against /_matrix/client/v3/sync
   - Parse m.room.message events
   - Route to correct session via SessionManager
   - Handle since/timeout for incremental sync

2. **Dual-persona session routing** (~100-200 LOC Zig)
   - Config: map rooms to agent personas
   - session_key format: `"matrix:red:room_id"` / `"matrix:blue:room_id"`
   - Each persona gets own SOUL.md, beliefs, priors

3. **Belief/observation tools** (~100-200 LOC Zig)
   - `file_observation`, `update_belief` tools
   - JSONL I/O
   - Confidence decay logic

**Total new code:** ~400-600 LOC (all in Zig, modifying the core binary)

**Risk:** All modifications are to Zig code that coding agents will struggle with. Every bug is a Zig debugging session. The vtable architecture helps (extensions don't touch core), but the Matrix receive and dual-persona routing do touch core.

---

## Recommendation: pi_agent_rust

**I'm revising the PRD v6 recommendation from nullclaw to pi_agent_rust.** Here's why:

### The decisive factors

1. **Dicklesworth's ecosystem.** You're using Agent Mail, CM, CASS, NTM — all Dicklesworth's tools. Using his agent runtime means fewer impedance mismatches, shared design assumptions, and likely better MCP integration. When you hit a weird edge case, the author's patterns will be consistent.

2. **Coding agent accessibility.** This is the user's key insight and it's correct. The girls' entire self-improvement thesis depends on agents modifying their own harness. If the harness is in Zig, that self-modification hits a wall. Rust is well within Claude's and GPT's capabilities. The agents can realistically propose and implement harness changes in Rust. In Zig, they'll struggle with allocator patterns, comptime, and build system — none of which are the problems they should be solving.

3. **RPC mode is the right abstraction.** Instead of trying to make a single binary do everything (daemon + heartbeat + multi-agent + Matrix), pi_agent_rust's RPC mode lets you separate concerns cleanly:
   - pi_agent_rust handles: LLM interaction, tool execution, context management, session persistence
   - External orchestrator handles: Matrix, heartbeat timing, message routing, shared state
   - MCP servers handle: custom tools (beliefs, observations, matrix comms)

   This is actually a *better* architecture than cramming everything into one binary. Each piece is testable, replaceable, and understandable independently.

4. **The 800-1200 LOC of new code is simple code.** The orchestrator is a timer + message router + process manager. The MCP tools are CRUD operations on JSONL files + HTTP calls to Matrix. None of this is architecturally hard. Compare to nullclaw's 400-600 LOC of Zig core modifications, which touch thread scheduling, session management, and protocol implementation — all in a language coding agents struggle with.

5. **Documentation.** 147KB README + AGENTS.md + EXTENSIONS.md + CONFORMANCE.md. When a coding agent needs to understand "how does pi_agent_rust handle X?", the answer is probably in the docs. This reduces the exploration overhead for every modification.

### What we give up

- **Startup time:** 100ms vs 2ms. Irrelevant for a persistent daemon.
- **Binary size:** 22MB vs 678KB. Irrelevant on a GCloud VM.
- **Built-in channels:** No Matrix/Discord/Telegram built in. Handled by the orchestrator instead.
- **Built-in heartbeat:** No daemon mode. Handled by the orchestrator instead.
- **Built-in multi-session:** No SessionManager. Each agent is a separate process with own sessions.
- **Tool count:** 7 vs 40+. The girls need maybe 10 custom tools (Matrix, memory, beliefs, observations) — all delivered via MCP. The built-in 7 (read/bash/edit/write/grep/find/ls) are the coding tools they need for self-modification.

### The architecture

```
┌──────────────────────────────────────────────────────┐
│  ORCHESTRATOR (Python or Rust, ~600 LOC)              │
│                                                        │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐     │
│  │ Heartbeat  │  │  Matrix    │  │  Process     │     │
│  │ Timer      │  │  Client    │  │  Supervisor  │     │
│  │            │  │  (nio/ruma)│  │              │     │
│  │ tick →     │  │  /sync ←   │  │  restart on  │     │
│  │ steer msg  │  │  room msgs │  │  crash       │     │
│  └─────┬──────┘  └──────┬─────┘  └──────────────┘     │
│        │                │                               │
│        │    ┌───────────┴──────────────┐               │
│        │    │  MESSAGE ROUTER          │               │
│        │    │  #warren → both agents   │               │
│        │    │  #red-thoughts → Red RPC │               │
│        │    │  #blue-thoughts → Blue   │               │
│        │    │  #shared → both          │               │
│        │    └──────┬──────────┬────────┘               │
│        │           │          │                         │
│   ┌────▼───────────▼──┐  ┌───▼──────────────────┐     │
│   │  RED               │  │  BLUE                │     │
│   │  pi_agent_rust     │  │  pi_agent_rust       │     │
│   │  --rpc mode        │  │  --rpc mode          │     │
│   │                    │  │                      │     │
│   │  stdin ← steer    │  │  stdin ← steer      │     │
│   │  stdout → events  │  │  stdout → events    │     │
│   │                    │  │                      │     │
│   │  Session: red/     │  │  Session: blue/     │     │
│   │  SOUL.md: Red      │  │  SOUL.md: Blue      │     │
│   │  Extensions: MCP   │  │  Extensions: MCP    │     │
│   └────────────────────┘  └──────────────────────┘     │
│                                                        │
│   ┌────────────────────────────────────────────┐       │
│   │  SHARED MCP SERVER (FastMCP, ~300 LOC)     │       │
│   │                                            │       │
│   │  Tools:                                    │       │
│   │  - matrix_send(room, message)              │       │
│   │  - matrix_read(room, since, limit)         │       │
│   │  - file_observation(type, content, conf)   │       │
│   │  - update_belief(belief, confidence, action)│       │
│   │  - search_memory(query, scope)             │       │
│   │  - adjust_heartbeat(interval, reason)      │       │
│   │  - read_architecture(path)                 │       │
│   │                                            │       │
│   │  Shared state:                             │       │
│   │  - observations.jsonl (append-only)        │       │
│   │  - Per-agent beliefs.jsonl / priors.jsonl  │       │
│   └────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────┘

  ┌──────────────────────────────────┐
  │  MATRIX SERVER (Synapse/GCloud)   │
  │  #warren, #red-thoughts,          │
  │  #blue-thoughts, #shared,         │
  │  #observations, #debug            │
  └──────────────────────────────────┘
```

### Migration from PRD v6

The PRD v6 architecture diagram, context window legend, memory files, and SOUL.md templates all remain valid. Only the harness layer changes:

- **Replace:** "NullClaw fork" → "pi_agent_rust (RPC) + orchestrator + shared MCP server"
- **Keep:** Matrix rooms, JSONL stores, heartbeat checklist, self-improvement loop, context injection, everything else

The playbook Sprint 1 needs updating to reflect this architecture, but Sprints 0, 2, 3, and 4 are unchanged.

---

## If nullclaw were still preferred

Keep it as a fallback. The path is shorter in terms of new code (400 vs 800+ LOC), but every line is in Zig. If the girls' self-improvement experiments never need to modify the harness binary itself (only the orchestrator/MCP layer), then the language gap matters less. But the whole thesis is that they WILL modify their own infrastructure — so the language needs to be one they can write in.

---

## Final Comparison Summary

| Factor | pi_agent_rust | nullclaw | Winner |
|---|---|---|---|
| Ecosystem fit (flywheel) | Same author | Different ecosystem | **pi_agent** |
| Coding agent modifiability | Rust (high) | Zig (low) | **pi_agent** |
| Matrix built-in | No | Yes (send only) | nullclaw |
| Heartbeat built-in | No | Yes | nullclaw |
| Daemon mode | No | Yes | nullclaw |
| Multi-agent built-in | No | SessionManager | nullclaw |
| Context compaction quality | Sophisticated | Basic | **pi_agent** |
| Extension system | WASM/JS/MCP (3-tier) | MCP only | **pi_agent** |
| Documentation | Exceptional (147KB) | Good | **pi_agent** |
| RPC/programmatic control | Full JSON protocol | HTTP gateway only | **pi_agent** |
| Self-improvement readiness | Agents can modify Rust code | Agents will struggle with Zig | **pi_agent** |
| New code to MVP | ~800-1200 LOC (Python/Rust glue) | ~400-600 LOC (Zig core changes) | nullclaw |
| Risk profile | Glue code is simple, tested core | Core modifications in unfamiliar language | **pi_agent** |

**Recommendation: pi_agent_rust + orchestrator + shared MCP server**
