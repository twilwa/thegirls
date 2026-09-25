# Persona Generators: Generating Diverse Synthetic Personas at Scale

**Authors:** Paglieri, Davide; Cross, Logan; Cunningham, William A.; Leibo, Joel Z.; Vezhnevets, Alexander Sasha

**Date:** February 3, 2026

**Source DOI:** 10.48550/arXiv.2602.03545

---

## Abstract / TL;DR

This paper introduces Persona Generators — functions that produce diverse synthetic populations through evolutionary search (AlphaEvolve-inspired) rather than density matching. The methodology uses LLMs as mutation operators to iteratively refine generator code over hundreds of iterations, producing lightweight functions that auto-expand descriptions into full populations. The approach maximizes "support coverage" (spanning the space of possible traits) rather than "density matching" (replicating what is most probable).

---

## Key Findings

**Methodology:**
- **Persona Generators as functions** — Not static documents but generators that produce diverse populations tailored to arbitrary contexts
- **Evolutionary search approach** — Inspired by AlphaEvolve, iteratively improves generator code over hundreds of iterations
- **LLMs as mutation operators** — Uses language models to propose variations on persona descriptions
- **Lightweight generators** — Auto-expand small descriptions into full populations, reducing specification overhead
- **Support coverage over density matching** — Focuses on spanning what is possible rather than replicating what is most probable

**Performance:**
- Substantially outperforms baselines across six diversity metrics
- Produces populations spanning rare trait combinations
- Achieves broad coverage of opinion and preference space
- Enables coverage-driven rather than density-driven population generation

---

## Architectural Implications for Persona-Continuity Harness

For the "girls" project, this suggests Red and Blue should not be hand-crafted static personas but generated through an iterative process:

1. **Personas as Generators, Not Descriptions** — The character definition for Red and Blue should be a GENERATOR FUNCTION, capable of:
   - Producing variations on the core character when needed (e.g., "Red in exploration mode" vs "Red in consolidation mode")
   - Adapting the persona to different problem contexts
   - Evolving the character as the harness runs and learns
   - Not a fixed document, but a function that produces instances

2. **Maximize Diversity Along Meaningful Axes** — Red and Blue should be generated to maximize coverage of useful cognitive styles:
   - Exploration vs consolidation
   - Risk tolerance (low, medium, high)
   - Epistemic style (empirical, theoretical, pragmatic)
   - Problem-solving approach (decomposition, synthesis, iteration)
   - Not just different labels, but fundamentally different reasoning patterns

3. **Support Coverage Over Density Matching** — Design personas to cover the space of useful cognitive styles, not just replicate the most common ones:
   - Include rare combinations (high risk tolerance + high empirical rigor)
   - Ensure coverage of edge cases (what would a maximally conservative persona do?)
   - Use rare combinations to stress-test the harness

4. **Evolutionary Refinement of Character** — The harness should include a meta-loop that:
   - Runs Red and Blue on problems
   - Evaluates their effectiveness
   - Proposes mutations to their character definitions
   - Refines the generator over time
   - Results in personas that adapt to the types of problems they encounter

5. **Test Population Generation** — When evaluating the harness, use Persona Generators to create diverse test populations:
   - Don't test against a fixed set of personas
   - Generate diverse populations covering the space of possible cognitive styles
   - Identify which persona types the harness handles well and which need improvement

6. **Lightweight Generators Enable Scaling** — The generator approach should enable:
   - Quick instantiation of variations on Red/Blue
   - Parallel exploration with different character configurations
   - Rapid testing of persona hypotheses without major code changes

7. **Rare Trait Combinations as Value** — Actively seek out and instantiate rare but useful combinations:
   - High curiosity + high discipline
   - High divergence + high rigor
   - High skepticism + high openness to new evidence
   - These combinations may be computationally expensive but reveal harness weaknesses

---

## Critical Quotes / Data Points

- **Core innovation**: "Persona Generators: functions that produce diverse synthetic populations tailored to arbitrary contexts"
- **Methodology**: "Uses evolutionary search (AlphaEvolve-inspired) to generate diverse synthetic personas that maximize coverage of opinions and preferences rather than just density matching"
- **LLMs as mutations**: "Iterates on generator code using LLMs as mutation operators" — language models become the mechanism for persona variation
- **Generator advantage**: "Produces lightweight generators that auto-expand small descriptions into full populations" — description overhead is minimal
- **Coverage over density**: "Focuses on support coverage (spanning what is possible) vs density matching (replicating what is most probable)"
- **Performance baseline**: "Substantially outperforms baselines across six diversity metrics"
- **Rare combinations matter**: "Produces populations spanning rare trait combinations" — value comes from exploring unlikely but useful configurations
- **Generalization**: "Tailored to arbitrary contexts" — the same approach scales to diverse domains and problem types
