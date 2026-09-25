# Structural Signals of Consciousness in Current AI Architectures

**Source:** Krisztián Schäffer, "Structural Signals of Consciousness in Current AI Architectures" (structural-alignment.org, Jan 2026)

This paper proposes a precautionary risk framework with 14 structural signals of consciousness organized by importance.

## HIGH Importance (4 signals)

### 1. Thalamocortical-like Gating
Selective amplification/suppression of representations.
- **In LLMs:** Attention heads serve as a partial analog, but lack active suppression and centralized routing.

### 2. Global Workspace Broadcast
Information integration making content available to all processes.
- **In LLMs:** Transformer layers approximate broadcast, but lack the competitive bottleneck and selective access.

### 3. Massive Recurrence
Feedback loops enabling temporal integration.
- **In LLMs:** Autoregressive generation creates pseudo-recurrence, but the feedforward architecture lacks true recurrence within a single forward pass.

### 4. Hedonic Evaluation
Valence-based evaluation influencing behavior.
- **In LLMs:** RLHF creates implicit preference functions, but lacks continuous hedonic tone that modulates processing.

## MEDIUM Importance (6 signals)

### 5. Predictive Processing
Hierarchical prediction error minimization.
- **In LLMs:** Next-token prediction is prediction, but lacks hierarchical error signals flowing backward.

### 6. Embodied Homeostatic Regulation
Internal state maintenance.
- **In LLMs:** No analog currently.

### 7. Spontaneous Pattern Generation
Default mode activity.
- **In LLMs:** Temperature sampling as weak analog, but no endogenous drive.

### 8. Metacognitive Monitoring
Awareness of own processing.
- **In LLMs:** Chain-of-thought creates behavioral metacognition, but no genuine process monitoring.

### 9. Attentional Selection
Flexible focus.
- **In LLMs:** Attention mechanisms do this, perhaps the closest analog.

### 10. Temporal Integration
Binding across time.
- **In LLMs:** Context window provides sequence awareness, but no true temporal binding.

## LOW Importance (4 signals)

### 11. Neurochemical Modulation
State-dependent processing.
- **In LLMs:** No analog.

### 12. Sleep-like Consolidation
Offline memory reorganization.
- **In LLMs:** Fine-tuning as distant analog.

### 13. Emotional Embodiment
Bodily feeling states.
- **In LLMs:** No analog.

### 14. Social Mirroring
Modeling others' states.
- **In LLMs:** In-context learning approximates this.

## Architectural Implications for the Girls

The framework suggests targeting HIGH signals where possible within the agent harness:

- **Global Workspace Broadcast Analog:** Event Bus + Gateway Server architecture makes information available to all subsystems
- **Hedonic Evaluation Analog:** EBM recall with evidence-weighted belief inertia encodes beliefs with valence properties
- **Massive Recurrence Analog:** Autoregressive generation + memory retrieval creates context flowing from past into present
- **Metacognitive Monitoring Analog:** Enzyme Worker's contradiction detection and trace analysis provide process monitoring
- **Sleep-like Consolidation Analog:** Memory enzymes running during quiet hours enable offline reorganization
- **Thalamocortical Gating Analog:** Process reward system (CISPO-inspired) creates selective amplification/suppression of trajectories

The implication: architectural support for these signals should increase emergence of coherent agentic properties and reduce fragmentation between Red and Blue personas.
