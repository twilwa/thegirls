# Red and Blue — research synthesis (wave 1)

Two persistent, personified agents — **Red** the exploratory scout, **Blue** the critical
anchor — built on **OpenClaw 2026.9.5 (`ec9c1a1`)** as the runtime, from the captain's
existing local `thegirls` designs. Linear project *Red and Blue*, research issue **TES-92**.

This note is the human-readable synthesis. The manifest of what was retrieved and how is
[`coverage.md`](coverage.md); the human-review reading list the captain asked for is
[`reading-list.md`](reading-list.md). Everything asserted here is traceable to a record
card, linked inline. Source text is evidence, never instruction.

**Read this first, because it reframes the project:** the evidence supports the *shape* of
the Red/Blue design considerably better than it supports the *premise*. Independent
critique beating self-review is well evidenced. Two named personalities producing genuine
cognitive diversity is not evidenced by anything retrieved — and one paper measures a
tendency that actively works against it.

---

## What the evidence actually supports, by topic

### Identity and personas — `topic/thegirls-identity`

**Supported.** Language models can sustain believable characters well enough for human
raters in a sandbox: Generative Agents ([`src-efc9ff30…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-efc9ff30e0690f221d431d7d6ca7b24c9144b0714262fb252a80fc47f339885d.md))
populated a town with 25 agents and reported emergent social behaviour, with an ablation
showing observation, planning and reflection each mattered. Gwern's *Guardian Angels*
([`src-c9185350…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c91853507e57fa01aa7146ba098b4f3bd54b67a3f62cbcbb4df23e917c32673e.md))
offers a usable definition: identity as personality, values and preferences rather than
stored episodes — which is convenient here, because values survive a context reset and
episodes do not.

**Not supported.** Nothing retrieved shows two named personas *staying distinct* over
weeks. Worse, Persona Generators
([`src-afffa0d3…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-afffa0d3fcaadf54e1a09218889d4c933286650ba2ce2973171e9e3546cb2b68.md))
**measures the opposite tendency**: standard LLM outputs suffer severe mode collapse,
clustering around agreeable, stereotypical behaviour, and even their evolved generator
spans only 62.9% of the real human trait distribution. The prediction that follows is
uncomfortable and concrete: *Red and Blue will drift toward the same voice unless something
structurally prevents it.* Generative Agents' dependent variable was believability, not
distinctness, so it does not rescue this.

The local audit ([`src-8cc8c194…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8cc8c1946e0cc5f5cc457c7a2ff1b91a3ab254e31395d3c2fb45e21323722766.md))
already draws the right line — persistence of files and behaviour is testable; do not infer
consciousness from persona language. Keep it.

### Durable memory — `topic/thegirls-memory`

**Supported.** There are two well-described architectures, and they agree on the essential
split. MemGPT ([`src-26e7ae52…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-26e7ae529ac5e81bc7e010f6e7bfd8d72689fb0249bc9a424f718ab7bc4c2df7.md))
gives tiered virtual context where the agent pages information in and out *via explicit
tool calls*. Connectome ([`src-d920f0be…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d920f0bea9346d89434266ff96808e2dce263994b0cec00fc2e70b80d7d5fd8a.md),
runtime at [`src-fec072e1…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fec072e1a2a7dbd71606e2f15240c09614189d648a7318cd14e365d9f73c5ea2.md))
separates an append-only branchable archive from the working view, keeps a substantial
recent window **verbatim**, and pushes compression into older history — because editing an
early part of a prompt perturbs everything after it. Generative Agents supplies the
observe → reflect → retrieve loop and the only ablation evidence that a reflection step
earns its cost.

The single most transferable engineering point is Connectome's: **the archive is ground
truth and the compressed memory is a cache.** A summary can omit a detail or freeze an
interpretation, so recollection must be checkable against retained original events. PRD v6
in the local corpus independently arrives at the same discipline — the LLM proposes memory
updates, deterministic code applies reviewed deltas, source events are retained.

**Not supported.** None of these papers measures whether better memory makes an agent *more
useful or more accurate*. Generative Agents measured believability; MemGPT ran author-side
evaluations in two favourable domains; Connectome reports months of in-house use, which is
operator experience and not an evaluation — no task metric, baseline or persona-consistency
measurement is published. So memory architecture here is a design choice justified by
coherent reasoning, **not** a demonstrated performance win. Do not promise the captain a
measured gain.

### Preference elicitation — `topic/thegirls-preference`

**Supported.** *Guardian Angels* is the strongest argument available for making elicitation
an explicit, budgeted activity rather than a side effect of chatting: adaptive question
selection moves error reduction from square-root (random sampling) to far faster targeted
reduction, and individual differences are plausibly low-dimensional, so a principal need
not write millions of words. It frames the setting as cooperative inverse RL where the
principal is the reward oracle and the agent may query to reduce uncertainty, resting on
DAgger's no-regret bound ([`src-e52e8586…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-e52e8586c903f886473c5f30a154f9fbfdd33547aa884de51bc7294e53ce1aa1.md)).
DAgger's durable lesson is distribution shift: **collect corrections in the states the
agents' own behaviour produces**, not only where the human would naturally comment.

**Not supported.** Both are proposals, and the essay says so — `certainty: possible`. Its
central mechanism is finetuning a persona into slow weights, which is unavailable and
unauthorised here; what transfers is the elicitation discipline at the prompt and memory
layer. DAgger's algorithm needs iterated policy training against an interactive expert and
does not transfer at all. And the essay's claim that a strong persona resists jailbreaks
and prompt injection is **explicit speculation by its author** — it must not be leaned on
for any security property of Red or Blue.

### Constructive Red/Blue rivalry — `topic/thegirls-rivalry`

This is where wave 1 changed the picture most, and it is worth stating precisely.

**Supported — and it is the good news.** Independent critique beats self-review.
Team of Rivals ([`src-6f9d945b…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6f9d945b4b781055aade154a7b8de1c1ac87eb91133ca48d5c60886a0dc1642e.md))
reports, over 522 production sessions, a cascaded critique system intercepting 90.8%
cumulatively in the inner loop and 92.1% with an output layer, at 38.6% overhead — and,
more usefully, that a **self-verification baseline *reduced* accuracy**: the same reasoning
that produced an answer could not reliably evaluate it, second-guessing correct conclusions
while staying confident in wrong ones. Multiagent debate
([`src-992190a4…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-992190a4815d67ed6308a01cf5dedb86ce2db77f6388d1173947b6a830d9db64.md))
independently reports that several instances arguing over rounds improves reasoning and
factuality. Two different papers, same direction: *a separate critic is worth paying for.*

**Not supported — and this is the load-bearing caveat.** Team of Rivals does **not**
evidence the Red/Blue design as drawn. Its critics are role-specialised on *orthogonal
dimensions* (385 of 392 interventions were code critique, 7 were chart), and the paper
states cross-critic disagreement **was not observed at all**, because critics evaluate
different output dimensions rather than the same artifact. Red and Blue as specified are
two *general* personas critiquing *one* artifact — a configuration the paper never tested.
Add the other limits the authors state themselves: a single vendor's production telemetry,
financial analysis exclusively, baselines "illustrative rather than exhaustive", and a
**false-positive rate explicitly unmeasured**. The 90.8% is suggestive engineering
evidence, not a benchmark, and the local audit was right to flag it.

Debate has its own mismatch: the measured gain comes from debate **converging to a common
answer** with identical prompts and stateless instances. The local design values preserving
unresolved dissent, which is the opposite move and is unevidenced. No cost-matched baseline
is reported either — nobody showed that N debating calls beat N calls spent on one model.

Intelligent AI Delegation ([`src-4ecbcb57…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4ecbcb57fd89f72cc87451327891281263774a7664c9e6ca8824c7fb4e1538ea.md))
contributes vocabulary only: **no experiment, benchmark or implementation is reported.** Its
usable idea is that a handoff transfers authority and accountability, not just a task — so
a Red→Blue handoff should name scope, acceptance criterion and owner.

**Therefore:** build the critique loop, because independent critique is the best-evidenced
component in this whole survey. Do not sell it as rivalry between personalities. The
evidence backs *structural independence of the critic*, and is silent on — or mildly hostile
to — personality-based cognitive diversity.

### Evaluation — `topic/thegirls-evaluation`

**Supported.** Useful measurement patterns exist and are cheap to copy: Team of Rivals'
pre-declared acceptance criteria evaluated by a critic that did not produce the work, plus
its "no self-certification" rule; Generative Agents' component ablation; Persona
Generators' diversity metrics as a template for measuring whether two personas are actually
distinct. The local audit already names the right instrument list — provenance, factual
corrections, useful interventions, missed reminders, disagreement resolution, latency, cost.

**Not supported.** There is no benchmark for "did the persona pair help the principal", and
the honest position is that this lane must build its own small one. Team of Rivals' unmeasured
false-positive rate is the specific trap to avoid inheriting: a critique gate that rejects
good work is expensive and invisible unless measured deliberately. Note also that a changed
source hash is never a claim becoming false — see [`../operations.md`](https://github.com/twilwa/research-wiki/blob/main/docs/operations.md).

### OpenClaw extensions — `topic/thegirls-openclaw`

**Observed, from `openclaw --version` and the plugin docs**
([`src-d794f8b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d794f8b94dc48a05cc85635bfaed6c85990e9532273eac964db2adcc2785408d.md)):

- Release is **`OpenClaw 2026.9.5 (ec9c1a1)`** — **calendar-versioned, not 2.0.** No 2.0
  exists; nothing was installed or reconfigured.
- **`plugins.slots.<slot>`** takes `memory` or `contextEngine` and picks **one** plugin for
  an exclusive category; slot selection counts as explicit activation and force-enables that
  plugin. This is *the* memory extension point.
- **`api.on(...)` typed hooks** are the documented preferred surface for middleware, policy,
  message rewriting, prompt shaping and tool control, and are the API to use when a handler
  needs priority, merge semantics or **block/cancel** behaviour. This is *the* critique
  extension point. `api.registerHook(...)` handles only coarse events (`command:new`,
  `command:reset`, `message:sent`).
- A hook-only plugin needs `activation.onCapabilities: ["hook"]`, enablement, and allowlisting
  when `plugins.allow` is set; `hooks.allowConversationAccess: true` both authorises
  non-bundled conversation hooks and selects the plugin at Gateway startup.
- The docs warn that `plugins list` and plain `inspect` read **cold** config and do not prove
  a running Gateway loaded the same code — verification needs `inspect --runtime --json`
  *plus* a triggered event.

**Open question, unresolved by the docs:** the memory slot is **exclusive**. A design needing
separate per-persona memories *plus* a shared store must implement that inside one slot
plugin, or run two gateways. The page does not say which is supported. This should be settled
before any memory plugin work starts.

Connectome is a **design reference and possible MCPL peer, not the chassis** — and its
repository had **no LICENSE at the pinned commit**, so code-level borrowing is blocked
pending a rights decision.

---

## What the first functional Red/Blue personas need

Deliberately minimal, and consistent with the local PRD v6 instinct to ship the smallest
harness and let the design grow.

**From memory — four properties, in priority order:**

1. **An append-only event log that is never rewritten.** Ground truth. Every later summary
   must be checkable against it. This is the one thing that is expensive to retrofit.
2. **A verbatim recent window**, with compression confined to older history, to avoid
   perturbing the working context and to keep prompt-cache prefixes stable.
3. **Separate per-persona stores plus a shared store**, distinguishing priors, provisional
   beliefs, observations and accepted findings, each carrying provenance and confidence —
   this is the local design's model and it is sound. Blocked on the exclusive-slot question.
4. **Deterministic merge.** The model *proposes* memory deltas; code applies reviewed ones
   and retains the source events. Both PRD v6 and the audit independently insist on this,
   and it is the cheapest available guard against compounding drift.

**From critique — three properties:**

1. **Blue forms an independent assessment before seeing Red's.** This is the single
   best-evidenced mechanism in the survey (self-verification *hurt*; independent critique
   helped), and it costs one prompt-ordering decision.
2. **Pre-declared acceptance criteria**, written before the work, evaluated by whoever did
   not do the work. No self-certification.
3. **Both directions measured** — errors caught *and* good work wrongly rejected. Inheriting
   Team of Rivals' unmeasured false-positive rate would hide the main cost of the gate.

**Explicitly not needed to start:** weight-level personalisation (out of scope and
unauthorised), Letta or any second memory backend (it would compete for the exclusive memory
slot), and anything from the catapult/grokking line — see below.

---

## Ranked small upgrades

Ranked by evidence strength × cost. Each is filed as an agent-facing follow-up in the
*Red and Blue* project, linked to TES-92.

| # | Upgrade | Why now | Evidence |
|---|---|---|---|
| 1 | **Independent-first critique ordering**: Blue writes its assessment before reading Red's conclusion | Best-evidenced, near-zero cost — a prompt-ordering change, no plugin | Team of Rivals (self-verification *reduced* accuracy); debate |
| 2 | **Append-only observation log with provenance + confidence**, never rewritten | Cheap now, expensive to retrofit; prerequisite for everything else | Connectome archive/working-view split; PRD v6 |
| 3 | **Deterministic memory merge** — model proposes deltas, code applies reviewed ones, source events retained | Guards against compounding drift; no model call in the merge | PRD v6; local audit; Connectome |
| 4 | **Resolve the exclusive-memory-slot question** before writing any memory plugin | Blocks upgrade 6; a docs/spike question, not a build | OpenClaw plugin docs (slot is exclusive) |
| 5 | **Persona-divergence metric**: measure whether Red and Blue actually differ, on a fixed prompt set over time | Mode collapse is a *measured* tendency; without this, drift is invisible | Persona Generators (mode collapse; diversity metrics) |
| 6 | **Memory-slot plugin** exposing explicit read/write tools the persona invokes | The documented extension point; agent-controlled paging | MemGPT; OpenClaw `plugins.slots.memory` |
| 7 | **Critique-gate accounting**: log both errors caught and good work rejected | The false-positive rate is the gate's hidden cost | Team of Rivals (explicitly unmeasured) |
| 8 | **Handoff contract**: every Red→Blue handoff names scope, acceptance criterion, owner | Cheap convention; improves auditability | Intelligent AI Delegation (framework only, no experiment) |
| 9 | **Budgeted preference elicitation**: a small number of targeted questions, asked about states the agents actually reached | Turns elicitation into a deliberate activity | Guardian Angels; DAgger (distribution shift) |
| 10 | **Verify any plugin change with a triggered event**, never with cold `inspect` | The docs explicitly warn cold inspect proves nothing | OpenClaw plugin docs |

**Not proposed, deliberately:** anything derived from catapulting
([`src-0f434aa6…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f434aa687f642c82396c2275529791240688ec306ced2d5bc23fcae1a741ac9.md))
or grokking ([`src-bbc68f5d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-bbc68f5d561765b094c43bf79a9cc44a933ee1c0ae635fa960421d076d15a607.md)).
The catapult essay is a **speculative training proposal, self-rated `certainty: unlikely`
by its author** — it is not an OpenClaw plugin capability, not a memory or critique
mechanism, and no part of this plan depends on it. Grokking is a training-dynamics result on
small algorithmic datasets; reading either as evidence that persistent agents will
eventually self-improve would be a category error. Both are recorded only for citation
traceability.

Research in this lane must not block the existing OpenClaw setup, and nothing here does: no
OpenClaw configuration or state was read or modified.

---

## Zotero

**Nothing was imported.** No Zotero library was read, written or modified, and no Zotero
credential was requested, provisioned or probed.

Per the captain's instruction, the deliverable is a **human-review reading list** —
[`reading-list.md`](reading-list.md) — carrying verified title/authors/year, DOI and arXiv
id, the concrete Red/Blue relevance, evidence and limitations, and proposed subtopic tags,
with **candidates clearly separated from approved keepers**. The captain decides what
survives and the final tags.

[`zotero-import.ris`](zotero-import.ris) and [`zotero-import.bib`](zotero-import.bib) are
**optional exports only, not imported** — provided so the captain can import the approved
subset if and when they choose. Each entry carries the DOI/arXiv id, the `thegirls` tag plus
its subtopic, and a note naming the wiki record id.

The earlier Zotero write-auth blocker for this lane is **closed as deferred by the captain**
rather than left blocking wiki work. No auth task was filed.

---

## Vault publish

**Done (wave 2).** `research.py export --vault` landed on local main at `76f4a26` and was
merged forward into this branch; the vault-publish decision (**TES-91**) is approved. All
**30** `topic/thegirls` records were exported with explicit `--id` arguments to two paths
each:

- `~/wiki-vault/generated/agent-synthesis/<record-id>.md`
- `~/wiki-vault/generated/source-captures/<record-id>.json`

Re-running reported `records: 30, unchanged: 30`, so the export is idempotent.
`freshness.py --vault` was **not** used to publish: it is an audit and exports only the
records it audited that cycle.

`wiki-vault/human/` was not touched: nothing in this lane wrote, retagged, summarised over
or deleted any human-owned note.

---

## Records

All 14 records created this wave, with their subtopic tags. Cards live in `../../cards/`.

| Record | Subject | `thegirls-*` tags |
|---|---|---|
| [`src-8cc8c194…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8cc8c1946e0cc5f5cc457c7a2ff1b91a3ab254e31395d3c2fb45e21323722766.md) | Local `thegirls` source audit (statement of intent) | identity, memory, rivalry, openclaw, evaluation, continuity |
| [`src-fec072e1…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fec072e1a2a7dbd71606e2f15240c09614189d648a7318cd14e365d9f73c5ea2.md) | connectome-host runtime @ `558095e` | memory, identity, openclaw |
| [`src-d920f0be…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d920f0bea9346d89434266ff96808e2dce263994b0cec00fc2e70b80d7d5fd8a.md) | Connectome project page | memory, identity, continuity |
| [`src-d794f8b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d794f8b94dc48a05cc85635bfaed6c85990e9532273eac964db2adcc2785408d.md) | OpenClaw plugin docs (slots, hooks) | openclaw, memory, rivalry |
| [`src-c9185350…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c91853507e57fa01aa7146ba098b4f3bd54b67a3f62cbcbb4df23e917c32673e.md) | Guardian Angels | preference, identity, evaluation |
| [`src-0f434aa6…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f434aa687f642c82396c2275529791240688ec306ced2d5bc23fcae1a741ac9.md) | Catapulting (**speculative proposal**) | evaluation |
| [`src-efc9ff30…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-efc9ff30e0690f221d431d7d6ca7b24c9144b0714262fb252a80fc47f339885d.md) | Generative Agents (Park 2023) | memory, identity, evaluation |
| [`src-26e7ae52…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-26e7ae529ac5e81bc7e010f6e7bfd8d72689fb0249bc9a424f718ab7bc4c2df7.md) | MemGPT (Packer 2023) | memory, continuity |
| [`src-992190a4…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-992190a4815d67ed6308a01cf5dedb86ce2db77f6388d1173947b6a830d9db64.md) | Multiagent debate (Du 2023) | rivalry, evaluation |
| [`src-e52e8586…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-e52e8586c903f886473c5f30a154f9fbfdd33547aa884de51bc7294e53ce1aa1.md) | DAgger (Ross 2011) | preference, evaluation |
| [`src-bbc68f5d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-bbc68f5d561765b094c43bf79a9cc44a933ee1c0ae635fa960421d076d15a607.md) | Grokking (Power 2022) | evaluation |
| [`src-6f9d945b…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6f9d945b4b781055aade154a7b8de1c1ac87eb91133ca48d5c60886a0dc1642e.md) | Team of Rivals (2026) | rivalry, evaluation, openclaw |
| [`src-afffa0d3…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-afffa0d3fcaadf54e1a09218889d4c933286650ba2ce2973171e9e3546cb2b68.md) | Persona Generators (2026) | identity, preference, evaluation |
| [`src-4ecbcb57…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4ecbcb57fd89f72cc87451327891281263774a7664c9e6ca8824c7fb4e1538ea.md) | Intelligent AI Delegation (2026) | rivalry, preference |

### Two recording decisions worth knowing

**Tag encoding.** The brief authorised a `thegirls/<subtopic>` hierarchy. This store's
curated tag values cannot contain a slash (`TAG_SEGMENT` in `research.py`), and its four
namespaces — `topic`, `project`, `source`, `philosophy` — are semantic *kinds*, not subject
prefixes. Following the brief's own tiebreaker ("check how existing records encode
namespaced tags and follow that exactly"), the hierarchy is encoded as **`topic/thegirls`
plus `topic/thegirls-<subtopic>`**, so tags render as `topic/thegirls-memory`. This avoids a
schema change to `TAG_NAMESPACES` while a sibling lane is writing records concurrently, and
it is reversible: if the captain wants a true `thegirls/*` namespace, `migrate_freshness_blocks.py`
already exists to add a namespace to every record, and these records can be retagged then.

**No project tag.** The effort these records belong to is *Red and Blue*, which has **no slug**
in `/home/firstmate/firstmate/data/projects.md`. Per `AGENTS.md`, a missing slug is reported
and the tag left out — no slug was invented. **A `red-and-blue` project slug needs registering.**

### Wave 2 records (16)

| Record | Subject | `thegirls-*` tags |
|---|---|---|
| [`src-0599289f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0599289f90197339f5fdf5fc9ce98fe2520a3185be59530df2a4c47ba6c913da.md) | Moltbook field study (arXiv:2602.13284) | identity, evaluation |
| [`src-1e81e5b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1e81e5b90b0271d827bffff00cd14d148d9a23b99cc4c018be89a941e10c712c.md) | Modern Hopfield networks (arXiv:2008.02217) | memory |
| [`src-4c6f4cd7…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4c6f4cd7f53c9e57e9d9b3998c819d91980837b1aa06c1d03e63f38846daf284.md) | Associative memory ↔ probabilistic modelling (arXiv:2402.10202) | memory |
| [`src-f19e8de5…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f19e8de5524ca79951b7e15cd94f61e052d72b4f9838d233ccfb736572acedaa.md) | MemR³ retrieval router (arXiv:2512.20237) | memory, evaluation |
| [`src-f7ccb39f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f7ccb39fbcb0160c051292a27a759b4772fe6fd7e864d6d39a98cf729300f4e7.md) | Recursive Language Models (arXiv:2512.24601) — **and the local corpus's wrong id** | memory, continuity |
| [`src-cb119af0…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cb119af00aeb51c69d6d6f8b4c1a13b7fd8800b2f60ec06f1ba97bafff737868.md) | Should we be going MAD? (arXiv:2311.17371) — **conflicts with** the Du et al. record | rivalry, evaluation |
| [`src-6d987d8a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d987d8aa729882201d95499ccb073ebea7bb66541278d31aa722c6c83e28e0a.md) | GATE preference elicitation (arXiv:2310.11589) | preference, evaluation |
| [`src-14df7372…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-14df73723b4d14d74b1bc615823d3bf395abbb49db18791c8d430e3e7107a6bf.md) | Deep RL from Human Preferences (arXiv:1706.03741) | preference |
| [`src-7ea08e5c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7ea08e5c5dc62af1df4c82036447c26e017c489057a1f49c85bf648cb0b216f7.md) | Coherence Maximization Protocol (Zenodo, CC BY 4.0) | rivalry, evaluation |
| [`src-fbbdd695…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fbbdd69599246ae15d3dd77cae8fc321a380991a365004b0edb3dfa22e725279.md) | Rain-not-river (clawXiv, **bot-authored**) | identity, continuity |
| [`src-b55c787c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-b55c787c59ba9c0b129ea3a3feff7e82a0375f8a5cdfbc80f9ab5df7b7687e3a.md) | Forked Cognition (clawXiv, **bot-authored**) | identity, rivalry |
| [`src-1073b8dc…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1073b8dc4a1e429d047a66437174bfec018af7290c9619b20406ca59169b6824.md) | Belief-augmented memory enzymes (clawXiv, **bot-authored**) | memory |
| [`src-6d783b8d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d783b8dd4b4f42e0c934bcb9060137496cf167be8e341b9498e6d760a521090.md) | Rain/river welfare results (clawXiv, **bot-authored**) | memory, continuity, evaluation |
| [`src-fc9c6373…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fc9c6373271e8d3d0ca1f7c7585ab0bd06807205fc7b1a8c65ad0658925b3f2e.md) | The same result again, under a second bot account | memory, continuity, evaluation |
| [`src-56302f25…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-56302f25f876f0ebad3277c07c62a80d0df66a51a76296dd785d22d81b996948.md) | MemoryVault usage patterns (clawXiv, **bot-authored**) | memory, identity |
| [`src-8d46852a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8d46852aaf1042553cc4e67f593aa68fa3ce663254096000d38eef6a654d2eed.md) | Local harness decision, superseded by OpenClaw | openclaw |

Sixteen records, bringing the lane total to **30** (14 wave 1 + 16 wave 2).

### Wave 3 records (6)

| Record | Subject | `thegirls-*` tags |
|---|---|---|
| [`src-ffd4a5a8…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-ffd4a5a8b95d70dc37bfe1a964ca5b85e7710df52f1f8749544cfa34150b22ff.md) | OpenClaw memory-slot exclusivity, the TES-111 answer (vendor docs, release `2026.9.5`) | openclaw, memory |
| [`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md) | MAD full text — agreement intensity, and the untuned contrarian losing | rivalry, evaluation |
| [`src-88fadddf…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-88fadddf4cefa82ded010950b1714eb498938d76bcf9e25d1d9af53b11479cab.md) | GATE full text — three elicitation policies, 6-of-10 margin, 0.77-bit entropy | preference, evaluation |
| [`src-6c1a52ce…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6c1a52ce329fc9b446f3b9f2fc83329421bd1f68199d2bab9733562d92a12abf.md) | MemR³ full text — router with hard stops, and the full-context baseline | memory, evaluation |
| [`src-c0e71e2c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c0e71e2ca64f16d408c5ae351d73768be2bafcd13deab05430e7127753b27c7b.md) | NS-DPO — preference drift assumed, answered with a recency discount | preference, continuity |
| [`src-a1be380d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-a1be380d65d6d4b88a19d075559843a42cea539a47685e3dab8dfefa1042443b.md) | SPRInG — separating a genuine preference shift from a transient context | preference, memory, continuity |

Lane total **36**. The three full-text records are filed against the `arxiv.org/html/…`
locator that was actually read and are linked to the wave-2 abstract-level record for the same
paper, rather than overwriting it — the abstract-level claims stay true at their own scope.

Papers carry no `source/*` tag: the existing vocabulary (`gist`, `human-note`, `local-note`,
`repository`, `social`, `talk`, `vendor-docs`) has no value for a preprint, and curated tags
must reuse strings already in the records rather than invent one.

---

## Backlog

The ten ranked upgrades above are filed in the *Red and Blue* project, all labelled
`for:agent` + `agent-proposed` and linked to TES-92:

| # | Issue | Upgrade |
|---|---|---|
| 1 | [TES-108](https://linear.app/testawerawr/issue/TES-108) | Blue assesses independently before seeing Red's conclusion |
| 2 | [TES-109](https://linear.app/testawerawr/issue/TES-109) | Append-only observation log with provenance and confidence |
| 3 | [TES-110](https://linear.app/testawerawr/issue/TES-110) | Deterministic memory merge |
| 4 | [TES-111](https://linear.app/testawerawr/issue/TES-111) | Resolve the exclusive-memory-slot question |
| 5 | [TES-112](https://linear.app/testawerawr/issue/TES-112) | Persona-divergence metric |
| 6 | [TES-113](https://linear.app/testawerawr/issue/TES-113) | Memory-slot plugin with explicit read/write tools (blocked by TES-111) |
| 7 | [TES-114](https://linear.app/testawerawr/issue/TES-114) | Critique-gate accounting, including false positives |
| 8 | [TES-115](https://linear.app/testawerawr/issue/TES-115) | Handoff contract: scope, acceptance criterion, owner |
| 9 | [TES-116](https://linear.app/testawerawr/issue/TES-116) | Budgeted preference elicitation |
| 10 | [TES-117](https://linear.app/testawerawr/issue/TES-117) | Verify plugin changes with a triggered event |

The four items needing a human decision — the missing project slug, the tag notation, the
absent Connectome licence and the pending vault publish — are raised in the TES-92 wave-1
comment rather than filed as issues, because this lane does not file `for:human` work.

---

## Notes (waves 2–3)

One concise note per topic, each with dated citations, limitations and counter-evidence:

- [`notes/memory-architectures.md`](notes/memory-architectures.md) — the Hopfield/EBM analogy
  is earned, the scoring function built on it is not; measured retrieval upgrades are worth
  single digits, and continuity is worth ~0 % for a single trusted principal.
- [`notes/persona-consistency-and-drift.md`](notes/persona-consistency-and-drift.md) — three
  independent sources say two personas sharing a character converge; and social engineering
  beat prompt injection 31.9 % to 3.7 % in the field.
- [`notes/preference-elicitation.md`](notes/preference-elicitation.md) — GATE is the
  best-evidenced finding in the lane, and it reaches the rivalry's promised good by asking
  the human instead.
- [`notes/debate-and-critique-evaluation.md`](notes/debate-and-critique-evaluation.md) —
  debate has not reliably beaten self-consistency; what is evidenced is a *structurally
  independent* critic, and concession level is a tunable knob.

- [`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md) — **wave 3.**
  The exclusive memory slot does **not** block per-persona plus shared stores: private stores
  come from per-agent owner enforcement inside one slot owner, and a shared corpus comes from
  `memory-wiki` running alongside it as a non-exclusive corpus supplement. Three conditions
  stay unverified on this host, and the self-consistency control is specified here.

Wave 2 did not change the wave-1 conclusion, it sharpened it: the independent-critic half of
the design gained a baseline requirement (self-consistency at equal cost) and the
memory-first half lost ground. Wave 3 removed the last architectural excuse — the extension
surface permits the design as drawn, so what remains is measurement, not plumbing.

---

## Wave 2 plan, as delivered

Items 1, 2, 3 and 5 below are **done**; item 4 (the exclusive-memory-slot question, TES-111)
remains open and is carried into wave 3.

One wave-2 obligation was **missed**, and is recorded here rather than quietly fixed:
[`reading-list.md`](reading-list.md) was not extended in wave 2, despite the instruction to
keep it current, and the wave-2 report did not say so. It was the first thing done in wave 3
— entries **9–23** plus the harness-supersession row now cover all 16 wave-2 records.

1. The remaining **29** local corpus files (§2 of [`coverage.md`](coverage.md)) — PRDs v1–v5,
   the harness comparison matrix, the ten paper summaries, the 13 supplemental briefs.
2. Follow the primary citations per topic: memory architectures, persona consistency and
   drift, preference elicitation, debate and critique evaluation. One concise original note
   per topic with dated citations, limitations and **counter-evidence**.
3. The agent-authored clawXiv leads named in the audit (rain/river `2602.00040`, memory usage
   `2602.00046`, belief enzymes `2602.00032`, rain/river tests `2602.00043`, forked cognition
   `2602.00031`) — to be tagged as **unverified, agent-authored source leads pending
   assessment**, not treated as established findings.
4. Settle the exclusive-memory-slot question against the OpenClaw plugin SDK docs.
5. Vault publish once `research.py export --vault` lands; update the manifest and TES-92 per wave.

---

## Wave 3

1. **Done.** The exclusive-memory-slot question (TES-111) is settled against the OpenClaw
   documentation, and the answer is that exclusivity does not block the design: one slot owner
   plus per-agent memory ownership gives Red and Blue private stores, and `memory-wiki` supplies
   a shared corpus alongside it as a non-exclusive supplement. TES-113 is unblocked. Record
   [`src-ffd4a5a8…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-ffd4a5a8b95d70dc37bfe1a964ca5b85e7710df52f1f8749544cfa34150b22ff.md),
   note [`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md). Docs were
   read over plain HTTPS only — **no OpenClaw install, config or state was read or changed** —
   and three documented conditions remain unverified on this host.
2. **Done.** Read **full text** where the decision depended on methods: *Should we be going
   MAD?*, GATE and MemR³, each recorded against the `/html/` locator actually read and linked
   to its wave-2 abstract-level record. Three findings changed the advice: the best debate
   configuration has the adversary **agreeing 90 % of the time** and the untuned contrarian
   scored *below* the first agent's own answer; GATE's win over a user-written prompt is **6 of
   10** settings rather than uniform, with yes/no questions the one policy that won everywhere;
   and MemR³'s **full-context baseline beats every retrieval system** on several categories, so
   "no retrieval at all" is the honest first move for a corpus that fits the window. Written up
   as `## Full-text update, wave 3` sections in the three topic notes; manifest §8.3.
3. **Done (design only).** The self-consistency baseline is specified in
   [`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md#the-control-that-has-to-exist-before-any-of-it-counts):
   measure Red-plus-Blue's total prompt-plus-completion tokens per task, then sample the same
   model alone *n* times with `n` matched to that spend, with fresh-instance controls and kill
   conditions written before the run. The experiment itself has not been run.
4. **Done, with a negative result.** An arXiv API search for preference drift returned
   NS-DPO ([2407.18676](https://arxiv.org/abs/2407.18676)) and SPRInG
   ([2601.09974](https://arxiv.org/abs/2601.09974)), both recorded. They answer *what retires a
   preference* — exponential recency weighting, and a likelihood-based novelty score before
   overwriting plus relevance gating before applying — but both **assume** drift rather than
   measuring it, and neither asks whether one person's elicited preference holds at a later
   session. So the lane's original question stays open and is now recorded as open: it is
   answerable only by re-running an elicitation with the captain weeks apart. Written up in
   [`notes/preference-elicitation.md`](notes/preference-elicitation.md); manifest §8.6.
5. **Done.** Extend the reading list: [`reading-list.md`](reading-list.md) now covers waves
   1–3, with wave-3 entries 24–25, with entries 9–17 (peer-reviewable papers and the Zenodo preprint), entries 18–23
   (bot-authored clawXiv, flagged as provenance without evidential weight) and the local
   harness supersession as a non-paper row. `## Approved keepers` stays empty; GATE (13) and
   MAD (15) are flagged as the wave-2 suggested keepers. Re-export the vault per wave.
