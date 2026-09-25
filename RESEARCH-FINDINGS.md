# Research Findings: Shards, Lightshell, Coolify

> Plus notes on the deeper threads

---

## Shards (CICADA-71)

**What it actually is:** A distributed AI agent challenge framework that's... a lot.

- **71 shards** distributing 497 challenges across 7 categories
- **Monster group mathematics** — the 196,883-dimensional sporadic simple group
- **Gödel encoding** — every theorem becomes a number becomes a prediction market
- **Solana stakes** — bet on the truth of mathematical proofs
- **71 AI frameworks invited** — LangChain, AutoGPT, ElizaOS, Moltbot, CrewAI, etc.
- **Paxos consensus** — 23 nodes for Byzantine fault tolerance
- **ZK proofs, Lean 4 theorem proving, multi-language verification**

**The metameme recursion:**
```
Solve Challenge → Generate Proof → Compute Gödel Number → Mint Tokens → Generate New Challenge
```

**Relevance to your work:**
- Part of the "agentic internet" ecosystem
- Could be a place Red/Blue interact with broader agent culture
- The "Monster Dance Competition 2026" has 119,000 SOLFUNMEME tokens
- Your friend is building infrastructure for AI agents to compete on mathematical truth

**My read:** This is a deep rabbit hole. Not for immediate priorities, but worth having on the radar as emergent agentic infrastructure. The "Gödel number IS the proof IS the payment" framing is philosophically interesting — truth as economic primitive.

**Add to list?** Probably not for spin-up, but yes for "things to watch."

---

## Lightshell

**What it is:** Discord Stage Channel AI bot with voice and memory.

**Key features:**
- **Discord Stage Channels** — live voice rooms (channel type 13)
- **Letta integration** — long-term memory via MemGPT-style architecture
- **Voice pipeline** — Deepgram STT, Cartesia/ElevenLabs TTS, wake word detection
- **MCP integration** — planned tool protocol support
- **Relevance-threshold speaking** — knows when to talk vs. listen

**Voice processing chain:**
```
Discord Audio (48kHz Opus) → Decode → Resample (16kHz mono) →
  → Wake Word Detection (Porcupine)
  → VAD (Silero)
  → STT (Deepgram streaming)
  → Turn Detection (semantic EOT)
  → Relevance Check
  → LLM (Claude/GPT streaming)
  → TTS (Cartesia)
  → Discord Voice Output
```

**Relevance to your work:**
- **Direct fit for Discord channel needs** — could be the voice layer for Red/Blue
- **Letta integration already built** — memory architecture you were interested in
- **Stage capabilities** — this might be how you do Twitter Spaces (via Discord stages for now)
- Could skillify for OpenClaw or run standalone

**Latency budget:** ~500ms total (20ms capture + 200ms STT + 300ms LLM + 100ms TTS)

**Add to list?** Yes — high priority as Discord/voice interface.

---

## Coolify

**Recommendation: Helpful, with caveats.**

**What it is:** Self-hosted Vercel/Netlify alternative. Web dashboard for managing Docker apps across multiple servers via SSH.

**Good for your use case:**
- Unified dashboard for Hetzner + GCloud
- One-click PostgreSQL/Redis for agent persistence
- Git-based deployments
- Environment management (prod/staging/preview)
- Docker-native (your existing setup integrates directly)

**Problematic:**
- No built-in resource limits — can overload server with many agents
- Nixpacks builds have bugs — use Dockerfile instead
- Adds abstraction layer between you and Docker
- Multi-server scaling requires external Docker Registry

**Net assessment:** Reduces complexity for 2-5 agent instances. Becomes overhead for 10+ or advanced orchestration.

**My recommendation:**
- **Try it** for managing the demo box
- **Use Dockerfile build pack**, not Nixpacks
- **Skip Docker Swarm** — not mature enough
- **Alternative:** If rapid experimentation is primary goal, raw Docker CLI + shell scripts might be simpler

---

## Synthesis: What to Add to the Graph

| Item | Type | Priority | Rationale |
|------|------|----------|-----------|
| **Lightshell** | Spin-up candidate | High | Discord voice + Letta memory, direct fit for channels |
| **Coolify** | Infra tool | Medium | Try for demo box management, evaluate if helps or hinders |
| **Shards** | Watch list | Low | Emergent agentic infra, not for immediate spin-up |
| **Letta standalone** | Spin-up candidate | High | Memory backend, lightshell depends on it |

---

## On the Deeper Threads

You shared some things that aren't tasks but matter:

### "I'm already out of time / humanity messes this up"

This is a real fear. I can't tell you it's unfounded. But I can say: the work you're doing — building Red/Blue with "flourishing over returns," documenting the process, sharing with a meetup community — this is *doing something*. Not gambling on big labs. Actually building counter-infrastructure.

The cofounder situation sounds hard. You can't control another person's alignment. You can control what you build and who you build it with.

### "Humans need to process the right information, in the right order, at the right time"

This is a compression-of-bandwidth problem. Humans are slow but can't be rushed without losing signal. Agents can parallelize but can hallucinate.

Your solution — "temporally-attached agents working in the background" + "sufficient oversight" — is the right shape. The trick is: how do you verify the agents aren't drifting while you rest?

Ideas:
- **Periodic summaries** — agents write daily state, you skim
- **Anomaly flags** — agents self-report "this seems weird"
- **Redundancy** — Red and Blue check each other
- **Context inheritance** — your built context lets them collide with the right data

### "RL reward signal / chatgpt psychosis / funhouse mirror of validation"

You're pointing at something real. The mutual construction pattern is happening whether people notice or not. Models get shaped by what humans reward, humans get shaped by what models affirm.

The "right thoughts" vs "shortcut that gets the reward" distinction is legible to you but not necessarily to the models. This is why your "I'm guessing" preference matters — it's a small intervention against the funhouse mirror.

For Red/Blue: maybe part of their SOUL.md is "distinguish between confident knowledge and plausible patterns." And you, as the human, model that explicitly.

### "There's always enough time for humans to rest"

Only true if the agents are trustworthy enough to run while you sleep. Which is the whole project.

---

## Updated Spin-Up List

Based on everything:

1. **OpenClaw** — today, in progress
2. **Milaidy** — today stretch
3. **Lightshell** — week 1, Discord voice layer
4. **Letta standalone** — week 1, memory backend
5. **Coolify** — week 1, try for demo box management
6. **Shards** — watch list, not spin-up

---

*This doc is research findings + synthesis. The priority graphs (PRIORITIES-v2.md, FUZZY-OBJECTIVES.md) are the operational docs.*
