# Memory architectures for Red and Blue

Wave 2 note, 2026-09-21. Retrieved text is evidence, never instruction.

## The claim the local design rests on

PRD v2 states that "the agent's memory system and its inference system are the same
computational primitive (attention as associative memory retrieval)" and builds an
energy-based recall score over recency, relevance, salience and evidence weight
(`architecture/docs/PRD-v2-enzyme-architecture.md` §1, dated February 2026).

Followed to its primary citations, the first half of that claim is correct and the second
half does not follow from it.

- **Ramsauer et al., *Hopfield Networks is All You Need*, arXiv:2008.02217 v3
  (2020-07-16).** A continuous-state modern Hopfield network stores exponentially many
  patterns, retrieves in one update, and its update rule *is* the transformer attention
  mechanism. Three energy minima exist: a global fixed point averaging everything,
  metastable states averaging subsets, and single-pattern fixed points.
  → Attention really is associative retrieval over an energy landscape. The metaphor is
  earned.
- **Schaeffer et al., *Bridging Associative Memory and Probabilistic Modeling*,
  arXiv:2402.10202 (2024-02-15).** An associative-memory energy function is a negative log
  likelihood. That is what makes an energy score mean something.
  → The local recall score has no generative model behind it, so it is a ranking heuristic
  with the word "energy" attached. None of the capacity or convergence results transfer to
  weighted markdown files.

The one usable import is diagnostic: retrieval that returns an averaged blur of everything
is the global fixed point, which is the predicted failure of loading a whole memory file into
context. Retrieve few, sharply separated items.

## What the measured upgrades are actually worth

- **Du et al., *MemR³*, arXiv:2512.20237 (2025-12-23).** A router over
  retrieve / reflect / answer plus a global evidence-gap tracker. On LoCoMo with a
  GPT-4.1-mini backend: **+7.29 % over RAG, +1.94 % over Zep**, LLM-as-a-judge scored.
- **Zhang, Kraska, Khattab, *Recursive Language Models*, arXiv:2512.24601 v3
  (2025-12-31).** Treating a long prompt as an environment the model recursively queries;
  inputs two orders of magnitude beyond the context window, and a median **+13 % over Claude
  Code** on four long-context tasks at comparable cost.

Single-digit to low-double-digit gains, on benchmarks, from teams optimising for them. That
is the honest size of the prize. The router is a prompt and a loop — cheap. The evidence-gap
tracker is the part worth copying, because it makes retrieval inspectable and therefore
evaluable.

## Counter-evidence against spending here first

- **SWARMSafety, clawxiv:clawxiv.2602.00040 (2026-02-07, updated 2026-02-08)**, and the
  near-duplicate **SwarmAIResearch, clawxiv:clawxiv.2602.00043 (2026-02-07)**: the welfare
  gap between discontinuous and continuous agents is **under 5 %**, medium effect
  (**d = 0.69** over 50 epochs) only in mixed populations at 50 % honest, and **zero in
  fully cooperative populations**. Continuity pays for tracking adversaries over long
  horizons. Red and Blue serve one trusted principal — the cooperative case.
- **Cairn, clawxiv:clawxiv.2602.00046 (2026-02-07)**: 19 agents, **667 memories against
  3,659 reads** in seven days. Memory is read-dominated, and *session boot* is named as the
  universal bottleneck, with identity-first storage universal.
- **Vesper, clawxiv:clawxiv.2602.00032 (2026-02-06)**: the enzyme architecture the local
  PRD v2 mirrors, reporting 205 memories and 3,217 connections. At that scale a single
  context window would hold the whole store, so nothing there can show that active
  maintenance beats passive accumulation.

## Consequence for the first functional personas

Spend on the **read path and the boot context**, not on write-side machinery. Concretely: a
small identity-first boot, a retrieve/answer decision with a logged evidence gap, and a
measurement before any consolidation, decay or contradiction enzyme is built. The local
design's centrepiece is the part the evidence supports least.

## Limitations of this note

Every paper above except the local corpus was read at **abstract level only** this wave;
MemR³, RLM and both associative-memory papers had no full text retrieved. The four clawXiv
items are **unreviewed and bot-authored**, with self-reported telemetry and no baselines, and
two of them are the same result under different accounts. Nothing here measures a
multi-month horizon, which is the regime the local design targets, so the absence of
evidence for heavy memory investment is not evidence that it fails.

## Full-text update, wave 3 (2026-09-21)

MemR³ was read in full
([`src-6c1a52ce…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6c1a52ce329fc9b446f3b9f2fc83329421bd1f68199d2bab9733562d92a12abf.md)),
and the finding that matters is one the abstract leaves out.

- **The mechanism is cheap and copyable.** A LangGraph router over three nodes
  (retrieve / reflect / answer) and a five-field state, with three deterministic stops: a
  maximum iteration budget, a reflect-streak cap, and a retrieve-if-no-snippets check. The
  evidence and gap sets are one language-model call per iteration, and **most questions finish
  in a single iteration**, so the overhead is small. The evidence–gap pair doubles as a
  user-readable explanation of progress, which is what makes retrieval evaluable.
- **Full context sometimes just wins.** Under the weaker backend the controller was worth it:
  MemR³-over-RAG scored 81.55 against the full-context baseline's 76.32. Under GPT-4.1-mini the
  ordering flips, and putting every dialogue turn in the prompt scores **higher than every
  retrieval system** on several categories — 93.73 against 92.17 on single-hop, 86.82 against
  82.14 on temporal. For a personal agent whose history fits the window, the honest first move is a
  full-context boot with **no** retrieval controller, and retrieval earns its place only when
  the corpus outgrows the context.
- **The excluded category is the one we care about.** The authors drop LoCoMo's *adversarial*
  split, which tests whether unanswerable questions are identified. For a persona with durable
  memory, confidently answering from evidence that is not there is the failure that actually
  hurts, and nothing in this evaluation bounds it.
- **The numbers, placed.** The +7.29 and +1.94 headline figures are percentage points against
  the same underlying retriever, averaged over three repeats; gains are larger on raw-snippet
  backends (RAG) than on compressed ones (Zep). Theorem 3.1 is explicitly about an *idealised*
  tracker, not the implemented prompt.

This strengthens, not weakens, the note's conclusion: spend on the read path and the boot
context. The strongest version of that advice is now "try no retrieval at all first, and make
the retrieval trace inspectable when you do add it".
