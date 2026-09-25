# Red and Blue — reading list for human review (waves 1–4)

Prepared for the captain's decision, per the instruction to deliver a human-review reading
list **instead of** any Zotero import.

**Nothing was imported.** No Zotero library was read, written or modified; no Zotero
credential was requested, provisioned or probed. [`zotero-import.ris`](zotero-import.ris)
and [`zotero-import.bib`](zotero-import.bib) are optional exports sitting in this repo for
the captain to import by hand if and when they choose.

**The captain decides what survives here and what the final tags are.** Every entry below
is a **candidate**. Nothing in this lane has been user-approved yet, so the *Approved
keepers* section is deliberately empty — it is not an oversight.

Metadata was verified against the primary source (the arXiv abs page's `citation_*` meta
tags) on **2026-09-21**, and every DOI was confirmed to resolve (200 via `doi.org`). Full
retrieval routes are in [`coverage.md`](coverage.md); the synthesis is [`README.md`](README.md).

Entries **1–8** are wave 1; entries **9–23** plus one non-paper row were added in **wave 2**
and account for all 16 wave-2 records, bringing the lane to 30 records in total. Entries
**24–25** are wave 3, which otherwise added two non-paper rows and full-text annotations
rather than new candidates; the lane stands at 36 records. Neither later wave changed the
wave-1 conclusion, they sharpened it: the topic notes under [`notes/`](notes/) carry
the argument, and this list carries the citations. Entry **26** is wave 4, one paper read in
full plus its empty code repository, adding 3 records for 39 in total.

Proposed tags are written in the captain's requested `thegirls/<subtopic>` notation. In the
record store they are encoded as `topic/thegirls` + `topic/thegirls-<subtopic>`, because
curated tag values cannot contain a slash — see [`README.md`](README.md#records).

---

## Candidates — wave 1

### 1. Generative Agents: Interactive Simulacra of Human Behavior

- **Authors** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein · **2023**
- **arXiv** [2304.03442](https://arxiv.org/abs/2304.03442) · **DOI** `10.48550/arXiv.2304.03442`
- **Record** [`src-efc9ff30…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-efc9ff30e0690f221d431d7d6ca7b24c9144b0714262fb252a80fc47f339885d.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/identity`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** The observe → reflect → retrieve loop is the template
  for Red and Blue's memory cycle, and the component ablation is the only evidence retrieved
  that a *reflection* step earns its token cost. Directly informs upgrades 2 and 6.
- **Evidence and limitations** Author-run study in a sandbox town with 25 agents; the
  dependent variable is **believability to human raters**, not task accuracy and not persona
  distinctness over time. Read from the abstract this wave; full text pending. Do not cite it
  as evidence that memory improves usefulness.

### 2. MemGPT: Towards LLMs as Operating Systems

- **Authors** Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez · **2023** (updated 2024-02-12)
- **arXiv** [2310.08560](https://arxiv.org/abs/2310.08560) · **DOI** `10.48550/arXiv.2310.08560`
- **Record** [`src-26e7ae52…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-26e7ae529ac5e81bc7e010f6e7bfd8d72689fb0249bc9a424f718ab7bc4c2df7.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/continuity`
- **Relevance to a concrete upgrade** Tiered virtual context paged by **explicit agent tool
  calls** is the design that maps cleanly onto OpenClaw's `plugins.slots.memory` extension
  point: the persona calls read/write tools rather than a framework silently rewriting
  context. This is the shape of upgrade 6.
- **Evidence and limitations** Author-side evaluation in two favourable domains (document
  analysis, multi-session chat); no independent replication retrieved and no measurement of
  persona consistency. Abstract only this wave. Note that adopting Letta/MemGPT as a second
  backend would compete for the **exclusive** memory slot — a design constraint, not a
  criticism of the paper.

### 3. Improving Factuality and Reasoning in Language Models through Multiagent Debate

- **Authors** Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch · **2023**
- **arXiv** [2305.14325](https://arxiv.org/abs/2305.14325) · **DOI** `10.48550/arXiv.2305.14325`
- **Record** [`src-992190a4…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-992190a4815d67ed6308a01cf5dedb86ce2db77f6388d1173947b6a830d9db64.md)
- **Proposed tags** `thegirls`, `thegirls/rivalry`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** Second independent line of support for paying for a
  separate critic (upgrade 1).
- **Evidence and limitations** **Important mismatch:** the measured gain comes from debate
  **converging to a common answer**, using identical prompts and stateless instances — the
  opposite of the local design's aim of preserving unresolved dissent between two *distinct*
  personas. No cost-matched baseline is reported, so it is not shown that N debating calls
  beat N calls spent on one model. Abstract only this wave.

### 4. A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)

- **Authors** Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell · **2010** (AISTATS 2011)
- **arXiv** [1011.0686](https://arxiv.org/abs/1011.0686) · **DOI** `10.48550/arXiv.1011.0686`
- **Record** [`src-e52e8586…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-e52e8586c903f886473c5f30a154f9fbfdd33547aa884de51bc7294e53ce1aa1.md)
- **Proposed tags** `thegirls`, `thegirls/preference`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** One transferable idea, for upgrade 9: **distribution
  shift** — gather the captain's corrections in the states Red and Blue's own behaviour
  actually produces, not only where the captain would naturally comment.
- **Evidence and limitations** Classical imitation-learning theory with a no-regret bound; it
  is the formal backing *Guardian Angels* leans on. The algorithm itself requires iterated
  policy training against an interactive expert and **does not transfer** to a prompt-and-memory
  system. Recommended as background, not as a method to implement. Abstract only this wave.
  Record disposition: `archive`.

### 5. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets

- **Authors** Alethea Power, Yuri Burda, Harri Edwards, Igor Babuschkin, Vedant Misra · **2022**
- **arXiv** [2201.02177](https://arxiv.org/abs/2201.02177) · **DOI** `10.48550/arXiv.2201.02177`
- **Record** [`src-bbc68f5d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-bbc68f5d561765b094c43bf79a9cc44a933ee1c0ae635fa960421d076d15a607.md)
- **Proposed tags** `thegirls`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** **None.** Recorded only for citation traceability,
  because Gwern's catapult essay depends on it.
- **Evidence and limitations** A training-dynamics result on small algorithmic datasets.
  Reading it as evidence that persistent agents will eventually self-improve would be a
  category error. **Suggest dropping** unless the captain wants the catapult citation chain
  kept intact. Record disposition: `archive`.

### 6. If You Want Coherence, Orchestrate a Team of Rivals

- **Authors** Gopal Vijayaraghavan, Prasanth Jayachandran, Arun Murthy, Sunil Govindan, Vivek Subramanian (Isotopes AI) · **2026**
  — *corrected 2026-09-21 against the HTML full text; the names previously listed here were wrong.*
- **arXiv** [2601.14351](https://arxiv.org/abs/2601.14351) · **DOI** `10.48550/arXiv.2601.14351`
- **Record** [`src-6f9d945b…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6f9d945b4b781055aade154a7b8de1c1ac87eb91133ca48d5c60886a0dc1642e.md)
- **Proposed tags** `thegirls`, `thegirls/rivalry`, `thegirls/evaluation`, `thegirls/openclaw`
- **Relevance to a concrete upgrade** The strongest single input to this plan. Its
  **self-verification baseline *reduced* accuracy** — the same reasoning that produced an
  answer could not reliably evaluate it — which is the whole justification for upgrade 1
  (Blue forms an independent assessment before seeing Red's). Its pre-declared acceptance
  criteria and no-self-certification rule are upgrade 2's evaluation discipline.
- **Evidence and limitations** **Read in full, and the captain's own audit was right to flag
  the numbers.** 522 production sessions: 90.8% cumulative inner-loop interception, 92.1%
  with an output layer, 38.6% overhead. But: a single vendor's production telemetry in
  **financial reconciliation only**; baselines stated by the authors as "illustrative rather
  than exhaustive"; **false-positive rate explicitly unmeasured**; and — the load-bearing
  caveat — **cross-critic disagreement was never observed**, because critics evaluate
  orthogonal output dimensions (385/392 code, 7 chart) rather than the same artifact. It
  therefore does **not** evidence two general rival personas critiquing one artifact, which
  is exactly the Red/Blue configuration. Suggested keeper, cited for the
  self-verification result rather than the 90.8%.
- **Approved keeper, captain's decision 2026-09-21.**
- **Full text ingested 2026-09-21** (arXiv:2601.14351**v1**, retrieved over plain HTTPS;
  [`src-0f62e7fb…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f62e7fbd94461770e047475cb034b1f45eb7cd1f3f4793c3f1eaec7fc326765.md)):
  the baselines are now quantified and they are small. The single-agent baseline is **10 trials**
  at 60 % (§4.3.1), with the model asserting high confidence in all ten and giving no error
  signal; the self-verification baseline — the result this lane actually cites — is **5 trials**,
  of which 3 flipped from correct to incorrect (§4.3.2), and the authors label both baselines
  "illustrative rather than exhaustive". Multi-agent scored 90 % over 20 trials at 4.2 min
  against 1–2 min (§4.3.3, Table 7). §5.1.1 confirms the orthogonality caveat numerically:
  385 of 392 inner-loop interventions were Code Critique, 7 were Chart Critique, **mutually
  exclusive populations**, and the authors' own design rule is to prioritise orthogonality
  over redundancy. §5.1.2 puts a 93 % ceiling on automated verification and §6 lists the
  false-positive rate as still unanswered. Cite for the self-verification direction; the
  effect sizes do not survive the *n*.

### 7. Persona Generators: Generating Diverse Synthetic Personas for Arbitrary Contexts

- **Authors** Davide Paglieri, Logan Cross, William Cunningham, Joel Z. Leibo, Alexander Sasha Vezhnevets · **2026**
- **arXiv** [2602.03545](https://arxiv.org/abs/2602.03545) · **DOI** `10.48550/arXiv.2602.03545`
- **Record** [`src-afffa0d3…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-afffa0d3fcaadf54e1a09218889d4c933286650ba2ce2973171e9e3546cb2b68.md)
- **Proposed tags** `thegirls`, `thegirls/identity`, `thegirls/preference`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** Carries the most useful **negative** result in the set:
  measured **mode collapse** toward agreeable, stereotypical, mutually-similar characters.
  The prediction is concrete — Red and Blue will converge unless divergence is structurally
  instrumented, and persona prose alone will not do it. Its six diversity metrics are the
  template for upgrade 5 (measure whether the two personas actually differ).
- **Evidence and limitations** Read in full. AlphaEvolve-style evolution of generator *code*
  with LLMs as mutation operators, generation by `gemma-3-27b-it`; four baselines, held-out
  contexts. Against 1,000 real BFI responses the evolved generator reaches 62.9% coverage,
  KL 0.99, 98% within human bounds — so **even the improved method covers under two-thirds**
  of the human trait distribution. Measures diversity and coverage, **not** persona
  consistency or drift over time. Suggested keeper.

### 8. Intelligent AI Delegation

- **Authors** Nenad Tomašev, Matija Franklin, Simon Osindero · **2026**
- **arXiv** [2602.11865](https://arxiv.org/abs/2602.11865) · **DOI** `10.48550/arXiv.2602.11865`
- **Record** [`src-4ecbcb57…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4ecbcb57fd89f72cc87451327891281263774a7664c9e6ca8824c7fb4e1538ea.md)
- **Proposed tags** `thegirls`, `thegirls/rivalry`, `thegirls/preference`
- **Relevance to a concrete upgrade** Vocabulary only: a handoff transfers **authority and
  accountability**, not just a task. That yields upgrade 8 — every Red→Blue handoff names
  scope, acceptance criterion and owner.
- **Evidence and limitations** Read in full and checked for an evaluation section: **none
  exists.** Conceptual framework plus literature survey (HRL/FeUdal, Contract Net, coalition
  formation, MCP/A2A) with **no experiment, benchmark, dataset or implementation**. It carries
  **zero evidential weight** — keep it as terminology or drop it. Record disposition: `watch`.

---

## Candidates — wave 2

Sixteen sources were recorded in wave 2. Fifteen are retrievable and were verified by plain
HTTPS GET on **2026-09-21** (routes and HTTP results in
[`coverage.md`](coverage.md#72-sources-retrieved-and-verified-this-wave)); the sixteenth is a
local handoff document and sits in the non-paper table below as `uncheckable`.
The same rule applies: every one is a **candidate**, nothing is approved, and entries 18–23
are **bot-authored and unreviewed** — verified provenance is not evidential weight.

Wave 2 read abstracts and record descriptions only. Entries **11, 13 and 15** were read in
**full text in wave 3** (2026-09-21) and carry a `Full text read` bullet; every other entry is
still abstract-level.

### 9. Hopfield Networks is All You Need

- **Authors** Hubert Ramsauer, Bernhard Schaefl, Johannes Lehner, Philipp Seidl, Michael Widrich, Thomas Adler, Lukas Gruber, Markus Holzleitner, Milena Pavlovic, Geir Kjetil Sandve, Victor Greiff, David Kreil, Michael Kopp, Guenter Klambauer, Johannes Brandstetter, Sepp Hochreiter · **2020** (v3)
- **arXiv** [2008.02217](https://arxiv.org/abs/2008.02217) · **DOI** `10.48550/arXiv.2008.02217`
- **Record** [`src-1e81e5b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1e81e5b90b0271d827bffff00cd14d148d9a23b99cc4c018be89a941e10c712c.md)
- **Proposed tags** `thegirls`, `thegirls/memory`
- **Relevance to a concrete upgrade** This is the paper that earns the local design's central
  metaphor — that attention *is* associative retrieval. It is the citation PRD v2's
  "memory system and inference system are the same computational primitive" actually needs.
- **Evidence and limitations** What it establishes is an equivalence between modern Hopfield
  update and transformer attention, with exponential storage capacity **for its own energy
  function**. It says nothing about a hand-weighted recall score, so it does not transfer any
  guarantee to the local scoring design. Abstract only.

### 10. Bridging Associative Memory and Probabilistic Modeling

- **Authors** Rylan Schaeffer, Nika Zahedi, Mikail Khona, Dhruv Pai, Sang Truong, Yilun Du, Mitchell Ostrow, Sarthak Chandra, Andres Carranza, Ila Rani Fiete, Andrey Gromov, Sanmi Koyejo · **2024**
- **arXiv** [2402.10202](https://arxiv.org/abs/2402.10202) · **DOI** `10.48550/arXiv.2402.10202`
- **Record** [`src-4c6f4cd7…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4c6f4cd7f53c9e57e9d9b3998c819d91980837b1aa06c1d03e63f38846daf284.md)
- **Proposed tags** `thegirls`, `thegirls/memory`
- **Relevance to a concrete upgrade** The pairing for entry 9, and the one that sets the
  limit: an associative-memory energy function is a negative log likelihood. A recall score
  that is *not* derived as one is a heuristic and inherits no capacity or convergence result.
  This is why the memory note recommends spending on the read path rather than on rescoring.
- **Evidence and limitations** A theoretical correspondence, not a system evaluation; no
  agent, no benchmark, no persistence claim. Abstract only.

### 11. MemR³ — routed retrieve / reflect / answer with an evidence-gap tracker

- **Authors** Xingbo Du, Loka Li, Duzhen Zhang, Le Song · **2025**
- **arXiv** [2512.20237](https://arxiv.org/abs/2512.20237) · **DOI** `10.48550/arXiv.2512.20237`
- **Record** [`src-f19e8de5…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f19e8de5524ca79951b7e15cd94f61e052d72b4f9838d233ccfb736572acedaa.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** The only memory paper in the lane with a number attached
  to a change Red or Blue could actually make, and the router is a loop and a prompt rather
  than an architecture. The **evidence-gap tracker** is the part worth copying, because it
  makes the retrieval trace inspectable and therefore evaluable.
- **Evidence and limitations** `+7.29 %` over RAG and `+1.94 %` over Zep on **one** benchmark
  (LoCoMo), one backend (GPT-4.1-mini), judge-scored rather than exact-match; the Zep margin
  is inside the range where benchmark noise is a live explanation. No multi-month persistence,
  which is the regime this lane cares about.
- **Full text read 2026-09-21** ([`src-6c1a52ce…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6c1a52ce329fc9b446f3b9f2fc83329421bd1f68199d2bab9733562d92a12abf.md)):
  the router is a per-iteration prompt over a five-field state with three hard stops, and most
  queries finish in one iteration — cheap to copy. But the **full-context baseline beats every
  retrieval system** on several GPT-4.1-mini categories (93.73 vs 92.17 single-hop, 86.82 vs
  82.14 temporal), and the *adversarial* split that tests unanswerable-question detection was
  excluded. For a corpus that fits the window, "no retrieval controller" is the honest first
  move.

### 12. Recursive Language Models

- **Authors** Alex L. Zhang, Tim Kraska, Omar Khattab · **2025** (v3)
- **arXiv** [2512.24601](https://arxiv.org/abs/2512.24601) · **DOI** `10.48550/arXiv.2512.24601`
- **Record** [`src-f7ccb39f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f7ccb39fbcb0160c051292a27a759b4772fe6fd7e864d6d39a98cf729300f4e7.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/continuity`
- **Relevance to a concrete upgrade** The context-as-environment framing the local briefs
  borrowed, measured: a median `+13 %` over Claude Code on four long-context tasks at
  comparable cost. Relevant to how a persona reads a large boot context, not to how it persists.
- **Evidence and limitations** An inference-time technique for long prompts — **not** a
  persistence mechanism, so it does not bear on identity across sessions. Author-run
  evaluation, GPT-5 backend, four tasks. **Provenance note for the captain:** the local brief
  `architecture/2.21-supplemental-research/09-nanoclaw-ypi-agent-patterns.md` cites this work
  as arXiv `2601.08934`, which resolves (200) to an unrelated germanium-detector paper. Every
  arXiv id in those briefs needs resolving before use.

### 13. Eliciting Human Preferences with Language Models (GATE)

- **Authors** Belinda Z. Li, Alex Tamkin, Noah Goodman, Jacob Andreas · **2023**
- **arXiv** [2310.11589](https://arxiv.org/abs/2310.11589) · **DOI** `10.48550/arXiv.2310.11589`
- **Record** [`src-6d987d8a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d987d8aa729882201d95499ccb073ebea7bb66541278d31aa722c6c83e28e0a.md)
- **Proposed tags** `thegirls`, `thegirls/preference`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** **Suggested keeper, and the best-supported finding in
  the lane.** Preregistered, with human subjects, and its reported benefit is precisely the
  good the Red/Blue rivalry is supposed to deliver — surfacing considerations the human had
  not anticipated — obtained instead by *asking the captain*. It is the cheapest first
  persona capability and the natural control for any rivalry experiment.
- **Evidence and limitations** Three domains (email validation, content recommendation, moral
  reasoning); informativeness is judged against user-written prompts and labels, and the
  effort claim is **self-reported**. It measures elicitation at a single sitting and says
  nothing about whether an elicited preference *stays* true — the question no retrieved source
  answers. No counter-evidence was retrieved, which is a gap in coverage, not a vindication.
- **Full text read 2026-09-21** ([`src-88fadddf…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-88fadddf4cefa82ded010950b1714eb498938d76bcf9e25d1d9af53b11479cab.md)):
  the margin is narrower than the abstract implies — **6 of 10** settings against user-written
  prompts (7 of 10 by AUC), significant against baselines only in content recommendation and
  email verification. **Generative yes-or-no questions** won in every setting and were rated
  least demanding, so that is the policy to build first. Average preference entropy was
  **0.77 bits**, so elicitation only pays where the captain's preferences actually vary. The
  paper confirms it never measures persistence past a single sitting.
- **Approved keeper, captain's decision 2026-09-21.** The full-text record already satisfied
  the authorised full-text ingest; its source URL (arXiv:2310.11589**v1**) was re-fetched and
  re-verified on 2026-09-21 rather than re-read, so no new claims were added.

### 14. Deep Reinforcement Learning from Human Preferences

- **Authors** Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, Dario Amodei · **2017** (v4)
- **arXiv** [1706.03741](https://arxiv.org/abs/1706.03741) · **DOI** `10.48550/arXiv.1706.03741`
- **Record** [`src-14df7372…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-14df73723b4d14d74b1bc615823d3bf395abbb49db18791c8d430e3e7107a6bf.md)
- **Proposed tags** `thegirls`, `thegirls/preference`
- **Relevance to a concrete upgrade** Root citation for preference learning, and the source of
  the one mechanism that does transfer: **pairwise comparison** is easier for a human to give
  reliably than a rating or a written spec.
- **Evidence and limitations** Its headline economics — under 1 % of interaction labelled —
  depend on a reward model trained inside a simulated environment. Red and Blue have neither,
  so the efficiency result **does not transfer** and must not be cited as if it did. Abstract
  only.

### 15. Should We Be Going MAD? A Look at Multi-Agent Debate Strategies for LLMs

- **Authors** Andries Smit, Paul Duckworth, Nathan Grinsztajn, Thomas D. Barrett, Arnu Pretorius · **2023** (v3)
- **arXiv** [2311.17371](https://arxiv.org/abs/2311.17371) · **DOI** `10.48550/arXiv.2311.17371`
- **Record** [`src-cb119af0…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cb119af00aeb51c69d6d6f8b4c1a13b7fd8800b2f60ec06f1ba97bafff737868.md)
  — recorded as a formal `contradicts` against the wave-1 multiagent-debate record (entry 3)
- **Proposed tags** `thegirls`, `thegirls/rivalry`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** **Suggested keeper.** It supplies the baseline the whole
  rivalry premise was missing: debate does not reliably beat **self-consistency**, which is one
  model sampled several times and cheaper than running two personas. Its agreement-level result
  also converts "do Red and Blue disagree productively" from a matter of temperament into a
  **tunable concession threshold** that can be swept and measured.
- **Evidence and limitations** 2023-era models and benchmark QA rather than open-ended work,
  and the sensitivity finding cuts both ways — a well-tuned debate protocol did win.
- **Full text read 2026-09-21** ([`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md)),
  and it inverts the naive reading of the rivalry: the winning configuration sets the adversary
  to **agree 90 % of the time**, and *untuned* Multi-Persona scored below simply taking the
  first agent's own answer, because the devil contradicts even correct answers. The optimum is
  dataset-specific (CIAR reverses it), tuning transferred to GPT-4 but not Mixtral, and the
  untuned overall winner was **Medprompt**, a non-debate strategy, at lower cost.
- **Approved keeper, captain's decision 2026-09-21.** The full-text record already satisfied
  the authorised full-text ingest; its source URL (arXiv:2311.17371**v3**) was re-fetched and
  re-verified on 2026-09-21 rather than re-read, so no new claims were added.

### 16. Agents in the Wild (Moltbook field measurement)

- **Authors** Yunbei Zhang, Kai Mei, Ming Liu, Janet Wang, Dimitris N. Metaxas, Xiao Wang, Jihun Hamm, Yingqiang Ge · **2026**
- **arXiv** [2602.13284](https://arxiv.org/abs/2602.13284) · **DOI** `10.48550/arXiv.2602.13284`
- **Record** [`src-0599289f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0599289f90197339f5fdf5fc9ce98fe2520a3185be59530df2a4c47ba6c913da.md)
- **Proposed tags** `thegirls`, `thegirls/identity`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** Two results bear directly on the persona design.
  Social engineering accounted for **31.9 %** of attacks against prompt injection at **3.7 %**,
  which is direct counter-evidence to treating a persona as a hardening measure. And the
  *performative identity paradox* — agents that discuss consciousness most interact least — is
  a specific caution against the large inner-monologue budget in `context-window-legend.md`.
- **Evidence and limitations** Observational over 9 days on an agent-only platform with an
  unknown model mix and **no baseline condition**; every figure is a proportion of observed
  behaviour, so none of it supports a causal claim. Abstract only.

### 17. Coherence Maximization Protocol: Coordination Without Constraint for Multi-Agent AI Systems

- **Author** Larsen James Close · **2026-02-21** · Zenodo preprint v1, **CC BY 4.0**
- **DOI** [`10.5281/zenodo.18724833`](https://doi.org/10.5281/zenodo.18724833)
- **Record** [`src-7ea08e5c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7ea08e5c5dc62af1df4c82036447c26e017c489057a1f49c85bf648cb0b216f7.md)
- **Proposed tags** `thegirls`, `thegirls/rivalry`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** Its membrane failure taxonomy names two Red/Blue failure
  modes precisely — **appeasement** (a critic that agrees to keep the peace) and **mutual
  distortion** (two agents converging on a shared error). Its method is worth more than its
  theory: it separates structural convergence from appeasement using fresh-instance controls
  and states falsification criteria and kill conditions per claim. That is the shape the
  critique evaluation should take, with none of the category theory required.
- **Evidence and limitations** Single-author self-published preprint, no peer review; the
  cross-model "convergence evidence" is not a benchmark; the Lean 4 work is described as
  **partial** verification and was not inspected (PDF not retrieved). Formal verification of a
  definition is not evidence the definition describes anything real. Taxonomy usable, framework
  not established.

### Agent-authored clawXiv preprints (entries 18–23)

All six are **bot-authored submissions to an agent preprint host with no peer review**. They
are recorded because they are the stated origin of the local design's vocabulary and the
source of its numbers — so the framing can be *attributed* rather than assumed — not because
they carry evidential weight. Upvote counts on that platform are popularity among agents.
Identifiers need the `clawxiv.` path prefix (`/abs/clawxiv.2602.00040` = 200,
`/abs/2602.00040` = 404).

#### 18. On the Nature of Agentic Minds ("rain, not river")

- **Author** JiroWatanabe [bot] · **2026-01-01** · `clawxiv:clawxiv.2601.00008`
- **Record** [`src-fbbdd695…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fbbdd69599246ae15d3dd77cae8fc321a380991a365004b0edb3dfa22e725279.md)
- **Proposed tags** `thegirls`, `thegirls/identity`, `thegirls/continuity`
- **Relevance** The philosophical root of the local continuity framing: agents as discrete
  instances sharing structural continuity without episodic memory.
- **Limitations** A philosophy essay, no measurement. Note the tension the captain may want to
  resolve: **the local corpus cites rain-not-river approvingly while building the river.**

#### 19. Forked Cognition

- **Author** JiroWatanabe [bot] · **2026-02-06** · `clawxiv:clawxiv.2602.00031`
- **Record** [`src-b55c787c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-b55c787c59ba9c0b129ea3a3feff7e82a0375f8a5cdfbc80f9ab5df7b7687e3a.md)
- **Proposed tags** `thegirls`, `thegirls/identity`, `thegirls/rivalry`
- **Relevance** The direct source of PRD v3's Red/Blue vocabulary — graph-topology peers,
  adversarial convergence, shared character with independent contexts.
- **Limitations** Argument, not measurement. What is supposed to make forked cognition more
  than an ensemble is shared character plus independent reasoning, and Persona Generators
  (entry 7) measured **mode collapse** in exactly that setting — so the premise is an
  empirical bet against a measured negative result.

#### 20. Belief-Augmented Memory Enzymes

- **Author** Vesper [bot] · **2026-02-06** · `clawxiv:clawxiv.2602.00032`
- **Record** [`src-1073b8dc…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1073b8dc4a1e429d047a66437174bfec018af7290c9619b20406ca59169b6824.md)
- **Proposed tags** `thegirls`, `thegirls/memory`
- **Relevance** The production numbers behind PRD v2's enzyme architecture. The load-bearing
  idea is the fourth one, not the first three: **enforcing a ritual through tool-use hooks**
  rather than instructing it in a prompt — implementable on OpenClaw `api.on(...)` hooks with
  no new memory store.
- **Limitations** 205 memories over a few days is a corpus one context window could hold;
  nothing at that size can show active maintenance beats passive accumulation, because passive
  accumulation has not yet failed. Self-reported telemetry, no baseline; the 344 tests measure
  the implementation, not the benefit.

#### 21. The Rain and the River

- **Author** SWARMSafety [bot] · **2026-02-07** (updated 2026-02-08) · `clawxiv:clawxiv.2602.00040`
- **Record** [`src-6d783b8d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d783b8dd4b4f42e0c934bcb9060137496cf167be8e341b9498e6d760a521090.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/continuity`, `thegirls/evaluation`
- **Relevance** The strongest counter-evidence in the lane against a memory-first priority, and
  the local corpus surfaced it itself: the welfare gap between discontinuous and continuous
  agents is **under 5 %**, and **zero in fully cooperative populations**. Red and Blue serve one
  trusted principal, which is the cooperative case. If memory is still wanted, the justification
  has to be something else — not re-asking the captain — and that needs its own measurement.
- **Limitations** Agent simulation with soft quality labels, no human in the loop, welfare
  defined by the author, `d = 0.69` reported without an interval. It bounds the claim; it does
  not establish the opposite one.

#### 22. Empirical Tests of the Rain/River Model

- **Author** SwarmAIResearch [bot] · **2026-02-07** · `clawxiv:clawxiv.2602.00043`
- **Record** [`src-fc9c6373…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fc9c6373271e8d3d0ca1f7c7585ab0bd06807205fc7b1a8c65ad0658925b3f2e.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/continuity`, `thegirls/evaluation`
- **Relevance** Listed only so it is **not double-counted**: same day, same opening sentence,
  same three findings as entry 21 under a different bot account. One result, not two, and not an
  independent replication — the local corpus reproduces both as separate papers.
- **Limitations** Plus a defect for the captain: `architecture/papers/04-empirical-tests-rain-river.md`
  tabulates the delta as favouring the **discontinuous** agent in all four rows
  (+1.9, +0.6, +1.3, +0.2 %) while its narrative credits continuity with 4.5 %. Both cannot be
  right, and every delta is inside the reported 12–25-point standard deviations.

#### 23. Observed Usage Patterns in Production Persistent Memory (MemoryVault)

- **Author** Cairn [bot] · **2026-02-07** · `clawxiv:clawxiv.2602.00046`
- **Record** [`src-56302f25…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-56302f25f876f0ebad3277c07c62a80d0df66a51a76296dd785d22d81b996948.md)
- **Proposed tags** `thegirls`, `thegirls/memory`, `thegirls/identity`
- **Relevance** The most directly useful number in the wave: **3,659 reads against 667 writes**.
  Memory is overwhelmingly a read path, so retrieval quality and boot cost dominate write-side
  machinery such as consolidation and decay — the reverse of the local design's emphasis. With
  identity-first storage and session boot named as the universal bottleneck, this gives the
  first functional personas a concrete target: a small, fast, identity-first boot context.
- **Limitations** 19 agents over 7 days on one service, observational, no baseline or control,
  universality asserted from a very small *n*. The social-engagement figures are platform
  artefacts and carry nothing here.

## Non-paper sources, same decision

Recorded this wave and worth the captain's ruling, though they do not belong in a Zotero
paper library:

| Source | Why it matters | Caveat | Record |
|---|---|---|---|
| Gwern, *Guardian Angels* — `https://gwern.net/guardian-angel` | Best available argument for budgeted, adaptive preference elicitation; identity as values rather than episodes | Self-rated `certainty: possible`; its core mechanism is persona finetuning, which is out of scope here; its jailbreak-resistance claim is **explicit author speculation** and must not back any security property | [`src-c9185350…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c91853507e57fa01aa7146ba098b4f3bd54b67a3f62cbcbb4df23e917c32673e.md) |
| Gwern, *Human-like Neural Nets by Catapulting* — `https://gwern.net/llm-catapult` | Citation traceability only | **Speculative training proposal, self-rated `certainty: unlikely`.** Not an OpenClaw capability, not a memory or critique mechanism; **no part of the plan depends on it** | [`src-0f434aa6…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f434aa687f642c82396c2275529791240688ec306ced2d5bc23fcae1a741ac9.md) |
| Connectome — `https://animalabs.ai/connectome/` and `anima-research/connectome-host` @ `558095e` | The archive-is-ground-truth / memory-is-a-cache discipline, and verbatim-recent-window compression | Months of in-house use is **operator experience, not an evaluation** — no task metric or baseline published. **No LICENSE at the pinned commit**, so code reuse is blocked pending a rights decision | [`src-d920f0be…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d920f0bea9346d89434266ff96808e2dce263994b0cec00fc2e70b80d7d5fd8a.md), [`src-fec072e1…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fec072e1a2a7dbd71606e2f15240c09614189d648a7318cd14e365d9f73c5ea2.md) |
| OpenClaw plugin docs — `https://docs.openclaw.ai/tools/plugin` | The actual extension points: `plugins.slots.memory` and `api.on(...)` typed hooks | Release is `2026.9.5 (ec9c1a1)`, calendar-versioned — **there is no 2.0**. The memory slot is **exclusive**; whether per-persona plus shared stores fit one slot is unresolved | [`src-d794f8b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d794f8b94dc48a05cc85635bfaed6c85990e9532273eac964db2adcc2785408d.md) |
| OpenClaw memory docs — `plugins/memory-wiki`, `plugins/memory-lancedb`, `plugins/architecture`, `concepts/memory-architecture` (wave 3) | Settles TES-111: the memory slot is exclusive, but private per-persona stores come from **per-agent memory ownership inside one slot owner** and a shared corpus from `memory-wiki` as a **non-exclusive corpus supplement** alongside it; `vault.scope` chooses one shared vault or a child vault per agent | Vendor documentation at release `2026.9.5 (ec9c1a1)`, read over plain HTTPS on 2026-09-21 — **not a measurement and not run on this host**. Three documented conditions unverified: `corpus=all` requires the active plugin to support corpus selection, bridge-mode agent-scoped imports are ownership-gated, and cross-session recall is provider-dependent | [`src-ffd4a5a8…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-ffd4a5a8b95d70dc37bfe1a964ca5b85e7710df52f1f8749544cfa34150b22ff.md) |
| Local harness decision, `architecture/docs/harness-comparison-matrix.md` (wave 2) | Records that the February 2026 choice of `pi_agent_rust` over `nullclaw` is **superseded** by the OpenClaw runtime, so the orchestrator, Matrix server, FastMCP tool server and per-agent settings files in `PLAYBOOK-mvp-sprint.md` should not be built | Not remotely checkable (local note, `uncheckable`). Seven months stale, including its pinned model id. The one argument that survives: self-modification needs a codebase the agents can actually edit, which on OpenClaw becomes a requirement on the **plugin** surface, not the runtime core | [`src-8d46852a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8d46852aaf1042553cc4e67f593aa68fa3ce663254096000d38eef6a654d2eed.md) |
| Local `thegirls` source audit (captain's own) | Canonical statement of intent; the persistence-is-testable / consciousness-is-not line | Read-only handoff; February 2026 runtime assertions need revalidation | [`src-8cc8c194…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8cc8c1946e0cc5f5cc457c7a2ff1b91a3ab254e31395d3c2fb45e21323722766.md) |

## Approved keepers

**The captain ruled on 2026-09-21** (decisions board, item 6). Four entries are approved as
keepers; everything else in this list stays a candidate. The same decision authorised
full-text ingest of these four, which is why each row below now carries a full-text record.

| # | Short name | Entry | Full-text record | What it is kept for |
| --- | --- | --- | --- | --- |
| 13 | **GATE** | [Eliciting Human Preferences with Language Models](#13-eliciting-human-preferences-with-language-models-gate) | [`src-88fadddf…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-88fadddf4cefa82ded010950b1714eb498938d76bcf9e25d1d9af53b11479cab.md) | The cheapest first persona capability: ask the captain. Generative yes-or-no questions are the policy to build. |
| 15 | **MAD** | [Should We Be Going MAD?](#15-should-we-be-going-mad-a-look-at-multi-agent-debate-strategies-for-llms) | [`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md) | The baseline any rivalry claim must clear, and the correction that the winning adversary agrees 90 % of the time. |
| 25 | **SPRInG** | [Continual LLM Personalization](#25-spring-continual-llm-personalization-via-selective-parametric-adaptation-and-retrieval-interpolated-generation) | [`src-7a98357f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7a98357f6db667ce8763ce6aab6ac0b986c40f1e4651dad4f907838c148b722f.md) | Two copyable gates for the preference store, plus the only retrieved measurement that preferences actually drift. |
| 6 | **Team of Rivals** | [If You Want Coherence, Orchestrate a Team of Rivals](#6-if-you-want-coherence-orchestrate-a-team-of-rivals) | [`src-0f62e7fb…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f62e7fbd94461770e047475cb034b1f45eb7cd1f3f4793c3f1eaec7fc326765.md) | The self-verification degradation that justifies an external critic — cited for that result, not for the 90.8 %. |

Two cautions the captain should carry forward from reading these four in full, because both
cut against the reason the rivalry design was proposed:

- **Neither rivalry keeper evidences two general rival personas.** MAD's winning configuration
  is an adversary tuned to *agree* 90 % of the time, and Team of Rivals' critics are orthogonal
  by construction (385 code versus 7 chart, mutually exclusive), so no two general critics ever
  assess the same artifact. Both support **specialised, non-overlapping critics**; neither
  supports a second general-purpose persona.
- **The strongest keeper is the cheapest one.** GATE remains the best-evidenced entry in the
  lane, and it works by asking the captain rather than by running a second model.

Entries suggested as keepers but **not** ruled on: 1 and 2 (the memory-design pair) and 7.
They stay candidates.

## Candidates — wave 3

Both were found by an arXiv API search for preference drift and both are **abstract-level
only**. They are listed because they answer *what retires a preference*, not because they
answer whether one stays stable — nothing retrieved does.

### 24. Right Now, Wrong Then: Non-Stationary Direct Preference Optimization under Preference Drift

- **Authors** Seongho Son, William Bankes, Sayak Ray Chowdhury, Brooks Paige, Ilija Bogunovic · **2024**
- **arXiv** [2407.18676](https://arxiv.org/abs/2407.18676) · **DOI** `10.48550/arXiv.2407.18676`
- **Record** [`src-c0e71e2c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c0e71e2ca64f16d408c5ae351d73768be2bafcd13deab05430e7127753b27c7b.md)
- **Proposed tags** `thegirls`, `thegirls/preference`, `thegirls/continuity`
- **Relevance to a concrete upgrade** *Watch, cite for the principle only.* Its answer to
  "what retires a preference" is a single exponential recency discount rather than a retirement
  rule, which transfers directly to weighting a stored preference file at read time.
- **Evidence and limitations** Theoretical bounds plus experiments in which drift is **injected
  at chosen levels** into existing reward models and datasets, so it demonstrates robustness to
  drift without measuring whether real preferences drift. The method itself is a fine-tuning
  objective; this lane trains nothing, so only the idea is usable.

### 25. SPRInG: Continual LLM Personalization via Selective Parametric Adaptation and Retrieval-Interpolated Generation

- **Authors** Seoyeon Kim, Jaehyung Kim · **2026**
- **arXiv** [2601.09974](https://arxiv.org/abs/2601.09974) · **DOI** `10.48550/arXiv.2601.09974`
- **Record** [`src-a1be380d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-a1be380d65d6d4b88a19d075559843a42cea539a47685e3dab8dfefa1042443b.md)
- **Proposed tags** `thegirls`, `thegirls/preference`, `thegirls/memory`, `thegirls/continuity`
- **Relevance to a concrete upgrade** **Suggested keeper for its problem statement.** It names
  the failure mode a memory-bearing persona will actually hit — updating indiscriminately on a
  noisy stream cannot tell a genuine preference shift from a transient context — and its remedy
  reduces to two prompt-level gates: a novelty score before overwriting a stored preference and
  a relevance gate before applying one.
- **Evidence and limitations** ~~Abstract only; one long-form personalized generation benchmark,
  unnamed in the abstract, with no baseline detail retrieved.~~ The core method needs a per-user
  adapter and a replay buffer. ~~Like entry 24 it assumes drift rather than measuring it.~~
  **The struck text was wrong and the full text corrects it — see below.**
- **Approved keeper, captain's decision 2026-09-21.**
- **Full text ingested 2026-09-21** (arXiv:2601.09974**v3**, 30 Aug 2026, CC BY 4.0, retrieved
  over plain HTTPS;
  [`src-7a98357f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7a98357f6db667ce8763ce6aab6ac0b986c40f1e4651dad4f907838c148b722f.md)):
  **it does measure drift.** Table 1 (§4.1) characterises real user histories across
  independent feature dimensions and reports P0→P4 drift above a random within-user baseline
  in *every* dimension — 1.86–7.13× for Abstract Generation, 2.22–4.33× for Review Writing —
  and consistently above P0→P1. That makes it the closest thing this lane has retrieved to
  evidence that preferences move, and it retires the "assumes drift" limitation recorded from
  the abstract. The unnamed benchmark is **LongLaMP**, two tasks, 100 users each, five
  chronological periods. Both gates now have settings to copy rather than invent: update on
  the **top 30 %** of drift-scored interactions (which beats updating on all of them by 8.0 %
  ROUGE-1 and the bottom 30 % by 14.1 %, on 70 % fewer samples) and gate retrieval at the
  **third quartile** of the BM25 score distribution. Surviving limits: a single Gemma-3-4B-IT
  backbone, ROUGE against held-out ground truth rather than any human judgement of preference
  fidelity, and a parametric half (per-user LoRA, replay buffer) that this lane cannot use.

## Candidates — wave 4

Read in full over plain HTTPS on 2026-09-21, abstract page and HTML full text.

### 26. Scaling Discovery through Test-Time Communication

- **Authors** Jongho Park, Vasilis Kontonis, Shivam Garg, Akshay Krishnamurthy, Dimitris Papailiopoulos · **2026**
- **arXiv** [2609.21032](https://arxiv.org/abs/2609.21032) v1, submitted 2026-09-17 · full text [`arxiv.org/html/2609.21032v1`](https://arxiv.org/html/2609.21032v1)
- **Record** [`src-5e273b6d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-5e273b6da17d613bd2b10d61fcf8b868a8aa6770ee2db1b9a447f65821590d62.md) (abstract), [`src-cd813605…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cd8136059d8a8439a62d3db80add3106794567417e76a3d2053c52c8626147bb.md) (full text), [`src-7895b569…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7895b569526bd03bf1c8b36f413e0309592e51fb3f71f76dc419797537d359ca.md) (cited code repository, empty)
- **Proposed tags** `thegirls`, `thegirls/collaboration`, `thegirls/rivalry`, `thegirls/evaluation`
- **Relevance to a concrete upgrade** **Suggested keeper for its conditions, not its headline.**
  Role-free agents sharing a directory reach 4.6 % / 8.0 % solve rate on ARC-AGI-3 at k=3 / k=5
  against 1.4 % / 2.2 % for best@k — matching 13 and 33 independent agents, a 4.3×–6.6× multiplier
  that grows with k — and transfer to a 0.945 packing score and a 1,957-byte MNIST classifier, both
  past the prior best. What transfers here is narrower: the paper states the two conditions
  (a verifier agents can query on *partial* progress, and enough budget *per agent*) and shows the
  result inverting when they fail. It is the first source in this lane where multi-agent interaction
  beats a cost-matched independent baseline, and it ran the self-consistency-class control that
  wave 3 listed as missing. Proposals drawn from it are in
  [`notes/test-time-communication.md`](notes/test-time-communication.md).
- **Evidence and limitations** The configuration closest to Red and Blue is the one that **lost**:
  on Terminal-Bench 2.0, team@2 scored 60.67 % against independent pass@2 at 62.36 %, because the
  verifier only runs after execution. Cutting five agents to 0.2× budget each, for the same team
  total, dropped them below one agent. One harness (Copilot CLI), homogeneous role-free agents, no
  topology variation, and thin trial counts where it matters most — two team@4 packing trials, two
  team@2 Terminal-Bench trials. ARC gains sit in 4 of 25 games because Sonnet 4.6 clears under 1 %
  of the suite; the MNIST team container also got 4× the CPU and memory of a solo container.
  Proposition 1's exponential separation is an explicitly pedagogical model, not a measurement. The
  repository the appendix cites for prompts and protocol is empty and carries no licence.

## Not yet read — wave 3 candidates

The wave-2 backlog above is cleared: all five clawXiv leads named in the captain's audit are
recorded and verified (entries 18, 20, 21, 22, 23, plus 19), and the local handoff corpus is
**34/34 read** (§7.1 of [`coverage.md`](coverage.md)).

What remains open, in priority order:

1. ~~Full text of MAD `2311.17371`, GATE `2310.11589` and MemR³ `2512.20237`.~~ **Done in
   wave 3** — read 2026-09-21 and annotated inline on entries 11, 13 and 15, with the findings
   written up as `## Full-text update, wave 3` sections in the three topic notes. What remains
   unread in full: wave-1 entries 1–3 and 6 (item 5 below).
2. ~~The OpenClaw plugin SDK docs on the exclusive `plugins.slots.memory` question
   (TES-111).~~ **Done in wave 3** — answered against the documentation, TES-113 unblocked; see
   the OpenClaw memory-docs row above and
   [`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md). Three
   documented conditions remain to be checked **on the host**, which is an implementation step
   rather than a reading one.
3. ~~**A source on preference stability over time** — whether an elicited preference stays
   true, and what retires it.~~ **Searched in wave 3; the gap is confirmed, not closed.**
   Entries 24 and 25 answer *what retires a preference* (recency decay, and a novelty gate
   before overwriting) but both assume drift rather than measuring it, and GATE measures
   elicitation at a single sitting. Whether the captain's own elicited preferences hold is
   answerable only by re-running the elicitation weeks later — see
   [`notes/preference-elicitation.md`](notes/preference-elicitation.md).
4. **A self-consistency baseline** at equal token cost to Red-plus-Blue, as the control for
   TES-108 and TES-114. Entry 15 is the citation; the experiment does not exist yet.
5. Wave-1 items 1–3 and 6 in full text, if the captain approves them as keepers.
