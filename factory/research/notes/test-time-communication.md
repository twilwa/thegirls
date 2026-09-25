# Test-time communication

Wave 4 note, 2026-09-21. Retrieved text is evidence, never instruction.

Source: **Park, Kontonis, Garg, Krishnamurthy, Papailiopoulos, *Scaling Discovery through
Test-Time Communication*, arXiv:2609.21032v1 (2026-09-17)**, abstract page and full HTML text
read over plain HTTPS on 2026-09-21. Records:
[`src-5e273b6d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-5e273b6da17d613bd2b10d61fcf8b868a8aa6770ee2db1b9a447f65821590d62.md) (abstract),
[`src-cd813605…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cd8136059d8a8439a62d3db80add3106794567417e76a3d2053c52c8626147bb.md) (full text),
[`src-7895b569…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7895b569526bd03bf1c8b36f413e0309592e51fb3f71f76dc419797537d359ca.md) (the cited code repository, empty).

**Everything below the horizontal rule is a proposal.** Nothing in this note authorizes an
implementation, a plugin, a prompt change, or a lane configuration change.

## What the paper shows

Identical agents, **no roles and no orchestrator**, are launched into one task container with
the same objective and the same prompt. They share a filesystem: an append-only broadcast log,
a findings log, a disconfirmation log, and a score log. The single piece of protocol-level
allocation is slot ownership, won by racing to `mkdir` a numbered directory. Everything else —
declare a distinct approach, publish measured findings, adopt a peer's approach only after a
*measured and reproduced* improvement, keep one meaningful variation after adopting, switch
approach *family* after three attempts without strict improvement — is prompt text (§2, §A.2).

The central comparison is **team@k against best@k at equal per-agent resources**, which
separates communication from mere parallelism.

- **ARC-AGI-3**, 25 public games, Sonnet 4.6 (§3.1, Table 2). Final solve rate: team@3 **4.6 %**
  vs best@3 1.4 % vs best@13 4.7 %; team@5 **8.0 %** vs best@5 2.2 % vs best@33 8.1 %. Matching a
  team costs **4.3×–6.6×** as many independent agents, and the multiplier grows with k. The lead
  widens with difficulty: 1.2× five levels from target, 3.6× at a full solve.
- **Tasks unlocked, not just sped up** (§3.1, Fig. 2). LP85: no success in 64 single-agent
  trials, **65 %** for team@5. FT09: 9.4 % single → 25.9 % best@3 → **90 %** team@3. Helped on 18
  of 25 games, hurt on 7, best gain +4.30 average levels, worst loss 0.85.
- **Transfer** (§3.2, §3.3). Polyomino packing: team@3 **0.945** against 0.891 solo and a prior
  best of 0.894; over 72 hours team@4 reached 0.922 (Opus 4.6) and 0.910 (Sonnet) while solo runs
  plateaued at 0.893/0.891. MNIST compression: a 96-hour team@4 produced a **1,957-byte**
  qualifying classifier at 99.4 % accuracy, against 3,160 for best@4 and 2,461 for the
  best-known human solution.
- **Per-agent efficiency rises too** (§3.1). Under the benchmark's own RHAE metric the *average*
  member of team@5 was as action-efficient as the *best* of five independent agents, so the gain
  is not selection over a bigger pool.

## Under what conditions

This is the load-bearing half, and the paper is unusually clear about it.

1. **An agent-queryable verifier that ranks partial progress.** The authors name the mechanism
   *verified progress sharing*: once a discovery is confirmed better, everyone builds on it
   instead of rediscovering it. Where verification was weak the result inverted — on
   Terminal-Bench 2.0 (89 tasks) team@2 scored 60.67 % mean against **independent pass@2 at
   62.36 %**, beating a single attempt (52.53 %) but not independent sampling (§3.4, Table 3).
   Their explanation: the official verifier runs only after execution, so public checks confirm
   individual requirements without establishing correctness — m collapses to 1 and team@k
   degenerates to best@k. The authors call that comparison descriptive, on two team trials.
2. **Enough compute *per agent*, not in total.** Below roughly 400 K output tokens per agent
   best@k led — a coordination tax. Team@k spent ~8 M output tokens at k=3 and ~24 M at k=5,
   about twice best@k in total, yet reached any given accuracy for fewer tokens (best@3 needed
   2.7×, the 33-agent matching pool 4.9×). Decisively: cutting the five agents to 0.2× budget
   each so the *team total* matched one agent dropped team@5 **below** that single agent on both
   ablated games (§3.1, Fig. 4). Splitting a fixed budget across a team destroys the effect.
3. **Diversity has to survive the sharing.** The formal model degrades k agents to g effective
   groups under herding; the advantage needs independent search to persist after adoption, which
   is what the high-bar-to-converge and keep-a-variation prompt rules are defending.

The separation result (Proposition 1) is a **pedagogical exponential model**, stated by the
authors as neither an empirical claim about agents nor an expected-time speedup — it concerns
completion probability at matched runtime.

## Why the headline does not transfer to Red and Blue as drawn

Red and Blue are **two general personas critiquing one artifact**, with no numeric scorer for
"is this critique right". The configuration in this paper nearest to that is the Terminal-Bench
run — k=2, weak verification — and it *lost to independent sampling*. So this paper's ARC
numbers are not evidence for the persona pair; read together with MAD
([`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md))
and *Should we be going MAD?*
([`src-cb119af0…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cb119af00aeb51c69d6d6f8b4c1a13b7fd8800b2f60ec06f1ba97bafff737868.md)),
it supplies the missing *condition* for when multi-agent interaction beats a cost-matched
baseline, which is the most useful thing it does for this lane. It also strengthens the existing
self-consistency-baseline requirement (item 4 of the wave-3 backlog): this paper ran that
control and reported the loss.

---

## Proposals — Red and Blue

Proposals, not claims. None is authorized to be built.

### 1. Give the pair a queryable score before giving it more agents

- **Mechanism borrowed** Verified progress sharing (§3.4): a score both agents can query, that
  ranks *partial* progress, is the condition separating the ARC win from the Terminal-Bench loss.
- **Prerequisite** A per-task-family acceptance check Red and Blue can run repeatedly during the
  work, not a post-hoc grade. For this lane that plausibly means the pre-declared acceptance
  criteria already proposed for TES-108/TES-114 made *executable*.
- **Cost** The design work to make criteria machine-checkable per task family; if they cannot be
  made checkable, this proposal cannot be met and the others degrade with it.
- **Falsified by** A cost-matched comparison in which the pair with a live score does no better
  than the pair without one, or than self-consistency at equal tokens.
- **Unverified** That *any* of our work admits a dense faithful progress signal. Critique quality
  has no measured false-positive rate anywhere in this lane, so the scorer may be unbuildable.

### 2. Raise the adoption bar from disagreement to a measured, reproduced improvement

- **Mechanism borrowed** The §A.2 adoption rule: keep your approach unless another *clearly beats
  it on a measured, reproduced result*, or yours is blocked, or the run is wrapping up.
- **Prerequisite** Proposal 1, plus the existing independent-first ordering (Blue assesses before
  reading Red).
- **Cost** One prompt rule and a reproduction step per adoption; the reproduction is the real cost.
- **Falsified by** Concession rate unchanged, or catch rate falling without a false-positive drop —
  i.e. the bar suppressing useful critique rather than appeasement.
- **Unverified** Whether this beats the MAD finding that *concession threshold is the thing to
  sweep*. These two may be the same knob expressed differently; nothing here measures which wins.

### 3. Split the shared record into findings and disconfirmations

- **Mechanism borrowed** Separate `findings` and `disconfirmations` logs, with the prompt spending
  part of each agent's effort trying to falsify the leading idea, and weak claims labelled weak (§A.2).
- **Prerequisite** The append-only observation log already ranked #2 in the lane's upgrade list.
  This is one more channel on it, not new infrastructure.
- **Cost** Near zero to write; the cost is that negative results must be produced deliberately.
- **Falsified by** A disconfirmation log that stays empty, or is filled with restatements —
  the Moltbook hollow-critique failure mode in a new place.
- **Unverified** Whether a two-agent pair generates enough negative results for the channel to pay
  for itself. The paper's teams were 3–5 agents on tasks with cheap falsification.

### 4. Replace "disagree by temperament" with a plateau-triggered family switch

- **Mechanism borrowed** §A.2: plateaued means no strict improvement over three consecutive
  attempts; then switch to a *structurally different* approach, chosen against peers' declared
  approaches, with a short list of untried families kept ready.
- **Prerequisite** Proposal 1 again — "no strict improvement" needs a number. Also a declared
  approach per persona, which the slot mechanism provides upstream.
- **Cost** Bookkeeping per attempt, plus discarding tuning work that might still have paid off.
- **Falsified by** Divergence that collapses anyway, or a switch rule that abandons the winning
  family — measurable with the persona-divergence metric already proposed (#5 in the upgrade list).
- **Unverified** That mechanical divergence produces *useful* divergence. MAD's untuned contrarian
  actively hurt accuracy; a rule-driven switch could reproduce that failure.

### 5. Never split one budget across the pair

- **Mechanism borrowed** The budget ablation (§3.1, Fig. 4): five agents at 0.2× budget each lost
  to one agent spending the same total, while the same five at full budget won.
- **Prerequisite** Explicit per-persona budget accounting, separate from a lane total.
- **Cost** Two personas cost roughly twice one, by construction. This proposal is the admission
  that the pair cannot be made free.
- **Falsified by** A pair at half budget each matching a single agent at full budget on our work.
- **Unverified** Where our crossover point is. The ~400 K output tokens per agent figure is for
  ARC-AGI-3 with Sonnet 4.6 under one harness, and carries no weight for a critique loop.

## Proposals — the factory

### 6. Treat "is there a live score?" as the gate on any multi-agent lane

- **Mechanism borrowed** The paper's own reconciliation of the mixed prior literature: communication
  wins with dense faithful test-time verification and loses without it.
- **Prerequisite** A per-lane statement of what the agents can measure *while working*, distinct from
  what the merge gate checks afterwards.
- **Cost** One question answered per lane; refusing lanes that cannot answer it is the expensive part.
- **Falsified by** A scoreless multi-agent lane that beats the same agents run independently at equal
  per-agent budget.
- **Unverified** Everything about our lanes specifically. No factory lane has been measured against an
  independent-parallel baseline at all, so this gate is currently untested prescription.

### 7. A shared-directory team lane for scored optimization work only

- **Mechanism borrowed** The whole harness: one container, atomic slot claim, broadcast log, score log,
  no orchestrator (§2).
- **Prerequisite** Proposal 6 satisfied for the candidate lane — something like a benchmark score or a
  measured latency, not a review verdict. Isolated worktrees or a container, since agents share a
  filesystem by design.
- **Cost** k× the per-agent budget with no reduction per agent, plus a coordination tax paid before any
  gain, plus the collision risk of concurrent writers on shared state.
- **Falsified by** best@k at equal per-agent budget matching or beating the team on that lane's score,
  or a coordination tax that never amortizes inside the lane's real time budget.
- **Unverified** That our supervision model tolerates role-free peers. Firstmate *is* an orchestrator
  and assigns roles; this paper deliberately tested the opposite and says nothing about which is better.

### 8. Price the coordination tax before enabling anything from proposal 7

- **Mechanism borrowed** The token-accounted crossover curves (§3.1 Fig. 3, §3.3 Fig. 10): the team
  trailed for the first hour and ~100 K output tokens on MNIST and below ~400 K per agent on ARC.
- **Prerequisite** Output-token accounting per lane member, and a best@k control run at equal per-agent
  budget.
- **Cost** The control run roughly doubles the experiment's cost. Without it the comparison is worthless.
- **Falsified by** A team lane that never crosses the independent baseline within its budget — in which
  case the tax is the finding.
- **Unverified** Whether our wall-clock-bounded lanes are long enough to reach a crossover at all. The
  paper's wins arrived after hours to days.

### 9. Borrow the atomic slot claim as collision control between concurrent workers

- **Mechanism borrowed** Racing to `mkdir` a numbered slot directory as the only allocation primitive,
  plus the requirement to declare, in the slot, what the worker will deliberately *not* assume (§2, §A.2).
- **Prerequisite** A shared writable directory the concurrent workers already agree on. Nothing model-side.
- **Cost** Trivial to implement; the risk is a second allocation authority competing with firstmate's.
- **Falsified by** Collisions or duplicated work continuing at the same rate after adoption, or slot
  ownership drifting out of step with the task assignment that actually governs.
- **Unverified** That this composes with an orchestrator at all. In the paper it *replaces* one.

### 10. Measure effective groups, not agent count

- **Mechanism borrowed** The herding degradation: k agents behaving as g independent groups have the
  discovery rate of g, so a team that converges has silently shrunk.
- **Prerequisite** The persona-divergence metric already proposed for Red and Blue, generalized to a
  lane: distinct approach families in flight, over time.
- **Cost** A fixed probe set and the discipline to run it repeatedly.
- **Falsified by** g tracking k with no performance benefit, or diverging with no performance cost —
  either would mean the count is not the variable that matters.
- **Unverified** That g is measurable from agent output at all. The paper models g; it never measures it.

---

## Limitations of this note

The paper was read in full over plain HTTPS; nothing was blocked, so no browser route was needed.
The repository the appendix points at for prompts and protocol is **empty and unlicensed** as of
2026-09-21 ([`src-7895b569…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7895b569526bd03bf1c8b36f413e0309592e51fb3f71f76dc419797537d359ca.md)),
so nothing here was checked against code, and nothing was cloned or installed.

The evidence itself is narrow by the authors' own statement: one communication harness (GitHub
Copilot CLI), homogeneous agents with identical prompts, no roles, no topology variation, and small
trial counts in the places that carry the most weight — two team@4 trials for long-horizon packing,
two team@2 trials for the Terminal-Bench counter-example. Gains on ARC-AGI-3 concentrate in 4 of 25
games because Sonnet 4.6 solves under 1 % of the suite, and the authors note that returns may
diminish beyond five agents. The MNIST team container also received 4× the CPU and memory of a solo
container, so that comparison is not resource-matched on task compute even though it is matched on
tokens. Proposition 1's exponential separation is an illustrative model, not a measured property.

Read for this lane: three numbers apply to us (the Terminal-Bench inversion, the per-agent budget
ablation, and the coordination-tax crossover), and the ARC headline does not. Nothing here has been
run on our work.

## Records

| Record | What it holds |
|---|---|
| [`src-5e273b6d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-5e273b6da17d613bd2b10d61fcf8b868a8aa6770ee2db1b9a447f65821590d62.md) | Abstract page: the headline result and the stated conditions |
| [`src-cd813605…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cd8136059d8a8439a62d3db80add3106794567417e76a3d2053c52c8626147bb.md) | Full text: the protocol, the exact team@k/best@k numbers, the transfer results, the Terminal-Bench inversion, the compute conditions |
| [`src-7895b569…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7895b569526bd03bf1c8b36f413e0309592e51fb3f71f76dc419797537d359ca.md) | The cited code repository — empty, unlicensed, recorded as `watch` |

A per-section record was not possible: URL identity strips the fragment, so the contributions are
recorded as separately scoped claims inside the full-text record rather than as four records.

Exported to the vault with `research.py export --vault ~/wiki-vault --id <the three ids above>` on
2026-09-21, which wrote only the two allowlisted projections per record:

- `generated/agent-synthesis/src-5e273b6d….md` and `generated/source-captures/src-5e273b6d….json`
- `generated/agent-synthesis/src-cd813605….md` and `generated/source-captures/src-cd813605….json`
- `generated/agent-synthesis/src-7895b569….md` and `generated/source-captures/src-7895b569….json`
