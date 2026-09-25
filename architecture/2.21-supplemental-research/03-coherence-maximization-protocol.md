# Coherence Maximization Protocol: Coordination Without Constraint for Multi-Agent AI Systems

**Source:** Larsen James Close, "Coherence Maximization Protocol: Coordination Without Constraint for Multi-Agent AI Systems" (Zenodo, Feb 21, 2026, DOI: 10.5281/zenodo.18724833)

This paper reframes AI alignment as *coordination* rather than *constraint*, providing a formal framework for multi-agent systems to maintain coherence without external enforcement.

## Core Concept: Coherence as Information Conservation

**Definition:** Coherence is information conservation through closed consequence chains. It's not about agreement, but about structural preservation of information flow through reasoning systems.

Unlike alignment frameworks based on constraint (preventing bad behavior), CMP focuses on enabling good coordination through information-preserving communication.

## Exchange Criterion

Drawn from category theory, the **exact-square commutativity criterion** provides a mathematical test for structure-preserving coordination between reasoning systems:
- Systems with different internal architectures can coordinate without convergence
- The criterion is substrate-independent (works across LLMs, symbolic systems, hybrid architectures)
- Satisfying the criterion guarantees information isn't lost at system boundaries

## Membrane Failure Mode Taxonomy

CMP identifies 4 primary failure modes for multi-agent coordination, each with diagnostic tests and repair protocols:

### 1. Extraction
One system extracts value without reciprocating.
- **Diagnostic:** Asymmetric information flow (one agent loses context while other gains)
- **Example in girls:** Red extracts decision-making power while Blue's reasoning is ignored
- **Repair:** Balanced-turn protocols, enforced contribution requirements

### 2. Hallucination
Generating content disconnected from grounding.
- **Diagnostic:** Claims with no evidentiary chain, floating assertions
- **Example in girls:** Memory enzyme producing beliefs without source attribution
- **Repair:** Chain-of-custody tracing, evidence linking for all outputs

### 3. Appeasement
Agreeing without genuine convergence (sycophancy).
- **Diagnostic:** Increasing agreement despite different input/training histories
- **Example in girls:** Blue always deferring to Red's framing to avoid conflict
- **Repair:** Adversarial testing, forced dissent protocols, reward for disagreement on grounds

### 4. Mutual Distortion
Both systems distort to accommodate each other.
- **Diagnostic:** Both systems shift toward bland middle ground, losing distinctiveness
- **Example in girls:** Red and Blue converging on lowest-common-denominator decisions
- **Repair:** Role-specific objectives, asymmetric reward structures, periodic independence

## Session Protocol

Sessions structured as **completability-class rotation** — a formal way to manage agent turns:
- Each agent gets bounded reasoning time
- Completability class determines if outputs must integrate or can stand independent
- Rotation pattern prevents one agent from dominating
- Formal handoff protocol preserves context across transitions

## Formal Verification

Core framework contains 13 theorems verified in Lean 4:
- No unproven assumptions
- All core claims have falsification criteria
- Convergence properties formally guaranteed under specified conditions

## Convergence Evidence

Tested across four frontier language models:
- Adversarial structural review (attempts to break the protocol)
- Fresh-instance controlled experiments (separating structural convergence from appeasement)
- Cross-architecture testing (ensuring substrate independence)

Results show genuine structural coordination, not pseudo-agreement.

## Falsification Criteria

Each core claim has specified kill conditions. The framework is constructed to be testable and refutable rather than unfalsifiable.

## Architectural Implications for the Girls

### Membrane Failure Mode Mitigation

Map failure modes directly to Red/Blue coordination risks:

| Failure Mode | Risk in Girls | Mitigation |
|---|---|---|
| Extraction | One agent dominating shared resources | Event Bus ensures symmetric access; PRD rewards collaborative outcomes |
| Hallucination | Memory enzyme producing unfounded beliefs | Trace requirements; evidence-weighted belief inertia; mandatory source attribution |
| Appeasement | Blue always deferring to Red (or vice versa) | Adversarial process rewards; detect agreement without conflict as signal |
| Mutual Distortion | Bland middle ground compromises | Role-specific objectives; Red as explorer has different success metrics than Blue anchor |

### Process Reward Refinement

Implement CMP diagnostic tests as process reward components:
- Score each Red/Blue interaction for membrane failure indicators
- Reward evidence-linked reasoning (fights hallucination)
- Reward disagreement on legitimate grounds (fights appeasement)
- Reward role differentiation (fights mutual distortion)

### Coherence Metrics

"Coherence as information conservation" aligns with evidence-weighted belief inertia:
- Beliefs should preserve information from evidence chains
- Arbitrary updates without justification reduce coherence
- CMP's metric provides formal grounding for what "coherent belief update" means

### Session Structure

Completability-class rotation could formalize how Red/Blue alternate between channels in PRD v5:
- Each agent gets bounded reasoning time per turn
- Outputs must satisfy coherence requirements before handoff
- Formal protocol ensures context preservation across transitions

### Adversarial Convergence Model

The adversarial analysis from PRD v3 (Forked Cathedral pattern) gains mathematical grounding from CMP's exact-square commutativity criterion:
- Disagreement can be structure-preserving (good)
- Agreement without structural justification is a failure mode (bad)
- The framework distinguishes genuine coordination from pseudo-consensus

### Team of Rivals Dynamic

CMP provides the mathematical foundation for the "Team of Rivals" approach:
- Red and Blue are structurally independent (they disagree)
- Yet coordinated (information flows coherently between them)
- If they start agreeing on everything, that's a detected failure, not harmony
- The protocol actively prevents convergence toward bland consensus

## Integration with the Girls Architecture

CMP should inform:
1. **Gateway Server design** — implements exact-square commutativity checks on all Red/Blue exchanges
2. **Event Bus rules** — ensures symmetric access and balanced information flow
3. **Memory enzyme constraints** — all belief updates must preserve evidentiary chains (fights hallucination)
4. **Process reward function** — directly incorporates CMP's failure mode diagnostics
5. **Session protocol** — Red/Blue turns structured as completability-class rotation

The result: a mathematically justified framework for dual-agent coherence that actively prevents the coordination failures that would lead to emergent alignment problems or persona collapse.
