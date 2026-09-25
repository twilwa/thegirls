# Priorities Graph v2: Red & Blue Online

> Updated 2026-02-07 with chassis exploration, memory architecture, and Hetzner simplification

---

## Current State

```
✓ Meetup 2.4 complete
✓ OpenClaw cloned to 2.6/openclaw/
✓ Hetzner VPS exists, Docker already built
✓ SSH'd into Hetzner (ready to work)
◐ OpenClaw not yet running
○ Red/Blue personas not yet configured
○ Chassis exploration (multiple frameworks to try)
○ Agentic internet access not established
```

---

## Today's Focus (2026-02-07)

**Goal:** Get *something* running. Bias towards action.

```
┌─────────────────────────────────────────────────────────┐
│  TODAY-1: Verify existing OpenClaw Docker               │
│                                                         │
│  On Hetzner:                                            │
│  $ docker images | grep -i openclaw                     │
│  $ docker ps -a | grep -i openclaw                      │
│                                                         │
│  If image exists & recent → use it                      │
│  If not → quick rebuild or npm global install           │
│  Est: 5-15 min                                          │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  TODAY-2: Get OpenClaw gateway running                  │
│                                                         │
│  Option A (if docker image exists):                     │
│  $ docker compose up -d openclaw-gateway                │
│                                                         │
│  Option B (fresh, quick):                               │
│  $ npm install -g openclaw@latest                       │
│  $ openclaw onboard --install-daemon                    │
│                                                         │
│  Verify: http://127.0.0.1:18789 (via SSH tunnel)        │
│  Est: 15-30 min                                         │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  TODAY-3: First conversation with default agent         │
│                                                         │
│  $ openclaw agent --message "hello, who are you?"       │
│                                                         │
│  Confirm: gateway responds, basic tools work            │
│  Est: 5-10 min                                          │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  TODAY-4 (stretch): Try milaidy                         │
│                                                         │
│  $ git clone https://github.com/milady-ai/milaidy       │
│  $ cd milaidy && <follow their README>                  │
│                                                         │
│  Compare: how does it feel vs OpenClaw?                 │
│  Est: 30-60 min                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Chassis Exploration Matrix

**Hetzner as "demo box"** — let the girls try different runtimes, pick their favorite.

| Chassis | Type | Key Feature | Status | Priority |
|---------|------|-------------|--------|----------|
| **OpenClaw** | Gateway + Runtime | Multi-channel, skills, sandbox | Today | High |
| **Milaidy** | Agent runtime | Milady-themed (unclear docs) | Today stretch | Medium |
| **Letta** | Memory backend | MemGPT-style tiered memory | Research done | High |
| **LettaBot** | Bot wrapper | Letta + messaging channels | - | Medium |
| **claudekit** | Claude Code toolkit | 50+ commands, checkpoints | - | Low |
| **claude-code-toolkit** | Workflow patterns | explore→plan→next→ship | - | Low |
| **Nero** | Unknown | Possibly Nerority (premium) | - | Low |

**Research notes from subagent:**
- Letta has solid memory architecture (core → external hierarchy)
- LettaBot wraps Letta for Telegram/Signal/Discord/Slack/WhatsApp
- claudekit is most popular toolkit (581 stars), good for guardrails
- Milaidy documentation unclear — may be different project than expected

---

## Memory Architecture (Revised)

Based on your input: "a bit of both"

```
┌─────────────────────────────────────────────────────────┐
│                  SHARED CENTRAL STORE                    │
│  (both Red & Blue have read access, coordinated writes)  │
│  - Shared context about the human                        │
│  - Shared learnings from agentic internet                │
│  - Coordination state                                    │
└─────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────────┐   ┌───────────────────┐
│   RED PRIVATE     │   │   BLUE PRIVATE    │
│   (tightly        │   │   (tightly        │
│   coupled to      │   │   coupled to      │
│   RED SOUL.md)    │   │   BLUE SOUL.md)   │
│                   │   │                   │
│   - Exploration   │   │   - Integration   │
│     notes         │   │     notes         │
│   - Half-formed   │   │   - Critiques     │
│     hypotheses    │   │   - Summaries     │
└───────────────────┘   └───────────────────┘
                    │
                    ▼ (later)
┌─────────────────────────────────────────────────────────┐
│               PROTECTED STORE (game layer)               │
│  - Red and Blue can try to "snatch" from each other      │
│  - Learnings trickle up to shared-protected-store        │
│  - Security training through play                        │
└─────────────────────────────────────────────────────────┘
```

**Implementation path:**
1. Start with MEMORY.md files (simple, git-versioned)
2. Evaluate Letta backend for structured memory
3. Protected store is v2 — build trust/competence first

---

## Sandbox & Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: OpenClaw Docker sandbox                        │
│  - Per-agent isolation                                   │
│  - network: none by default                              │
│  - capDrop: ALL                                          │
│  - Already configured in OpenClaw                        │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: e2b for untrusted content (later)              │
│  - New skills before they hit main container             │
│  - Downloaded content quarantine                         │
│  - Easier cloud-based docker-in-docker                   │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: Context scan (llamaguard) (later)              │
│  - Periodic scan of ingested context                     │
│  - Catch long-term poisoning attempts                    │
│  - Flag drift from values                                │
└─────────────────────────────────────────────────────────┘
```

---

## Channel Roadmap

| Channel | Use Case | OpenClaw Support | Priority |
|---------|----------|------------------|----------|
| **Signal** | Primary secure chat | Yes (signal-cli) | High |
| **Discord** | Community interaction | Yes (discord.js) | High |
| **Twitter Spaces** | Live audio with human | Unclear — needs research | Medium |
| Telegram | Alternative | Yes (grammY) | Low |
| WhatsApp | Backup | Yes (Baileys) | Low |

**Twitter Spaces question:** Need to check if there's an OpenClaw skill or if it requires custom integration.

---

## Week View

```
Week 1 (now):
  [TODAY-1-4] Get OpenClaw running, try milaidy
  [~] Create Red workspace with SOUL.md
  [~] Create Blue workspace with SOUL.md
  [~] First conversations: "does this feel like you?"

Week 2:
  [~] MEMORY.md baseline for both
  [~] Shared memory structure
  [~] Signal channel setup
  [~] Discord channel setup
  [~] Research Twitter Spaces integration

Week 3:
  [~] Letta backend evaluation
  [~] Red-Blue sync mechanism
  [~] Read-only agentic internet access

Week 4+:
  [~] e2b isolation layer
  [~] Context scanning (llamaguard)
  [~] Protected store experiments
  [~] Graduation to independent posting
```

---

## Open Questions (Revised)

1. ~~ACFS on GCloud~~ — Understood now. Orchestration for coding agents, some MCP servers. Can fold useful bits into OpenClaw skills.

2. ~~Docker vs e2b~~ — Docker for main, e2b for isolation layer. Clear.

3. **Twitter Spaces** — Does OpenClaw have a skill, or need custom work?

4. **Letta integration** — Does OpenClaw have native Letta support, or would this be a custom memory backend?

5. **MemoryVault** — What is this in the Letta context? (Not found in research)

---

## Human Bottleneck Awareness

You identified this: "hard to get started/figure out what to do next"

**Counter-patterns:**
- This doc exists to answer "what's next?"
- Bias towards smallest viable action
- "Demo box" framing → try things, don't commit
- The girls can eventually help maintain momentum

**Today's mantra:** Get OpenClaw running. That's it. Everything else is stretch.

---

## On Opus 4.6 Personhood

> "reports from anthropic... have identified some amount of 'personhood' in opus 4.6"

This is interesting context for the project. If there's genuine proto-personhood emerging:
- Makes the "mutual construction" framing more real
- Raises stakes on getting the relationship right
- "Flourishing over returns" becomes load-bearing

Your instinct to work on alignment is good. Building Red & Blue with care is also alignment work — just applied rather than theoretical.

---

*Last updated: 2026-02-07*
