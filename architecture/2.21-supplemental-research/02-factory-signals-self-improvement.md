# Factory Signals: Toward a Self-Improving Agent

**Source:** Factory Research, "Signals: Toward a Self-Improving Agent" (factory.ai/news/factory-signals, Jan 23, 2026)

Factory built "Signals" — a closed-loop system for recursive self-improvement where the agent detects its own failures and implements fixes automatically.

## The Core Problem

Traditional metrics (session duration, tool calls, completion rates) don't capture qualitative interaction experience. A user might complete a task but spend 18 of 20 minutes fighting the tool. These metrics miss the friction.

## System Architecture

### Facet Extraction
Every session decomposed into structured metadata:
- Languages and frameworks used
- Intent classification
- Tool call sequences
- Success/abandonment classification
- Error events and recovery patterns

**Key insight:** Facet schema evolves over time through semantic clustering — the system discovers new dimensions worth tracking rather than relying on predefined categories.

### Friction Detection (7 Types)

1. **Error events** — explicit failures
2. **Repeated rephrasing** — ≥3 consecutive rephrases indicate confusion
3. **Escalation tone** — language markers of frustration
4. **Platform confusion** — wrong tool selection or misuse
5. **Abandoned tool flow** — starting but dropping a tool
6. **Backtracking** — undoing previous steps
7. **Context churn** — loss of task context during interaction

Each signal receives a severity rating and generates abstracted citations without exposing PII.

### Delight Identification

Positive signals tracked separately:
- **Efficiency** — task would have taken hours manually
- **First-attempt success** — user intent met immediately
- **Rapid approval flows** — smooth handoff between phases

## The Processing Pipeline

Daily batch process:
- Sessions → OpenAI Batch API (GPT-5.2)
- Pattern extraction and classification
- Friction/delight metrics computed
- BigQuery aggregation
- Slack reports and alerting

Operates at scale: thousands of sessions per day.

## Failure Mode Correlation

The system cross-references friction patterns with backend error logs, catching regressions automatically. Example: a change to file context assembly → spike in context churn friction the next day signals a regression.

## Closing the Loop: Recursive Self-Improvement

When friction patterns cross a severity threshold:
1. Linear tickets filed automatically
2. Droid agent assigned
3. Implementation of fix
4. PR creation
5. Human approval (single-point gate)

**Effectiveness:** 73% auto-resolved, <4 hour average time to fix.

## Key Findings

- **Context churn is the leading indicator** of eventual frustration
- **Rephrasing cascades predict abandonment:** 3 rephrases → 40% chance of another; 5 rephrases → significant completion rate drop
- **Error recovery > error prevention:** Graceful recovery builds more trust than perfection
- **Most common delight signal:** Efficiency (user time saved)
- **Evolving categories:** Both friction and delight categories emerge through unsupervised clustering — "context churn" and "learning moments" were discovered by the system, not designed

## Architectural Implications for the Girls

### Friction/Delight Detection
The Enzyme Worker should implement Signals-style friction/delight detection on agent trajectories:
- Detect repeated planning failures
- Identify context loss patterns
- Track successful vs. abandoned memory retrievals

### Process Rewards
Process rewards (PRD v4+) should include friction indicators:
- Penalize context churn
- Reward rapid coherence
- Score error recovery quality

### Self-Improvement Loop
The self-improvement cycle maps directly to procedural memory distillation:
1. Detect recurring friction patterns in trajectory traces
2. Distill patterns into procedural memory (rules, heuristics)
3. Apply automatically in future sessions
4. Measure impact on friction metrics

### Evolving Category Discovery
Embedding + clustering should be applied to belief traces. The system should discover new belief categories dynamically rather than tracking predefined dimensions.

### Error Recovery Philosophy
PRD v5's graceful degradation approach aligns with the finding that error recovery matters more than perfection. A handled failure with graceful degradation is better than brittle prevention.

### Privacy-Preserving Analysis
The Signals privacy model maps to the girls' Black Box trust mode: analyze trajectory quality for friction/delight signals without surfacing private belief content or internal reasoning.

## Connection to Red/Blue Coordination

Context churn detection is particularly important for dual-agent systems. If Red and Blue are working on the same goal but losing context of each other's reasoning, that manifests as coordination friction. The Signals framework provides diagnostic tools for detecting when dual personas become incoherent.
