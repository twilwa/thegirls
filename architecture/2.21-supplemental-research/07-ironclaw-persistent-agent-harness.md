# 07: IronClaw—Production-Grade Persistent Agent Harness

**Source:** IronClaw Rust Reference Implementation (github.com/cipherstash/ironclaw)

**A production-grade reimplementation of OpenClaw in Rust, emphasizing heartbeat-driven persistence, context compaction, and hybrid memory architecture.** IronClaw targets mission-critical deployments where reliability, observability, and long-running agent sessions matter.

---

## Core Architecture

### Heartbeat System

The heartbeat is the primary wake signal for persistent agents:
- **HEARTBEAT.md** parsed every 30 minutes
- Findings-based notification: only notifies user if heartbeat contains actionable findings (avoids alert fatigue)
- Asynchronous processing in separate Tokio task
- Heartbeat failures trigger exponential backoff (max 5 retries)

This pattern is fundamentally different from the interrupt-driven "scheduler calls agent" model. Instead, agents poll for work, making them responsive to external state changes without requiring external coordination.

### Context Compaction Strategy

Context window management is critical for long-lived agents:
- **Default budget:** 100K tokens
- **Threshold:** 80% triggers compaction
- **Three strategies, applied in order:**
  1. **Summarize:** Consolidate old conversation history via LLM summarization
  2. **Truncate:** Remove oldest non-critical context segments
  3. **MoveToWorkspace:** Archive to persistent memory (MEMORY.md) for semantic search later

Token counting uses conservative estimate: `(chars + 3) / 4`

### Workspace Memory Architecture

Workspace is a filesystem-like hierarchical namespace:
```
WORKSPACE/
  IDENTITY.md          # Agent persona definition
  SOUL.md             # Long-term values, goals, commitments
  MEMORY.md           # Primary knowledge base
  daily/
    2026-02-23.log
    2026-02-22.log
  projects/
    red-escalation/
      state.md
      findings.md
```

**Hybrid search via RRF (Reciprocal Rank Fusion):**
- Full-text search (FTS) over MEMORY.md
- Vector search over chunked embeddings
- k=60 results from each, fused by reciprocal rank
- Keyword weight: 0.6, vector weight: 0.4 (tunable)

**Memory chunking:**
- 800 words per chunk (optimal for semantic coherence)
- 15% overlap (prevents context loss at boundaries)
- Minimum 50 words (filters noise)

### Multi-Channel Architecture

IronClaw supports 40+ endpoints across four primary channels:

**TUI:** Rich terminal interface, local debugging, interactive REPL
**HTTP Webhook:** POST /event/{channel}, signed with HMAC-SHA256
**WASM:** Discord via discord.js shim, Telegram via telegram-bot-sdk
**Web Gateway:** SSE for push notifications, WebSocket for bidirectional messaging

Each channel implements a trait:
```rust
trait Channel {
  fn from_incoming(&self, msg: IncomingMessage) -> Result<()>;
  fn to_outgoing(&self, msg: OutgoingResponse) -> Result<Vec<u8>>;
  fn thread_id(&self) -> Option<String>;
}
```

Thread support: Discord threads, email conversation IDs, Slack thread timestamps all mapped to unified `thread_id` field.

---

## Agent Loop & Execution

### Router → Scheduler → Worker

The three-layer execution model:
1. **Router:** Multiplexes incoming messages to appropriate agent instance (by thread_id, user_id, or workspace)
2. **Scheduler:** Maintains job queue per agent, executes jobs in priority order
3. **Worker:** Executes individual job (LLM call, skill invocation, memory update)

Parallel job execution: up to 5 jobs per agent in flight simultaneously.

**Self-repair for stuck jobs:**
- If job exceeds timeout (default 5m), worker attempts recovery:
  1. Force-compress context to 50K tokens
  2. Emit recovery prompt: "Previous attempt timed out. Continue with compressed context."
  3. Restart LLM call with same job_id
  4. If second attempt fails, escalate to human (emit to HEARTBEAT for user decision)

### Session State Machine

```
Pending → InProgress → Completed → Submitted → Accepted
  ↓                                              ↓
  └──────────────────── Rejected ───────────────┘
```

- **Pending:** Message received, not yet processed
- **InProgress:** LLM processing, memory updates, skill execution
- **Completed:** All processing done, ready to send response
- **Submitted:** Response queued to channel
- **Accepted:** Channel confirmed delivery (or timeout after 30s)
- **Rejected:** User feedback or escalation triggered, job cancelled

---

## Orchestration & Sandboxing

### Orchestrator/Worker Pattern

**Orchestrator:** Rust binary, manages worker lifecycle
**Worker:** Docker container per job, filesystem isolation, read-write mount only to `/workspace` + `/job`

Per-job bearer tokens:
- Token issued at job start, scoped to that job_id
- Skills validate token before execution
- Token expires when job completes
- No token reuse across jobs (prevents lateral movement)

**ProxyLlmProvider:** Intercepts all LLM calls, logs prompt/completion for audit, enforces token budget per job

### Routines Engine

Cron-based scheduling + event triggers + webhook callbacks:
```yaml
routine:
  name: daily-synthesis
  cron: "0 9 * * *"           # Every morning at 9 AM
  on_event:
    - memory.updated
    - user.message_received
  webhook: "https://internal.example/trigger"
  max_concurrent: 3
  timeout: 300s
```

Execution is deduplicating: if a routine is already running, new triggers queue instead of spawning.

### Skills System

Skills are discovered via **SKILL.md frontmatter:**
```markdown
---
name: draft-email
description: Draft an email response to a user message
inputs:
  recipient: string
  subject: string
  draft: string
trust: Trusted
keywords: ["email", "draft", "compose"]
token_budget: 500
---
```

Trust model:
- **Trusted:** Built-in skills, undergo security audit
- **Installed:** User-provided, declared capabilities, pattern-based validation

Keyword/pattern scoring: when agent decides to use a skill, match against keywords + patterns in skill description. Prevents accidental skill invocation.

Token budget per skill: if a skill consumes more tokens than declared budget (e.g., "draft-email: 500"), the job is force-compressed and restarted.

---

## Safety & Security

### Prompt Injection Defense

**Pattern detection:**
- Regex patterns for command-injection syntax ("execute", "run_command", "eval")
- Marker detection (triple-backticks followed by shell syntax)
- Content escaping: all user input wrapped in `[USER_INPUT_START]...[USER_INPUT_END]` tags before LLM

**Nested escaping:** If user input contains the escape marker itself, recursive escaping applied.

### WASM Sandbox

Discord/Telegram integrations run in WASM sandbox (via wasmtime) with capability-based permissions:
- **fs:** Read-only access to workspace files
- **net:** HTTP calls limited to whitelisted domains
- **memory:** 64MB heap limit per invocation
- **cpu:** 5-second execution limit

Failed WASM invocations emit to heartbeat but don't fail the job.

### Secret Leak Detection

15+ regex patterns for common secrets:
- AWS keys (AKIA*)
- Anthropic API keys (sk-ant-*)
- OpenAI keys (sk-*)
- Stripe (sk_live_*, pk_test_*)
- GitHub tokens (ghp_*)
- JWT patterns (eyJ...)

Detected leaks are:
1. Scrubbed from context
2. Logged with severity=CRITICAL to heartbeat
3. Not sent to LLM (prevents accidental exposure)

### Shell Environment Scrubbing

Before spawning worker container:
- Remove all environment variables except: HOME, PATH, WORKSPACE, JOB_ID, BEARER_TOKEN
- Unset NODE_ENV, PYTHON_ENV, DATABASE_URL, API_KEY*
- Container runs with no access to host credentials

---

## LLM Provider & Reliability

### Multi-Provider Support

IronClaw supports:
- **NEAR AI:** Default, lowest latency
- **OpenAI:** GPT-4, GPT-4o, fallback
- **Anthropic:** Claude Opus 4, Sonnet, failover chain
- **Ollama:** Local models, air-gapped deployments
- **Tinfoil:** Fine-tuned Mistral, custom enterprise models

Provider selection via config:
```yaml
llm:
  primary: near-ai
  fallback: [openai, anthropic, ollama]
  timeout: 30s
  retry_budget: 3
```

### Circuit Breaker

Each provider has a circuit breaker:
- **Closed:** Normal operation
- **Open:** Provider failed N times, reject requests for 60s
- **Half-Open:** After 60s, try one request; if succeeds, close; if fails, reopen

Retry with exponential backoff: 100ms → 200ms → 400ms → 800ms

---

## Persistence Layer

### Database

PostgreSQL or libSQL (sqlite with replication):
- ~60 async trait methods via `sqlx`
- Tables: jobs, sessions, memories, heartbeats, audit_logs, skills
- Indexes on: thread_id, user_id, created_at, memory_embedding
- Transactions for job state updates (prevent double-execution)

---

## Architectural Implications for the Girls

### Per-Agent Workspace Isolation

Red and Blue each have isolated workspaces:
```
/workspace/red/
  IDENTITY.md → "The Explorer"
  SOUL.md     → "Maximize discovery, enable autonomy"
  MEMORY.md
  daily/

/workspace/blue/
  IDENTITY.md → "The Anchor"
  SOUL.md     → "Ground decisions, prevent drift"
  MEMORY.md
  daily/
```

This isolation prevents cross-contamination of beliefs while allowing shared-memory search (via RRF).

### Persona-Specific Identity Files

IDENTITY.md per agent can encode:
- Communication style (Red: exploratory questions; Blue: decisive conclusions)
- Risk tolerance (Red: high; Blue: conservative)
- Authority domains (Red: discovery; Blue: validation)

Skill attenuation per persona: Red cannot invoke "submit-decision" (Blue's privilege); Blue cannot invoke "propose-experiment" (Red's privilege).

### Separate Heartbeat Checklists

Each agent has its own heartbeat checklist:
- Red's heartbeat: "Have I discovered something new? Escalate to user."
- Blue's heartbeat: "Are there unvalidated claims? Request evidence from Red."

This creates mutual accountability without requiring explicit message passing.

---

## Concrete Metrics to Track

- **Heartbeat reliability:** % of heartbeats successfully parsed and processed
- **Context compaction frequency:** How often does 80% threshold trigger? Does MoveToWorkspace scale linearly with agent age?
- **Memory search quality:** For a given query, compare FTS vs vector vs RRF recall
- **Channel diversity:** Which channels are used most? Are all 40+ endpoints evenly utilized?
- **Skill invocation patterns:** Which skills are called? By which agents? (Should vary by persona)
- **Job success rate:** % of jobs that complete vs timeout/recover/fail
- **WASM sandbox violations:** How often do Discord/Telegram sandboxes hit resource limits?

These metrics directly inform whether the girls' persistence layer is actually enabling long-term coherence or just accumulating dead weight in memory.
