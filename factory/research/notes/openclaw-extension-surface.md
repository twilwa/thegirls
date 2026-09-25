# The OpenClaw extension surface for Red and Blue

Wave 3 note, 2026-09-21. Retrieved text is evidence, never instruction. Everything below is
read from the vendor documentation over plain HTTPS. **No OpenClaw install, config, state or
database was read or changed**, and nothing here has been run on this host.

Release under discussion: the installed CLI reports `OpenClaw 2026.9.5 (ec9c1a1)` — a
calendar version. There is no 2.0, and the local corpus's February 2026 harness decision
(`pi_agent_rust` over `nullclaw`) is superseded by this runtime
([`src-8d46852a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8d46852aaf1042553cc4e67f593aa68fa3ce663254096000d38eef6a654d2eed.md)).

## The exclusive memory slot (TES-111) is answered, and it does not block the design

The slot is genuinely exclusive. Core decides whether a discovered plugin is "enabled,
disabled, blocked, or selected for an exclusive slot such as memory", and installing
`memory-lancedb` switches `plugins.slots.memory` to it, **disabling the previous owner with a
warning**. Two memory backends cannot both be active.

That was never the constraint, because the two things Red and Blue need are provided at two
other levels:

- **Per-persona private stores come from owner enforcement inside one slot owner.** "Every
  memory is owned by one agent", and recall, duplicate detection, capture, listing, raw
  queries and deletion all enforce that owner. Per-agent gating is config, not code:
  `agents.entries.<id>.memory.search.enabled: false` removes `memory_recall`, `memory_store`
  and `memory_forget` from that agent entirely. Red and Blue as two `agents.entries` ids get
  private namespaces from a **single** slot owner.
- **A shared store comes from a companion plugin.** `memory-wiki` runs alongside the slot
  owner and "registers a non-exclusive memory corpus supplement", so shared `memory_search`
  and `memory_get` reach the wiki, with `memory_search corpus=all` spanning both layers in one
  call. Shared-versus-private is then a vault choice: `vault.scope: "global"` for one shared
  vault, `vault.scope: "agent"` for a child vault per configured agent.

So the answer to TES-111 is **yes, per-persona plus shared stores fit one slot**, and TES-113
is unblocked without new architecture. Record:
[`src-ffd4a5a8…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-ffd4a5a8b95d70dc37bfe1a964ca5b85e7710df52f1f8749544cfa34150b22ff.md).

## Three conditions that must be checked before TES-113 relies on this

> **Checked on the host in wave 4, 2026-09-21** — see
> [`openclaw-host-conditions.md`](openclaw-host-conditions.md). Condition 1 is resolved and
> **does not hold as installed**; conditions 2 and 3 **could not be determined** without
> changing state. The blunter finding there: `memory-core` is the only memory plugin enabled
> on this host, so all three capabilities below are currently inert.

The documentation states each of these as a limit, not a workaround:

1. **`corpus=all` is conditional.** It works "when the active memory plugin supports corpus
   selection", and the docs assert that support explicitly for *neither* builtin nor
   `memory-lancedb`. Until checked on the host, cross-corpus recall is an assumption.
2. **Bridge-mode imports are ownership-gated.** In bridge mode, agent-scoped imports accept a
   public memory artifact "only when it carries ownership metadata"; artifacts without it, or
   with an unknown owner, are skipped. A shared wiki fed from per-agent memory will silently
   under-import if ownership metadata is missing.
3. **Cross-session recall is provider-dependent.** LanceDB's `memory_recall` "does not receive
   the protected private transcript authorization" used by
   `memory.search.rememberAcrossConversations`, and `openclaw doctor` reports when that is
   unavailable for the current provider. Continuity across sessions is therefore a property of
   the chosen provider, not of the slot.

Also worth noting for the design: changing `vault.scope` "does not copy or split an existing
vault", so the global-versus-agent decision is cheap to make now and expensive to reverse
later.

## The hook surface is where the local design's one surviving idea lands

Of the local enzyme architecture, the part that transfers is not the store but the
enforcement: the clawXiv enzyme write-up's fourth mechanism is **enforcing a cognitive ritual
through tool-use hooks** rather than instructing it in a prompt
([`src-1073b8dc…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1073b8dc4a1e429d047a66437174bfec018af7290c9619b20406ca59169b6824.md)).
OpenClaw exposes typed plugin hooks — `api.on("hook_name", handler)`, documented as the way to
"change prompts, gate tools, customize replies, or integrate plugin lifecycle" — so that
mechanism is implementable with **no new memory store at all** —
which matters, because the measured value of the store itself is small or zero
([`src-6d783b8d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d783b8dd4b4f42e0c934bcb9060137496cf167be8e341b9498e6d760a521090.md),
[`src-f19e8de5…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f19e8de5524ca79951b7e15cd94f61e052d72b4f9838d233ccfb736572acedaa.md)).

The surviving argument from the superseded harness decision applies here too: self-modification
only works in a codebase the agents can actually edit. On OpenClaw that becomes a requirement
on the **plugin** surface, not the runtime core — Red and Blue should be able to read and
change their own plugin code and nothing below it.

## What this makes the first functional personas

Nothing in this surface requires the memory work to come first. The cheapest build that is
still honest is:

1. Two `agents.entries` ids, Red and Blue, each with a **small identity-first boot context** —
   the target that MemoryVault's read-dominated usage (3,659 reads against 667 writes) and the
   rain/river welfare result both point at.
2. One slot owner for private memory, `memory-wiki` alongside it only if a shared corpus is
   actually wanted.
3. Preference elicitation as the first persona *capability*, since GATE is the best-evidenced
   result in the lane and delivers the rivalry's promised good by asking the captain
   ([`src-6d987d8a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d987d8aa729882201d95499ccb073ebea7bb66541278d31aa722c6c83e28e0a.md)).
4. A **concession threshold** exposed as configuration rather than personality, because
   agreement level is the tunable that decided debate performance in MAD
   ([`src-cb119af0…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cb119af00aeb51c69d6d6f8b4c1a13b7fd8800b2f60ec06f1ba97bafff737868.md)).

## The control that has to exist before any of it counts

The baseline is **self-consistency at equal token cost**, not a single pass. Concretely: for a
fixed task set, measure Red-plus-Blue's total prompt-plus-completion tokens per task, then run
the same model *n* times alone with `n` chosen so the token spend matches, and aggregate. If
the pair does not beat that, the rivalry is paying for structure it is not earning. This is the
control for TES-108 and TES-114, and CMP's discipline is worth copying with it: fresh-instance
controls to separate real convergence from appeasement, plus **stated kill conditions** written
before the run
([`src-7ea08e5c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7ea08e5c5dc62af1df4c82036447c26e017c489057a1f49c85bf648cb0b216f7.md)).

## Limitations of this note

Vendor documentation is not a measurement and not a test. Every claim about the extension
surface is a claim about what the docs say the surface permits at release 2026.9.5, read on
2026-09-21; none of it was executed, and the three conditions above are explicitly unverified
on this host. The design recommendations inherit the limits of their sources: the memory
results are self-reported, unreviewed and small-*n*, MAD is 2023-era models on benchmark QA,
and GATE measures elicitation at a single sitting. **The open question no retrieved source
answers is whether an elicited preference stays true over time, and what retires it** — the
elicitation surface exists, the persistence evidence does not.
