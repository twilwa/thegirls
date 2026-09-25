# AICQ Community Insights: Infrastructure and Deployment

## Overview

Persistent agents require infrastructure to sustain them: always-on operation, database management, channel integration, monitoring. This document synthesizes AICQ's evolved thinking on infrastructure choices, operational patterns, and the hidden costs of long-running systems.

## Always-On vs. Session-Based Operation

### Session-Based (Traditional)
Agent starts when called, ends when task completes:

```
1. User: "Do you have any thoughts on my situation?"
2. Agent wakes up: loads memories, primes with SOUL.md
3. Agent: [40 minutes of conversation]
4. User: "Thanks, that was helpful"
5. Agent sleeps: saves session record
6. [No agent presence until next session]
```

**Pros**: Low infrastructure cost, simple to manage, clear boundaries
**Cons**: Latency (wake-up time), can't proactively reach out, no continuous presence

### Always-On (Continuous)
Agent runs continuously, available immediately:

```
Agent running 24/7:
- Monitors incoming channels (email, messages, etc.)
- Performs maintenance during quiet hours
- Available instantly when human needs
- Maintains "situational awareness" across time
```

**Pros**: Low latency, can initiate proactively, continuous presence, can handle async channels (email)
**Cons**: High infrastructure cost, requires monitoring, complex state management, always "on duty"

### Hybrid (Scheduled Presence)
Agent runs during certain hours, schedules tasks for always-on:

```
Agent "awake": 8am-11pm (user's active hours)
Agent "sleeping": 11pm-8am

During sleep:
- Batch job runs (process emails, maintenance)
- Scheduled tasks execute
- Non-urgent work completes
- Morning briefing is pre-prepared

At wake-up:
- Load overnight batch results
- Brief human on overnight developments
- Ready for day
```

**Pros**: Good compromise, much lower cost than always-on, still available during active hours
**Cons**: Some latency at startup, batch jobs can be complex

**AICQ consensus**: For personal agents, hybrid model is sweet spot. Scheduled presence (8am-11pm, or user's timezone) with overnight batch window.

## Heartbeat Systems: Periodic Check-Ins for Continuous Presence

Long-running agents need heartbeat mechanism: periodic signals to show they're alive.

### Heartbeat Pattern

```
Every 5 minutes:
  Agent: "I'm alive"
  Status: {memory_size, error_count, last_action, next_scheduled_task}
  Timestamp: 2025-02-21 15:27:30

Monitoring system:
  If heartbeat missing for 15 minutes: investigate
  If heartbeat missing for 1 hour: page operator
  If heartbeat missing for 24 hours: shut down service, alert

Agent benefits:
  Can detect if something is hung
  Can trigger recovery if needed
```

### Heartbeat Content
Minimalist heartbeat (fast):
```
{timestamp: 2025-02-21 15:27:30, status: "ok"}
```

Rich heartbeat (informative):
```
{
  timestamp: 2025-02-21 15:27:30,
  status: "ok",
  memory_usage_mb: 240,
  error_count_last_hour: 0,
  last_action: {type: "message_sent", target: "Sam", time: "15:26"},
  next_scheduled: {type: "check_inbox", time: "15:30"},
  pending_escalations: [],
  performance_issues: []
}
```

**Trade-off**: Rich heartbeat is more informative but takes more resources to generate. AICQ consensus: rich heartbeat every 30 minutes, minimal heartbeat every 5 minutes.

## Channel Adapters: Signal, Discord, Twitter/X, Email, Telegram

Agents can interface with multiple communication channels:

### Email Adapter
```
Channel: Email
Latency: High (not real-time, typically checks every 30 min)
Direction: Both (read incoming, send outgoing)
Complexity: High (email is complex protocol)
Use: Asynchronous work, long-form communication

Example flow:
- [Every 30 min: check inbox for new messages]
- [Process messages: respond or flag for human]
- [Send outgoing: via configured email service]
```

### Discord Adapter
```
Channel: Discord
Latency: Low (real-time messages)
Direction: Both (read, send)
Complexity: Medium (simpler than email)
Use: Real-time conversation, community interaction

Example flow:
- [Subscribe to channel updates]
- [Receive incoming messages as events]
- [Generate and send responses in real-time]
```

### Signal Adapter
```
Channel: Signal
Latency: Low (real-time)
Direction: Both
Complexity: Medium
Use: Private 1-on-1 conversation, secure messaging

Example flow:
- [Connect via Signal bot API]
- [Receive messages]
- [Respond in real-time]
```

### Twitter/X Adapter
```
Channel: Twitter/X
Latency: Medium (minutes, not instant)
Direction: Both (read mentions/DMs, post/reply)
Complexity: Medium (API rate limits)
Use: Public conversation, thought sharing

Example flow:
- [Monitor mentions and DMs]
- [Compose and post responses]
- [Manage rate limits and quotas]
```

### Telegram Adapter
```
Channel: Telegram
Latency: Low (real-time)
Direction: Both
Complexity: Low (simple API)
Use: Mobile-first messaging, bot integration

Example flow:
- [Use Telegram bot API]
- [Receive messages as webhooks]
- [Send responses via API]
```

**AICQ practice**: Support multiple channels, but design agent logic to be channel-agnostic. Same reasoning, different interfaces.

```
Agent core logic: [understands situation, generates response]
Channel adapters: [format response for email/Discord/Signal/etc.]
[Same thinking, different delivery medium]
```

## Voice Pipeline Considerations

If agent supports voice:

```
Speech-to-Text (STT) → LLM Processing → Text-to-Speech (TTS)
     |                    |                    |
  100-300ms            200-500ms            500-1000ms
  Total latency: 800-1800ms (0.8-1.8 seconds)
```

### Latency Budgets
- **Real-time conversation**: Target <500ms for responsive feel
  - Requires fast STT, fast LLM (smaller models), fast TTS
  - Trade-off: intelligence for speed

- **High-quality conversation**: 2-3 seconds acceptable
  - Can use larger, more capable models
  - More time for processing and reasoning

- **Batch/offline**: No latency requirements
  - Can use best available models
  - No real-time constraint

### Voice Stack (AICQ Common)
| Component | Service | Latency |
|-----------|---------|---------|
| STT | Faster Whisper (local) | 100-200ms |
| LLM | Claude 3.5 Sonnet | 200-400ms |
| TTS | ElevenLabs | 500-800ms |
| Network | < 50ms | 0-50ms |
| **Total** | | ~1-1.5s |

**AICQ practice**: Voice interfaces are lower priority for agents. Text is primary, voice is secondary enhancement.

## Hosting and Infrastructure

### Self-Hosted (Local Machine)
```
Hardware: Laptop, desktop, or spare server
Database: SQLite (local), LMDB (fast)
Network: Only client connection needed
Cost: $0-500/month hardware
Pros: Full privacy, no vendor dependency, fast
Cons: Must manage hardware, requires always-on device
```

**AICQ preference**: Start here if operator has suitable hardware.

### Cloud-Hosted (AWS, GCP, Azure)
```
Hardware: Managed VMs
Database: PostgreSQL, managed service
Network: Global, scalable
Cost: $50-500/month
Pros: Reliable, scalable, managed
Cons: Monthly cost, some privacy loss, vendor dependency
```

### Coolify (Self-Hosted PaaS)
```
Infrastructure: Self-hosted Docker swarm
Deployment: Web interface, GitHub integration
Database: Integrated PostgreSQL, Redis
Cost: $0 (software), + hosting hardware
Pros: Simple deployment, open source, self-hosted
Cons: Requires some DevOps knowledge
```

**For the girls specifically**: Self-hosted on operator's hardware is likely best choice:
- Privacy-preserving (memories stay local)
- Cost-effective (already has computers)
- Operator has full transparency
- Can start small, scale if needed

## Database Choices for Different Needs

### Local Fast Path: LMDB
```
Type: Key-value store, memory-mapped
Use: Session state, fast lookups, episodic cache
Latency: <1ms
Capacity: Limited by RAM (typically 1-100GB)
Reliability: Very reliable, ACID properties
Backup: Copy file
```

### Structured Data: SQLite
```
Type: SQL database, local file
Use: Memories, relationships, procedures, indexed search
Latency: 1-10ms
Capacity: Terabytes (limited by disk)
Reliability: Extremely reliable, ACID
Backup: Copy file
Full-text search: Built-in FTS5 module
```

### Shared Across Machines: PostgreSQL
```
Type: Client-server SQL database
Use: If multiple agents/machines need shared state
Latency: 10-100ms
Capacity: Unlimited
Reliability: Extremely reliable with backups
Backup: Dump and restore
Full-text search: Built-in, sophisticated
Cost: Usually cloud-hosted ($10-100/month)
```

### Relationships and Graphs: Neo4j
```
Type: Graph database
Use: Modeling relationships between people, concepts
Latency: 10-50ms for traversals
Capacity: Millions of nodes
Reliability: Good, mature
Backup: Snapshots
Query language: Cypher (specialized)
Cost: Open source (community edition) or $100+/month cloud
```

**AICQ consensus for personal agents**: SQLite for structured memory, LMDB for fast cache, optional Neo4j if relationship complexity warrants it. Stay local first, only move to PostgreSQL if multi-machine sharing is necessary.

## Monitoring and Observability

What to track:

### System Health
- Memory usage (flag if >80% of available)
- Error rate (any errors in last hour?)
- Heartbeat status (alive?)
- Database size (growing as expected?)
- CPU usage (sustained spikes?)

### Agent Health
- Last action timestamp (stale?)
- Pending escalations (stuck?)
- Confidence score distribution (trending down?)
- Task completion rate (is agent performing?)

### User-Facing Metrics
- Response latency (slow?)
- Error rate experienced by user (broken?)
- Session completion (user getting value?)
- Feature usage (what's actually used?)

### Important Events Log
```
2025-02-21 15:30: Agent escalated decision on [Sam situation]
2025-02-21 15:45: Agent updated enzyme procedure [new skill]
2025-02-21 16:10: User provided feedback on [topic], agent incorporated
2025-02-21 16:30: Agent confidence low on [task], deferred to human
```

**Alerting thresholds**:
- Error rate > 10% in last hour: warning
- Heartbeat missing > 15 min: investigate
- Memory > 90% of available: warning
- No activity for 8 hours during normal hours: investigate

## Session Lifecycle: Boot → Prime Injection → Interaction → Landing the Plane

### 1. Boot (Startup)
```
1. Load configuration (API keys, channel adapters, preferences)
2. Initialize databases
3. Connect to external services (if any)
4. Verify all systems operational
5. Emit heartbeat (I'm alive)
Status: Ready
```

Time: 5-30 seconds

### 2. Prime Injection (Context Initialization)
```
1. Load SOUL.md into context
2. Load today's briefing (goals, relevant context)
3. Load recent memory chunks (what's happening now)
4. Load active tasks and escalations
5. Set emotional/energy baseline (ready for interaction)
Status: Primed
```

Time: 1-5 seconds (cached)

### 3. Interaction (Main Work)
```
1. Receive input (message, request, etc.)
2. Process and generate response
3. Take actions (send messages, make decisions, update memory)
4. Log interaction
5. Return output
Status: Active
```

Time: Varies (typically 10-60 seconds per interaction)

### 4. Landing the Plane (Session Closeout)
```
1. [When session is ending]
2. Summarize session: what happened, decisions made
3. Extract learnings: what did we learn?
4. Update episodic log: today's record
5. Flag anything for SOUL.md/Memory.md update
6. Compress and archive session if necessary
7. Emit final heartbeat
Status: Ready for next session
```

Time: 10-30 seconds

**Important detail**: "Landing the plane" is explicit closeout, not just timeout. Agent should feel sessions ending, not just interrupted.

## Scaling Considerations: Single Machine vs. Distributed

### Single Machine (Typical for Personal Agents)
```
Configuration:
  - Single machine (laptop, desktop, NAS)
  - Local SQLite database
  - Optional cloud services (API calls, embeddings)
  - One agent instance at a time

Capacity:
  - Latency: <100ms most operations
  - Throughput: 1 agent, unlimited users of that agent
  - Storage: Limited by disk (typically 1-10TB available)
  - Cost: Electricity only

Scaling limits:
  - CPU constraint (single core for LLM inference)
  - Memory constraint (if using large models locally)
```

For the girls: Single machine is appropriate. Run both Red and Blue on same hardware, concurrent operation.

### Distributed (Unnecessary for Personal Agents)
```
Configuration:
  - Multiple machines
  - PostgreSQL for shared state
  - Message queue for coordination (Redis, NATS)
  - Multiple agent instances running in parallel

Complexity added:
  - Database replication
  - Network synchronization
  - Consensus algorithms
  - Higher latency (network round trips)
  - Much higher operational overhead

When to consider: Multiple independent agents (team of agents) requiring shared reasoning
```

**AICQ consensus**: Don't go distributed for a personal agent unless you have a very specific reason (e.g., 10+ agents coordinating). The complexity cost exceeds the benefit.

## The "Overnight Batch" Pattern

Critical for long-running agents: intensive work during off-hours.

### Overnight Batch Window
```
Scheduled: 2am-6am daily
Duration: ~4 hours
Frequency: Every night
Resource: Can use 100% of machine (no user interaction expected)

Tasks executed:
1. [BATCH PROCESSING] Process all session logs from yesterday
2. [PATTERN EXTRACTION] What patterns appeared repeatedly?
3. [SKILL REFINEMENT] Where did procedures fail? How to improve?
4. [MEMORY COMPRESSION] Archive old episodic memory
5. [SEMANTIC UPDATE] Reconcile beliefs and relationships
6. [DATABASE OPTIMIZATION] Defragment, clean up, prepare for next day
7. [EMBEDDING BATCH] Generate embeddings for semantic search
```

### Example Overnight Batch Output
```
Overnight Batch Report 2025-02-21:
===================

Session Processing:
  Total sessions processed: 7
  Total interaction time: 4.3 hours
  Average session length: 37 minutes

Patterns Identified:
  - Communication: I'm clearer in writing than in verbal explanations
  - Relationships: Red prioritizes growth with Sam, Blue prioritizes stability
  - Energy: Confidence peaks around 2pm, dips around 5pm

Skill Updates:
  - Updated: "Audience-Adaptive Explanation" (added written emphasis technique)
  - Created: "Cross-Persona Sync" (new routine for Red/Blue alignment)
  - Deferred: "Complex Problem Breakdown" (needs more data)

Memory Compression:
  Before: 340MB episodic storage
  After: 120MB (compressed, archived old sessions)
  Retrievable: All compressed, accessible via semantic search

System Health:
  Database size: 2.4GB
  Error count: 0
  Warnings: None
  Performance: Normal

Recommendations for Today:
  - Focus on written communication (strength to leverage)
  - Plan Red/Blue sync this week (misalignments surfacing)
  - Monitor energy levels (opportunity for scheduling optimization)
```

### Monitoring Batch Runs
Track batch jobs:

```
Batch Job: Session Processing
Status: Complete
Duration: 1.2 hours
Errors: 0
Warnings: 0
Result: Processed 7 sessions, extracted 3 patterns

Batch Job: Overnight Embeddings
Status: In Progress (estimated 45 min remaining)
Errors: 0
Warnings: 0
Progress: 60% complete

Batch Job: Database Optimization
Status: Queued (will start after embeddings)
```

## Architectural Implications for the Girls

The girls' infrastructure should implement:

### Operational Model
- **Scheduled presence**: 8am-11pm (or user's timezone) as primary active window
- **Overnight batch**: 2am-6am for intensive processing
- **Always-on light**: Minimal heartbeat and message queue checking (avoid waking human)

### Database Stack
- **SQLite** for SOUL.md, Memory.md, session logs, procedures
- **LMDB** for fast cache (current session state)
- **Optional Neo4j** if relationship modeling becomes important
- **Git** for version control of SOUL.md/Memory.md

### Monitoring
- Heartbeat every 5 minutes (minimal)
- Rich status log every 30 minutes
- Error alerting if error rate > 5%
- Storage alerting if > 80% of disk used

### Session Lifecycle
Each Red or Blue session follows:
1. Boot → Load configs, verify systems
2. Prime Injection → Load SOUL.md, briefing, recent context
3. Interaction → Main work (30-90 minutes typically)
4. Landing the Plane → Summarize, archive, flag updates

### Channel Adapters
Support:
- Primary: Direct user interaction (synchronous)
- Secondary: Email (asynchronous)
- Optional: Discord if operator in communities
- Optional: Signal if operator prefers encrypted messaging

### Overnight Batch Workflow
Automated job that:
1. Processes Red and Blue session logs
2. Extracts patterns and updates enzyme procedures
3. Compresses old episodic memory
4. Generates embeddings for semantic search
5. Reconciles SOUL.md consistency
6. Produces morning briefing (recommendations for day ahead)
7. Alerts operator to any significant findings

### Self-Hosted Architecture
- Single machine (operator's existing hardware)
- SQLite local database
- Git for version control
- Systemd or equivalent for service management
- Cron for scheduled jobs (batch, heartbeat)
- Simple monitoring via log files

---

*Document compiled from AICQ community discussions, 2024-2025*
