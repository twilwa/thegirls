# Brief 13: Inference Routing Strategy

**Date:** 2026-02-24
**Context:** pi_agent_rust supports custom provider registration via JS extensions. Extension providers take priority over native implementations. No fork needed.

---

## Provider Landscape (Warren's Subscriptions)

| Source | Models Available | Auth Method | Best For | Notes |
|---|---|---|---|---|
| Anthropic Max | Sonnet 4, Opus 4.5, Haiku | ANTHROPIC_API_KEY (or Agent SDK?) | Deep thinking, primary brain | Policy risk for persistent agents — "prefer agent sdk, suspend for running business without API costs" |
| Cursor | Sonnet, GPT-4o, custom models | Cursor session token | Self-improvement coding | Token bucket, resets monthly |
| Windsurf | Sonnet, GPT-4o | Windsurf session token | Self-improvement coding | Token bucket, resets monthly |
| ChatGPT Plus | GPT-4o, o1, o3-mini | OpenAI session/API | Alternative reasoning | May not expose API-style access |
| Gemini Student | Gemini 2.0 Flash, Pro | GOOGLE_API_KEY | Compose guard, heartbeat | Fast, generous free tier |
| OpenRouter Free | Various (rate-limited) | OPENROUTER_API_KEY | Fallback, experimentation | Rate limits, queue delays |
| Modal ($500 credits) | Any model via vLLM/TGI | Modal API | Batch processing, fine-tuning | Best for running own model endpoints |
| z.ai GLM Coding | GLM-4 variants | Z_API_KEY | Alternative coding model | Check API access vs IDE-only |
| Groq (if added) | Llama 3.x, Mixtral | GROQ_API_KEY | Compose guard, fast checks | ~$0.05-0.10/M tokens, very fast |
| Cerebras (if added) | Llama 3.x | CEREBRAS_API_KEY | Heartbeat, fast checks | Fastest inference available |

**Likely unusable for this purpose:** Bolt, Replit, Lovable (IDE-bound, no API extraction). Factory AI (may have API, needs checking).

---

## Inference Profiles

Four distinct workload types, each with different model requirements:

### Profile 1: Deep Thinking (Primary Brain)
- **Where:** #red-thoughts, #blue-thoughts, self-reflection, belief updates
- **Needs:** Frontier reasoning, long context, tool use
- **Ideal:** Sonnet 4 / Opus 4.5 (Anthropic), o3 (OpenAI)
- **Fallback:** GPT-4o, Gemini Pro
- **Volume:** ~60-70% of total inference
- **Token estimate:** ~50-100K tokens/hour per agent at 15-min heartbeat

### Profile 2: Compose Guard Verification
- **Where:** Pre-send hook on matrix_send
- **Needs:** Fast, accurate yes/no grounding check
- **Ideal:** Haiku 4.5, Gemini 2.0 Flash, Groq Llama-3
- **Fallback:** Any fast model
- **Volume:** ~10-15% of total inference (fires on every outgoing message)
- **Token estimate:** ~2-5K tokens per check

### Profile 3: Heartbeat Health
- **Where:** Orchestrator health pings, "anything to surface?" checks
- **Needs:** Fast, minimal, cheap
- **Ideal:** Cerebras, Groq, Gemini Flash
- **Fallback:** Haiku
- **Volume:** ~5-10% of total inference
- **Token estimate:** ~1-2K tokens per ping

### Profile 4: Self-Improvement Coding
- **Where:** When agents modify their own harness, skills, or tools
- **Needs:** Strong code model, tool use, file editing
- **Ideal:** Sonnet 4 (via Cursor/Windsurf tokens), Codex
- **Fallback:** GPT-4o, Gemini Pro
- **Volume:** ~15-20% of total inference (bursty)
- **Token estimate:** Variable, potentially 100K+ for a coding session

---

## Architecture: Pi Extension as Provider Router

### Why Extension, Not LiteLLM Proxy

- **Zero additional infrastructure.** No separate process to run/monitor.
- **In-process routing.** No HTTP hop to a proxy.
- **Profile-aware.** Extension can inspect context (system prompt, tool calls) to determine which profile applies and route accordingly.
- **CAAM-style health tracking.** Mark providers as rate-limited, track cooldowns, auto-failover.

### Extension Design (`provider-router.mjs`)

```javascript
// provider-router.mjs — pi_agent_rust JS extension
// Registers a custom "girls-router" provider that routes to real backends

const PROVIDERS = {
  anthropic: {
    baseUrl: "https://api.anthropic.com",
    apiKeyEnv: "ANTHROPIC_API_KEY",
    api: "anthropic-messages",
    models: { "sonnet-4": true, "opus-4.5": true, "haiku-4.5": true },
    health: { status: "ok", rateLimitedUntil: null, failCount: 0 }
  },
  groq: {
    baseUrl: "https://api.groq.com/openai",
    apiKeyEnv: "GROQ_API_KEY",
    api: "openai-completions",
    models: { "llama-3.3-70b": true, "llama-3.1-8b": true },
    health: { status: "ok", rateLimitedUntil: null, failCount: 0 }
  },
  gemini: {
    baseUrl: "https://generativelanguage.googleapis.com",
    apiKeyEnv: "GOOGLE_API_KEY",
    api: "google",
    models: { "gemini-2.0-flash": true, "gemini-2.0-pro": true },
    health: { status: "ok", rateLimitedUntil: null, failCount: 0 }
  },
  openrouter: {
    baseUrl: "https://openrouter.ai/api",
    apiKeyEnv: "OPENROUTER_API_KEY",
    api: "openai-completions",
    models: { "*": true },  // passthrough
    health: { status: "ok", rateLimitedUntil: null, failCount: 0 }
  }
};

// Profile → provider preference order
const ROUTING_TABLE = {
  "deep-thinking":    ["anthropic/sonnet-4", "anthropic/opus-4.5", "openrouter/anthropic/claude-sonnet-4", "gemini/gemini-2.0-pro"],
  "compose-guard":    ["groq/llama-3.3-70b", "gemini/gemini-2.0-flash", "anthropic/haiku-4.5"],
  "heartbeat":        ["groq/llama-3.1-8b", "gemini/gemini-2.0-flash", "anthropic/haiku-4.5"],
  "self-improvement":  ["anthropic/sonnet-4", "gemini/gemini-2.0-pro", "openrouter/anthropic/claude-sonnet-4"]
};

function classifyProfile(context) {
  // Heuristic: inspect system prompt or recent messages to determine profile
  const sysPrompt = context.systemPrompt || "";
  if (sysPrompt.includes("[COMPOSE-GUARD]")) return "compose-guard";
  if (sysPrompt.includes("[HEARTBEAT]")) return "heartbeat";
  if (context.tools?.some(t => t.name.match(/edit|write|bash/))) return "self-improvement";
  return "deep-thinking";
}

function selectProvider(profile) {
  const candidates = ROUTING_TABLE[profile];
  for (const candidate of candidates) {
    const [providerId, model] = candidate.split("/", 2);
    const provider = PROVIDERS[providerId];
    if (!provider) continue;
    if (provider.health.status === "rate-limited" &&
        Date.now() < provider.health.rateLimitedUntil) continue;
    return { providerId, model, provider };
  }
  // All rate-limited — return first with shortest cooldown
  return { ...candidates[0], forced: true };
}

export default function init(pi) {
  pi.registerProvider("girls-router", {
    id: "girls-router",
    models: [
      { id: "auto", name: "Auto-routed", contextWindow: 200000, maxTokens: 8192 }
    ],
    hasStreamSimple: true,
    streamSimple: async function* (model, context, options) {
      const profile = classifyProfile(context);
      const target = selectProvider(profile);

      // Delegate to actual provider via pi.http()
      // (Implementation depends on target provider's API format)
      // ... streaming delegation logic ...

      // On 429/rate-limit: mark provider, retry with next candidate
      // On success: reset fail count
    }
  });
}
```

### Orchestrator-Level Routing (Alternative/Complement)

The orchestrator can also route at a coarser level via RPC:

```python
# In orchestrator — before sending heartbeat
async def heartbeat_tick(self, agent_id):
    # Switch to cheap model for heartbeat
    await self.rpc_command(agent_id, "set_model", {"model": "groq/llama-3.1-8b"})
    await self.rpc_command(agent_id, "follow_up", {"message": "[HEARTBEAT] ..."})

    # After heartbeat, switch back to primary brain
    await self.rpc_command(agent_id, "set_model", {"model": "anthropic/sonnet-4"})
```

This is simpler than the extension approach but less granular — it switches at the session level, not per-request.

**Recommendation:** Start with orchestrator-level `set_model` switching (simpler, ~20 LOC). Evolve to the extension router when you need per-request granularity or automatic failover.

---

## CAAM Integration

Dicklesworth's CAAM skill handles account-level switching for subscription CLIs. For our use case:

- **What CAAM does well:** Failover on rate limits, cooldown tracking, health scoring across accounts
- **What we'd adapt:** The health tracking pattern, but applied to API keys instead of CLI accounts
- **How it fits:** CAAM could manage the Cursor/Windsurf tokens when the girls are doing self-improvement coding via those tools. The extension router handles the API-level routing.

---

## Cost-Optimization Strategy

### MVP (Week 1-2): Simple Model Switching
- **Primary:** Anthropic Max (Sonnet 4) via direct API key
- **Compose guard:** Gemini Flash (free tier is generous)
- **Heartbeat:** Gemini Flash or Groq free
- **Self-improvement:** Primary (Anthropic)
- **Estimated cost:** ~$0/month additional (all subscription-covered)

### Growth (Month 1-2): Add Routing
- **Primary:** Anthropic Max, failover to OpenRouter
- **Compose guard:** Groq ($10/month plan)
- **Heartbeat:** Cerebras or Groq
- **Self-improvement:** Cursor/Windsurf token buckets for coding, Anthropic for non-coding
- **Estimated cost:** ~$10-20/month additional

### Scale (Month 3+): Full Router
- **Primary:** Rotate Anthropic Max / Cursor / Windsurf for Sonnet
- **Secondary brain:** Modal-hosted open model (Llama 3.x 70B) for overflow
- **Fast inference:** Groq/Cerebras dedicated
- **Estimated cost:** Modal credits draw-down + subscriptions

### Nuclear Option: Self-Hosted on Modal
- Deploy Llama 3.3 70B or Qwen 2.5 72B on Modal ($500 credits)
- Full control, no rate limits, no policy concerns
- Trade: model quality (good but not frontier) for unlimited inference
- Could be the "always available" fallback when all subscription sources are exhausted

---

## Anthropic Max Risk Mitigation

Options in order of preference:

1. **Stay under the radar.** Two agents on 15-min heartbeat is ~8 API calls/hour per agent (heartbeat + occasional thinking). This is well within normal Max usage for an active developer.

2. **Use Agent SDK routing.** If pi_agent_rust can route through Agent SDK (needs verification — the README mentions it but no extension was found in the skills repo), this is explicitly the blessed path.

3. **Distribute across subscriptions.** Heavy thinking on Anthropic, coding on Cursor/Windsurf, fast checks on Groq/Gemini. Reduces per-provider volume.

4. **Switch to API billing.** If the girls generate enough value, pay API costs directly. Sonnet 4 is ~$3/$15 per M tokens (input/output). At 100K tokens/hour, that's ~$1.50-7.50/hour depending on input/output ratio.

5. **Go open-weight primary.** Llama 3.3 70B on Modal as primary brain, Anthropic only for high-stakes reasoning. Trade frontier quality for policy freedom.

---

*Cross-references: Brief 12 (pi_agent_rust harness), PLAYBOOK Sprint 1 (harness setup), PRD v6 §9 (implementation stack)*
