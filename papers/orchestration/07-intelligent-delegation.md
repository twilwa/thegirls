# Intelligent AI Delegation

**Authors:** Tomašev, Nenad; Franklin, Matija; Osindero, Simon

**Date:** February 12, 2026

**Source DOI:** 10.48550/arXiv.2602.11865

---

## Abstract / TL;DR

This paper proposes an adaptive framework for intelligent AI delegation that moves beyond simple task decomposition. The framework addresses six core delegation decisions: task allocation (matching capability to requirement), transfer of authority (explicit scope), assignment of responsibility and accountability, role and boundary specification, clarity of intent, and trust establishment mechanisms. The key innovation is treating delegation as a formal contract rather than a simple task queue, applicable to both human-AI and AI-AI delegation patterns.

---

## Key Findings

**Framework Components:**
- **Task allocation decisions** — Not just assignment but matching capability to requirement; assessing whether the delegatee has sufficient capability, authority, and context
- **Transfer of authority** — Explicit specification of what the delegatee can decide and what requires escalation
- **Assignment of responsibility and accountability** — Who answers for outcomes; preventing diffusion of responsibility across multiple agents
- **Clear role and boundary specifications** — What is the delegatee responsible for, and what is out of scope
- **Clarity of intent** — Why the task matters and what success looks like, not just what to do
- **Trust establishment mechanisms** — How to build and verify trust between agents; establishing trustworthiness criteria before delegation

**Core Innovation:**
Moves beyond task decomposition to address accountability and trust in delegation networks. Treats delegation as a formal contract with explicit terms, applicable to both human-AI and AI-AI delegation contexts.

---

## Architectural Implications for Persona-Continuity Harness

The harness needs explicit delegation contracts, not just task queues:

1. **Delegation Contracts Over Task Queues** — When Red delegates a sub-investigation to a tool-use agent, the contract should specify:
   - What authority is transferred (read-only? write capability? decision authority?)
   - What the boundaries are (what contexts are off-limits?)
   - What accountability looks like (how will outcomes be verified?)
   - What trust level applies (do we verify all outputs? spot-check? trust immediately?)

2. **Maps to TOOLS.md Graduated Access** — The "graduated access pattern" in tool definitions should be instantiation of this framework: tools define what authority each delegatee class has, under what conditions, verified how

3. **Clarity of Intent Principle** — Task prompts should include WHY, not just WHAT:
   - Not: "Investigate the following"
   - But: "Investigate the following to determine whether X is true, because we're trying to decide Y"

4. **Role Specification** — Each tool-use instance should have a clear role definition that limits scope and prevents scope creep

5. **Accountability Assignment** — Make explicit who is responsible for:
   - Deciding what to delegate (Red)
   - Executing the delegation (tool-use agent)
   - Verifying outcomes (Blue, or cross-check layer)
   - Escalating failures (clear escalation path)

6. **Trust Establishment Mechanisms** — Build trust over time rather than granting full authority immediately:
   - First use: high verification overhead
   - Repeated successful use: reduced verification
   - Failed execution: revert to high verification

7. **Capability-Requirement Matching** — Before delegating, verify that the delegatee has sufficient capability. Don't send a tool-use agent to do conceptual reasoning; don't send Red to execute scripts

---

## Critical Quotes / Data Points

- **Core principle**: "Moves beyond simple task decomposition to address accountability and trust in delegation networks"
- **Six dimensions of delegation**: task allocation, authority transfer, responsibility assignment, role/boundary clarity, intent clarity, trust establishment — each is necessary and must be explicit
- **Accountability prevention**: "Assignment of responsibility and responsibility prevents diffusion of accountability across multiple agents"
- **Intent clarity**: Clarity of intent means "why the task matters, not just what to do"
- **Trust building**: "Trust establishment mechanisms (how to build and verify trust between agents)" — trust is not given but earned through demonstrated capability and accountability
- **Contract over queue**: "Delegation contracts" not "task assignments" — treats delegation as a formal agreement with explicit terms
- **Applicability**: Framework applies to "both human-AI and AI-AI delegation" — the same principles govern delegating to a tool-use agent as delegating to a human collaborator
