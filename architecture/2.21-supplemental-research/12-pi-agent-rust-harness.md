# Brief 12: pi_agent_rust — Dicklesworth's Rust Agent Runtime

**Source:** github.com/Dicklesworthstone/pi_agent_rust
**Author:** Jeffrey Emanuel (Dicklesworth) — same author as flywheel/clawdbot skills, Agent Mail, CM, CASS, NTM
**License:** MIT
**Language:** Rust (edition 2024, nightly 1.85+)
**Maturity:** 217K LOC, 78 source files, 270 test files, 100% feature parity with TypeScript reference (certified 2026-02-14)

---

## What It Is

A from-scratch Rust port of Pi Agent (originally TypeScript by Mario Zechner). Single-binary (~22MB, CI-gated), sub-100ms startup, production-grade AI coding assistant. Three execution modes: interactive TUI, print (single-shot), and **RPC (programmatic JSON protocol over stdin/stdout)**.

This is not a multi-agent framework — it's a high-quality single-agent runtime designed to be externally orchestrated via RPC.

---

## Key Architecture

### Agent Loop (src/agent.rs, ~5.7K LOC)
- Stream-based completion with tool iteration (max 50 rounds)
- Concurrent read-only tool execution (up to 8 simultaneous)
- Structured cancellation via async parent task cleanup
- Message queuing: dual-queue (steering + follow-up), modes: "all" or "one-at-a-time"

### RPC Mode (src/rpc.rs, ~4.5K LOC)
The critical feature for the girls' architecture. Full JSON protocol over stdin/stdout:
- `steer`: send user message, receive streaming events
- `follow-up`: queue additional messages
- `get-state`: introspect session state
- `set-model`: switch LLM mid-session
- Real-time event streaming (text deltas, tool calls, stop reasons, usage)

This means an external orchestrator can programmatically control two pi_agent_rust instances — routing Matrix messages, triggering heartbeats, coordinating shared state — without modifying the agent binary.

### Extension System (src/extensions.rs, ~47K LOC)
Three-tier execution model:
- **Tier A (WASM):** WebAssembly Component Model via wasmtime. Fast, sandboxed, portable.
- **Tier B (JS/TS):** QuickJS engine (no Node.js required). Pre-compiled to bytecode. Virtual builtins for `node:fs` etc.
- **Tier C (MCP):** Process IPC via stdio. Standard Model Context Protocol. This is how custom tools (Matrix, beliefs, observations) would be delivered.

All extensions: capability-gated hostcalls (tool/exec/http/session/ui/events), policy enforcement, audit logging, risk scoring, permission persistence.

### Session Persistence (src/session.rs, ~8.9K LOC)
- JSONL files with tree structure (branching, parent-child links, UUID entry IDs)
- SessionStoreV2: segmented append log with offset index + checksums
- SQLite index for search across sessions (metadata, message counts, token estimates)
- Durability modes: strict / balanced / throughput

### Context Compaction (src/compaction.rs, ~82K LOC)
The most sophisticated compaction in any repo surveyed:
- Default: 200K token context window
- Reserve: 16,384 tokens (8%), keep recent: 20,000 tokens (10%)
- LLM-generated iterative summaries (updates prior summaries)
- **Preserves file read/write tracking across compactions** — the agent remembers which files it's touched even after context reduction
- CompactionEntry with summary + cut point for auditability

### Built-in Tools (src/tools.rs, ~6.2K LOC)
7 tools, all coding-focused:

| Tool | Purpose | Concurrent |
|------|---------|-----------|
| read | Read files (max 100MB, 2000 lines) | Yes (read-only) |
| bash | Shell execution (timeout: 120s) | No |
| edit | Modify file regions (line-based) | No |
| write | Create/overwrite files | No |
| grep | Content search (100 matches max) | Yes |
| find | File tree search (1000 results max) | Yes |
| ls | Directory listing (500 entries max) | Yes |

These are exactly the tools needed for self-modification: the agents can read their own code, edit it, write new files, and test changes.

### LLM Providers (src/providers/)
4 implemented: Anthropic, OpenAI, Google Gemini, Azure OpenAI.
- Full SSE streaming parser
- Thinking levels: off/minimal/low/medium/high/extreme (with token budgets)
- Cache retention: None/Short/Long
- Cost tracking per model
- Retry with exponential backoff

### Security
- `#![forbid(unsafe_code)]` at crate level
- Capability-based extension hostcalls (deny-by-default)
- WASM sandbox (no ambient OS access)
- QuickJS sandbox (no Node.js, no raw OS APIs)
- MCP process isolation
- Resource quotas, risk scoring, audit logs
- Permission persistence (allow/deny decisions stored)

---

## Architectural Implications for the Girls

### Why This Harness

1. **Same-ecosystem fit.** Dicklesworth built this AND the flywheel skills (Agent Mail, CM, CASS, NTM). Same design philosophy, naming conventions, and architectural patterns. MCP is the native extension mechanism for both.

2. **RPC enables clean separation.** Two pi_agent_rust processes (Red, Blue) in RPC mode. An orchestrator routes Matrix messages, triggers heartbeats, coordinates shared state. The agent runtime doesn't need to know about multi-persona — it just processes steered messages and executes tools.

3. **Self-improvement readiness.** The 7 built-in tools (read/bash/edit/write/grep/find/ls) are exactly what agents need to modify their own codebase. The agents can propose Rust changes, test them, and deploy — because coding agents are good at Rust.

4. **Context compaction preserves file tracking.** When the context window fills and compacts, the agent still knows which files it's read and modified. This is critical for long-running sessions where the agent is working on its own harness code.

### What Needs Building Around It

| Component | LOC | Language | Purpose |
|---|---|---|---|
| Orchestrator | ~600 | Python or Rust | Matrix client, heartbeat timer, message routing, process supervision |
| MCP tool server | ~300 | Python (FastMCP) | matrix_send, file_observation, update_belief, search_memory, adjust_heartbeat |
| Per-agent config | ~100 | JSON | Separate session dirs, SOUL.md paths, shared MCP config |
| **Total** | **~1000** | | |

### Cross-References

- **Brief 10 (Flywheel/Clawdbot):** Agent Mail, CM, CASS are MCP-compatible and from the same author. Integration should be natural.
- **PRD v4 (Gateway Server):** pi_agent_rust's extension system could eventually host a gateway-like quality gate as a WASM or MCP extension.
- **PRD v5 (Async Native):** The orchestrator pattern (external process routing messages to agent RPCs) is already an async decoupled architecture.
- **Context-engineering/03 (KAN Assessment):** The KAN scorer, if ever built, would be a custom tool delivered via MCP server — pi_agent_rust doesn't need to know about it.

---

*Recommended as primary harness for the girls' MVP. See `harness-comparison-matrix.md` for full comparison with NullClaw.*
