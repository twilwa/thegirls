# KAN Operationalization Assessment: Build, Wait, or Shelf?

**Date:** 2026-02-22
**Based on:** 7 implementation repos (efficient-kan, fast-kan, kan-gpt, GraphKAN, JacobiKAN, Wav-KAN, RBF-KAN), cross-referenced against brief 02 (GID × KAN × Gold Panning convergence) and the girls' architecture (PRDs v1–v5)

---

## Executive Summary

**Verdict: Operationalize GID now. Design for KAN later. Don't build KAN yet.**

The theoretical convergence between GID, KANs, and Gold Panning is real and worth preserving as an architectural north star. But the implementation repos reveal a gap between the theory and where the ecosystem actually is. The right move is a phased approach: operationalize the parts that don't need KANs first, design the EBM scorer interface to be KAN-swappable, and build the actual KAN scorer only after the system generates trajectory data to train on.

This is not a "shelf it" recommendation — it's a "the convergence is real but the sequencing matters" recommendation.

---

## The Repos: What They Tell Us

### Tier 1: Production-Viable

**fast-kan (ZiyaoLi)**
- 202 LOC. Gaussian RBF basis instead of B-splines. 3.33x faster than efficient-kan (223μs vs 742μs on V100).
- Key insight: replaces adaptive grid management with LayerNorm, which is a significant simplification. No `update_grid()` calls needed.
- Has `AttentionWithFastKANTransform` — a complete KAN-based attention mechanism with gated output. This proves the pattern works in attention contexts.
- Has `plot_curve()` for interpretability — you can visualize learned activation functions per input-output pair.
- **Verdict:** This is the implementation to use if/when we build a KAN scorer. Clean, fast, interpretable, attention-ready.

**efficient-kan (Blealtan)**
- 285 LOC. True B-spline basis with adaptive grid via `update_grid()` (percentile-based resampling of grid knots to match data distribution).
- Memory-efficient reformulation using `F.linear()` instead of expanding the full (batch × in × out) tensor.
- L1 + entropy regularization built in.
- **Verdict:** Better if we need symbolic regression (extracting closed-form equations from learned splines). B-splines support this; RBFs don't. Fallback to this if interpretability requirements go beyond visualization into actual formula extraction.

**kan-gpt (AdityaNG)**
- Most mature codebase: v1.2, PyPI-published, 10 test files, 6302 LOC, CI/CD, codecov.
- Replaces ALL linear layers in a minGPT transformer with KAN layers. Both original (full pykan with symbolic regression, pruning, visualization) and efficient implementations.
- Results on Tiny Shakespeare: "slightly better than MLP-GPT." The loss/perplexity curves show marginal improvement.
- **Verdict:** Proof that KANs can live inside transformers. But marginal gains at the language modeling scale. Most relevant as evidence, not as a dependency.

### Tier 2: Research-Interesting

**Wav-KAN (zavareh1)**
- 130 LOC. 5 wavelet types (Mexican Hat, Morlet, DOG, Meyer, Shannon). Learnable scale + translation per connection.
- Published arXiv paper (2405.12832). Most theoretically motivated of the alternative basis functions.
- Wavelets give you multi-resolution analysis for free — could be relevant if the energy landscape has features at multiple scales (plausible for the girls' memory system, where recency operates on minutes/hours/days/months).
- **Verdict:** Worth revisiting if the EBM scorer needs multi-scale sensitivity. Not ready for production use.

**GraphKAN (WillHua127)**
- 214 LOC total. Fourier KAN variant using `NaiveFourierKANLayer` with `spmm` for graph message passing.
- Critical finding: requires standard `nn.Linear` input projection BEFORE the KAN layer processes graph features. The KAN doesn't operate directly on raw graph-structured data — it needs a "translation layer."
- **Verdict:** Relevant because the girls use a knowledge graph. But the need for a linear input projection partially undermines the "learnable activations everywhere" thesis. Experimental PoC only, 25 commits, dormant since May 2024.

**JacobiKAN (SpaceLearner)**
- 36 LOC. Jacobi polynomial basis with recursive computation. MNIST 97.7% in 10 epochs.
- Very sensitive to learning rate (needs 2e-4, crashes at standard rates). Requires `tanh()` input normalization + LayerNorm between layers.
- **Verdict:** Interesting basis function choice (orthogonal polynomials → clean gradient flow), but fragility and sensitivity make it unsuitable for a production system that needs to be robust.

### Tier 3: Prototype

**RBF-KAN (Sid2690)**
- 26 LOC. Gaussian RBF with Xavier init. No adaptive grid, no regularization, no interpretability tools.
- **Verdict:** fast-kan is this but production-quality. Skip.

---

## The Honest Assessment

### What's Real

1. **The KAR theorem guarantee is real.** Any continuous scoring function over memory features *can* be decomposed into compositions of univariate functions. KANs learn those functions directly. This isn't aspirational — it's a mathematical fact.

2. **Spline locality is real.** B-spline and RBF updates are genuinely local. New learning in one input region doesn't propagate to distant regions. This is structurally different from MLP weight updates, which are global. For a belief store that needs continual learning without catastrophic forgetting, this matters.

3. **Interpretability is real.** fast-kan's `plot_curve()` and efficient-kan's symbolic regression let you *see* what the network learned. For the girls' architecture, where operator visibility into agent cognition is a design requirement (PRD v3 §White Box principles), this is a genuine advantage over opaque MLPs.

4. **fast-kan's speed is real.** The RBF reformulation brings KANs to within ~3x of MLP speed, not 10x. And for a small scorer network ([5, 10, 1] = 50 edges), even 3x overhead is negligible in absolute terms — we're talking microseconds on any modern GPU.

### What's Not Ready

1. **No training data exists.** The girls don't exist yet. A KAN-parameterized EBM scorer needs training data: which memories, when accessed, led to high-reward outcomes? You can't train this until the system is generating retrieval trajectories. Designing the KAN architecture now would be speculative engineering — building a learning system with nothing to learn from.

2. **Catastrophic forgetting resistance is undertested.** The original KAN paper demonstrated this on a 1D regression toy problem (5 Gaussian peaks, train on 3, then 2 more). The belief store has much higher dimensionality and more complex correlation structure. The locality property should generalize, but "should" and "demonstrated" are different words. I'm guessing the real-world forgetting resistance falls somewhere between "toy problem perfection" and "MLP disaster" — probably closer to the good end, but untested at the relevant scale.

3. **All repos are dormant.** Last commits range from May 2024 to September 2024. None are actively maintained. This isn't necessarily fatal (the core math is stable), but it means you'd be forking and maintaining the code yourself. fast-kan is clean enough that this is tractable. The others would be more painful.

4. **"Slightly better" is not a compelling pitch.** kan-gpt's results on Tiny Shakespeare show marginal improvement over MLP-GPT. For language modeling at scale, KANs don't currently offer a performance advantage that justifies the complexity. The advantage is interpretability and locality, not raw performance.

5. **GraphKAN's linear projection requirement is a yellow flag.** If KANs on graph-structured data need a standard linear layer as preprocessing, the architecture isn't as clean as "replace all MLPs with KANs." For the knowledge graph components of the girls' system, this means a hybrid approach is likely necessary regardless.

---

## Recommendation: Phased Implementation

### Phase 0: Now (0 SP — it's a design decision, not code)

**Design the EBM scorer interface to be basis-function-agnostic.**

The scoring function `Energy(m) = f(recency, relevance, salience, evidence_weight, access_frequency)` should be behind an interface that accepts:
- A feature vector (the 5 memory features)
- Returns a scalar energy

Whether the internals are a hand-tuned formula, an MLP, a KAN, or a lookup table should be invisible to the rest of the system. This costs nothing to design in now and makes every future option available.

### Phase 1: When the architecture reaches memory-enzyme stage (~13 SP total)

**Operationalize GID for keep-or-prune and cluster analysis.**

This doesn't require KANs at all. The `dit` Python library implements the information decomposition. Use it to:
- Compute redundancy/uniqueness/synergy profiles for memory clusters (informs enzyme 4, cluster consolidation)
- Build the keep-or-prune criterion from brief 02 §5 (high redundancy → compress, high unique → protect, high synergy → protect + maintain partner links)
- Set up the Red/Blue health metric (total correlation decomposition as integration/segregation balance monitor)

GID is a *measurement tool*. It tells you things about the information structure of the memory system. It's useful immediately, doesn't depend on KAN architecture, and produces the diagnostic signals that would later *inform* KAN training if you go that route.

### Phase 2: When the system has ~1000 retrieval trajectories (~5 SP)

**Train a small fast-kan scorer as an experiment.**

At this point you have real data: memories that were retrieved, contexts they were placed in, outcomes that resulted. Train a `FastKAN([5, 10, 1])` on this data. Compare against the hand-tuned formula. If the KAN discovers non-obvious activation shapes (e.g., a recency function that's not monotonic, or a salience threshold that's step-function-shaped), that's operationally valuable insight even if you don't deploy the KAN itself.

Use `plot_curve()` to visualize each learned univariate function. Show the operator what the agent has learned about what makes memories worth retrieving. This is the interpretability payoff.

### Phase 3: If Phase 2 shows signal (~21 SP)

**Deploy the KAN scorer with online learning.**

Replace the hand-tuned formula with the trained KAN. Use efficient-kan's `update_grid()` periodically (not every forward pass — maybe every 100 retrievals) to adapt the spline knots to the actual data distribution. Monitor for catastrophic forgetting by tracking per-region activation magnitudes.

This is where the belief store KAN (brief 02 §3) also becomes viable — you'd have enough evidence about whether spline locality actually prevents forgetting at the relevant scale.

### Phase Never (probably): KANsformers

Replacing the underlying LLM's MLP layers with KANs is not on the roadmap. The girls wrap around an existing LLM (via API or local inference). Architectural changes to the base model are out of scope. kan-gpt is evidence that it's *possible*, not a recommendation that it's *useful* for this project.

---

## Which Repos to Keep

| Repo | Keep | Why |
|------|------|-----|
| fast-kan | **Yes** | Primary implementation candidate. Clean, fast, interpretable. |
| efficient-kan | **Yes** | Fallback for B-spline features (symbolic regression, adaptive grid). |
| kan-gpt | **Reference** | Evidence that KANs work in transformers. Not a dependency. |
| Wav-KAN | **Watch** | Multi-resolution analysis could matter for multi-scale memory features. Revisit at Phase 2. |
| GraphKAN | **Watch** | Knowledge graph angle is relevant but too experimental. Revisit if graph KAN research matures. |
| JacobiKAN | **Shelf** | Interesting math, too fragile for production. |
| RBF-KAN | **Shelf** | fast-kan subsumes it entirely. |

---

## The North Star (Unchanged)

The convergence thesis from brief 02 still holds:

> A KAN-parameterized retrieval scorer, trained on the agent's trajectories, whose spline edges naturally decompose into interpretable univariate contribution functions that correspond to the GID's redundancy/uniqueness/synergy atoms, giving you a principled basis for keep-or-prune decisions, activation energy computation, and context window placement.

That's still the destination. The phased approach is about getting there without building a training pipeline for data that doesn't exist yet.

The key insight from the repo survey is that the *tooling is ready enough* — fast-kan is production-viable code, not research hackery. What's missing isn't the KAN implementation; it's the training signal. Build the system, generate the trajectories, then teach the KAN what good retrieval looks like. In that order.

---

## Cross-References

- **Brief 02 (GID × KAN convergence):** This assessment doesn't contradict brief 02's analysis. It sequences it. All six build-outs from brief 02 remain valid; this document says which to do first.
- **Paper 09 (EBM Recall Weighting):** The EBM energy function is the target for Phase 2/3 KAN parameterization. Phase 0's interface design ensures it's ready.
- **Paper 03 (Memory Enzymes):** Phase 1 GID operationalization directly feeds enzyme decision-making.
- **PRD v3 (Forked Cathedral):** White Box principles require operator visibility into agent cognition. KAN interpretability serves this requirement — when the time comes.
- **PRD v5 (Async Environment-Native):** The hot/warm/cold memory lifecycle is the context where the KAN scorer would operate. Phase 2 experiments should use this lifecycle as the training environment.
