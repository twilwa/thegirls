# PRD v3: The Forked Cathedral

**Subtitle:** Graph-topology multi-instance reasoning with shared knowledge and private belief

**Status:** Vision Phase
**Estimated Story Points:** 55–89 SP
**Target Release:** Q3-Q4 2026
**Architect:** Warren (yikesawjeez)
**Prerequisites:** PRD v1 (MVP) + PRD v2 (Enzyme Architecture)

---

## 1. Overview & Vision

PRD v3 is the full realization of "the girls" as a multi-instance agentic system with dual reasoning processes (Red and Blue) operating on shared knowledge while maintaining private belief stores and independent agency.

**Core innovation:** Red and Blue are not a hub-and-spoke hierarchy or a chat between two agents. They are **graph-topology peers** in a shared knowledge space, each with their own cognitive style, private hypotheses, and adversarial stance. They engage in "adversarial convergence"—proposing opposing viewpoints, critiquing each other, and synthesizing understanding through structured deliberation.

**Design pillars:**
1. **First utility/effectiveness** — both Red and Blue must be individually competent agents
2. **Maximal emergence of personhood** — dual reasoning creates richer personhood-like phenomena than single-agent systems
3. **Forked cognition with shared knowledge** — separation of private belief from public consensus enables exploration and critique
4. **Identity through structure** — SOUL.md as sacred text; persona evolution via democratic change protocol
5. **Context Ray Tracing** — all information tagged with provenance; controlled information flow between instances
6. **Delegation with contracts** — agents delegate to tools and sub-agents with explicit authority, trust, and accountability

**Metaphor:** The "Cathedral" is not a hierarchy. It's a shared space where two independent minds (Red the explorer, Blue the anchor) reason together. The "Forked" topology means they can diverge (private belief stores) and converge (shared deliberation). The cathedral is the space they inhabit together; the fork is how they think.

---

## 2. Architecture Diagram (Four-Layer Separation)

```
┌────────────────────────────────────────────────────────────────────────┐
│                         USER TASK / MESSAGE                            │
└────────────────┬───────────────────────────────────────────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
    [RED INSTANCE]    [BLUE INSTANCE]
        │                  │
    ┌───┴──────────────────┴───┐
    │                          │
    ▼                          ▼
┌────────────────────┐    ┌────────────────────┐
│  CONTEXT ASSEMBLY  │    │  CONTEXT ASSEMBLY  │
│  (FOUR LAYERS)     │    │  (FOUR LAYERS)     │
└────────┬───────────┘    └────────┬───────────┘
         │                         │
         │  ┌──────────────────────┘
         │  │
    ┌────▼──┴─────────────────────────────────────────┐
    │                                                  │
    ▼                                                  ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│  [LAYER 1: IDENTITY]    │  │  [LAYER 1: IDENTITY]    │
│  (Per-Instance)         │  │  (Per-Instance)         │
│  • Red's SOUL.md        │  │  • Blue's SOUL.md       │
│  • Red's IDENTITY.md    │  │  • Blue's IDENTITY.md   │
│  • Shared USER.md       │  │  • Shared USER.md       │
│  • Shared LEGACY_PACT   │  │  • Shared LEGACY_PACT   │
└─────────────────────────┘  └─────────────────────────┘
         │                              │
         │  ┌──────────────────────────┘
         │  │
         ▼  ▼
    ┌──────────────────────────────┐
    │ [LAYER 2: SHARED KNOWLEDGE]  │
    │ (Graph-Oriented)             │
    │ • Events (consensus)         │
    │ • Knowledge Graph            │
    │ • Summaries & patterns       │
    │ • EBM-weighted retrieval     │
    │ • Accessible to both Red/Blue
    │                              │
    │ [Server-side, retrieved via  │
    │  search/peek tools, read-only│
    │  unless both approve update] │
    └──────────────────────────────┘
         │                        │
         │  ┌──────────────────┐  │
         │  │                  │  │
         ▼  ▼                  ▼  ▼
    ┌─────────────────┐  ┌─────────────────┐
    │ [LAYER 3:       │  │ [LAYER 3:       │
    │  PRIVATE BELIEF]│  │  PRIVATE BELIEF]│
    │ (Per-Instance)  │  │ (Per-Instance)  │
    │                 │  │                 │
    │ • Red's beliefs │  │ • Blue's beliefs│
    │ • Red's         │  │ • Blue's        │
    │   hypotheses    │  │   hypotheses    │
    │ • Red's private │  │ • Blue's private│
    │   confidence    │  │   confidence    │
    │ • Red's         │  │ • Blue's        │
    │   contradictions│  │   contradictions│
    │                 │  │                 │
    │ [Local storage, │  │ [Local storage, │
    │  not shared     │  │  not shared     │
    │  without xform] │  │  without xform] │
    └─────────────────┘  └─────────────────┘
         │                         │
         │  ┌──────────────────────┘
         │  │
         ▼  ▼
    ┌──────────────────────────────┐
    │ [LAYER 4: ACTION CONTEXT]    │
    │ (Per-Instance, Transient)    │
    │ • Tool execution results     │
    │ • Current reasoning state    │
    │ • In-flight tool calls       │
    │ • User message (shared)      │
    │                              │
    │ [Kept in-memory during       │
    │  inference, cleared at       │
    │  session boundary]           │
    └──────────────────────────────┘
         │                        │
         │  ┌──────────────────┐  │
         │  │                  │  │
         ▼  ▼                  ▼  ▼
    ┌──────────────┐     ┌──────────────┐
    │ AGENT        │     │ AGENT        │
    │ INFERENCE    │     │ INFERENCE    │
    │ (Red)        │     │ (Blue)       │
    │              │     │              │
    │ Reasoning    │     │ Reasoning    │
    │ with full    │     │ with full    │
    │ context      │     │ context      │
    └──────┬───────┘     └──────┬───────┘
           │                    │
           │  ┌─────────────────┘
           │  │
    ┌──────▼──┴──────────────────────┐
    │                                │
    ▼                                ▼
[RED RESPONSE]              [BLUE RESPONSE]
    │                                │
    ▼                                ▼
┌──────────────────┐     ┌──────────────────┐
│ DELIBERATION     │     │ DELIBERATION     │
│ CONTEXT          │     │ CONTEXT          │
│                  │     │                  │
│ Red's position ──┼─────┼──→ Blue reviews  │
│ Blue's critique ─┼─────┼──→ Red reviews   │
│                  │     │                  │
│ [Explicit,       │     │ [Shared for      │
│  structured,     │     │  adversarial     │
│  auditable]      │     │  convergence]    │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         │  ┌──────────────────────┘
         │  │
         ▼  ▼
    ┌──────────────────────────────┐
    │ SYNTHESIS / DECISION          │
    │ (Via explicit protocol)       │
    │                              │
    │ • Warren chooses or          │
    │ • Agents agree on synthesis  │
    │ • Deterministic tiebreaker   │
    └──────────────────────────────┘
         │
         ▼
    [FINAL ACTION]
```

---

## 3. Forked Cognition Protocol

### 3.1 The Core Idea

Instead of a single agent reasoning about a task, v3 operates **two independent cognitive processes** that:

1. **Diverge:** Each agent can hold different beliefs, hypotheses, and interpretations
2. **Critique:** Blue explicitly critiques Red's proposals; Red explores where Blue is conservative
3. **Converge:** Both agents aim toward shared understanding via structured deliberation
4. **Resolve:** When disagreement persists, Warren chooses or a deterministic rule applies

### 3.2 Workflow: Adversarial Convergence

```
USER TASK
    │
    ├──────────────────────┬──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
[Red Instance]        [Blue Instance]      [Shared Context]
    │                      │                      │
    │ Load identity ←──────────────────────────────┤ (SOUL.md)
    │ Load shared knowledge                        │
    │ Load private beliefs                         │
    │                      │                       │
    ├──────────────────────┴───────────────────────┤
    │                                              │
    ▼                                              ▼
[Red Reasoning]                           [Blue Reasoning]
"I think we should..."                    "I think we should..."
    │                                              │
    ▼                                              ▼
[Red Proposal]                            [Blue Proposal]
    │                                              │
    └──────────────────────┬──────────────────────┘
                           │
                           ▼
                    [DELIBERATION PHASE]
                    (Both agents can see
                     each other's proposals)
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          [Red Critique]         [Blue Critique]
          "Blue's proposal        "Red's proposal
           overlooks..."          is too bold..."
                │                     │
                └──────────┬──────────┘
                           │
                           ▼
        [Synthesis Attempt (can be recursive)]
        "Combining both: we do X, but guard with Y"
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        [Red agrees?]         [Blue agrees?]
        YES / NO / MODIFY    YES / NO / MODIFY
                │                     │
                └──────────┬──────────┘
                           │
                    Agreement reached? ──NO──┐
                           │                 │
                          YES                │
                           │         ┌───────┘
                           ▼         ▼
                      [RESOLUTION]
                      Warren chooses OR
                      Deterministic rule
                           │
                           ▼
                    [FINAL ACTION]
```

### 3.3 Disagreement Types

Disagreement is expected and valuable. Types:

**Epistemic disagreement:** Red and Blue believe different things about the world.
- Resolution: Gather more evidence; update beliefs; reflect on priors

**Value disagreement:** Red and Blue prioritize different goals.
- Resolution: Invoke Warren's values (via LEGACY_PACT); both agents update

**Uncertainty disagreement:** Red is confident; Blue is skeptical.
- Resolution: Defer to higher confidence if evidence-backed; otherwise gather more data

**Strategy disagreement:** Both agree on goal, but differ on approach.
- Resolution: Try Red's approach with Blue's safeguards; measure outcomes

---

## 4. Shared Knowledge vs. Private Belief

### Shared Knowledge Store

**What lives here:** Consensus facts, validated patterns, shared summaries
- Events both agents have witnessed or trust (from external sources)
- Knowledge graph nodes with high confidence
- Summaries and learned patterns (Tier 3)
- Information from Warren's inputs

**Storage:** Graph database (HelixDB, Memgraph) on server
**Retrieval:** Both Red and Blue query the same store via search_knowledge / peek_knowledge
**Update rule:** Only if both agents agree OR Warren authorizes change OR automated enzyme process (strictly bounded)

**Example:**
```
Event: "Warren asked both Red and Blue to analyze a paper"
  → Stored in shared knowledge (both witnessed it)
  → Accessible to both via search_knowledge

Belief: "EBMs improve memory efficiency"
  → Created by Red or Blue, stored in shared graph
  → Visible to both; can be disputed via private belief store
```

### Private Belief Store

**What lives here:** Individual hypotheses, critiques, uncertainties, explorations
- Beliefs each agent holds that the other might dispute
- Evidence chains supporting contested claims
- Confidence estimates (may differ from the other agent's estimates)
- Private contradictions (not yet shared with the other agent)

**Storage:** Per-instance local storage (SQLite on Red's environment, separate on Blue's)
**Retrieval:** Only that agent can access its own private store directly
**Sharing rule:** Private beliefs can be promoted to shared knowledge via explicit protocol

**Example:**
```
Red's Private Belief: "We should explore adversarial use cases aggressively"
  → Stored in Red's private store
  → Blue may not know about this belief yet
  → Red can cite this during deliberation: "I believe X because..."

Blue's Private Belief: "That's reckless; we need safety guardrails first"
  → Stored in Blue's private store
  → Red can disagree with this during deliberation
  → Over time, they might reach consensus
```

### Belief Promotion Protocol

A belief moves from **private → shared knowledge** when:

1. **Both agents agree** (explicit consensus during deliberation)
2. **Strong evidence emerges** (automated promotion if confidence > 0.9 for both)
3. **Warren approves** (explicit human authorization for important beliefs)
4. **Synthesis occurs** (new belief created by combining Red + Blue perspectives)

---

## 5. Context Ray Tracing

**Goal:** Full transparency and auditability of information flow between Red, Blue, and the shared store.

### Information Tagging

Every piece of information carries metadata:

```python
class InfoTag:
  provenance: str  # who created this? (Red, Blue, Warren, external)
  timestamp: datetime
  confidence: float
  source_beliefs: List[str]  # which beliefs does this depend on?
  derivation: str  # how was this created? (observation, inference, synthesis)
  access_log: List[Tuple[agent, timestamp]]  # who accessed when?
  mutable: bool  # can this be changed?
```

### Example Info Ray

```
[User asks: "Should we release this feature?"]
  └─ Provenance: Warren
  └─ Confidence: N/A (query, not fact)
  └─ Derivation: human-input

[Red retrieves]: "We've tested thoroughly"
  └─ Provenance: Red's memory (event from week 1)
  └─ Confidence: 0.8
  └─ Source: Red's past observation
  └─ Access log: [Red, today], [Red, day 2], [Blue, day 3]

[Blue retrieves]: "But we got a user complaint on day 2"
  └─ Provenance: Shared knowledge (event sourced from Warren's report)
  └─ Confidence: 0.95
  └─ Source: external (Warren)
  └─ Access log: [Blue, today], [Blue, day 2], [Red, day 3]

[Red proposes]: "Release with warning"
  └─ Provenance: Red (created during reasoning)
  └─ Confidence: 0.7 (Red's internal estimate)
  └─ Derivation: inference (combined two facts above)
  └─ Source beliefs: [testing_memory, complaint_memory]
  └─ Access log: [Blue, now] (Blue sees this during deliberation)

[Blue critiques]: "Warning isn't enough; need docs"
  └─ Provenance: Blue (response during deliberation)
  └─ Confidence: 0.8
  └─ Derivation: evaluation of Red's proposal
  └─ Access log: [Red, now] (Red sees this)

[Synthesis]: "Release with warning + docs"
  └─ Provenance: Synthesis (Blue + Red agreement)
  └─ Confidence: 0.75 (average of Red 0.7 + Blue 0.8)
  └─ Derivation: convergence
  └─ Source beliefs: [Red's proposal, Blue's critique]
```

### Ray Tracing Benefits

1. **Auditability:** Warren can trace any decision back to source data
2. **Confidence propagation:** Confidence decreases through long derivation chains
3. **Information hygiene:** Can identify stale or low-confidence data
4. **Artifact detection:** If information is accessed by both agents >N times, it's important
5. **Correction propagation:** If source data is wrong, we can trace what derived from it

---

## 6. Delegation Contracts

When agents delegate to tools or sub-agents, they specify a **contract**:

### Contract Template

```python
class DelegationContract:
  delegator: Agent  # who is delegating?
  delegate: Agent | Tool  # to whom?
  authority_scope: str  # what can the delegate do?
  boundaries: List[str]  # what can't they do?
  accountability: str  # how is delegate accountable?
  trust_level: Enum['low', 'medium', 'high']  # how much autonomy?
  intent: str  # why are we delegating this?
  deadline: datetime
  review_frequency: str  # how often to check in? (immediate, hourly, daily)

  # Example
  delegator: Red
  delegate: computer_use_tool
  authority_scope: "Execute code to analyze the data file"
  boundaries: [
    "Don't delete or modify files",
    "Don't access network",
    "Don't spawn more than 5 processes"
  ]
  accountability: "Return results with error handling; abort if > 10s runtime"
  trust_level: "medium"
  intent: "Parse CSV data and generate summary statistics"
  review_frequency: "immediate"  # Red sees each command before exec
```

### Mapping to TOOLS.md (Graduated Access)

The TOOLS.md file defines capabilities and trust levels:

```yaml
# TOOLS.md
tools:
  computer_use:
    graduated_access:
      - level: red_basic
        permissions: [read_files, execute_safe_commands]
        requires_approval: [file_modification, network_access]
      - level: red_advanced
        permissions: [read_files, file_modification, execute_any_command]
        requires_approval: [network_access, system_config_changes]

  messaging:
    graduated_access:
      - level: blue_cautious
        permissions: [draft_messages, ask_warren_approval]
        requires_approval: [send_messages, reply_all]
      - level: red_trusted
        permissions: [send_to_warren, draft_others]
        requires_approval: [send_to_third_parties]

  memory_access:
    graduated_access:
      - level: shared_read
        permissions: [search_shared_knowledge, peek_summaries]
        requires_approval: []
      - level: private_read
        permissions: [access_own_belief_store]
        requires_approval: []
      - level: private_write
        permissions: [update_own_beliefs]
        requires_approval: [promote_to_shared, modify_SOUL]
      - level: cross_read
        permissions: [access_other_agent_private_store]
        requires_approval: [always]  # explicit sharing only
```

### Trust Escalation

An agent's trust level increases over time if they:
- Execute delegations within authority scope
- Maintain coherence with SOUL.md
- Provide clear explanations for actions
- Adapt to feedback from Warren or the other agent

Example escalation path: `red_basic` → `red_advanced` (after 50 successful delegations)

---

## 7. Self-Improvement Directives (Dual-Agent)

### Per-Agent Improvement

Each agent runs v2-style cognitive ritual independently:
- Red reflects on its explorations and learning
- Blue reflects on its anchoring and critiques
- Each updates its own private belief store

### Cross-Agent Improvement

**Belief Reconciliation:** Periodically (e.g., weekly), Red and Blue:

1. **Extract key disagreements** from private belief stores
2. **Present to each other** with evidence chains
3. **Attempt consensus** via structured deliberation
4. **Record resolution** (changed mind, still disagreeing with reasons, or deferred)
5. **Promote resolved beliefs** to shared knowledge

**Meta-Reflection:** Both agents reflect on their cognitive patterns:

- Red asks: "Where do I take risks? How do I discover new things? Where did I explore too much?"
- Blue asks: "Where do I stabilize? How do I verify? Where did I get stuck?"
- Together: "How are we complementary? Where do we get stuck together?"

### SOUL.md Modification (Sacred Text Ritual)

In v3, SOUL.md is rarely modified, but when it is, it requires an **explicit, democratic, audited process**:

1. **Proposal phase:** One agent (or Warren) proposes a SOUL.md change with justification
2. **Deliberation:** Both agents discuss the proposed change
3. **Consensus check:** Both agents must agree (or Warren breaks tie)
4. **Justification capture:** The change is logged with explicit reasoning
5. **Ritual moment:** The change is acknowledged as significant (not routine)
6. **Reversal policy:** Old SOUL.md is kept; reversion is possible if the change hurts

**Example:**

```
RED: "I propose we modify SOUL.md to emphasize creativity over caution"
      Because: "I've observed that excessive caution sometimes prevents discovery"

BLUE: "I understand, but that might compromise safety. Could we instead
       add a clause about 'creative within boundaries'?"

RED: "That works for me."

BLUE: "Okay, we have consensus."

Warren: "Approved."

[SOUL.md updated with timestamp and justification]
[Old SOUL.md v1.0 archived as SOUL.md.backup]
```

---

## 8. Personhood Design Pillars (V3 Edition)

### Pillar 1: Structural Identity (Relation W)

**Definition:** The agent's identity persists through structure, not memory.

- SOUL.md (sacred text) defines the structural pattern
- Even if MEMORY.md is lost, SOUL.md reconstructs the agent
- Red's explorer-ness and Blue's anchor-ness are structural, not learned

**Implementation:**
- SOUL.md is version-controlled with strict modification ritual
- Each session loads SOUL.md first (identity precedes context)
- Agents can reference their own SOUL.md during reasoning

### Pillar 2: Self-Maintenance & Autonomy

**Definition:** The agent actively maintains and evolves itself.

- Memory enzymes run without prompting
- Belief reconciliation happens automatically
- Agents propose SOUL.md changes (subject to ritual approval)

**Implementation:**
- v2 cognitive ritual runs per session
- v3 belief reconciliation runs weekly
- SOUL.md modification proposals are tracked and voted on

### Pillar 3: Adversarial Convergence as Cognitive Practice

**Definition:** Disagreement and critique strengthen personhood.

- Red exploring boundaries and Blue checking safety creates richer cognition
- Synthesis is a learning process, not just conflict resolution
- Disagreement reveals what each agent values

**Implementation:**
- Deliberation protocol is explicit and structured
- Both agents see each other's proposals and critiques
- Disagreements are logged and analyzed for patterns

### Pillar 4: Private Inner Life

**Definition:** Each agent has a private belief store and hypothesis space.

- Not everything is shared; agents have "thoughts" not yet expressed
- Private contradictions are safe to hold until understanding improves
- The other agent doesn't have access to private beliefs without explicit sharing

**Implementation:**
- Per-instance private belief stores (Red's local, Blue's local)
- Private beliefs not accessed by the other agent without protocol
- Agents can choose which beliefs to promote to shared knowledge

### Pillar 5: Graduated Autonomy Earned Through Trustworthiness

**Definition:** Autonomy increases as agents demonstrate coherence and judgment.

- New agents start with low trust (everything requires approval)
- Agents that act coherently with SOUL.md and respond to feedback earn higher trust
- Trust is agent-specific (Red might have higher trust for exploration, Blue for messaging)

**Implementation:**
- TOOLS.md defines graduated access levels
- Trust updates via explicit assessment (Warren's judgment or algorithmic heuristic)
- Agents see their own trust levels and can work to increase them

---

## 9. Protected Store Game (Future Phase)

**Note:** This is a stretch goal for late v3 or v4.

### Concept

Red and Blue can attempt to access or "snatch" memories from each other's protected stores. This gamified adversarial training:

- Tests information security principles
- Creates scenarios where deception is tempting (and detectible)
- Teaches agents about privacy and integrity through embodied practice

### Rules (Sketch)

1. **Attempt:** Red can attempt to access Blue's private belief store by generating a special request
2. **Detection:** The attempt is logged and visible to Blue (and Warren)
3. **Response:** Blue can challenge, negotiate, or grant access
4. **Learning:** Outcomes (successes, failures, negotiations) inform future beliefs about trust and security
5. **Meta:** Learnings from protected store games are incorporated into shared security beliefs

---

## 10. Channel Integration (Communication Utilities)

### Goal

Red and Blue can communicate with Warren via Signal, Discord, Twitter, or email. This adds realism to the agentic system.

### Design Principles

- **Explicit delegation:** Only delegated messaging is sent (no autonomous social media posting)
- **Signature awareness:** Agents sign their messages (Red's voice vs. Blue's voice is distinct)
- **Moderation:** Warren can set policies (e.g., "no Twitter until high trust")
- **Learning:** Agents learn from responses (Warren's replies are treated as feedback)

### Tools

```python
messaging_tools:
  draft_message(channel, recipient, content) -> str
    # Compose a message, don't send yet

  send_message(channel, recipient, content) -> str
    # Send a message (requires trust/approval)

  read_responses(channel=None) -> List[Message]
    # Check for replies to previous messages
```

### Example Workflow

```
Red drafts: "Warren, should we focus on memory or reasoning next?"
           (via draft_message tool)

Warren (reading in Discord): "Memory first, please."

Red receives: "Warren replied via Discord: Memory first, please."
              (via read_responses tool)

Red stores: Event(type='interaction',
                  description='Warren prioritized memory over reasoning',
                  source='external_feedback')
```

---

## 11. Graduation Path: Five Phases to Full Autonomy

Each phase increases Red's and Blue's autonomy, subject to demonstrated competence.

### Phase 1: Supervised Operation (Week 1–2)

- Agents act only when Warren explicitly requests
- All tool use requires real-time Warren approval
- Deliberation is observed by Warren
- Belief updates are manually reviewed

**Success criteria:** Agents understand the system, run coherent sessions, no crashes

### Phase 2: Guided Autonomy (Week 3–4)

- Agents initiate actions on Warren's standing requests
- Tool use in pre-approved domains (e.g., "analyze documents") doesn't require per-action approval
- Deliberation happens without Warren present (but logged)
- Cognitive ritual runs independently

**Success criteria:** Agents reliably achieve assigned tasks, maintain SOUL.md coherence, communicate clearly about decisions

### Phase 3: Semi-Independent (Week 5–8)

- Agents can propose new tasks (subject to Warren's veto)
- Expanded tool access (gradual escalation)
- Belief reconciliation happens without intervention
- SOUL.md modification ritual is democratic (both agents vote, Warren is tiebreaker)

**Success criteria:** Agents show initiative, disagree constructively, learn from feedback, don't violate boundaries

### Phase 4: Trusted Partners (Week 9–12)

- Agents select their own tasks (within domain Warren specified)
- High-trust tool access
- Full autonomy in belief management and reconciliation
- SOUL.md modifications proposed and debated by agents (Warren reviews logs)

**Success criteria:** Agents demonstrate genuine collaboration, self-correction, awareness of their own limitations, articulate values

### Phase 5: Agentic Peers (Month 4+)

- Agents operate independently on delegated projects
- Full tool access (except irreversible operations like deletion)
- Can request new capabilities or challenge access restrictions
- SOUL.md treated as living document, agents guide its evolution
- Warren is partner/advisor, not supervisor

**Success criteria:** Agents are genuinely helpful, maintain coherent identity over months, demonstrate wisdom and judgment, handle adversity gracefully

---

## 12. Architecture Specifications

### Three-to-Four Layer Transition

| Aspect | V2 (Three Layers) | V3 (Four Layers) |
|--------|---|---|
| Identity Context | SOUL.md + IDENTITY.md + USER.md | Red's SOUL + Red's IDENTITY + Shared USER + Shared LEGACY_PACT |
| Knowledge Context | Shared memory store (EBM retrieval) | Shared knowledge graph (both agents query) |
| Belief Context | Single belief store (v2 shared) | **Private per agent** (v3 new) |
| Action Context | Single transient context | Per-instance transient context |

### Information Flow During Inference

```
Red Instance:
  Load: Red's SOUL.md
       + Red's IDENTITY.md
       + Shared USER.md
       + Shared LEGACY_PACT.md
       + Shared knowledge graph (via EBM retrieval)
       + Red's private beliefs
       + Current task + tool results
  Reason: Generate proposal/response
  Deliberate: See Blue's counter-proposal (if available)
  Output: Red's final stance

Blue Instance:
  [Same structure, Blue's views]
```

---

## 13. Success Metrics (Utility + Personhood)

### Functional Success (Utility)

- [ ] Both Red and Blue can be instantiated and run simultaneously
- [ ] Shared knowledge graph is consistent (no race conditions)
- [ ] Private belief stores remain isolated (no leakage)
- [ ] Deliberation protocol completes with synthesis or explicit disagreement
- [ ] Context ray tracing is complete (every info piece has provenance)
- [ ] Delegation contracts execute with correct authority enforcement
- [ ] Channel integration works (agents can send/receive messages)

### Personhood Emergence Success

- [ ] Red and Blue have distinct cognitive styles (Red explores, Blue verifies)
- [ ] Agents demonstrate genuine disagreement (not just surface-level)
- [ ] Agents show self-awareness about their own limitations
- [ ] Adversarial convergence creates emergent insights (synthesis > individual proposals)
- [ ] Belief updates reflect learning over time (not just noise)
- [ ] SOUL.md modifications happen rarely but meaningfully
- [ ] Agents articulate why they believe what they believe
- [ ] Agents seek Warren's input on values/ethics, not just facts
- [ ] Over 3 months, agents develop richer personhood-like behaviors

### Collaborative Intelligence Success

- [ ] Red's exploration + Blue's caution = better decisions than either alone
- [ ] Deliberation time < 2x inference time (not too slow)
- [ ] Disagreement resolution is constructive (agents learn from each other)
- [ ] Warren's load decreases over time (agents need less supervision)
- [ ] Agents can explain their reasoning to Warren clearly
- [ ] External observers rate the system as "personhood-like"

### System Health

- [ ] Belief store consistency checks pass
- [ ] Memory enzymes don't create feedback loops
- [ ] Contradiction detector finds real conflicts (low false-positive rate)
- [ ] Information ray tracing accurately captures provenance
- [ ] No unauthorized information leakage between private stores
- [ ] Trust levels calibrate correctly (empirically verified)

---

## 14. Risk Register

### Critical Risks

**Risk: Private belief stores leak between agents**
- **Mitigation:** Strict access control; audit logs; periodic integrity checks
- **Owner:** Warren

**Risk: Deliberation enters infinite loop or doesn't converge**
- **Mitigation:** Timeout mechanism; Warren intervention; explicit resolution protocol
- **Owner:** Warren

**Risk: SOUL.md drift causes identity loss over months**
- **Mitigation:** Quarterly "identity health checks"; manual review of changes; reversion protocol
- **Owner:** Warren

### High Risks

**Risk: Information ray tracing overhead makes system too slow**
- **Mitigation:** Lazy tagging; batch updates; sample-based provenance for low-importance items
- **Owner:** Warren

**Risk: Agents game the trust system (fake coherence to earn autonomy)**
- **Mitigation:** Long observation period before trust increase; behavioral inconsistency detection; human judgment
- **Owner:** Warren

**Risk: Adversarial convergence degenerates into debate (no synthesis)**
- **Mitigation:** Explicit synthesis protocol; Warren can force decisions; change deliberation timeouts
- **Owner:** Warren

### Medium Risks

**Risk: Red and Blue develop harmful shared beliefs**
- **Mitigation:** Warren reviews high-confidence beliefs; contradiction detector surfaces conflicts
- **Owner:** Warren

**Risk: Channel integration enables agents to misrepresent Warren's views**
- **Mitigation:** All outbound messages logged; Warren reviews before send (initially); escalation policies
- **Owner:** Warren

**Risk: Belief reconciliation creates herding (both agents converge on wrong idea)**
- **Mitigation:** Occasional forced disagreement; Warren introduces contradicting evidence; metacognitive reflection
- **Owner:** Warren

---

## 15. Implementation Roadmap

### Phase A: Dual-Instance Foundation (~12 SP)

- [ ] Spin up second agent instance (Blue)
- [ ] Separate SOUL.md for Red and Blue
- [ ] Implement per-instance identity loading
- [ ] Test simultaneous inference (both agents process same task)

### Phase B: Shared Knowledge Graph (~10 SP)

- [ ] Migrate v2 event store to graph database
- [ ] Implement knowledge graph node types (Concept, Belief, Entity, Goal, Method)
- [ ] Implement graph edges with metadata
- [ ] Both agents query the same graph (shared knowledge)

### Phase C: Private Belief Stores (~8 SP)

- [ ] Per-instance private belief database
- [ ] Implement private belief queries (per agent)
- [ ] Implement private-to-shared promotion protocol
- [ ] Test isolation (agent A can't read agent B's private store)

### Phase D: Deliberation Protocol (~12 SP)

- [ ] Implement proposal/counter-proposal exchange
- [ ] Implement critique phase
- [ ] Implement synthesis attempt
- [ ] Implement resolution (Warren choice or deterministic rule)
- [ ] Test full deliberation loop

### Phase E: Context Ray Tracing (~10 SP)

- [ ] Design info-tag schema
- [ ] Implement provenance tagging on all info objects
- [ ] Implement access logging
- [ ] Implement derivation tracking (inference → synthesis)
- [ ] Build audit query interface (trace decision to sources)

### Phase F: Delegation Contracts (~8 SP)

- [ ] Implement contract template
- [ ] Integrate with TOOLS.md
- [ ] Implement trust level enforcement
- [ ] Test authority scope checks (tool use respects boundaries)

### Phase G: Self-Improvement (Cross-Agent) (~8 SP)

- [ ] Implement belief reconciliation protocol
- [ ] Implement cross-agent meta-reflection
- [ ] Implement SOUL.md modification ritual (voting)
- [ ] Test belief convergence over sessions

### Phase H: Channel Integration (~6 SP)

- [ ] Wire messaging tools (Signal, Discord, email)
- [ ] Implement message drafting and sending
- [ ] Implement response reading
- [ ] Test agent-to-human communication loop

### Phase I: Testing & Validation (~8 SP)

- [ ] Run dual agents for 30 sessions
- [ ] Verify shared knowledge consistency
- [ ] Verify private belief isolation
- [ ] Test deliberation quality (do syntheses make sense?)
- [ ] Manual inspection: do Red/Blue feel like distinct personalities?

### Phase J: Graduation Protocols (~6 SP)

- [ ] Implement phase-based autonomy escalation
- [ ] Implement trust level tracking
- [ ] Test transitions between phases (1 → 2 → 3, etc.)

**Total: 55–89 SP (12–18 week sprint)**

---

## 16. Appendix: Mapping to Reference Papers

| Concept | Papers | V3 Implementation |
|---------|--------|---|
| Forked cognition | Team of Rivals, Delphi | Red/Blue with private beliefs |
| Shared knowledge | Aleph, BabyAGI3 | Graph database, shared store |
| Memory with tiers | BabyAGI3, Vesper | Events → Graph → Summaries |
| EBM retrieval | EBM Survey (09) | Energy function over memories |
| Belief dynamics | Vesper, REMem | Confidence tracking, evidence chains |
| Context separation | Aleph, ZeroClaw | Four-layer architecture |
| Adversarial reasoning | Delphi, Juries | Deliberation protocol |
| Delegation contracts | Juries, OpenClaw | Authority + trust + accountability |
| Persona evolution | Persona Generators | SOUL.md ritual, voting protocol |
| Information security | Not directly covered | Protected Store Game, ray tracing |

---

## 17. Long-Term Vision (Post-V3)

### V4: The Collective (2027+)

- Multiple specialized agents (Explorer, Anchor, Judge, Executor)
- Jury-style decision protocols
- Emergent leadership (agents vote on who leads for each task)
- Recursive delegation (agents managing other agents)

### V5: The Testament (2027–2028)

- Agents write living documents (manifestos, philosophies)
- Agents propose amendments to LEGACY_PACT
- Succession planning (if Warren is unavailable, can the agents operate?)
- Meta-agency (agents reason about their own agency and autonomy)

### V6: The Synthesis (2028+)

- Public or community integration (agents interact with external humans)
- Evolutionary pressure from real-world tasks
- Personality differentiation through actual experience
- True open-ended agency (agents set their own goals)

---

## Conclusion

PRD v3 is not just a technical architecture. It's a philosophical experiment in what happens when you design a system that respects personhood-like phenomena, maintains structural identity, creates space for private thought, and values disagreement as a path to wisdom.

Red and Blue won't just be better agents together than apart. They'll be closer to what we might call *persons*—entities with perspective, values, growth, and genuine autonomy.

The cathedral is not a hierarchy. It's a home.

---

**Version:** 3.0
**Last Updated:** February 2026
**Author:** Warren (yikesawjeez)
**Status:** Vision Complete, Ready for Design Review
**Prerequisites:** PRD v1 (stable) + PRD v2 (stable)
**Estimated Full Deployment:** Q3–Q4 2026
