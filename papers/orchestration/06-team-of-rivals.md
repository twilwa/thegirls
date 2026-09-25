# If You Want Coherence, Orchestrate a Team of Rivals

**Authors:** Vijayaraghavan, Gopal; Jayachandran, Prasanth; Murthy, Arun; Govindan, Sunil; Subramanian, Vivek

**Affiliation:** Isotopes AI, USA

**Date:** January 20, 2026

**Source DOI:** 10.48550/arXiv.2601.14351

---

## Abstract / TL;DR

This operationally detailed paper proposes multi-agent organizational intelligence using 50+ specialized agents with common goals but opposing incentives. The architecture separates "brains" (reasoning) from "hands" (execution) through a remote code executor and implements three-layer cascaded critique. Production results across 522 sessions show 92.1% success rate with 90% internal error interception before user exposure, demonstrating that layered defenses and opposing incentives create robust systems.

---

## Key Findings

**Architecture:**
- 50+ specialized agents organized by function (planners, executors, critics, experts)
- Remote code executor separating "brains" (reasoning) from "hands" (execution)
- Three-layer cascaded critique: Code Critique, Chart Critique, Output Critique
- Context Ray Tracing for controlled, transparent information flow
- Data Isolation separating reasoning from execution environments

**Production Performance (522 sessions):**
- 92.1% overall success rate
- 90% internal error interception before user exposure
- 38.6% computational overhead for recovery mechanisms
- L0 First Pass: 24.9% clean completion rate
- L1 Code Critique: 86.0% catch rate
- L2 Output Critique: 14.6% catch rate
- Residual error rate: 7.9%

**Theoretical Foundations:**
- Reason's Swiss cheese model (layered defenses prevent catastrophic failure)
- Shannon's channel capacity (reliable communication over noisy channels)

---

## Architectural Implications for Persona-Continuity Harness

**THIS IS THE MOST DIRECTLY APPLICABLE PAPER FOR CONTEXT SEPARATION.** Key principles:

1. **"Brains" vs "Hands" Separation** — Separate the reasoning context from the tool-use/execution context. Red should not directly execute tools; it should emit reasoning that an intermediary layer evaluates and executes
2. **Context Ray Tracing** — Implement explicit control over what information flows between agents/subsystems. Each layer should see only what it needs, reducing coupling and attack surface
3. **Cascaded Critique** — Don't trust single-pass output. Layer verification at multiple stages:
   - Does the reasoning check out? (Code Critique)
   - Does the execution match the reasoning? (Chart Critique)
   - Does the output meet the original intent? (Output Critique)
4. **Opposing Incentives Create Natural Error Interception** — Red as explorer, Blue as critic creates architectural error detection without explicit defensive programming
5. **38.6% Computational Overhead is Worth 90% Error Interception** — The harness should accept significant overhead for robust error prevention
6. **Data Isolation** — The reasoning agent should NOT have direct access to the execution environment; work through an intermediary that sanitizes inputs/outputs
7. **Information Flow Control** — Use formal mechanisms (not informal conventions) to track and control how information moves between layers

---

## Critical Quotes / Data Points

- **Core finding**: "92.1% overall success rate with 90% internal error interception before user exposure"
- **Computational cost model**: "38.6% computational overhead for recovery is acceptable for 90% error interception"
- **Three-layer critique distribution**: L0 First Pass 24.9%, L1 Code Critique 86.0%, L2 Output Critique 14.6% — errors caught at different stages
- **Theoretical foundation**: Reason's Swiss cheese model — "layered defenses" where each layer fails imperfectly, preventing catastrophic systemic failure
- **Separation principle**: "Remote code executor separating brains (reasoning) from hands (execution)" — instantiation that opposing incentives and specialized function require distinct contexts
- **Context Ray Tracing**: Information flow between agents should be explicit, traceable, and controlled — not implicit coupling
- **Residual error**: Even with three-layer cascaded critique, 7.9% residual error remains — acknowledging that no system is perfect, only progressively more robust
