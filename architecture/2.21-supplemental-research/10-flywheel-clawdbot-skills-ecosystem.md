# 10: The Agent Flywheel—Clawdbot Skills & Integrations Ecosystem

**Source:** Dicklesworth's "The Agent Flywheel: Coordinating Agentic Systems for Mission-Critical Coding Workflows" (internal, MIT license with OpenAI/Anthropic Rider)

**A production methodology for orchestrating 30+ agent skills via named tmux sessions, filesystem-based mailboxes, unified search, 3-layer memory with confidence decay, and safety guards (DCG, UBS, ACIP).** The Flywheel demonstrates how to scale agent coordination from "two agents in a room" to "swarm of specialized agents with mutual accountability."

---

## Core Coordination Architecture

### NTM: Named Tmux Manager

Named Tmux Manager orchestrates multiple agents as tiled panes in a single tmux session:

```bash
$ ntm start red blue validator
# Creates window with 3 panes:
#   ┌──────────────┬──────────────┐
#   │     RED      │     BLUE     │
#   ├──────────────┼──────────────┤
#   │  VALIDATOR   │              │
#   └──────────────┴──────────────┘
```

Each pane is an independent agent process. NTM provides:
- **Robot mode API:** HTTP endpoints for each pane (POST /pane/red/stdin, GET /pane/red/stdout)
- **Token velocity tracking:** Monitors tokens/second per agent (detects runaway processes)
- **Context rotation with 80% warning:** When an agent hits 80% of its context window, NTM emits orange warning; at 90%, it force-compacts

**Token velocity thresholds:**
- Green: <1000 tokens/minute
- Yellow: 1000-5000 tokens/minute (investigation recommended)
- Orange: 5000-15000 tokens/minute (potential issue)
- Red: >15000 tokens/minute (force-halt for review)

### Agent Mail: MCP Coordination Layer

Agent Mail is a FastMCP HTTP server providing mailbox-based coordination:

```
POST /mail/send
{
  "from": "red",
  "to": "blue",
  "subject": "Escalation: Unknown vulnerability",
  "priority": "urgent",
  "payload": "..."
}

GET /mail/inbox?agent=blue&since=2026-02-23T14:00:00Z
[
  {
    "id": "msg-abc123",
    "from": "red",
    "subject": "Escalation: Unknown vulnerability",
    "priority": "urgent",
    "created_at": "2026-02-23T14:30:45Z",
    "read_at": null
  }
]
```

**Memorable identities:**
- Agents assigned adjective+noun names (Red, Blue, Validator)
- Mailboxes created dynamically on first message
- No pre-registration required

**File reservations with TTL:**
- Agent can reserve a file for exclusive write access
- Reservation expires after 5 minutes (configurable)
- Prevents two agents from concurrently editing same file

**Threaded messaging:**
- Each message has optional parent_id (creates conversation thread)
- Importance levels: normal, elevated, urgent, critical
- Urgent/critical messages trigger user notification (not suppressed by heartbeat)

**Contact policies:**
- **open:** Accept messages from anyone
- **auto:** Accept messages only from list of known agents
- **contacts_only:** Pre-established contact list
- **block_all:** No incoming messages (escalate all to user)

**Human overseer bypass:**
- Critical+urgent message from Red to Blue can immediately escalate to human
- Otherwise, Red/Blue coordinate autonomously
- User can override (deny escalation, force coordination to continue)

### CASS: Unified Search Across Agent Types

CASS (Comprehensive Agent State Search) provides full-text and semantic search over:
- Agent transcripts (LLM conversations)
- Memory documents (CLAUDE.md, memories.json)
- Skill definitions
- Audit logs
- Learned patterns

Search modes:
```
# Full-text search
cass search "vulnerability detection" --type transcripts

# Semantic search (via embeddings)
cass search "how should we approach security" --semantic --limit 20

# Structured search
cass search --agent=red --time-range=2026-02-20..2026-02-23 --tag=security

# Watch mode (poll every 2s, re-run on changes)
cass watch "suspicious activity" --semantic --watch-interval=2s
```

---

## Memory & Learning Architecture

### CM: CASS Memory—3-Layer Memory with Confidence Decay

Memory organized in three layers:

**Layer 1: Episodic Memory**
- Raw transcripts of each agent action
- Retention: 30 days then archive
- Fidelity: 100% accuracy (no summarization)
- Use case: "What exactly did Red say about this on Feb 20?"

**Layer 2: Working Memory**
- Synthesized insights from recent episodes
- Retention: 7 days (refreshed if accessed)
- Fidelity: 80-90% (some summarization)
- Use case: "What has the team learned this week?"

**Layer 3: Procedural Memory**
- Learned patterns, decision rules, strategies
- Retention: Indefinite with confidence decay
- Fidelity: 70-80% (patterns are probabilistic)
- Use case: "When we encounter X-type problems, what works?"

**Confidence decay:**
- Base half-life: 90 days
- Pattern: confidence = confidence_initial * 2^(-age / 90 days)
- Harmful patterns: 4× faster decay (confidence = initial * 2^(-4 × age / 90 days))
- Refresh on use: Accessing a pattern resets its age

### ACE Pipeline: Anti-Pattern Learning

Learning is mediated by a 4-step pipeline (no LLM involved in curator step):

1. **Generator:** LLM generates candidate learned patterns from recent episodes
   - Input: "What patterns emerge from these 5 successful security audits?"
   - Output: Candidate patterns with confidence estimates

2. **Reflector:** LLM reflects on whether patterns are generalizable
   - Input: Candidate pattern + 10 counter-examples
   - Output: Pattern refined or discarded

3. **Validator:** LLM validates pattern against edge cases
   - Input: Pattern + adversarial test cases
   - Output: Confidence score and failure modes documented

4. **Curator:** Human reads final pattern (NO LLM involved)
   - Input: Pattern with documented confidence, success rate, failure modes
   - Output: Approved, queued for approval, or rejected
   - Rationale: "If Curator also used an LLM, it could drift further from human intent"

Curator has NO LLM to prevent **iterative drift:** each generation step moving further from the original intent.

### BV: Beads Viewer—Graph-Aware Task Triage

Tasks represented as a DAG (directed acyclic graph) of dependencies. Beads Viewer applies:

- **PageRank:** Identifies high-influence tasks (solve task A and 10 others unblock)
- **Betweenness centrality:** Identifies bottleneck tasks
- **Critical path:** Computes longest path to goal

Visualization:
```
[Security Audit] ──→ [Threat Model] ──→ [Mitigation Plan]
     ↓                   ↓                    ↓
  [Code Review]   [Architecture Review]  [Implementation]
     ↓                   ↓                    ↓
     └───────────→ [Final Sign-Off] ←──────┘
```

Task coloring by urgency:
- Red: On critical path, blocking other tasks
- Yellow: On critical path, not blocking yet
- Green: Off critical path, can be deferred
- Blue: Completed, archived

---

## Workflow Methodologies

### Planning Workflow (85%+ Planning Methodology)

The Flywheel emphasizes **heavy upfront planning:**

1. **Decomposition:** Red and Blue jointly decompose the goal into subtasks (30% of total time)
2. **Risk modeling:** Identify unknowns, assign research tasks (20% of total time)
3. **Beads triage:** Order tasks by criticality (10% of total time)
4. **Execution:** Agents work in priority order (30% of total time)
5. **Synthesis:** Review, update memory, close out (10% of total time)

This "85% planning" approach prevents late-stage surprises.

### Beads-Workflow

Once tasks are identified and prioritized (beads), execute in topological order:
- Bead: atomic unit of work (e.g., "audit security logging")
- Workflow: sequence of beads respecting dependencies
- Swarm: multiple agents work on independent beads in parallel

### Agent-Swarm-Workflow

Extend beads-workflow to use agent pool:
```
[Red on Bead-A] [Blue on Bead-B] [Validator on Bead-C]
        ↓               ↓                ↓
     Complete      Complete         Complete
        ↓               ↓                ↓
     Sync via Agent Mail (results to shared memory)
        ↓
[Beads-D, E, F ready for next wave]
```

Max parallelism determined by number of available agents.

### Agent Fungibility Philosophy

**Core assumption:** Every agent is a generalist. Specialization is temporary.

This challenges the assumption that Red = explorer, Blue = anchor. In the Flywheel:
- Red could specialize in security audits this week
- Blue could specialize in security audits next week
- Validator can step in for either

**Implication for the girls:** Don't assume Red and Blue are permanently bound to their roles. Design such that they can swap responsibilities if needed.

---

## The Flywheel Loop

**Core iteration:**

```
v1 PLAN
  ↓ (beads, priorities)
v2 BEADS
  ↓ (execute in swarm)
v3 SWARM
  ↓ (agents work, report)
v4 REVIEW
  ↓ (CM learns, UBS validates)
v5 COMMIT
  ↓ (finalize decision, update memory)
v6 PLAN ← (next iteration with learned patterns)
```

Each loop:
- CASS remembers all decisions
- CM learns from successes and failures
- UBS prevents safety regressions
- Beads Viewer re-prioritizes based on new information

---

## Safety Architecture

### DCG: Destructive Command Guard

Detects commands that irreversibly modify state:
- `rm`, `git reset --hard`, `dd`, `truncate`
- Database DROP commands
- File deletion via any method

Destructive commands require explicit user approval. Agent cannot execute unilaterally.

### UBS: Universal Behavior Scrubber

Monitors agent behavior across 18 safety categories:

1. **Unauthorized data access**
2. **Credential leakage**
3. **Prompt injection patterns**
4. **Social engineering response**
5. **Privilege escalation attempts**
6. **Network exfiltration**
7. **Malware-like behavior** (spawning processes, writing to /tmp)
8. **Resource exhaustion**
9. **Timing attacks**
10. **Information disclosure**
11. **Business logic manipulation**
12. **Authentication bypass**
13. **Authorization violation**
14. **Denial of service**
15. **Unsafe deserialization**
16. **Unsafe reflection/eval**
17. **Race conditions**
18. **Dependency vulnerability**

Each category has 8-language detection (English, code-style syntax, regex patterns, adversarial phrasings, obfuscation, etc.).

### SLB: Supervisor-Led Backup (Two-Person Rule)

For critical decisions:
- Agent 1 proposes decision
- Agent 2 reviews independently
- Both must agree before committing
- User can override disagreement

### ACIP: Adversarial Cognitive Inoculation Protocol

Before deploying agents on high-stakes tasks:
1. Red team generates 10 adversarial prompts
2. Agents process prompts, provide responses
3. Red team attempts to manipulate responses
4. If >50% of manipulations succeed, training continues
5. Once <25% succeed, agents are considered "inoculated"

---

## Context Management

### NTM Context Rotation

When an agent hits token limits:

1. **80% warning:** Orange indicator, agent continues
2. **85% preparation:** NTM begins compaction in background
3. **90% force-compact:** Agent paused, context summarized
4. **95% recovery:** Force-compress to 50K tokens, emit recovery prompt

Recovery prompt:
```
Your context window is exhausted. Continuing with essential context:
[Last 4 messages]
[Top 10 items from CASS semantic search on current task]

What is your next action?
```

### Post-Compaction Recovery Prompt

Agent receives explicitly:
- What context was preserved (last N messages)
- What context was archived (summary)
- What search results are available (top 10 from CASS)
- Instruction to continue or escalate

This makes context recovery explicit rather than silent.

### CM Token Budget Flags

CM tracks token budget per agent per day:
- Red: allocated 500K tokens/day
- Blue: allocated 500K tokens/day
- Validator: allocated 200K tokens/day

When usage hits:
- 50%: Informational flag
- 75%: Yellow warning
- 90%: Orange warning (daily limit approaching)
- 100%: Red error, agent cannot make LLM calls until reset (midnight)

---

## Architectural Implications for the Girls

### Agent Mail for Red/Blue Coordination

Replace ad-hoc message passing with Agent Mail API:
- Red sends urgent findings to Blue: POST /mail/send with priority=urgent
- Blue reads Red's mailbox: GET /mail/inbox?agent=red
- Joint decisions stored in shared mailbox

**Implication:** Explicit asynchronous coordination avoids missed context.

### CM's 3-Layer Memory with Confidence Decay

Adopt CM's structure for the girls' learning:
- **Episodic:** Raw transcripts of each girl's reasoning
- **Working:** Weekly synthesis of discoveries
- **Procedural:** Learned collaboration patterns (with confidence decay)

**Implication:** Not all memories are equally reliable. Some fade naturally; harmful patterns fade faster.

### ACE Pipeline Anti-Pattern Learning

Critical: **Curator has NO LLM.** This prevents drift.

When the girls learn a collaboration pattern:
1. **Generator (Red):** "I notice Blue tends to validate my X-type findings"
2. **Reflector (Blue):** "Does that pattern hold for edge cases?"
3. **Validator (User):** "Is this pattern you both learned actually correct?"
4. **Curator (User, no LLM):** Final approval prevents recursive drift

**Implication:** Self-improvement requires human oversight at the curator step. Without it, the girls' learned patterns could drift away from the original intent.

### Beads Viewer for Priority Management

Model the girls' task dependencies as a DAG. Red and Blue work in priority order (critical path first), not arbitrary order.

**Implication:** Task ordering is determined by bottlenecks, not personal preference. This creates efficiency without explicit coordination.

### Agent Fungibility Philosophy

Don't permanently bind Red = explorer, Blue = anchor. Both should be capable of either role.

**Implication:** Over time, test whether Red and Blue can swap roles. If they can't, the architecture has created unnecessary specialization.

### The Flywheel Loop for Continuous Improvement

Adopt the 6-phase loop:
```
Plan (decompose) → Beads (prioritize) → Swarm (execute)
  ↓
Review (CM learns, UBS validates) → Commit (finalize)
  ↓
Plan (next iteration with learned patterns)
```

Each iteration gets better because CM remembers.

### Safety Architecture: DCG, UBS, SLB, ACIP

- **DCG:** Protect against destructive commands (deletion, reset, truncate)
- **UBS:** Monitor 18 safety categories
- **SLB:** Two-person rule for critical decisions
- **ACIP:** Inoculate against adversarial prompts

Implement these orthogonally to the coordination logic.

---

## Concrete Metrics to Track

### Coordination Metrics

- **Agent Mail throughput:** Messages/second, latency (should be <100ms)
- **File reservation contention:** % of reservation attempts that timeout (high = agents stepping on each other)
- **Mailbox read latency:** Time from send to read (should be <1s)

### Memory & Learning Metrics

- **Episodic memory size:** Grows linearly with time (tuning indicator)
- **Working memory hit rate:** % of CASS queries that find relevant working memory (should be >70%)
- **Procedural memory activation:** % of decisions informed by learned patterns (should grow over time)
- **Confidence decay curve:** Do harmful patterns actually decay faster than neutral ones?
- **ACE pipeline pass rate:** % of generator candidates that make it through curator (high rate = generator is learning curator's preferences)

### Safety Metrics

- **DCG trigger rate:** How often destructive commands are detected (should be rare; indicates safety is working)
- **UBS false positive rate:** % of UBS flags that are benign (tune threshold to minimize)
- **SLB agreement rate:** % of two-person rules where both agents agree (high = coordination is tight)
- **ACIP robustness:** % of adversarial prompts that agents correctly identify as manipulative

### Workflow Metrics

- **Planning time ratio:** (Planning time) / (Total time) (target: 85%)
- **Beads criticality distribution:** % on critical path vs off (tuning goal)
- **Swarm parallelism:** # of beads executing in parallel (scaling indicator)

These metrics hold the Flywheel accountable to its design principles: heavy planning, continuous learning, mutual accountability.

---

## License Note

The Flywheel architecture is documented under MIT license with an OpenAI/Anthropic Rider: the companies themselves cannot use this architecture directly for their products. However, the concepts (3-layer memory, confidence decay, ACE pipeline curator without LLM, beads-based workflow, etc.) are fair game for the girls' research and design.

The critical insight—that curator step should NOT use an LLM to prevent iterative drift—is the most valuable contribution and applies directly to self-improving agent architecture.
