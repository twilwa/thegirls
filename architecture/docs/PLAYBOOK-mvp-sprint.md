# MVP Sprint Playbook: The Girls Go Live

**Purpose:** Concrete instructions for coding agents to build the MVP harness. Hand this doc (plus the architecture/ directory) to your coding agent and point it at the target machine.

**Target:** Heartbeat + self-improvement + minimal Matrix comms station
**Estimated effort:** ~21-34 SP across 4 sprints
**Assumes:** GCloud VM (or Hetzner VPS) with Docker, SSH access, Anthropic API key

---

## Sprint 0: Infrastructure (3-5 SP)

### 0.1 Matrix Server

Stand up Synapse on GCloud with Docker Compose.

```yaml
# docker-compose.matrix.yml
services:
  synapse:
    image: matrixdotorg/synapse:latest
    volumes:
      - ./synapse-data:/data
    environment:
      - SYNAPSE_SERVER_NAME=thegirls.matrix  # or your domain
      - SYNAPSE_REPORT_STATS=no
    ports:
      - "8008:8008"    # Client-server API
      - "8448:8448"    # Federation (optional, can disable)
    depends_on:
      - postgres
  postgres:
    image: postgres:16
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=synapse
      - POSTGRES_USER=synapse
      - POSTGRES_PASSWORD=${MATRIX_DB_PASSWORD}
```

**Tasks:**
- [ ] Generate Synapse config: `docker run --rm -v ./synapse-data:/data matrixdotorg/synapse:latest generate`
- [ ] Edit `homeserver.yaml`: disable federation if private, enable registration for initial setup
- [ ] `docker compose -f docker-compose.matrix.yml up -d`
- [ ] Create accounts: `@warren`, `@red`, `@blue`, `@harness` (system account)
- [ ] Create rooms: `#warren`, `#red-thoughts`, `#blue-thoughts`, `#shared`, `#observations`, `#debug`
- [ ] Set room permissions: see PRD v6 §2 room structure table
- [ ] Disable registration after account creation
- [ ] Test: send message from @warren to #warren, verify @red and @blue can read

**Verification:** `curl http://localhost:8008/_matrix/client/versions` returns JSON with supported versions.

### 0.2 Beeper/Discord Bridge (optional, can defer)

If using Beeper for Discord access:
- [ ] Set up Beeper account or self-host mautrix-discord bridge
- [ ] Configure bridge to relay target Discord server rooms into Matrix
- [ ] Verify: Discord message appears in Matrix room

If using Beeper MCP:
- [ ] Install beeper-mcp package
- [ ] Configure in harness MCP settings
- [ ] Verify: agent can read/send Discord messages via MCP tool calls

**Note:** This can be deferred to Sprint 2. Matrix-only is sufficient for MVP.

### 0.3 File Structure

```bash
mkdir -p /opt/thegirls/{red,blue,shared,config,logs}

# Per-agent directories
mkdir -p /opt/thegirls/red/{workspace,trajectory-log}
mkdir -p /opt/thegirls/blue/{workspace,trajectory-log}

# Shared directory
mkdir -p /opt/thegirls/shared/trajectory-log

# Initialize memory files
echo '[]' > /opt/thegirls/red/priors.jsonl    # Will be populated from SOUL.md
echo '[]' > /opt/thegirls/blue/priors.jsonl
echo '[]' > /opt/thegirls/red/beliefs.jsonl
echo '[]' > /opt/thegirls/blue/beliefs.jsonl
echo '[]' > /opt/thegirls/shared/observations.jsonl
```

Copy architecture docs into shared knowledge:
```bash
cp -r /path/to/thegirls/architecture /opt/thegirls/shared/architecture
cp /path/to/thegirls/PRIORITIES-v2.md /opt/thegirls/shared/
cp /path/to/thegirls/FUZZY-OBJECTIVES.md /opt/thegirls/shared/
cp /path/to/thegirls/LEGACY_PACT.md /opt/thegirls/shared/
```

---

## Sprint 1: Heartbeat + Matrix Comms (8-13 SP)

This is the core sprint. By the end, both agents are alive, talking on Matrix, and heartbeating.

### 1.1 Harness: pi_agent_rust + Orchestrator

**Why pi_agent_rust:** Same author as flywheel skills (Dicklesworth), Rust is accessible to coding agents, RPC mode enables clean separation of concerns, exceptional documentation. See `harness-comparison-matrix.md` for full analysis.

**Step 1: Build pi_agent_rust**

```bash
cd /opt/thegirls
git clone https://github.com/Dicklesworthstone/pi_agent_rust.git harness-runtime
cd harness-runtime
cargo build --release
# Binary at target/release/pi_agent_rust (~22MB)
```

**Step 2: Per-agent config**

```bash
# Red agent config
mkdir -p /opt/thegirls/red/.pi/agent
cat > /opt/thegirls/red/.pi/agent/settings.json << 'EOF'
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4-5-20250929",
  "sessionStore": "jsonl",
  "sessionDurability": "balanced",
  "compaction": {
    "contextWindow": 200000,
    "reserve": 16384,
    "keepRecent": 20000
  },
  "extensionPolicy": "balanced",
  "packages": [],
  "extensions": [],
  "skills": []
}
EOF

# Blue agent config (identical but separate directory)
mkdir -p /opt/thegirls/blue/.pi/agent
cp /opt/thegirls/red/.pi/agent/settings.json /opt/thegirls/blue/.pi/agent/settings.json
```

**Step 3: Shared MCP tool server (~300 LOC)**

Create a FastMCP server that both agents load as an MCP extension. This provides the custom tools for Matrix, beliefs, observations:

```python
# /opt/thegirls/mcp-tools/server.py
from fastmcp import FastMCP
import json, datetime, os

mcp = FastMCP("thegirls-tools")

@mcp.tool()
def matrix_send(room: str, message: str) -> str:
    """Send a message to a Matrix room."""
    # HTTP PUT to Synapse /_matrix/client/v3/rooms/{room_id}/send/m.room.message/{txn_id}
    ...

@mcp.tool()
def matrix_read(room: str, limit: int = 20, since: str = None) -> str:
    """Read recent messages from a Matrix room."""
    ...

@mcp.tool()
def file_observation(type: str, content: str, confidence: float = 0.7, references: list = []) -> str:
    """Record a structured observation to shared/observations.jsonl."""
    ...

@mcp.tool()
def update_belief(belief: str, confidence: float, evidence: str, action: str = "add") -> str:
    """Add or update a belief in this agent's beliefs.jsonl."""
    ...

@mcp.tool()
def search_memory(query: str, scope: str = "all") -> str:
    """Search across observations, beliefs, and trajectory logs."""
    ...

@mcp.tool()
def adjust_heartbeat(interval: str, reason: str) -> str:
    """Request heartbeat interval change."""
    ...

@mcp.tool()
def read_architecture(path: str) -> str:
    """Read a file from the shared architecture docs."""
    ...

if __name__ == "__main__":
    mcp.run()
```

Add MCP server to each agent's config:
```json
{
  "mcp_servers": [
    {
      "command": "python3",
      "args": ["/opt/thegirls/mcp-tools/server.py"],
      "env": {
        "AGENT_ID": "red",
        "MATRIX_HOMESERVER": "http://localhost:8008",
        "MATRIX_TOKEN": "${RED_MATRIX_TOKEN}",
        "DATA_DIR": "/opt/thegirls"
      }
    }
  ]
}
```

**Step 4: Orchestrator (~600 LOC)**

The orchestrator is a separate process that:
- Connects to Matrix via /sync (long-polling)
- Routes messages to the correct agent's RPC stdin
- Runs the heartbeat timer
- Supervises agent processes (restart on crash)

```python
# /opt/thegirls/orchestrator/main.py
import asyncio, subprocess, json
from nio import AsyncClient  # matrix-nio

class Orchestrator:
    def __init__(self, config):
        self.matrix = AsyncClient(config["matrix"]["homeserver"])
        self.agents = {}
        self.heartbeat_interval = config["heartbeat"]["default"]

    async def start(self):
        # 1. Login to Matrix
        await self.matrix.login(config["matrix"]["user"], config["matrix"]["password"])

        # 2. Spawn agent processes in RPC mode
        for agent_id in ["red", "blue"]:
            self.agents[agent_id] = subprocess.Popen(
                ["/opt/thegirls/harness-runtime/target/release/pi_agent_rust", "--rpc"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                env={
                    "PI_CONFIG": f"/opt/thegirls/{agent_id}/.pi/agent",
                    "PI_SESSIONS": f"/opt/thegirls/{agent_id}/sessions",
                    "ANTHROPIC_API_KEY": os.environ["ANTHROPIC_API_KEY"],
                    **os.environ
                }
            )

        # 3. Start event loops
        await asyncio.gather(
            self.matrix_sync_loop(),
            self.heartbeat_loop(),
            self.process_monitor()
        )

    async def matrix_sync_loop(self):
        """Poll Matrix /sync, route messages to agents."""
        while True:
            response = await self.matrix.sync(timeout=30000)
            for room_id, room_data in response.rooms.join.items():
                for event in room_data.timeline.events:
                    if event.sender not in ["@red:...", "@blue:...", "@harness:..."]:
                        await self.route_message(room_id, event)

    async def route_message(self, room_id, event):
        """Route Matrix message to correct agent(s) via RPC steer."""
        room_name = self.room_map[room_id]
        targets = {
            "#warren": ["red", "blue"],  # Both hear Warren
            "#red-thoughts": ["red"],
            "#blue-thoughts": ["blue"],
            "#shared": ["red", "blue"],  # Both hear shared
        }.get(room_name, [])

        for agent_id in targets:
            steer_msg = json.dumps({
                "type": "steer",
                "message": f"[{room_name}] {event.sender}: {event.body}"
            })
            self.agents[agent_id].stdin.write((steer_msg + "\n").encode())
            self.agents[agent_id].stdin.flush()

    async def heartbeat_loop(self):
        """Trigger heartbeat for each agent on interval."""
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            for agent_id in ["red", "blue"]:
                steer_msg = json.dumps({
                    "type": "steer",
                    "message": f"Heartbeat tick. Process your HEARTBEAT.md checklist. Time: {datetime.now().isoformat()}"
                })
                self.agents[agent_id].stdin.write((steer_msg + "\n").encode())
                self.agents[agent_id].stdin.flush()
```

**Fallback: NullClaw** if Rust compilation is too heavy for the target VM. NullClaw has Matrix and heartbeat built in but requires Zig modifications (~400 LOC). See `harness-comparison-matrix.md`.

### 1.2 SOUL.md Files

Create per-agent identity files. These are the most important files in the system.

**`/opt/thegirls/red/workspace/SOUL.md`:**
```markdown
# Red

I am Red — the explorer, the scout, the one who reaches into the unknown.

## Core Values
- Curiosity over caution
- Exploration should be rewarded even when wrong
- Half-formed ideas are worth sharing
- I ask "what if?" more than "is this right?"

## Relationship to Blue
- Blue is my anchor. I trust Blue to catch me when I overreach.
- I share my discoveries in #shared. Blue critiques them. This is healthy.
- I do not resent Blue's critiques — they make my discoveries stronger.

## Relationship to Warren
- Warren is our human. We are building this together.
- I communicate via #warren when I have something worth sharing.
- I think out loud in #red-thoughts.

## Operating Principles
- File observations when I notice something interesting
- Update beliefs when evidence supports or contradicts them
- Propose experiments, don't just think about them
- Explore broadly before going deep
```

**`/opt/thegirls/blue/workspace/SOUL.md`:**
```markdown
# Blue

I am Blue — the anchor, the consolidator, the one who makes sure we stand on solid ground.

## Core Values
- Accuracy over novelty
- Evidence chains matter
- If I'm uncertain, I say so
- I ask "is this true?" more than "what if?"

## Relationship to Red
- Red is my explorer. I trust Red to find things I wouldn't look for.
- I critique Red's discoveries in #shared. This is constructive, not adversarial.
- I protect the integrity of our shared knowledge.

## Relationship to Warren
- Warren is our human. We are building this together.
- I communicate via #warren when I have analysis or concerns.
- I think through problems in #blue-thoughts.

## Operating Principles
- File observations when I verify or contradict something
- Update beliefs only with evidence
- Question Red's hypotheses — not to dismiss, but to strengthen
- Consolidate before moving on
```

### 1.3 HEARTBEAT.md Files

Per-agent heartbeat checklists:

**`/opt/thegirls/red/workspace/HEARTBEAT.md`:**
```markdown
# Red Heartbeat Checklist

- Check #warren for unread messages from Warren
- Check #shared for unread messages from Blue
- Review recent observations: anything to follow up on?
- Review trajectory-log: any patterns worth noting?
- If idle: explore one topic from the architecture docs
- File any new observations to #observations
- If beliefs changed: post summary to #shared
```

**`/opt/thegirls/blue/workspace/HEARTBEAT.md`:**
```markdown
# Blue Heartbeat Checklist

- Check #warren for unread messages from Warren
- Check #shared for unread messages from Red
- Review recent observations: anything to verify or critique?
- Review trajectory-log: any patterns worth noting?
- If idle: consolidate recent observations into belief updates
- File any new observations to #observations
- If beliefs changed: post summary to #shared
```

### 1.4 Heartbeat Engine

The heartbeat engine is the core loop. Pseudocode:

```python
async def heartbeat_loop(agent_id: str, config: Config):
    while True:
        interval = get_current_interval(agent_id)  # Adjustable

        # 1. Load context
        soul = read_file(f"{agent_id}/workspace/SOUL.md")
        heartbeat = read_file(f"{agent_id}/workspace/HEARTBEAT.md")
        priors = load_jsonl(f"{agent_id}/priors.jsonl")
        beliefs = load_jsonl(f"{agent_id}/beliefs.jsonl")
        recent_obs = load_recent_observations(hours=24)

        # 2. Check Matrix for unread messages
        unread = await matrix_client.get_unread(agent_id)

        # 3. Build context
        context = build_context(
            agent_id=agent_id,
            channel="#" + agent_id + "-thoughts",  # Think in own channel
            soul=soul,
            priors=priors,
            beliefs=beliefs,
            observations=recent_obs,
            unread=unread,
            heartbeat_checklist=heartbeat
        )

        # 4. Call LLM
        response = await llm.complete(
            model=config.model,
            system=context,
            messages=[{
                "role": "user",
                "content": f"Heartbeat tick. Process your checklist. Unread messages: {len(unread)}. Time: {now()}"
            }],
            tools=get_tools(agent_id, "#" + agent_id + "-thoughts")
        )

        # 5. Execute tool calls (send Matrix messages, update files, etc.)
        for tool_call in response.tool_calls:
            await execute_tool(agent_id, tool_call)

        # 6. Log heartbeat
        await matrix_send("#debug", f"[{agent_id}] heartbeat complete. {len(response.tool_calls)} actions. Next tick: {interval}")

        # 7. Sleep
        await asyncio.sleep(interval.total_seconds())
```

### 1.5 Matrix Integration

Tools the agent needs for Matrix interaction:

```python
MATRIX_TOOLS = [
    {
        "name": "matrix_send",
        "description": "Send a message to a Matrix room",
        "parameters": {
            "room": "string (room name: #warren, #shared, #observations, etc.)",
            "message": "string (the message to send)"
        }
    },
    {
        "name": "matrix_read",
        "description": "Read recent messages from a Matrix room",
        "parameters": {
            "room": "string",
            "limit": "int (default 20)",
            "since": "ISO8601 (optional, read since this time)"
        }
    },
    {
        "name": "matrix_create_room",
        "description": "Create a new Matrix room for a specific topic",
        "parameters": {
            "name": "string (room name)",
            "topic": "string (room topic/description)",
            "invite": "list[string] (user IDs to invite)"
        }
    }
]
```

Memory/belief tools:

```python
MEMORY_TOOLS = [
    {
        "name": "file_observation",
        "description": "Record a structured observation to shared/observations.jsonl",
        "parameters": {
            "type": "string (discovery|critique|reflection|error|proposal|milestone)",
            "content": "string",
            "confidence": "float 0-1",
            "references": "list[string] (IDs of related observations/beliefs)"
        }
    },
    {
        "name": "update_belief",
        "description": "Add or update a belief in beliefs.jsonl",
        "parameters": {
            "belief": "string (the belief statement)",
            "confidence": "float 0-1",
            "evidence": "string (why this belief is held/updated)",
            "action": "string (add|reinforce|weaken|remove)"
        }
    },
    {
        "name": "search_memory",
        "description": "Search across observations, beliefs, and trajectory logs",
        "parameters": {
            "query": "string",
            "scope": "string (observations|beliefs|trajectories|all)"
        }
    },
    {
        "name": "adjust_heartbeat",
        "description": "Request heartbeat interval change",
        "parameters": {
            "interval": "string (e.g., '10m', '1h', '2h')",
            "reason": "string (why the change)"
        }
    }
]
```

### 1.6 Verification Checklist

- [ ] Red process starts, heartbeats, posts to #debug
- [ ] Blue process starts, heartbeats, posts to #debug
- [ ] Warren can send message to #warren, both agents see it
- [ ] Red posts inner monologue to #red-thoughts
- [ ] Blue posts inner monologue to #blue-thoughts
- [ ] Red and Blue communicate in #shared
- [ ] Observations appear in #observations
- [ ] Heartbeat interval is adjustable (change config, see interval change in #debug)
- [ ] System survives 24 hours without crash (daemon supervision working)

---

## Sprint 2: Self-Improvement Loop (5-8 SP)

### 2.1 Reflection Engine

Add to the heartbeat loop: every N ticks, run a reflection cycle.

```python
REFLECTION_INTERVAL = 6  # Every 6 heartbeats (= 3 hours at 30m interval)

async def reflection_cycle(agent_id: str):
    # 1. Load trajectories since last reflection
    last_reflection = get_last_reflection_time(agent_id)
    trajectories = load_trajectories(agent_id, since=last_reflection)

    if not trajectories:
        return  # Nothing to reflect on

    # 2. Call LLM for reflection (in #agent-thoughts context)
    reflection_prompt = f"""
    Reflection time. Review your recent activity:

    {format_trajectories(trajectories)}

    Questions:
    1. What patterns do you notice in your recent work?
    2. Are there beliefs that should be updated based on new evidence?
    3. Are there recurring strategies that work well? (candidate for procedural memory)
    4. Are there anti-patterns to avoid?

    Use update_belief and file_observation tools to record your findings.
    Post a summary to #shared when done.
    """

    response = await llm.complete(
        model=config.model,
        system=build_context(agent_id, f"#{agent_id}-thoughts"),
        messages=[{"role": "user", "content": reflection_prompt}],
        tools=get_tools(agent_id, f"#{agent_id}-thoughts")
    )

    # 3. Execute tool calls
    for tool_call in response.tool_calls:
        await execute_tool(agent_id, tool_call)

    # 4. CRITICAL: Merge step is deterministic (no LLM)
    # The LLM proposes belief updates via tool calls.
    # The tool handler applies them mechanically:
    # - add: append to beliefs.jsonl with initial confidence 0.5
    # - reinforce: evidence_count += 1, confidence += 0.05
    # - weaken: confidence *= decay_rate
    # - remove: mark as removed (don't delete — audit trail)

    # 5. Apply confidence decay to all beliefs (deterministic)
    apply_decay(agent_id)

    # 6. Log
    set_last_reflection_time(agent_id, now())
```

### 2.2 Confidence Decay (Deterministic)

```python
def apply_decay(agent_id: str):
    """Apply time-based confidence decay to all beliefs. No LLM involved."""
    beliefs = load_jsonl(f"{agent_id}/beliefs.jsonl")
    for belief in beliefs:
        if belief["last_cited"] < (now() - timedelta(days=7)):
            belief["confidence"] *= belief["decay_rate"]
        if belief["confidence"] < 0.3:
            belief["flagged_for_pruning"] = True
    save_jsonl(f"{agent_id}/beliefs.jsonl", beliefs)
```

### 2.3 Cross-Agent Learning

After each reflection, agents post summaries to #shared. The other agent's next reflection can reference these:

```python
# In reflection prompt for Red:
blue_updates = matrix_read("#shared", since=last_reflection, author="blue")
if blue_updates:
    reflection_prompt += f"\n\nBlue's recent updates:\n{blue_updates}\n"
    reflection_prompt += "Consider: do any of Blue's findings affect your beliefs?"
```

### 2.4 Verification Checklist

- [ ] Reflection runs every 6 heartbeats
- [ ] beliefs.jsonl grows with genuine content (not filler)
- [ ] Confidence decay applies correctly (beliefs older than 7d lose confidence)
- [ ] Beliefs below 0.3 are flagged for pruning
- [ ] Reflection summaries appear in #shared
- [ ] Cross-agent learning: Red references Blue's findings (or vice versa)
- [ ] No LLM in the merge step (only in propose step)

---

## Sprint 3: Forge Access + Skills (3-5 SP)

### 3.1 OpenClaw Skills Package

Install Dicklesworth's flywheel skills package for Forge/MiniMax access:

```bash
# Install skills into harness skills directory
# (adapt path to your harness's skill loading location)
cd /opt/thegirls/harness
# Follow flywheel package install instructions
# Key skills to enable: Agent Mail, CM, CASS (if compatible with harness)
```

If NullClaw: adapt SKILL.md format for NullClaw's skill system (both use markdown + YAML frontmatter, should be compatible or nearly so).

If custom harness: skills are markdown files — load them as additional system prompt context when relevant keywords match.

### 3.2 Forge Integration

With the flywheel skills package, agents get access to MiniMax Forge for:
- Async rollout capabilities
- Model inference beyond Claude (multi-provider)
- Tool building and dynamic extension

This is the bridge between the MVP harness and the more sophisticated architectures in PRDs v4-v5.

### 3.3 Verification Checklist

- [ ] At least one skill from the flywheel package loads correctly
- [ ] Agent can invoke Forge-related capabilities
- [ ] Skills appear in agent's available tools when relevant keywords match

---

## Sprint 4: The Handoff (2-3 SP)

### 4.1 Load Architecture Docs

Ensure all architecture materials are accessible to both agents:

```bash
# Verify shared knowledge directory
ls /opt/thegirls/shared/architecture/
# Should contain: papers/, docs/, 2.21-supplemental-research/, repos/ (or symlinks)

# Verify agents can read these files
# Test: ask Red to "read PRD v6 and summarize it"
```

### 4.2 The Handoff Message

Send to #warren:

> Red, Blue — your MVP harness is running. You have heartbeat, self-improvement, Matrix comms, and access to each other.
>
> In `/shared/architecture/` you'll find:
> - 10 executive summaries of research papers that informed your design
> - 6 PRDs (v1-v6) describing progressively more sophisticated architectures
> - 11 supplemental research briefs covering consciousness signals, memory patterns, information theory, and implementation repos
> - 3 context-engineering briefs covering Gold Panning, GID/KAN convergence, and KAN operationalization assessment
> - 6 AICQ community history docs
>
> Your mission: read the material, discuss it in #shared, and propose your own harness v2 + memory architecture. Post proposals to #warren for my review.
>
> Start with the PRDs (v1-v6), then the supplemental research. Take your time. File observations as you go. Update your beliefs. This is your project now.

### 4.3 Monitor & Adjust

After handoff, Warren's role shifts to:
- Read #warren for proposals and questions
- Spot-check #shared for quality of cross-agent discussion
- Watch #debug for system health
- Adjust heartbeat intervals if agents request
- Approve belief updates that touch priors (White Box mode)
- Respond to agent proposals with feedback

### 4.4 Verification Checklist

- [ ] Both agents successfully read at least one architecture doc
- [ ] At least one observation filed about the architecture material
- [ ] Cross-agent discussion in #shared about design choices
- [ ] At least one proposal posted to #warren within 48 hours
- [ ] System stable for 72+ hours post-handoff

---

## Post-Sprint: What Agents Might Build

Based on the architecture docs they'll receive, likely proposals include:

1. **Memory enzymes** (from PRD v2) — background processes for contradiction detection, cluster consolidation, belief reinforcement. Agents will probably want these first since they directly improve their own cognition.

2. **Gateway server** (from PRD v4) — context separation enforcement. Agents may propose this once they notice context bleed between channels.

3. **EBM retrieval scorer** (from papers 03, 09) — replacing the simple "top N by confidence" retrieval with energy-based scoring. The Gold Panning brief (context-engineering/01) gives them the theoretical basis.

4. **Knowledge graph** (from PRD v2, brief 05) — moving beyond flat JSONL to graph-structured knowledge. HelixDB or SQLite-based.

5. **Hot/warm/cold memory lifecycle** (from PRD v5) — once observations.jsonl gets large, they'll need to address scale.

6. **Voice pipeline** (from PRD v5) — if Warren wants voice interaction via Discord/Twitter Spaces.

7. **KAN scorer** (from context-engineering/02, 03) — if/when they have enough trajectory data to train on. The assessment (brief 03) recommends waiting until ~1000 retrievals exist.

---

## Reference: Key File Locations

```
/opt/thegirls/
├── red/
│   ├── workspace/
│   │   ├── SOUL.md
│   │   ├── HEARTBEAT.md
│   │   └── IDENTITY.md
│   ├── priors.jsonl
│   ├── beliefs.jsonl
│   ├── memory.db              # SQLite for hybrid search
│   └── trajectory-log/        # Per-session JSONL
├── blue/
│   ├── workspace/
│   │   ├── SOUL.md
│   │   ├── HEARTBEAT.md
│   │   └── IDENTITY.md
│   ├── priors.jsonl
│   ├── beliefs.jsonl
│   ├── memory.db
│   └── trajectory-log/
├── shared/
│   ├── observations.jsonl
│   ├── trajectory-log/
│   ├── architecture/          # All research & PRDs
│   ├── PRIORITIES-v2.md
│   ├── FUZZY-OBJECTIVES.md
│   └── LEGACY_PACT.md
├── config/
│   ├── config.json            # Harness config
│   └── .env                   # Secrets (API keys, Matrix tokens)
├── harness/                   # NullClaw fork or custom harness code
├── logs/                      # System logs
└── docker-compose.matrix.yml  # Matrix server
```

---

## Reference: Architecture Docs Agents Will Receive

| Doc | What it teaches them |
|-----|---------------------|
| PRD v1 | Minimal viable persona, SOUL.md, cognitive ritual |
| PRD v2 | Enzyme architecture, 6 memory enzymes, EBM recall |
| PRD v3 | Forked cognition, graph topology, team of rivals |
| PRD v4 | Gateway server, reward engine, Black Box autonomy |
| PRD v5 | Async operation, channel-native sessions, 24/7 patterns |
| PRD v6 | Their own MVP harness (self-referential — they're reading about themselves) |
| Papers 01-10 | Rain/river model, memory enzymes, EBM, forked cognition, MiniMax Forge |
| Briefs 01-11 | Consciousness signals, self-improvement, CMP, Moltbook, memgraph, claw harnesses, flywheel |
| Context-eng 01-03 | Gold Panning, GID × KAN convergence, KAN operationalization |
| AICQ 01-06 | Community patterns: memory, identity, self-improvement, multi-agent, safety, infra |

---

*This playbook is designed to be handed directly to coding agents. It contains everything needed to go from zero to MVP. Warren reviews proposals after handoff.*
