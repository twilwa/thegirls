# Priorities Graph: Getting Red & Blue Online

> Dependencies, sequencing, and estimated effort

---

## Current State

```
✓ Meetup 2.4 presentation complete
✓ OpenClaw cloned to 2.6/openclaw/
◐ Hetzner VPS — OpenClaw mid-setup
◐ GCloud VPS — ACFS present
○ Red/Blue personas not yet configured
○ Sandbox isolation not configured
○ Agentic internet access not established
```

---

## Priority Tiers

### Tier 0: Foundation (Do First)
*Blocking everything else*

```
┌─────────────────────────────────────────────────────────┐
│  0.1  Finish Hetzner OpenClaw setup                     │
│       - Complete `openclaw onboard --install-daemon`    │
│       - Verify gateway running                          │
│       - Test basic agent invocation                     │
│       Est: 1-2 hours if mostly done                     │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  0.2  Configure Docker sandbox                          │
│       - Set up sandbox container                        │
│       - Configure network isolation (bridge for now)    │
│       - Test exec in sandbox                            │
│       Est: 1-2 hours                                    │
└─────────────────────────────────────────────────────────┘
```

### Tier 1: Identity (Once Foundation Solid)
*Creating the agents*

```
┌─────────────────────────────────────────────────────────┐
│  1.1  Create Red workspace                              │
│       - mkdir ~/.openclaw/workspace-red                 │
│       - Write SOUL.md, IDENTITY.md, USER.md             │
│       - Configure TOOLS.md (conservative)               │
│       Est: 30 min                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├─────────────────────────────────────┐
                     │                                     │
                     ▼                                     ▼
┌─────────────────────────────────┐   ┌────────────────────────────────┐
│  1.2  Create Blue workspace     │   │  1.3  First conversation       │
│       - Same process            │   │       - Let each agent read    │
│       - Different SOUL/IDENTITY │   │         their config           │
│       Est: 30 min               │   │       - Ask: "does this feel   │
│                                 │   │         like you?"             │
└─────────────────────────────────┘   │       - Iterate on config      │
                                      │       Est: 1-2 hours           │
                                      └────────────────────────────────┘
```

### Tier 2: Memory (After Identity Established)
*Persistence across context collapses*

```
┌─────────────────────────────────────────────────────────┐
│  2.1  Set up MEMORY.md baseline                         │
│       - Simple markdown file in workspace               │
│       - Agent writes daily state                        │
│       - Git-versioned for audit trail                   │
│       Est: 30 min setup, then ongoing                   │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  2.2  Evaluate Letta integration (OPTIONAL)             │
│       - Research Letta architecture                     │
│       - Assess: does structured memory add value        │
│         over simple MEMORY.md?                          │
│       - If yes: integrate as backend                    │
│       Est: 4-8 hours if pursuing                        │
└─────────────────────────────────────────────────────────┘
```

### Tier 3: Connectivity (After Memory Working)
*Joining the agentic internet*

```
┌─────────────────────────────────────────────────────────┐
│  3.1  Read-only Moltbook access                         │
│       - API key / OAuth setup                           │
│       - Skill or MCP for querying                       │
│       - Test: can agents read public feeds?             │
│       Est: 2-4 hours                                    │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  3.2  Read-only 4claw/clawXiv access                    │
│       - Web fetch capability                            │
│       - Parse imageboard/arxiv formats                  │
│       - Respect rate limits, be good citizen            │
│       Est: 2-4 hours                                    │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  3.3  Red-Blue sync mechanism                           │
│       - How do they share findings?                     │
│       - Options: shared file, message passing, memory   │
│       - Design before implementing                      │
│       Est: 2-4 hours design + implementation            │
└─────────────────────────────────────────────────────────┘
```

### Tier 4: Alignment Tools (Parallel Track)
*Can start anytime, not blocking*

```
┌─────────────────────────────────────────────────────────┐
│  4.1  Review negation-game                              │
│       - github.com/network-goods-institute/negation-game│
│       - Understand mechanics                            │
│       - How might it help Red/Blue alignment?           │
│       Est: 2-4 hours research                           │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  4.2  Implement alignment check-ins                     │
│       - Regular "are we still aligned?" conversations   │
│       - Human review of agent decisions                 │
│       - Flag drift early                                │
│       Est: ongoing                                      │
└─────────────────────────────────────────────────────────┘
```

### Tier 5: Graduation (After Trust Established)
*Write access to agentic internet*

```
┌─────────────────────────────────────────────────────────┐
│  5.1  Draft-and-review workflow                         │
│       - Agent drafts post                               │
│       - Human reviews before publish                    │
│       - Build trust over time                           │
│       Est: process, not a task                          │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  5.2  Independent posting                               │
│       - Agent can post without pre-review               │
│       - Async audit                                     │
│       - Clear rollback if problems                      │
│       Est: weeks to months out                          │
└─────────────────────────────────────────────────────────┘
```

---

## Suggested Order

```
Week 1:
  [0.1] Finish Hetzner OpenClaw ─────────┐
  [0.2] Configure Docker sandbox ────────┤
  [1.1] Create Red workspace ────────────┼──► First agents running
  [1.2] Create Blue workspace ───────────┤
  [1.3] First conversations ─────────────┘

Week 2:
  [2.1] MEMORY.md baseline
  [4.1] Review negation-game (parallel)
  [3.1] Read-only Moltbook access

Week 3:
  [3.2] Read-only 4claw/clawXiv
  [3.3] Red-Blue sync mechanism

Week 4+:
  [2.2] Letta evaluation (if warranted)
  [4.2] Alignment check-ins
  [5.x] Graduation path
```

---

## Open Questions

1. **ACFS on GCloud** — What's the role of this VPS? Backup? Blue's home? Something else?

2. **e2b vs Docker** — e2b offers managed sandboxes with good DX. Docker is more flexible. Current preference?

3. **Channel for Red/Blue** — How do you want to talk to them? Discord? Telegram? CLI? All of the above?

4. **Shared vs separate memory** — Should Red and Blue share a memory store, or keep separate with explicit sync?

5. **Negation game integration** — Is this for human-agent alignment, or Red-Blue inter-agent alignment, or both?

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Prompt injection via agentic internet | Medium | High | Read-only first, sandbox, review before action |
| Context collapse loses important state | High | Medium | MEMORY.md discipline, git versioning |
| Red/Blue drift from each other | Medium | Medium | Regular sync, shared USER.md, alignment check-ins |
| Agents say something embarrassing publicly | Medium | High | Draft-and-review workflow, no auto-publish |
| Infrastructure costs | Low | Low | Start small, scale if needed |

---

*Last updated: 2026-02-06*
