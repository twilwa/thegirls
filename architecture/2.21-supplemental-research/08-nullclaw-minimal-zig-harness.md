# 08: NullClaw—Ultra-Minimal Zig Agent Harness

**Source:** NullClaw Zig Implementation (github.com/kevincliff/nullclaw)

**A bare-metal agent harness written in Zig, targeting embedded and resource-constrained deployments: 678KB binary, <2ms startup, ~1MB RAM baseline.** NullClaw proves that persistent agent architecture doesn't require heavyweight frameworks. Core principle: every subsystem is an interface.

---

## Core Architecture

### Vtable-Driven Plugin System

Every subsystem exposed as an interface (vtable):

```zig
pub const ChannelVtable = struct {
  init: *const fn() ChannelContext,
  handle_message: *const fn(*ChannelContext, []const u8) void,
  send_message: *const fn(*ChannelContext, []const u8) void,
  deinit: *const fn(*ChannelContext) void,
};
```

Runtime selection via config file (TOML):
```toml
[channel]
provider = "discord"

[channel.discord]
token = "${DISCORD_TOKEN}"
```

At startup, NullClaw dlopen()s the appropriate plugin (libchannel_discord.so) and wires the vtable. No recompilation needed to swap providers.

### Heartbeat Mechanism

**parseTasks from HEARTBEAT.md:**
- Default interval: 30 minutes (configurable)
- Blocks agent loop only if tasks exist
- Non-blocking async check via inotify (Linux) or FSEvents (macOS)

If HEARTBEAT.md is updated while agent is sleeping, inotify wakes the event loop immediately.

---

## Context Compaction

### Token Budget & Threshold

- **Default budget:** 128K tokens
- **Threshold:** 75% triggers compaction
- **Token estimate:** `(chars + 3) / 4` (conservative)

### Multi-Part Summarization

For very long histories (>50K tokens), NullClaw applies **split-summarize-merge:**
1. **Split:** Divide history into 10K-token segments
2. **Summarize:** LLM generates 500-token summary per segment (in parallel, up to 4 concurrent)
3. **Merge:** Concatenate summaries, run second-pass merge if still >10K tokens

This allows compaction of 200K-token histories in a single pass without exceeding model context.

### Context Recovery

If token exhaustion occurs mid-request:
- Force-compress to fit last 4 messages (preserving critical context)
- Emit recovery prompt: "Token limit reached. Continuing with essential context."
- Restart LLM call with same request_id

---

## Daemon Supervision & State

### Component Spawning with Backoff

Each subsystem (channel, memory, scheduler) spawns as a separate OS thread:
```zig
var backoff: u32 = 100;  // ms
while (true) {
  if (component.spawn()) |_| {
    backoff = 100;
  } else |err| {
    warn("Component failed: {}", .{err});
    sleep(backoff);
    backoff = @min(backoff * 2, 30000);
  }
}
```

### State File (daemon_state.json)

Daemon restarts are idempotent via state persistence:
```json
{
  "started_at": "2026-02-23T14:30:45Z",
  "uptime_seconds": 3600,
  "component_states": {
    "channel_discord": "running",
    "memory_sqlite": "running",
    "scheduler": "running"
  },
  "last_heartbeat": "2026-02-23T14:28:00Z",
  "pending_jobs": [
    {"job_id": "abc123", "state": "in_progress"}
  ]
}
```

On restart, NullClaw reads daemon_state.json and resumes pending jobs.

---

## Memory Architecture

### SQLite with Hybrid Search

Primary datastore is a single SQLite database (~2MB for typical agent):

**Tables:**
- `memories`: content (text), category (core/daily/conversation/custom), created_at, expires_at
- `embeddings`: memory_id (FK), vector (1536-dim float32 quantized to u8), metadata
- `search_index`: FTS5 virtual table over memories

**Hybrid Search Implementation:**

```zig
pub fn search(query: []const u8, k: u32) ![]Memory {
  // FTS5 search
  var fts_results = try fts.search(query, k);

  // Vector search (via local embedding model)
  var embedding = try embed(query);
  var vector_results = try vector_search(embedding, k);

  // RRF fusion (reciprocal rank fusion)
  var scores = AutoHashMap(MemoryId, f32).init(allocator);
  for (fts_results, 0..) |mem, i| {
    var score = scores.get(mem.id) orelse 0;
    scores.put(mem.id, score + 1.0 / (i + 60)) catch unreachable;
  }
  for (vector_results, 0..) |mem, i| {
    var score = scores.get(mem.id) orelse 0;
    scores.put(mem.id, score + 1.0 / (i + 60)) catch unreachable;
  }

  // Return sorted by score
  ...
}
```

**Weights (configurable):**
- Keyword weight: 0.6 (default)
- Vector weight: 0.4 (default)

**Expiration support:**
- Each memory has optional `expires_at` timestamp
- Periodic cleanup task runs every hour, deletes expired entries
- Prevents stale beliefs from cluttering search results

---

## Matrix Client Built-In

NullClaw includes a native Matrix client-server implementation (no libmatrix dependency):

### Client-Server Protocol

Implements Matrix v1.3 subset:
- **GET /sync:** Long-polling with 30-second timeout, returns rooms + messages + state
- **PUT /send:** Transaction ID-based deduplication, prevents double-send
- **GET /rooms/{room_id}/state:** Room filtering via allowlist (config)
- **POST /join:** Join only allowlisted rooms on startup

### Room Filtering

```toml
[matrix]
homeserver = "https://matrix.example.com"
user = "@agent:example.com"
password = "${MATRIX_PASSWORD}"

[matrix.rooms]
allowed = [
  "!room1:example.com",
  "!room2:example.com"
]
```

Prevents agent from accidentally joining malicious rooms or being social-engineered into them.

### Message Routing

Matrix messages route through the unified channel abstraction:
- Raw message → Channel.handle_message()
- Response generated → Channel.send_message()
- Sent via PUT /send with transaction ID = `msg_id + timestamp`

This allows Red and Blue to coordinate via Matrix rooms without additional IPC.

---

## Discord Integration

Native Discord Gateway v10 implementation (no discord.js dependency):

### WebSocket Gateway

- Connects to wss://gateway.discord.gg
- Maintains heartbeat (25-60 second interval, server-specified)
- Handles READY, MESSAGE_CREATE, GUILD_UPDATE events
- Sends IDENTIFY with bot token

### Message Splitting

Discord has 2000-char limit. Messages longer than 1900 chars are split:
```zig
var pos: usize = 0;
while (pos < full_message.len) {
  var chunk_end = @min(pos + 1900, full_message.len);
  // Backtrack to last space if mid-word
  while (full_message[chunk_end] != ' ' and chunk_end > pos) {
    chunk_end -= 1;
  }
  var chunk = full_message[pos..chunk_end];
  send_to_discord(chunk);
  pos = chunk_end;
}
```

---

## Subagent Manager

NullClaw supports background subagents (for delegation) with safety guardrails:

### Separate OS Threads

Each subagent spawns as a separate thread:
```zig
var subagent = try SubAgent.spawn("draft_response", allocator);
// Main agent continues
var result = try subagent.wait();
```

### Restricted Tool Set

Subagents cannot:
- Spawn further subagents (prevents infinite recursion)
- Delegate to other subagents (prevents loops)
- Access heartbeat (prevents direct user notification)

Subagent permissions:
- Read from memory (shared RO view)
- Write to temporary workspace
- Call LLM (with subagent-specific bearer token)

### Max Concurrent Configuration

```toml
[scheduler]
max_subagents = 4
subagent_timeout_sec = 300
```

Default is 4 concurrent subagents. Excess requests queue.

---

## Security Model

### Pairing Protocol

On first startup, NullClaw requires a pairing handshake:
1. Agent generates 6-digit code (e.g., 487923)
2. Code displayed to user via stdout
3. User enters code in companion app (web/mobile/CLI)
4. Shared secret derived via PAKE (Password Authenticated Key Exchange)
5. All subsequent communication signed with shared secret

This prevents an attacker from compromising an agent simply by finding its configuration file.

### Workspace Scoping

Agent operates only within its workspace directory:
```
/home/user/.nullclaw/agent-red/
  config.toml
  daemon_state.json
  workspace/
    IDENTITY.md
    SOUL.md
    MEMORY.sqlite
    daily/
```

Filesystem permissions: agent process runs as unprivileged user, workspace owned by that user with 0700 permissions.

### Encryption

All messages at rest and in transit encrypted with **ChaCha20-Poly1305**:
```zig
var cipher = try ChaCha20Poly1305.init(key, nonce);
var ciphertext = try cipher.encrypt(plaintext);
// Stored as: [nonce (12 bytes) || ciphertext || tag (16 bytes)]
```

Decryption validates auth tag; corrupted messages fail fast.

### Sandbox Auto-Detection

On startup, NullClaw detects if running inside a sandbox:
```zig
var sandboxed = os.access("/proc/self/ns/mnt", os.F_OK) != 0 or
                os.getenv("NULLCLAW_SANDBOX") != null or
                // Landlock, Firejail, Bubblewrap, Docker detection...
                detect_docker() or detect_landlock();
```

If sandboxed, restrict network access to only localhost and whitelisted domains.

### Signed Audit Trail

Every significant action logged to immutable audit log:
```json
[
  {
    "timestamp": "2026-02-23T14:30:45Z",
    "action": "memory.write",
    "subject": "agent_id:red",
    "object": "memory:abc123",
    "signature": "ed25519(...)"
  }
]
```

Each entry signed with agent's private key. Hash chain prevents tampering.

---

## Provider Ecosystem

NullClaw supports **22+ AI providers** and **13 channels:**

**AI Providers:**
- NEAR AI, OpenAI, Anthropic, Ollama, Tinfoil
- Mistral, Groq, Together.ai, Replicate
- vLLM (self-hosted), HF Inference API
- (+ 11 more)

**Channels:**
- Discord, Matrix, Telegram, Slack, IRC
- Email (IMAP/SMTP), Web (HTTP), WebSocket
- Twilio (SMS), Mastodon, Bluesky
- (+ 3 more)

Each integrated as a plugin, can be independently enabled/disabled.

---

## Architectural Implications for the Girls

### Matrix Support Out of the Box

Built-in Matrix client is **enormous** for the girls' "mind palace" concept:
- Red and Blue can coordinate via encrypted Matrix rooms
- External agents (future: third-party AI services) can join the same rooms
- Room state provides shared context without explicit message passing
- Federation allows the girls' workspace to extend beyond a single homeserver

**Implication:** Design the girls' coordination protocol around Matrix room semantics:
- Red's findings → Red's exploration room (Blue observes)
- Blue's validations → Blue's anchor room (Red observes)
- Joint decisions → Shared decision room
- External stakeholders → Guest access to read-only summary rooms

### Vtable Architecture & Swappability

The vtable-driven design means:
- Swapping Discord for Slack requires only a config change
- Adding a new LLM provider is pure plugin (no core recompilation)
- Memory search algorithm can be upgraded (FTS5 → BM25 → whatever) without touching the agent loop

**Implication:** Don't hardcode assumptions about which channels the girls use. Design the girl-coordination protocol to work over Matrix, Discord, email, etc., with feature degradation (e.g., threads might not exist in email).

### Ultra-Minimal Footprint

678KB binary + 1MB RAM baseline means the girls could run as:
- Background process on a Raspberry Pi
- Serverless function (AWS Lambda, Cloudflare Workers)
- Embedded in other applications

**Implication:** The architectural design should not assume always-on server infrastructure. Consider intermittent connectivity: Red and Blue might sync once per hour, not continuously.

### Local Embedding & Search

NullClaw's SQLite + local embedding model means no external vector DB required. The girls' memories are portable:
```bash
$ cp ~/.nullclaw/agent-red/MEMORY.sqlite ~/.nullclaw/agent-blue/
$ agent-blue search "red's recent findings"
```

**Implication:** Cross-agent memory search is O(query time) not O(network round trip). This enables the girls to be extremely chatty without incurring latency.

---

## Concrete Metrics to Track

- **Binary size:** Monitor that core NullClaw stays under 1MB (feature bloat detection)
- **Startup latency:** Should stay <2ms (regression testing)
- **Memory baseline:** Agent-red + agent-blue should use <10MB combined (tuning indicator)
- **Heartbeat responsiveness:** Time from HEARTBEAT.md write to action taken (should be <1s on Linux via inotify)
- **Search quality:** For identical queries, compare FTS vs vector vs RRF (k=60) recall
- **Subagent overhead:** Time to spawn/join a subagent thread (should be <10ms)
- **Encryption overhead:** Percentage of CPU spent in ChaCha20Poly1305 (should be <5%)

These metrics keep NullClaw honest about its core promise: minimal footprint without sacrificing capability.
