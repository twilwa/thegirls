# 09: NanoClaw & YPI—Agent Patterns for Isolation and Recursion

**Source:** NanoClaw (github.com/anysphere/nanoclaw) and YPI: Recursive Language Models as Autonomous Agents (arxiv 2601.08934, Jan 2026)

**Two complementary minimalist agent designs: NanoClaw enforces per-group isolation via containers, while YPI treats context as a finite budget and agents as self-delegating recursive functions.** Together they model the architecture for scaling agent coordination without exploding complexity.

---

## NanoClaw: Container-Based Group Isolation

### WhatsApp Integration

NanoClaw targets WhatsApp groups (via baileys library, reverse-engineered client):
- Per-group isolated agent instance
- One `.claude/` directory per group
- Message isolation: group A cannot see group B's messages

**Per-group CLAUDE.md memory:**
- Local: writes happen within that group's instance
- Global: read-only copy from non-main groups (allows cross-group knowledge without write coupling)

### Queue & Concurrency Model

**Global concurrency control:**
```
group_queue[A] → jobs → [executor 1]
group_queue[B] → jobs → [executor 2]
                         ...
                      [executor N]
```

All groups share a pool of N executors (default N=4). This prevents runaway consumption: if one group is malicious (spamming commands), others still get throughput.

Each group has its own queue:
- Messages enqueue in arrival order
- Queue processes sequentially per group (no race conditions on that group's memory)
- Queues drain in parallel (executor pool)

### Container-Based Execution

Each group's job runs in a Docker container:
```dockerfile
FROM ubuntu:22.04
WORKDIR /group-workspace
COPY group-A/.claude /workspace/.claude
COPY shared-base /workspace/base
RUN --mount=type=bind,source=/tmp,target=/tmp \
    /usr/bin/claude < /workspace/.claude/prompt.txt
```

**Per-group mounts:**
- Read-write: `/workspace/.claude/` (this group's memory)
- Read-only: `/workspace/base/` (shared immutable knowledge)
- Read-only: `/tmp/` (host tmp, for IPC)

Container exits after job completes; no persistent process means no state leaks.

### Isolated `.claude/` Directories

```
/nanoclaw/workspace/
  groups/
    group-A/.claude/
      CLAUDE.md (rw)
      memories.json (rw)
      .gitignore
    group-B/.claude/
      CLAUDE.md (rw)
      memories.json (rw)
    main/.claude/
      CLAUDE.md (rw) [source of truth for global memories]
```

Each group's `.claude/` is a git working tree. When group-B updates memory, NanoClaw:
1. Commits to group-B's branch
2. Rebases main's global memories (merge-base resolution)
3. Syncs read-only copy back to group-B

### Task Scheduler

Three types of scheduled tasks:
- **cron:** "Every 3 hours, synthesize insights from all groups"
- **interval:** "Every 30 seconds, check for urgent messages"
- **once:** "When system starts, load shared knowledge"

Tasks enqueue into the group_queue just like regular messages.

### IPC: Filesystem-Based JSON Messages

Groups communicate via `/tmp/nanoclaw-ipc/`:
```
/tmp/nanoclaw-ipc/
  group-A → group-B.json: {"type": "query", "payload": "..."}
  group-B ← group-A.json: {"type": "response", "payload": "..."}
```

**Authorization:** Each group verifies that the sender's `chatJid` matches the file creator (via file stat).

This prevents spoofing: group-A cannot fake a message from group-B.

### Skills with Three-Way Merge

When group-A and group-B both invoke a skill (e.g., "draft-email"), they work from a shared skill base:
```
skill-draft-email (base) ← (from shared/skills/)
  ↙ (merge)         ↖
group-A:local       group-B:local
(conflict resolution)
  ↓
merged version (committed back to shared/skills/)
```

Three-way merge using `git merge-file`:
```bash
$ git merge-file -p group-A group-B base
```

Conflicts are resolved by **conflict resolution levels:**
- **auto:** Automated resolution (if no overlapping edits)
- **prompt:** Agent halts, emits to heartbeat for user decision
- **accept-ours:** Group-A's version wins
- **accept-theirs:** Group-B's version wins

### Sentinel-Free Skill Installation

Installing a new skill doesn't require a sentinel (supervisor agent). Instead:
- Skill file placed in `/workspace/skills/new-skill.md`
- Agent detects via inotify
- Attempts dry-run (simulates invocation, doesn't execute)
- If safe, commits to shared skills; if unsafe, asks user

This is "skill installation without a gatekeeper."

---

## YPI: Recursive Language Models as Autonomous Agents

**Core insight:** Problems aren't too hard, they're too big for one context window. Solution: recursive decomposition.

### Self-Delegating LLM: rlm_query

Instead of a single LLM call, the agent breaks down the problem:

```python
def rlm_query(problem: str, depth: int = 0) -> str:
  if depth > MAX_DEPTH:
    return "depth limit exceeded"

  # LLM decomposes the problem
  subproblems = llm(f"""
    Break down this problem into subproblems:
    {problem}

    Return JSON array of subproblems.
  """)

  results = []
  for subproblem in subproblems:
    # Recursive delegation
    result = rlm_query(subproblem, depth + 1)
    results.append(result)

  # Synthesize results
  synthesis = llm(f"""
    Given these results:
    {results}
    Synthesize a solution to: {problem}
  """)

  return synthesis
```

Each recursive call consumes only the tokens needed for that subproblem, not the full problem.

### Five Recursion Guardrails

1. **Depth limit:** MAX_DEPTH (default 5)
   - Prevents infinite recursion
   - Enforced hard limit in agent loop

2. **PATH scrubbing:** Environment variable $PATH removed before subprocess spawn
   - Prevents agent from accidentally calling /bin/rm, etc.
   - Subagents inherit minimal env

3. **Call count:** RLM_MAX_CALLS (default 100)
   - Tracks total LLM calls across entire recursion tree
   - If exceeded, agent stops decomposing and returns best-effort result

4. **Budget:** RLM_BUDGET (default 1M tokens)
   - Total token allowance for entire recursive tree
   - Enforced via per-call token accounting
   - When exhausted, agent switches to summarization mode

5. **Timeout:** RLM_TIMEOUT (default 1 hour)
   - Wall-clock time limit for entire tree
   - If exceeded, agent kills pending subagents and returns partial results

### Context as Finite Non-Renewable Resource

YPI treats context like a budget:
- Each problem costs tokens
- Subproblems share the budget
- No infinite context carryover

**Symbolic file access:** Instead of loading entire files into context:
```bash
$ grep "security" /workspace/threat-model.md | wc -l  # 47 lines
$ sed -n '10,15p' /workspace/design.md                # 6 lines
```

Agent can run symbolic queries (grep, sed, wc) to understand file content without consuming tokens. If necessary, load targeted excerpts.

### Sentinel-Based Background Task Notifications

YPI supports background tasks (e.g., "while I'm decomposing, check the email inbox"):

Background tasks write sentinels to `/tmp/ypi-signal-*/`:
```
/tmp/ypi-signal-red/email-check-2026-02-23-14-35-22.json
{
  "source": "email_checker",
  "event": "urgent_email",
  "summary": "User sent: 'STOP IMMEDIATELY'"
}
```

Main agent polls `/tmp/ypi-signal-*` every 5 seconds. If sentinel found:
1. Reads the signal
2. Evaluates urgency (does this interrupt the current decomposition?)
3. If high urgency, cancels pending subagents and switches context
4. If low urgency, queues for later

This avoids busy-waiting while still remaining responsive.

### Peer Discovery via /proc Scanning

YPI agents can discover each other without central coordination:

```python
def find_peers() -> List[PeerId]:
  peers = []
  for pid in os.listdir("/proc"):
    try:
      cmdline = open(f"/proc/{pid}/cmdline").read()
      if "rlm_agent" in cmdline:
        peers.append(pid)
    except OSError:
      pass
  return peers
```

**Implication:** Red and Blue discover each other by /proc scanning. No service discovery needed.

### Shared Session Memory: rlm_sessions

Each agent can read sibling and parent transcripts:

```python
def rlm_sessions() -> Dict[AgentId, TranscriptId]:
  sessions = {}
  for agent_id in find_peers():
    transcript_path = f"/tmp/ypi-transcript-{agent_id}.jsonl"
    if os.path.exists(transcript_path):
      sessions[agent_id] = transcript_path
  return sessions
```

Agent can query: "What did Blue discover about this?" and read Blue's transcript.

### Self-Improvement: Agents Modifying Their Own Code

YPI agents can edit their own rlm_query and SYSTEM_PROMPT.md:

```python
# In a routine, after a successful complex decomposition:
with open("/tmp/ypi-system-prompt.md", "a") as f:
  f.write("""
## Learned Pattern: Multi-Level Decomposition
When encountering X-type problems, decompose as:
1. [subproblem 1]
2. [subproblem 2]
...
""")
```

On next startup, agent reads updated SYSTEM_PROMPT.md and incorporates learned patterns.

**Caveat:** Self-modification is logged to audit trail. Agents cannot silently rewrite their own code.

### Cost Tracking Environment Variables

```bash
export RLM_BUDGET=1000000        # tokens
export RLM_TIMEOUT=3600          # seconds
export RLM_MAX_CALLS=100         # LLM invocations
export RLM_MAX_DEPTH=5           # recursion depth
```

These are immutable during a single agent run (set at startup). Changing them requires supervisor approval.

---

## Architectural Implications for the Girls

### NanoClaw's Per-Group Isolation Maps to Per-Persona Isolation

Red and Blue are analogous to WhatsApp groups:
```
nanoclaw/workspace/
  groups/
    red/.claude/
      CLAUDE.md (Red's persona)
      memories.json
    blue/.claude/
      CLAUDE.md (Blue's persona)
      memories.json
    joint/.claude/
      CLAUDE.md (shared)
```

Each persona has isolated memory. Joint decisions written to the shared group.

**Implication:** Design Red and Blue's `.claude/` structures to enforce isolation:
- Red cannot directly write to Blue's CLAUDE.md
- Cross-persona communication happens via IPC (filesystem JSON) or shared memories
- Skill installation requires consensus (three-way merge resolution)

### YPI's "Context as Budget" & Self-Modifying Infrastructure

The girls should adopt YPI's recursion guardrails:

1. **Depth limit:** If Red's decomposition goes 5+ levels deep, escalate to user
2. **Budget:** Red and Blue share RLM_BUDGET; if one burns tokens recklessly, the other suffers
3. **Call count:** Total LLM calls tracked; prevents runaway decomposition
4. **Timeout:** If the girls are stuck in a decomposition loop >1 hour, auto-escalate
5. **Token estimation:** Use symbolic queries (grep logs, count entries) instead of loading everything

**Implication:** This creates enforced scarcity. The girls can't both run unlimited recursion simultaneously. Design a negotiation protocol: Red requests budget, Blue approves or delays.

### Transcript Sharing via rlm_sessions

Instead of explicit message passing, Red and Blue each write their transcript to:
```
/tmp/ypi-transcript-red.jsonl
/tmp/ypi-transcript-blue.jsonl
```

Blue can read Red's transcript without Red explicitly sending a message. This is "memory reading" instead of "message passing."

**Implication:** Design the girls' coordination to use transcript reading as the primary synchronization mechanism. Messages are higher-bandwidth (more expensive) and should be reserved for urgent escalations.

### Self-Improvement Architecture

YPI's learned-patterns approach (appending to SYSTEM_PROMPT.md) gives the girls a concrete self-improvement mechanism:

After a successful multi-agent collaboration on a hard problem:
```markdown
## Learned: Blue-Red Coordination on X-type Problems
When Red proposes [exploration pattern], Blue should [validation pattern].
Confidence: 90% (3/3 successes)
Last updated: 2026-02-23
```

These learned patterns accumulate in SYSTEM_PROMPT.md and inform future decisions.

### Peer Discovery & No Central Coordination

YPI's /proc scanning means the girls don't need a coordinator. They discover each other autonomously. This is critical for resilience:
- If the coordinator process dies, the girls still function
- New agents can join without registration
- No single point of failure

**Implication:** Don't design a "Red controller" or "Blue controller." Let them discover and coordinate via /proc, filesystem sentinels, and transcript reading.

---

## Concrete Metrics to Track

### NanoClaw Metrics

- **Per-group container overhead:** Time to spawn/destroy (should be <100ms)
- **Memory per group:** Should scale linearly with group age, not explosively
- **IPC latency:** Time from group-A writing to group-B reading (should be <10ms on same host)
- **Skill merge conflicts:** Frequency of three-way merge conflicts (high frequency = personas are diverging)
- **Global queue throughput:** Messages/second across all groups

### YPI Metrics

- **Recursion depth distribution:** What's the median rlm_query depth? (Lower is better for efficiency)
- **Token efficiency per problem:** Total tokens used / problem complexity (can infer complexity from subproblem count)
- **Call count per budget:** What fraction of RLM_MAX_CALLS is typically used?
- **Timeout frequency:** How often does RLM_TIMEOUT trigger? (Indicates problems need larger budget)
- **Learned patterns activation:** How often does a learned pattern contribute to a decision? (Measures self-improvement effectiveness)

These metrics reveal whether the isolation+recursion model is actually enabling scalable agent coordination or just adding complexity.
