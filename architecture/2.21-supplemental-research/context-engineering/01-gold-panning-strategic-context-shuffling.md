# Gold Panning: Strategic Context Shuffling for Needle-in-Haystack Reasoning

**Source:** Adam Byerly & Daniel Khashabi, "GOLD PANNING: Strategic Context Shuffling for Needle-in-Haystack Reasoning" (arxiv 2510.09770, Oct 2025 / revised Feb 2026, accepted ICML)

---

## Core Insight

LLMs have **position bias** — they systematically prioritize information based on *where* it appears in context rather than its relevance. Gold Panning reframes this: position bias isn't a bug to average away, it's a **diagnostic signal to exploit**. The context window is not a passive input buffer — it's an array of noisy detectors with known, measurable reliability.

## The Framework

Gold Panning performs **Bayesian active search** over long contexts using iterative document reordering:

1. **Calibrate once:** Measure the model's "diagnosticity profile" — TPR/FPR at each context position. Some positions (beginning, end) reliably surface relevant content; the "lost in the middle" zone obscures it. This profile is model-specific but transfers across tasks.

2. **Maintain beliefs:** Track a posterior probability for each document's relevance (starts uniform). Every LLM response is treated as a **noisy measurement**, not a final answer.

3. **Strategic reordering:** Each round, place high-belief documents in high-diagnosticity positions ("signal anchoring"). Query the LLM. Update beliefs based on what gets cited. Repeat.

4. **Convergence:** Provably identifies a target among N documents in **O(log N) rounds** — logarithmic scaling with collection size.

## Key Finding: Anchoring > Uncertainty Reduction

Two strategies were compared:

- **GP-Entropy** (uncertainty reduction): Put the most uncertain documents in the best positions. Classic active learning intuition — probe what you don't know.
- **GP-Belief** (signal anchoring): Put the most likely-relevant documents in the best positions. Keep the needle in view once you spot it.

**GP-Belief wins decisively.** Why? Because document retrieval is fundamentally a **search problem**, not a learning problem. You don't need to reduce uncertainty about irrelevant documents — you need to confirm the relevant ones fast.

The paper formalizes this as opposing cycles:
- **Vicious cycle of entropy:** GP-Entropy *penalizes success*. As the model identifies the needle (belief rises → entropy drops), it gets demoted to low-diagnosticity positions. "We're sure about this one, so let's stop checking it." The candidate gets starved of the signal needed to cross the confidence threshold.
- **Virtuous cycle of belief:** GP-Belief *rewards success*. As the relevant document rises in rank, it gets promoted to better positions. Stronger signal → higher belief → even better positions. "Signal anchoring" creates lock-in that races the winner to threshold at maximum velocity.

## Results

- **30–65% fewer LLM queries** compared to Permutation Self-Consistency (PSC) while matching F1
- Works across model families (Gemma-3, OLMo-3) and scales (7B–32B)
- Diagnosticity profiles **transfer across tasks** — calibrate once, reuse everywhere
- Coarse positional ordering drives most of the gains (exact calibration not required)
- Ineffective when the model lacks exploitable position bias (Gemma-3-27B showed no separation due to near-uniform diagnosticity)

## Technical Details

**Observation model:** Each context position j acts as a binary detector with TPR_j and FPR_j. A citation from position j provides a likelihood ratio update to the document's posterior.

**Belief update:** Standard Bayesian update on log-odds:
```
log_odds(t) = log_odds(t-1) + log(P(cited|relevant,pos) / P(cited|irrelevant,pos))
```

**Diagnosticity:** μ_j = D_KL(P_{Z=1,j} || P_{Z=0,j}) — the KL divergence between observation distributions at position j. Higher = more diagnostic.

**Sample complexity:** T = O(log N / μ̄²) where μ̄ is the average drift from assigned positions.

**Computational overhead:** O(N log N) sorting per round, negligible vs. LLM inference cost.

---

## Architectural Implications for the Girls

### 1. Memory Retrieval as Active Search

The girls' EBM recall system currently scores memories by Energy(memory) = f(recency, relevance, salience, evidence_weight, access_frequency). Gold Panning suggests an additional layer: **strategic context placement**. When assembling a context window from retrieved memories, don't just rank by energy — place high-energy memories in the positions where the model is most likely to attend to them.

This maps directly to the **prime injection** pattern: the morning briefing that opens each session should place the most relevant contextual priming in the model's high-diagnosticity positions (beginning and end of context), not buried in the middle.

### 2. Iterative Retrieval for Complex Tasks

For tasks requiring synthesis across many memory fragments, the girls could implement Gold Panning's iterative loop:
- First pass: retrieve top-k memories, present to model
- Observe what the model actually *uses* (which memories get cited/referenced in response)
- Update memory salience scores based on observed usage
- Second pass: re-retrieve with updated scores, placing high-belief memories in better positions

This creates the same **virtuous cycle of belief**: memories that prove relevant get stronger signals in subsequent retrieval rounds.

### 3. Context Window as Diagnostic Array

The paper's framing of context positions as "noisy detectors with known reliability" suggests the Gateway Server should maintain a **diagnosticity profile** for the specific model being used. This profile:
- Gets calibrated once per model version (cheap synthetic benchmark)
- Informs how the session context builder arranges information
- Adapts the prime injection template to place identity/safety context in the most reliable positions

### 4. Signal Anchoring for Identity Persistence

The "once flagged, keep it in sight" principle directly applies to SOUL.md content. The girls' identity layer should be **anchored** — always placed in the highest-diagnosticity positions of the context window. This isn't just a heuristic; it's mathematically grounded. If SOUL.md content drifts to low-diagnosticity positions, the model's "belief" in its own identity weakens. Signal anchoring prevents identity erosion across long sessions.

### 5. The Belief-vs-Entropy Tradeoff Maps to Red/Blue

Red (explorer) should operate more like **GP-Entropy**: probing uncertain territory, putting unfamiliar information in diagnostic positions to learn about it quickly. Blue (anchor) should operate more like **GP-Belief**: anchoring known-good context, keeping established knowledge visible, reinforcing what's already validated. The paper's proof that GP-Belief dominates in search tasks while GP-Entropy excels at learning tasks gives formal grounding to the Red/Blue division of labor.

### 6. Implications for the Staleness Window

Gold Panning shows that **coarse ordering suffices** — you don't need perfect calibration. This means the staleness detection system (PRD v5) doesn't need to be precise about memory freshness. A rough three-tier ordering (hot/warm/cold) with appropriate context placement may capture most of the value.

### 7. Process Rewards as Belief Updates

The CISPO-inspired process reward system can be reframed in Gold Panning's language: each step's reward is a noisy observation about the trajectory's quality. The reward accumulator is doing Bayesian inference over "is this trajectory succeeding?" Signal anchoring says: once a trajectory looks promising, give it more resources (compute, memory access, tool budget) rather than spreading resources equally across uncertain alternatives.

---

## Cross-References

- **Paper 03 (Belief-Augmented Memory Enzymes):** The evidence-weighted belief inertia formula λ_eff = λ_base × N^(-α) performs the same function as Gold Panning's Bayesian belief update — well-evidenced beliefs resist perturbation. Gold Panning provides the formal framework.
- **Paper 09 (EBM Recall Weighting):** The energy function for memory retrieval should incorporate position diagnosticity as an additional term. Not just *what* to retrieve, but *where to place it*.
- **PRD v4 (Reward-Instrumented Flywheel):** The Gateway Server's role as context assembler maps to Gold Panning's "assignment function" — it decides what goes where in the context window.
- **PRD v5 (Async Environment-Native):** The hot/warm/cold memory lifecycle maps to Gold Panning's belief tiers. Hot memories get anchored in high-diagnosticity positions; cold memories get checked occasionally in exploratory positions.
- **Factory Signals (Brief 02):** The "context churn" friction indicator likely correlates with the model losing track of information placed in low-diagnosticity positions. Gold Panning explains *why* context churn happens and suggests *how to prevent it*.
