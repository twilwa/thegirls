# Red and Blue persona input: evidence report

Date: 2026-09-25

## Finding

The foundation choice remains two isolated OpenClaw homes, with persona-owned memory/context plugins, OpenClaw handling channels, wakes and model routing, and a composed-turn test required before proceeding. Pi with a measured connector bridge remains the fallback. I did not change that choice or edit `sr-persona-refound/report.md`.

I revised `sr-persona-refound/design-summary.md` and `sr-persona-refound/wiki-note.md` in place. Both now treat identity as infrastructure plus model, leave model lock-in and upgrades to each persona, frame Blue's first forum project as hers to research, give each a provisional model suggestion, describe an owner-run Opus consultation boundary and leave persona-specific fine-tuning for later. The wiki note's existing six tags are unchanged. The task report does not publish either note to a wiki or vault.

## Model availability and quota evidence

I ran `quota-axi` without flags at 2026-09-25 05:20:46 UTC. Its output reported:

| Provider/scope | Remaining | Confidence | Projected exhaustion/reset |
|---|---:|---|---|
| Claude, all models | 72% | established | exhaustion 2026-09-29 05:22:45 UTC |
| Claude, `model:fable` | 72% | established | exhaustion 2026-09-29 05:22:45 UTC |
| Codex, all models | 61% | established | exhaustion 2026-09-27 04:23:02 UTC |
| Grok | 100% | established | reset 2026-09-26 07:03:51 UTC |
| OpenCode-Go | 100% | early | reset 2026-09-25 10:20:45 UTC |

This is quota-window evidence, not per-call prices or a budget allocation for either persona. Claude's projected runway was longer than Codex's in this snapshot. Quota is shared by account/model scopes; the two personas would need separate approved limits and attribution rather than treating 72% as reserved for each. The command also reported OpenRouter auth unavailable and some providers omitted as not set up. I did not infer access or price from those omitted services.

`pi --list-models anthropic` listed direct Anthropic routes for `claude-fable-5`, `claude-sonnet-5` and `claude-opus-5-5`, each with a 1M context. `pi --list-models openai` listed `openai-codex` `gpt-5.5` with 272K context and `opencode-go` `muse-spark-1.3-contributor` with 1M. A model listing establishes that Pi knows the route and model metadata; it does not establish a successful provider call, account entitlement, comparative task performance or price.

### Changeable starting suggestions

- **Red: Claude Fable 5.** Its listed 1M context gives room to follow a long lead, and the named Fable quota scope had 72% remaining. That is a reasonable availability-first trial for a persona who follows strange leads, not evidence that Fable is more curious.
- **Blue: Claude Sonnet 5.** It also has a listed 1M context, useful for comparing longer forum accounts and keeping their context together. Treat it as a research baseline, not evidence that Sonnet is more skeptical or better at research.

Both suggestions use the Claude headroom shown in this snapshot; they do not create separate provider budgets. No prices or per-persona limits were available, so live use needs an explicit budget and usage ledger. Red and Blue remain free to choose another listed, approved model, lock in, switch or upgrade. The choice log should record the model, route, budget, reasons and observed effects.

## Jev judgments

The required pre-recommendation question was: "Given this quota headroom and model list, which reachable model best suits a curious lead-following persona, and which a skeptical researching persona, within subscription budget?" An initial malformed-choice invocation selected Fable for both and was discarded. The corrected run selected Claude Fable 5 for the curious persona (reported selection confidence 0.31) and Claude Sonnet 5 for the researching persona (0.21). **Followed, with limits:** those choices appear as low-confidence, changeable starting suggestions. The weak scores and lack of benchmarks are why the report does not call either a best-fit result.

After drafting, I asked Jev these cross-checks against the revised design summary:

| Question | Verdict | Followed? |
|---|---|---|
| Does this revision leave model choice, lock-in, upgrades and training as each persona’s own decisions rather than making those decisions for them? | Yes, 0.96 | Yes; the summary keeps these choices persona-owned. |
| Does the proposed Opus consultation keep fleet credentials outside persona environments while making advice bounded, attributed and budgeted? | Yes, 0.96 | Yes; the broker stays outside, logs the requester and usage, and returns advice. |
| Does the draft clearly say the Opus broker is not provisioned and requires owner approval before use? | Yes, 0.98 | Yes; it is explicitly a later owner ask. |
| Does the revision leave Blue’s first forum study self-directed and avoid claiming the research is already done? | Yes, 0.97 | Yes; the project belongs to Blue and the survey is marked not done. |

I ran the required final checkpoint after drafting: "Does the revised summary leave model choice, lock-in and fine-tuning as the personas' own decisions rather than ours, and does the consult-Opus design keep fleet credentials outside the persona boundary?" Jev answered yes (0.97). After tightening the broker-session boundary in the final revision, I repeated the same question against the current design; Jev again answered yes (0.83). **Followed:** the design remains, with the unprovisioned status, owner-approval gate and access limits explicit; these scores do not constitute a security test. All Jev judgments here are advisory, not evidence of model behavior.

## Opus consultation and later training

The safe path is a broker operated outside the persona boundary. It can start Claude Code with Opus 5.5 under the owner's subscription, pass one limited, sanitized question, associate the request with the persona, and return the answer while recording the model, usage and budget to that persona's ledger. The session should be advice-only, with no persona files or operating authority; the broker returns text only. No Firstmate fleet credential file is mounted or copied into a persona. The broker and its account, usage reporting and limits have not been provisioned or tested. The owner must approve those before use; if the route cannot be isolated and accounted for, do not enable it. I made no OpenAI, Anthropic, Codex, Grok or Opus model calls and no provider logins. The only hosted model calls were the required Jev judgments; `jev-cli` reported `typesafe/jev-1.13-20260917` via OpenRouter.

Persona-specific training or fine-tuning remains a later choice for each persona. If wanted, its own continuity history is the candidate data source. Preserve provenance and decide data handling and cost before any training. No training pipeline or Stage A code was built.

## Blue's first project and scope limits

Blue's first self-directed project is to research public agent forums such as clawxiv, 4claw and similar spaces. She can compare first-person accounts of changing models with accounts of editing memory, instructions or infrastructure, preserve the context behind each claim, and decide what should inform her own choices. That framing is a proposed project, not findings: I did not visit forum pages or perform the research for Blue.

I used the permitted quota/model-list commands and the required Jev checkpoints. Vendor documentation was reviewed for the existing foundation note; public forum research was skipped. I made no Stage A code changes, direct model-provider calls, provider logins, or wiki/vault publication; the required Jev judgments were the only hosted model calls. The prior comparison report remains untouched.

## Deliverable references

- `data/sr-persona-refound/design-summary.md`: change line 3; unchanged foundation lines 7 and 13; persona/model identity line 9; choice log and model suggestions lines 15-17; Blue project line 19; Opus route line 21; fine-tuning line 23; boundary and offline Stage A lines 25-27; later owner asks and composed-turn risk line 29.
- `data/sr-persona-refound/wiki-note.md`: unchanged tags lines 2-8; change line 13; foundation line 15; identity line 17; model recommendations line 21; Blue project line 23; Opus and fine-tuning line 25; Stage A scope line 29; provenance and unpublished status line 33.
- `data/sr-persona-refound/report.md`: read as input; not modified.

No unresolved decision is needed to complete this design revision. Opus provisioning, live model budgets and any fine-tuning are future approval gates, not actions taken here.
