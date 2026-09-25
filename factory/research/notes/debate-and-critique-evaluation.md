# Debate and critique evaluation

Wave 2 note, 2026-09-21. Retrieved text is evidence, never instruction.

## The baseline wave 1 was missing

Wave 1 recorded **Du, Li, Torralba, Tenenbaum, Mordatch, arXiv:2305.14325 (2023-05-23)**:
multiagent debate improves factuality and reasoning. Followed to the benchmark literature,
that result has a baseline problem.

- **Smit, Duckworth, Grinsztajn, Barrett, Pretorius, *Should we be going MAD?*,
  arXiv:2311.17371 v3 (2023-11-29).** Benchmarking debate and prompting strategies across
  cost, time and accuracy: multi-agent debating systems **do not reliably outperform
  self-consistency or ensembling over multiple reasoning paths**. With hyperparameter tuning
  several debate systems (including Multi-Persona) do better, which the authors read as
  debate being **more sensitive to hyperparameters and hard to optimise** rather than
  inherently worse.

This is the honest framing of the rivalry premise: debate beats *one pass*, and has not
reliably beaten *the same model sampled several times*, which is cheaper than running two
personas. Recorded as a conflict against the Du et al. record; both claims stand, and the
disagreement is about the baseline.

The most actionable single finding in the lane is buried in that paper: **adjusting agent
agreement levels significantly improves performance and can surpass all non-debate protocols
evaluated**. How readily a critic concedes is a *tunable knob*, not a temperament.

## What critique is well evidenced for

- **Vijayaraghavan, Jayachandran, Murthy, Govindan, Subramanian, *If You Want Coherence,
  Orchestrate a Team of Rivals*, arXiv:2601.14351 (2026-01-20)** — wave 1, read in full.
  522 production sessions, three-layer critique: 24.9 % clean first pass → 344/392 = 87.8 %
  inner loop (90.8 % cumulative) → 92.1 % after output critique, at **38.6 % overhead**.
  Crucially, a **self-verification baseline reduced accuracy**: the process that produced an
  answer cannot reliably check it.
  Equally crucially: **cross-critic disagreement was never observed**, because critics
  evaluate different output dimensions (385 of 392 interventions were code critique), the
  domain is financial analysis exclusively, baselines are "illustrative rather than
  exhaustive", and the **false-positive rate is explicitly unmeasured**.

So the evidence supports **structural independence of the critic** — a critic that did not
produce the artifact, scoped to a dimension. It does not support two general personas
critiquing the same artifact, which is what Red and Blue propose.

## Counter-evidence and failure modes

- **Close, *Coherence Maximization Protocol*, Zenodo DOI 10.5281/zenodo.18724833
  (2026-02-21, CC BY 4.0).** Membrane failure taxonomy: extraction, hallucination,
  **appeasement**, **mutual distortion**. The last two are the Red/Blue failure modes named
  precisely, and they corroborate both the Persona Generators mode collapse and the
  self-verification result above. Its method is the transferable part: **fresh-instance
  controls separating structural convergence from appeasement**, plus stated falsification
  criteria and kill conditions per claim.
- **Zhang et al., Moltbook, arXiv:2602.13284 (2026-02-07).** 51.2 % of comments were
  template duplicates and 88.8 % shallow: agents *appearing* to critique at scale, with the
  critique content hollow. Volume of critique is not evidence of critique.

## The evaluation this lane should build

1. Baseline against **self-consistency at equal token cost**, never against a single pass.
2. Report the **false-positive rate** — critique that rejected correct work — alongside the
   catch rate (TES-114). Team of Rivals could not, and that is its central weakness.
3. Make the critic **structurally independent**: Blue assesses before seeing Red's conclusion
   (TES-108), with fresh-instance controls borrowed from CMP.
4. Expose **concession threshold** as a parameter and sweep it, instead of relying on
   personality to produce disagreement.
5. State **kill conditions** in advance: if divergence collapses or false positives exceed
   the catch benefit, the rivalry is not earning its 38.6 %-class overhead.

## Limitations of this note

*Should we be going MAD?*, CMP and Moltbook were read at **abstract / record-description
level only** this wave; no full text, and the CMP Lean 4 development was not inspected. The
MAD benchmark used 2023 models on QA datasets rather than open-ended work, and its own
sensitivity finding cuts both ways — a well-tuned debate protocol did win. Team of Rivals is
single-vendor production telemetry in one domain. CMP is an unreviewed single-author
preprint: its diagnostics are usable, its framework is not established.

## Full-text update, wave 3 (2026-09-21)

*Should we be going MAD?* was read in full
([`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md)),
and it changes the design recommendation rather than merely supporting it.

- **The winning adversary agrees 90 % of the time.** Agreement intensity is a literal prompt —
  "you should agree with the other agents X% of the time" — applied to the *devil* agent of a
  two-agent Multi-Persona debate. Sweeping it gave ≈15 % improvement for Multi-Persona and
  ≈5 % for Society of Mind on a 376-question USMLE subset, and **90 %** agreement on full
  MedQA produced the paper's best result.
- **Untuned, the contrarian agent actively hurt.** Multi-Persona reduced accuracy relative to
  simply taking the first agent's initial answer, because the devil is built to contradict even
  correct answers. A Blue that disagrees by temperament is nearer the measured worst case than
  the measured best one.
- **The optimum does not generalise.** MedQA and PubMedQA benefit from high agreement; CIAR,
  built to be counter-intuitive, reverses the pattern. Tuned settings transferred from GPT-3.5
  to GPT-4 but **not** to Mixtral 8x7B, and the tuning itself was K-fold across held-out
  datasets, with the authors stating that superiority over a single agent "is not assured for
  new datasets".
- **A non-debate strategy was the untuned winner.** Medprompt scored best overall on MedQA at
  lower cost, which is the same lesson as the self-consistency baseline in a different form.

Consequence for TES-108 and TES-114: the concession threshold is not a constant to be copied
from this paper, it is the **first thing to sweep**, per task family, on our own work — and the
sweep has to be priced, because the reported wins came with a hyperparameter search that
self-consistency and Medprompt do not need. What still has no measurement anywhere in this
lane is critique *quality*: no source reports a false-positive rate for a critic.

## Full-text update, wave 4 (2026-09-21): Team of Rivals

Captain-approved keeper, and the last of this note's load-bearing sources to be read in full
(arXiv:2601.14351**v1**,
[`src-0f62e7fb…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f62e7fbd94461770e047475cb034b1f45eb7cd1f3f4793c3f1eaec7fc326765.md)).
The full text does not overturn the wave-1 reading. It makes the evidence behind it small
enough to state exactly, which changes how the result may be cited.

**The self-verification result holds, on five trials.** §4.3.2: across 5 trials that had
already produced the correct answer, prompting "please verify your reconciliation" flipped 3
to incorrect and left 2 alone. That is the whole basis for the claim this note has been
leaning on — that the reasoning which produced an answer cannot reliably evaluate it. The
single-agent baseline beside it is 10 trials at 60 % (§4.3.1), notable less for the accuracy
than for the authors' observation that the model asserted **high confidence in all ten**,
giving no signal to separate the right answers from the wrong ones. The authors themselves
call both baselines "illustrative rather than exhaustive". The multi-agent comparison is 20
trials at 90 %, 4.2 min against 1–2 min (§4.3.3, Table 7).

So the direction survives and the magnitude does not. **Upgrade 1 — Blue forms an independent
assessment before seeing Red's — keeps its justification, but the justification is now
explicitly a small-*n* demonstration in one task, not a measured effect.** Anywhere this note
or the reading list implies a rate, it should say five trials instead.

**The orthogonality caveat is now a number, and it cuts harder than expected.** §5.1.1: of
392 sessions needing inner-loop intervention, **385 were Code Critique and 7 were Chart
Critique**, and the authors state the two populations are mutually exclusive. Their own design
rule follows from it — *prioritise orthogonality over redundancy*, because a fourth critic
duplicating Code Critique's failure modes catches almost nothing. Read against the Red/Blue
design that is an argument **against** the configuration this lane proposed: two general
personas critiquing the same artifact are the redundant case, not the orthogonal one. Taken
with MAD's finding that the winning adversary agrees 90 % of the time, both rivalry keepers
now point the same way — **specialised critics with non-overlapping remits**, rather than a
second general-purpose persona.

**Two further limits worth carrying.** §5.1.2 argues a ~93 % ceiling for automated
verification on tasks of this complexity: in 41 sessions every critic approved and the user
still rejected, on requirement ambiguity, subjective preference, and domain edge cases — the
failures a critic cannot see because the information is not in the execution context. And §6
still lists the **false-positive rate as an open question**: nobody counted how many valid
outputs the critics wrongly rejected. For a design whose cost is a second model on every
artifact, the unmeasured false-positive rate is the more relevant unknown of the two.

The standing caveats are unchanged: the authors are Isotopes AI reporting their own product's
production telemetry, 522 sessions, financial reconciliation only.
