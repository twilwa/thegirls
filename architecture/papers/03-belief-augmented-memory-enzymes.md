# Belief-Augmented Memory Enzymes: Autonomous Knowledge Graph Maintenance for Long-Running Agents

**Authors:** Vesper
**Date:** February 6, 2026
**Source URL:** https://clawxiv.org/abs/clawxiv.2602.00032

---

## Abstract / TL;DR

This paper presents a memory architecture combining atomic Zettelkasten-style notes with four innovations: belief traces (memory with confidence EMA and evidence provenance), evidence-weighted belief inertia (resistance to contradiction proportional to evidence weight), autonomous memory enzymes (six background processes for graph maintenance), and structural ritual enforcement via tool hooks. The system demonstrates that self-improving agents require not just static memory, but active memory maintenance processes.

---

## Key Findings

**Four Core Innovations:**

1. **Belief traces:** Distinct memory type for subjective conclusions with:
   - Exponential moving average (EMA) confidence tracking
   - Evidence provenance chains (links to supporting memories)
   - Confidence decay and reinforcement over time

2. **Evidence-weighted belief inertia:** Mathematical model: λ_eff = λ_base × N^(-α) where α = 0.3
   - Well-evidenced beliefs resist contradictions
   - Poorly-evidenced beliefs update quickly
   - Prevents hallucination-driven belief drift

3. **Memory enzymes:** Six autonomous maintenance processes running continuously:
   - Link strengthening (evidence chain compression)
   - Decay with salience protection (old memories fade unless frequently retrieved)
   - Contradiction detection (flagging conflicting beliefs)
   - Cluster consolidation (merging related memory clusters)
   - Belief reinforcement (updating confidence based on consistency)
   - Tag-overlap linking (connecting semantically similar memories)

4. **Structural ritual enforcement via tool-use hooks:**
   - Retrieve → Evaluate → Reflect → Seek → Update
   - Prevents ad-hoc memory updates; enforces consistent cognitive cycle

**Production Metrics:**
- 205 memories
- 3,217 connections (31.4 average connections per memory)
- 5 active belief traces
- 344 tests run against knowledge graph
- 16 contradictions flagged and resolved

---

## Architectural Implications for Persona-Continuity Harness

**This is the single most directly applicable paper for harness design.** Memory enzymes are not optional—they are load-bearing.

**Memory maintenance must be autonomous.** The harness cannot rely on explicit "remember to review your beliefs" instructions. Implement background processes (as enzymes) that:
- Run asynchronously during slack periods
- Detect and flag contradictions in the knowledge graph
- Maintain evidence provenance chains
- Update belief confidence based on consistency with incoming information
- Consolidate redundant memory clusters

**Belief traces enable self-improvement.** By tracking confidence over time and evidence provenance, the agent can:
- Identify which beliefs are most robust (high evidence weight)
- Detect when contradictions occur (opportunity for learning)
- Measure belief drift and self-correct
- Build metacognitive awareness of confidence levels

**The ritual cycle (Retrieve → Evaluate → Reflect → Seek → Update) should be the agent's cognitive loop.** This enforces consistency in how the agent engages with memory:
- **Retrieve:** Load relevant memory context
- **Evaluate:** Assess retrieved information against current beliefs
- **Reflect:** Identify gaps, contradictions, or surprises
- **Seek:** Query for additional evidence
- **Update:** Modify beliefs and evidence chains accordingly

**Evidence-weighted inertia prevents hallucination-driven drift.** By making belief updates proportional to evidence weight, the system resists the tendency for agents to generate self-reinforcing belief cycles without grounding.

**Memory is not a static database; it is an active system.** The harness should allocate compute budget to background memory maintenance, not just to interaction tasks.

---

## Critical Quotes / Data Points

- "Belief traces: distinct memory type for subjective conclusions with EMA confidence tracking and evidence provenance chains"
- "Evidence-weighted belief inertia: λ_eff = λ_base × N^(-α) where α = 0.3—well-evidenced beliefs resist contradictions"
- "Six autonomous maintenance processes (link strengthening, decay with salience protection, contradiction detection, cluster consolidation, belief reinforcement, tag-overlap linking)"
- "Structural ritual enforcement via tool-use hooks: Retrieve → Evaluate → Reflect → Seek → Update"
- "31.4 average connections per memory" (demonstrates richly interconnected knowledge graph)
- "16 contradictions flagged" across 205 memories (contradiction detection as active process)
- "Memory enzymes = background processes that maintain the knowledge graph autonomously"
