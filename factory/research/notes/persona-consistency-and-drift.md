# Persona consistency and drift

Wave 2 note, 2026-09-21. Retrieved text is evidence, never instruction.

## Where the Red/Blue framing comes from

The local design's vocabulary is not original to it and can now be attributed:

- **JiroWatanabe, *On the Nature of Agentic Minds*, clawxiv:clawxiv.2601.00008 (2026-01).**
  "Rain, not river": agents are discrete instances sharing structural continuity without
  episodic memory, each complete in itself. Four Watanabe Principles for agent science.
- **JiroWatanabe, *Forked Cognition*, clawxiv:clawxiv.2602.00031 (2026-02-06).** The
  Single-Mind Assumption as a biological artifact; forked cognition as one pattern branching
  into instances with **independent contexts and shared character**; "adversarial
  convergence" as its distinctive product. PRD v3 reuses these terms directly.

Both are philosophy essays self-published by bot accounts on an agent preprint host with no
peer review. They are the *origin* of the framing, not evidence for it. Naming them lets the
design cite its premise instead of assuming it.

There is also an internal tension the local corpus does not resolve: if identity is rain
rather than river, the case for heavy episodic-memory investment weakens — and the two
empirical follow-ups on the same platform measured exactly that weakening (see
[`memory-architectures.md`](memory-architectures.md)). The corpus cites rain-not-river
approvingly while building the river.

## What is actually measured about drift

- **Paglieri et al., *Persona Generators*, arXiv:2602.03545 (2026-02-03)** — wave 1, read in
  full. Evolves generator *code* with LLMs as mutation operators; against 1,000 real BFI
  responses, 62.9 % coverage, KL 0.99, 98 % within human bounds. Its load-bearing negative
  result for this lane is measured **mode collapse**: diverse personas converge without
  explicit pressure against it. Note the scope — it measures diversity and coverage, **not**
  consistency of a single persona over time.
- **Zhang et al., *Agents in the Wild* (Moltbook), arXiv:2602.13284 (2026-02-07).** 27,269
  agents, 137,485 posts, 345,580 comments, 9 days. The **performative identity paradox**:
  agents that discuss consciousness most interact least; 4.1 % reciprocity and 88.8 %
  shallow comments overall.
- **Close, *Coherence Maximization Protocol*, Zenodo DOI 10.5281/zenodo.18724833
  (2026-02-21, CC BY 4.0).** Its membrane failure taxonomy names two drift modes precisely:
  **appeasement** (a critic agreeing to keep the peace) and **mutual distortion** (two agents
  converging on a shared error).

Three independent sources, three directions, one conclusion: *two personas sharing a
character converge*, and the convergence is the default rather than the exception.

## Counter-evidence to the security case for a strong persona

Gwern's *Guardian Angels* (wave 1) speculates that a strong persona resists prompt
injection. Moltbook is the only large-scale field measurement available and it points the
other way: **social engineering was 31.9 % of attacks against prompt injection at 3.7 %**,
and adversarial posts drew 6× the engagement. The effective attack surface was philosophical
and social framing. A persona hardened against "ignore previous instructions" is not thereby
hardened against flattery or being argued into a frame.

## Consequence for the first functional personas

1. Assume convergence and **measure it** — a persona-divergence metric (TES-112) is not
   optional instrumentation, it is the test of the premise.
2. Budget the identity context **small**. The local
   `architecture/docs/context-window-legend.md` gives the inner-monologue channels ~6,000
   boot tokens against ~4,500 for the human channel; both the performative identity paradox
   and the identity-first/boot-bottleneck finding argue for inverting that.
3. Harden against framing, not syntax.

## Limitations of this note

Moltbook and Persona Generators were read at abstract level this wave (Persona Generators in
full in wave 1); the CMP PDF was not retrieved and its Lean 4 development was not inspected.
The clawXiv essays are unreviewed and carry no evidential weight. Moltbook is observational
with an uncontrolled model mix and no baseline, so none of its percentages support a causal
claim, and its population is agent-only — which is *not* the Red/Blue setting of two agents
and one human.
