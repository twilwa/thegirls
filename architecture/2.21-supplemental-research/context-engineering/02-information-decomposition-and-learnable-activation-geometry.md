# Information Decomposition, Learnable Activation Geometry, and the Energy Landscape of Memory

**Sources:**
- Thomas F. Varley, "Generalized Decomposition of Multivariate Information" (arxiv 2309.08003, Dec 2023)
- Ziming Liu et al., "KAN: Kolmogorov-Arnold Networks" (arxiv 2404.19756, Apr 2024 / revised Jan 2025)

**Cross-references:** Gold Panning (brief 01), EBM Recall Weighting (paper 09), Belief-Augmented Memory Enzymes (paper 03), PRD v2/v4

---

## Why These Two Papers Belong Together

On the surface, Varley's GID is pure information theory (how to decompose multivariate information into redundant, unique, and synergistic atoms) and Liu et al.'s KAN is a neural architecture paper (learnable spline activations on edges instead of fixed activations on nodes). They come from different fields and cite zero overlapping references.

But the convergence is structural, not topical. Both papers are about the same underlying problem: **how does information get distributed across the components of a complex system, and how do you build representations that respect that distribution?**

The connecting thread — and what makes this relevant to the girls — is the question of *activation energy in information landscapes*. When the girls' retrieval system pulls memories from a knowledge graph, it's navigating an energy surface. Some memories sit in deep basins (high-evidence, frequently accessed, well-connected). Others sit on ridges (contradictory, novel, weakly evidenced). The EBM recall formula computes a scalar energy for each memory, but it treats each memory as a point. It doesn't tell you anything about the *shape of the basin* that memory sits in, or whether two memories are in the same basin or different ones, or whether a cluster of memories has synergistic information that no individual memory contains.

Varley gives you the math to answer those questions. KANs give you (potentially) the architecture to learn the activation functions that navigate those basins. Gold Panning gives you the search strategy. Together, they sketch a retrieval system that's significantly more sophisticated than "rank by energy, take top-k."

---

## Varley's GID: What It Actually Does

### The Core Move

Standard information theory gives you mutual information I(X;Y) — how much knowing X tells you about Y. The Partial Information Decomposition (PID) breaks this into:
- **Redundancy**: information that both X₁ and X₂ provide about Y (either alone is sufficient)
- **Unique**: information only X₁ provides (or only X₂)
- **Synergy**: information that *only exists in the combination* — neither X₁ nor X₂ alone contains it

PID's limitation: you have to designate "sources" and "targets." Varley's GID removes this requirement by decomposing the KL divergence D(P‖Q) — the information gained when updating from any prior Q to any posterior P — into the same redundant/unique/synergistic atoms.

**Why this matters:** Any information-theoretic measure writable as a KL divergence gets a free decomposition. This includes mutual information, total correlation, negentropy, cross-entropy, and (critically for us) *the belief update step in Bayesian retrieval systems like Gold Panning*.

### The Synergy–Complexity Connection

Varley proves a deep link between synergistic information and Tononi-Sporns-Edelman (TSE) complexity. High TSE complexity requires a balance between integration (elements are correlated) and segregation (elements are also partially independent). Too much of either kills the complexity.

The punchline: **synergistic information requires this same integration/segregation balance.** A system where everything is perfectly correlated has high redundancy but zero synergy. A system where everything is independent has zero of everything. Synergy lives in the sweet spot — and that sweet spot is exactly where complex, emergent behavior happens.

### Many Different Synergies

A critical subtlety: there isn't one "synergy." Depending on what measure you decompose (total correlation vs. mutual information vs. negentropy), you get different decompositions with different synergy values that can even have different signs. Varley calls this "pragmatic pluralism" — the right decomposition depends on what question you're asking.

---

## KAN: What Makes It Different

### The Kolmogorov-Arnold Representation Theorem

The KAR theorem states that any multivariate continuous function f(x₁,...,xₙ) can be written as:

```
f(x) = Σ_{q=1}^{2n+1} Φ_q( Σ_{p=1}^{n} φ_{q,p}(x_p) )
```

i.e., a finite composition of *univariate* functions and addition. No multiplication required at the base level — everything decomposes into 1D functions composed together.

### KANs vs. MLPs: The Architectural Difference

- **MLPs**: Fixed activation functions on nodes (ReLU, tanh, etc.), learnable linear weights on edges.
- **KANs**: Learnable activation functions on edges (B-splines), no linear weights at all.

This seems like a small change but the consequences are significant:

1. **Interpretability**: Each edge learns a visible, plottable univariate function. A human can look at a trained KAN and *read the math* it discovered. KANs rediscovered knot theory invariants and Anderson localization boundaries from data.

2. **Scaling laws**: KANs have faster neural scaling laws than MLPs — smaller KANs match or beat larger MLPs.

3. **Continual learning / catastrophic forgetting**: Because B-splines are *local* (a data point only affects nearby spline coefficients), KANs exhibit natural local plasticity. New learning in one region doesn't destroy memories stored in distant regions. In their toy demo, KANs showed zero catastrophic forgetting while MLPs catastrophically forgot everything.

4. **The efficiency problem**: KANs are ~10x slower to train than MLPs because different activation functions can't batch. The paper acknowledges this as engineering debt, not fundamental limitation. "Multi-head" grouping (some edges share activations) interpolates between KAN and MLP.

---

## The Convergence: Information Geometry of Memory Retrieval

### 1. GID Decomposes What Gold Panning Computes

Gold Panning performs Bayesian belief updates using KL divergence at each round. Varley shows any KL divergence admits a redundancy/synergy decomposition. So when the girls' retrieval system updates its beliefs about which memories are relevant, we can now ask:

- **What fraction of the retrieval signal is redundant?** (Multiple memories pointing to the same conclusion — safe to prune duplicates)
- **What fraction is unique?** (Only one memory provides this information — critical, cannot be pruned)
- **What fraction is synergistic?** (Only visible when specific memories are combined — this is where novel insight lives, and it's invisible to single-memory energy scoring)

**Actionable build-out:** The memory enzyme that does "cluster consolidation" (paper 03, enzyme 4) currently merges overlapping memory clusters. GID gives it a principled criterion: merge when information is *redundant*, keep separate when information is *unique*, and create explicit "synergy links" when the combination is more informative than the parts.

### 2. KAN Splines as Learnable Energy Surfaces

The EBM recall formula is currently hand-designed:
```
Energy(m) = f(recency, relevance, salience, evidence_weight, access_frequency)
```

This is an MLP-style approach: fixed features, fixed combination function, learned weights. A KAN-style approach would instead learn the *shape of each feature's contribution* as a univariate spline. The recency function might not be linear or exponential — it might have a bump at "yesterday" and a plateau at "last week" and a cliff at "last month," and the shape would be *learned from the agent's actual retrieval patterns* rather than hand-designed.

**The KAR theorem guarantees this works.** Any continuous scoring function over memory features can be decomposed into compositions of univariate functions. KANs learn those univariate functions directly, and they're *interpretable* — you can plot the learned recency curve and see what the agent actually values.

**Actionable build-out:** Replace the EBM energy function with a small KAN (maybe [5, 10, 1] — five features, ten intermediate nodes, one energy output). Train it on the agent's own retrieval patterns: which memories, when accessed, led to high-reward outcomes? The trained KAN gives you a *visible, interpretable* energy landscape that the agent (and the operator) can inspect.

### 3. Catastrophic Forgetting Resistance for Belief Stores

This is where KAN's locality property gets really interesting for the girls. The private belief store (PRD v3) faces a classic continual learning problem: Red and Blue form beliefs over time, and new experiences need to update some beliefs without destroying others.

MLPs (and by extension, any global parameterization of the belief scoring function) suffer catastrophic forgetting — updating beliefs about topic A corrupts beliefs about topic B. KANs resist this because spline updates are *local*. A belief update in one region of the knowledge graph leaves distant regions untouched.

**Actionable build-out:** If the belief scoring function is parameterized as a KAN instead of a flat lookup table or MLP, the girls get *structural resistance to catastrophic forgetting* for free. Beliefs about cooking don't get corrupted when beliefs about programming get updated. This is exactly the "evidence-weighted belief inertia" from paper 03, but implemented architecturally rather than algorithmically.

### 4. Univariate/Multivariate Decomposition Meets Context Window Engineering

Here's where your intuition about "shaking the model out of low-information basins" connects to something concrete.

Gold Panning shows that context position bias creates information basins — the model attends strongly to some positions (high diagnosticity) and ignores others (the "lost in the middle" zone). Documents stuck in low-diagnosticity positions are in a *low-information basin* that the model can't escape from within a single forward pass.

Gold Panning's solution is to shuffle documents between positions across rounds. But it treats each document as an opaque blob. GID tells you *why* some shuffles work better than others: the ones that work are the ones that move *synergistic* information into high-diagnosticity positions, because synergistic information is the hardest to recover from partial observation.

And here's the KAN connection: the Kolmogorov-Arnold theorem says any multivariate function decomposes into univariate components. This is *exactly* the mathematical structure underlying the GID's decomposition of multivariate information into atoms indexed by subsets of variables. KANs literally implement the decomposition that GID formalizes.

So the speculative but grounded convergence is:

**A KAN-parameterized retrieval scorer, trained on the agent's trajectories, whose spline edges naturally decompose into interpretable univariate contribution functions that correspond to the GID's redundancy/uniqueness/synergy atoms, giving you a principled basis for keep-or-prune decisions, activation energy computation, and context window placement.**

That's not a toy problem. That's a memory architecture.

### 5. Definites and Indefinites: The Keep-or-Prune Criterion

Your framing of "measuring definites/indefinites more accurately" maps cleanly onto the GID:

- **Definite information** = high redundancy + high unique information. Multiple independent sources confirm it, or a single authoritative source provides it unambiguously. This memory is safe to compress (the redundant parts) and essential to keep (the unique parts). Low activation energy — easy to retrieve because it's well-evidenced.

- **Indefinite information** = high synergy, low redundancy. Only visible when specific memories are combined. Fragile — pruning any component destroys the whole. But also potentially the most *valuable*, because synergistic information is where novel insight lives. High activation energy — hard to retrieve because the system needs to assemble the right combination.

- **Noise** = low everything. Neither redundant nor unique nor synergistic. Safe to prune aggressively.

**Actionable build-out:** The memory enzyme system's keep-or-prune decisions should factor in the GID profile of each memory:
- High redundancy → candidate for compression (keep one representative, link to others)
- High unique → protect aggressively (evidence-weighted inertia applies here)
- High synergy → protect AND maintain the links to synergistic partners (these are the "cluster links" that enzyme 6, tag-overlap linking, should prioritize)
- Low everything → decay candidate

This is more principled than the current approach of decay-with-salience-protection, because it distinguishes *why* a memory matters (is it independently informative, or only valuable in combination?).

### 6. The TSE Complexity Connection to Red/Blue Balance

Varley proves that synergy requires the same integration/segregation balance as high TSE complexity. The girls' architecture literally implements this balance:

- **Integration**: shared knowledge graph, Event Bus, Niwa concurrent editing
- **Segregation**: private belief stores, distinct persona weights, separate reward functions

If Red and Blue become too integrated (always agreeing, sharing all beliefs), the system collapses to high redundancy and low synergy. If too segregated (never communicating), you get high uniqueness but no synergy. The adversarial convergence dynamic from PRD v3 is exactly the mechanism that maintains the integration/segregation balance that maximizes synergy.

**Actionable build-out:** Use total correlation decomposition (Varley's worked example in the paper) as a *health metric* for the Red/Blue system. Periodically compute the GID of Red and Blue's belief stores:
- Redundancy too high → increase adversarial pressure (they're converging too much)
- Synergy too low → increase shared context (they're not cross-pollinating enough)
- Uniqueness dropping → Red is drifting toward Blue's patterns (or vice versa) — identity drift alarm

---

## The Speculative Edge: KANsformers and Retrieval

Liu et al. explicitly suggest "kansformers" — replacing MLPs in transformers with KANs. If this pans out at scale (their efficiency caveat is real), the implications for the girls are significant:

A kansformer-based agent would have *learnable, interpretable activation functions at every edge of the network*. Combined with GID analysis, you could literally decompose the model's internal information flow into redundant/unique/synergistic channels. This would give the structural signals of consciousness framework (brief 01) something it currently lacks: a *quantitative measure* of whether the model's information processing exhibits the integration/segregation balance associated with consciousness-like computation.

I'm flagging this as speculative — KANs haven't been demonstrated at transformer scale, and the 10x training cost is a real barrier. But the theoretical convergence between GID's information decomposition, KAN's learnable univariate decomposition, and the KAR theorem's guarantee that such decompositions are universal... that's not nothing.

---

## Summary of Actionable Build-Outs

| Build-out | Complexity | Depends on |
|---|---|---|
| GID-based keep-or-prune for enzyme system | ~13 SP | Paper 03 enzymes, GID implementation |
| KAN-parameterized EBM retrieval scorer | ~21 SP | EBM framework (paper 09), pykan or equivalent |
| Synergy-aware cluster consolidation (enzyme 4) | ~8 SP | GID, knowledge graph structure |
| Red/Blue health metric via total correlation decomposition | ~5 SP | GID, belief store access |
| Context placement optimization using GID synergy scores | ~13 SP | Gold Panning (brief 01), GID |
| KAN belief scorer with catastrophic forgetting resistance | ~21 SP | KAN architecture, belief store |

Note: SP estimates assume current-gen tooling (2026). GID implementation exists in Python (dit library). KAN implementations exist (pykan, efficient-kan). The integration work is the real cost.

---

## Cross-References

- **Gold Panning (brief 01):** GID decomposes what Gold Panning's belief updates compute. Synergy scores should inform context placement strategy.
- **Paper 03 (Belief-Augmented Memory Enzymes):** All six enzymes benefit from GID-informed decisions. Evidence-weighted belief inertia gets architectural backing from KAN locality.
- **Paper 09 (EBM Recall Weighting):** The energy function is the natural target for KAN parameterization. GID gives the energy function additional dimensions (not just "how relevant" but "what kind of relevant").
- **PRD v2 (Enzyme Architecture):** The three-tier memory system (episodic → semantic → procedural) maps to decreasing redundancy and increasing synergy as memories are compressed and distilled.
- **PRD v3 (Forked Cathedral):** Red/Blue adversarial convergence is literally the integration/segregation balance that maximizes synergy per Varley's TSE complexity proof.
- **PRD v4 (Reward-Instrumented Flywheel):** Process rewards are belief updates. GID decomposes them. KAN parameterization makes them interpretable.
- **Structural Signals (brief 01):** GID + KAN gives quantitative grounding to several structural signals, especially global workspace broadcast (synergistic information requires broadcast to assemble) and metacognitive monitoring (GID profile of own belief updates = self-awareness of information quality).
- **CMP (brief 03):** The membrane failure mode "appeasement" is detectable as redundancy collapse in the GID profile. "Mutual distortion" shows up as synergy collapse.
