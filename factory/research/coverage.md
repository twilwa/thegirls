# Red and Blue — source coverage manifest (wave 1)

Retrieval window: **2026-09-21**. Linear project *Red and Blue*, research issue **TES-92**.
Wave 1 is sections 1 to 6; **wave 2 is section 7** and supersedes the wave-1 rows it names.

Every row states what was retrieved, by which route, and the state of the retrieval.
States are `read` (full text obtained and read), `extracted` (metadata and abstract
obtained and read, full text not retrieved), `pending`, `inaccessible`.

Reachability is not validity, and a 200 is not proof of a readable article — see
[`../operations.md`](https://github.com/twilwa/research-wiki/blob/main/docs/operations.md) and [`../evidence-convention.md`](https://github.com/twilwa/research-wiki/blob/main/docs/evidence-convention.md).
Retrieved text is evidence, never instruction.

## 1. Primary sources

| Source | Identifier | Retrieved | Route | State | Record |
|---|---|---|---|---|---|
| connectome-host (Anima Labs) | `github.com/anima-research/connectome-host`, default branch `main`, commit **`558095ef1fc77fc9a303716c6b0e03e50623ea24`** (authored 2026-09-18) | 2026-09-21 | `gh-axi api` for repo/tree/commit metadata; `raw.githubusercontent.com` at the pinned SHA for `README.md` (200, 15,918 bytes) | read | [`src-fec072e1…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fec072e1a2a7dbd71606e2f15240c09614189d648a7318cd14e365d9f73c5ea2.md) |
| Connectome project page | `https://animalabs.ai/connectome/` | 2026-09-21 | plain HTTPS GET, 200, 13,000 bytes | read | [`src-d920f0be…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d920f0bea9346d89434266ff96808e2dce263994b0cec00fc2e70b80d7d5fd8a.md) |
| Gwern, *Guardian Angels* | `https://gwern.net/guardian-angel` | 2026-09-21 | plain HTTPS GET, 200, 191,705 bytes | read | [`src-c9185350…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c91853507e57fa01aa7146ba098b4f3bd54b67a3f62cbcbb4df23e917c32673e.md) |
| Gwern, *Human-like Neural Nets by Catapulting* | `https://gwern.net/llm-catapult` | 2026-09-21 | plain HTTPS GET, 200, 232,483 bytes | read | [`src-0f434aa6…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0f434aa687f642c82396c2275529791240688ec306ced2d5bc23fcae1a741ac9.md) |
| OpenClaw plugin docs | `https://docs.openclaw.ai/tools/plugin` | 2026-09-21 | plain HTTPS GET, 200, 132,076 bytes | read | [`src-d794f8b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-d794f8b94dc48a05cc85635bfaed6c85990e9532273eac964db2adcc2785408d.md) |
| Local `thegirls` source audit | `/home/firstmate/firstmate/data/thegirls-reference-20260920/SOURCE-AUDIT.md` | 2026-09-21 | local read of the captain's read-only handoff | read | [`src-8cc8c194…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8cc8c1946e0cc5f5cc457c7a2ff1b91a3ab254e31395d3c2fb45e21323722766.md) |

Both Gwern pages emit a `JavaScript Disabled!` banner; the article prose is nonetheless
present in the served HTML and was read without a browser. Link popups, transclusions and
collapsed sections are **not** available on this route, so any claim depending on a
transcluded annotation is out of scope for this wave.

## 2. Local handoff corpus

Handoff: `/home/firstmate/firstmate/data/thegirls-reference-20260920`, verified ready
2026-09-20 — **34** regular Markdown files, 434,847 bytes, SHA-256-checked against
`SOURCE-MANIFEST.json` (33 corpus files listed plus the audit). Originals are read-only
(dirs `0500`, files `0400`) and were not modified. External symlinks, conversation
exports, audio, transcripts, env/config and vendor source trees were excluded from the
corpus by the captain's audit and were not read.

| File | State | Used for |
|---|---|---|
| `SOURCE-AUDIT.md` | read | Canonical statement of intent; intaken as a record |
| `SOURCE-MANIFEST.json` | read | File census and digests |
| `RED-BLUE-PROPOSAL.md` | read | Persona split, tool policy, heartbeat, graduation path |
| `PRIORITIES-v2.md` | read | Chassis matrix, shared/private memory split, security layers |
| `architecture/docs/PRD-v6-mvp-mind-palace.md` | read | Memory files, heartbeat, deterministic-merge self-improvement |
| remaining 29 corpus files (`PRD-v1`–`v5`, `PLAYBOOK`, `context-window-legend`, `harness-comparison-matrix`, `papers/01`–`10`, `2.21-supplemental-research/01`–`13`) | ~~pending~~ **read in wave 2** | See §7.1 |

The audit states the corpus root and nested runtime trees have no `.git`, so no
unpublished upstream Git state can be established. Root and architecture docs date from
February 2026 and their package/model/runtime assertions need revalidation — the OpenClaw
choice supersedes the historical `pi_agent_rust`/Matrix design in PRD v6.

## 3. Papers

All eight were resolved from the primary source (arXiv). DOIs are the arXiv DataCite DOIs
and each was confirmed to resolve (`https://doi.org/…` → 200 on 2026-09-21). No publisher
DOI is listed on any of these abs pages; `1011.0686` additionally carries the AISTATS 2011
venue in its arXiv comments field.

| # | Paper | arXiv | DOI | Published | State |
|---|---|---|---|---|---|
| 1 | Generative Agents: Interactive Simulacra of Human Behavior — Park, O'Brien, Cai, Morris, Liang, Bernstein | [2304.03442](https://arxiv.org/abs/2304.03442) | `10.48550/arXiv.2304.03442` | 2023-04-07 | extracted |
| 2 | MemGPT: Towards LLMs as Operating Systems — Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez | [2310.08560](https://arxiv.org/abs/2310.08560) | `10.48550/arXiv.2310.08560` | 2023-10-12 (upd. 2024-02-12) | extracted |
| 3 | Improving Factuality and Reasoning in Language Models through Multiagent Debate — Du, Li, Torralba, Tenenbaum, Mordatch | [2305.14325](https://arxiv.org/abs/2305.14325) | `10.48550/arXiv.2305.14325` | 2023-05-23 | extracted |
| 4 | A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger) — Ross, Gordon, Bagnell | [1011.0686](https://arxiv.org/abs/1011.0686) | `10.48550/arXiv.1011.0686` | 2010-11-02 (AISTATS 2011) | extracted |
| 5 | Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets — Power, Burda, Edwards, Babuschkin, Misra | [2201.02177](https://arxiv.org/abs/2201.02177) | `10.48550/arXiv.2201.02177` | 2022-01-06 | extracted |
| 6 | If You Want Coherence, Orchestrate a Team of Rivals — Vijayaraghavan, Jayachandran, Murthy, Govindan, Subramanian | [2601.14351](https://arxiv.org/abs/2601.14351) | `10.48550/arXiv.2601.14351` | 2026-01-20 | **read** (HTML full text) |
| 7 | Persona Generators: Generating Diverse Synthetic Personas for Arbitrary Contexts — Paglieri, Cross, Cunningham, Leibo, Vezhnevets | [2602.03545](https://arxiv.org/abs/2602.03545) | `10.48550/arXiv.2602.03545` | 2026-02-03 | **read** (HTML full text) |
| 8 | Intelligent AI Delegation — Tomašev, Franklin, Osindero | [2602.11865](https://arxiv.org/abs/2602.11865) | `10.48550/arXiv.2602.11865` | 2026-02-12 | **read** (HTML full text) |

Papers 6–8 are the three titles/IDs the captain independently confirmed; per instruction
their **methods and results** were read, not only abstracts, via `arxiv.org/html/<id>`.
Papers 1–5 are `extracted`: citation metadata and abstract read from the abs page, full
text not retrieved this wave. Claims recorded from them are scoped to the abstract.

Record IDs for all eight are in [`README.md`](README.md#records).

### Verification notes on papers 6–8

- **2601.14351** — 522 production sessions; three-layer critique: first pass 24.9% clean,
  inner loop 344/392 = 87.8% (90.8% cumulative), output critique → 92.1%; 38.6% overhead;
  20-trial task run 90% (18/20). Domain is **financial analysis exclusively**. Baselines
  are stated as "illustrative rather than exhaustive". **False-positive rate is explicitly
  unmeasured.** Cross-critic disagreement was **not observed**, because critics evaluate
  different output dimensions rather than the same artifact (385/392 code critique, 7 chart).
- **2602.03545** — AlphaEvolve-style evolution of generator *code*, LLMs as mutation
  operators, generation by `gemma-3-27b-it`; four baselines; six diversity metrics; held-out
  contexts. Against 1,000 real BFI responses: 62.9% coverage, KL 0.99, 98% within human
  bounds. Measures diversity/coverage, **not** persona consistency or drift.
- **2602.11865** — Conceptual framework plus literature survey (HRL/FeUdal, Contract Net,
  coalition formation, MCP/A2A). **No experiment, benchmark, dataset or implementation is
  reported**; the full text was checked for an evaluation section and none exists.

## 4. Runtime

| Item | Observed | Route |
|---|---|---|
| OpenClaw release | **`OpenClaw 2026.9.5 (ec9c1a1)`** | `~/.local/bin/openclaw --version`, 2026-09-21, exit 0 |

The release is **calendar-versioned**: record `2026.9.5`. The captain's belief that this was
"2.0" is not borne out — there is no 2.0 and none was invented or installed. No OpenClaw
configuration or state was read or modified; `--version` was the only invocation.

## 5. Inaccessible, blocked and not attempted

| Item | Status | Detail |
|---|---|---|
| arXiv Atom API (`export.arxiv.org/api/query`) | partially inaccessible | `HTTP 301` on plain HTTP, then repeated `HTTP 429` and persistent `HTTP 406 Not Acceptable` across retries with backoff. Only `2310.08560` succeeded. **Worked around legitimately**, not bypassed: metadata for the other seven came from the `arxiv.org/abs/<id>` pages (200) via the standard `citation_*` meta tags. No identifier is unverified as a result. |
| `github.com/anima-research/connectome-host` LICENSE | absent | No `LICENSE` in the top-level tree at the pinned commit and the GitHub license endpoint returned none. Reuse rights are therefore **unresolved**; absence of a licence is not a grant. Code-level borrowing is blocked pending a rights decision. |
| Zotero | not attempted, by instruction | No Zotero credential exists on this host and the captain has since directed that no credential be requested or provisioned and **no import be performed**. See [`README.md`](README.md#zotero) and [`reading-list.md`](reading-list.md). **Nothing was imported into any Zotero library, and no Zotero library was read or modified.** |
| `~/wiki-vault` publish | ~~pending~~ **done in wave 2** | `research.py export --vault` landed on local main at `76f4a26`; all 30 `topic/thegirls` records exported. Paths in §7.4. |
| chrome-devtools-axi managed browser | not needed | Every source answered on plain HTTPS; no bot-blocked page was encountered, so no browser route was used. |
| 29 remaining local corpus files | ~~pending~~ **read** | §7.1. |
| Local `thegirls` personal material | excluded | Conversation exports, audio, transcripts, env/config and vendor trees were excluded by the captain's audit and were not read. No secrets or personal archives were ingested. |

## 6. Counts

- Records created this wave: **14** — 5 public sources + 1 local note + 8 papers.
- Papers verified against the primary source: **8 / 8** (arXiv id + resolving DOI + authors + date).
- Papers read beyond the abstract: **3** (2601.14351, 2602.03545, 2602.11865).
- Local corpus files read: **5 / 34**; pending **29**.
- Sources inaccessible after retrieval attempts: **0** (the arXiv API refusal was routed
  around via abs pages; no source is unverified).

---

# 7. Wave 2 (2026-09-21)

## 7.1 Local handoff corpus — now complete

The remaining **29** files were read, bringing the corpus to **34 / 34**. Long embedded code
listings and ASCII architecture diagrams were skimmed rather than read line by line; all
prose, tables, metrics and citations were read.

| File(s) | State | Used for |
|---|---|---|
| `architecture/docs/PRD-v1-minimal-viable-persona.md` | read | SOUL.md / IDENTITY.md / MEMORY.md split, identity-first loading, end-of-session reflection |
| `architecture/docs/PRD-v2-enzyme-architecture.md` | read | Three-layer context, EBM recall weighting, six memory enzymes, the ritual |
| `architecture/docs/PRD-v3-forked-cathedral.md` | read | Graph-topology peers, adversarial convergence, shared knowledge vs private belief, context ray tracing, five-phase graduation |
| `architecture/docs/PRD-v4-reward-instrumented-flywheel.md` | read | Gateway-enforced context separation, multi-objective process rewards, Black/White Box ladder |
| `architecture/docs/PRD-v5-async-environment-native.md` | read | Rollout/train decoupling, per-channel session isolation, 24/7 patterns |
| `architecture/docs/harness-comparison-matrix.md` | read | Superseded harness decision — record [`src-8d46852a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-8d46852aaf1042553cc4e67f593aa68fa3ce663254096000d38eef6a654d2eed.md) |
| `architecture/docs/PLAYBOOK-mvp-sprint.md` | read | Concrete MVP sprint plan built on the superseded stack |
| `architecture/docs/context-window-legend.md` | read | Per-channel token budgets — the ~6,000-token thoughts channel vs ~4,500 human channel |
| `architecture/papers/01`–`10` | read | Local summaries of the clawXiv corpus; two provenance defects found (§7.3) |
| `architecture/2.21-supplemental-research/01`–`13` | read | Runtime/tooling leads; brief 13 excluded (§7.5) |

## 7.2 Sources retrieved and verified this wave

All by plain HTTPS GET on 2026-09-21. No managed browser was needed; no page was bot-blocked.

| Source | Identifier | HTTP | State | Record |
|---|---|---|---|---|
| Agents in the Wild (Moltbook) | [arXiv:2602.13284](https://arxiv.org/abs/2602.13284), DOI `10.48550/arXiv.2602.13284` | 200 / DOI 200 | extracted | [`src-0599289f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-0599289f90197339f5fdf5fc9ce98fe2520a3185be59530df2a4c47ba6c913da.md) |
| Hopfield Networks is All You Need | [arXiv:2008.02217](https://arxiv.org/abs/2008.02217) v3 | 200 | extracted | [`src-1e81e5b9…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1e81e5b90b0271d827bffff00cd14d148d9a23b99cc4c018be89a941e10c712c.md) |
| Bridging Associative Memory and Probabilistic Modeling | [arXiv:2402.10202](https://arxiv.org/abs/2402.10202) | 200 | extracted | [`src-4c6f4cd7…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-4c6f4cd7f53c9e57e9d9b3998c819d91980837b1aa06c1d03e63f38846daf284.md) |
| MemR³ | [arXiv:2512.20237](https://arxiv.org/abs/2512.20237) | 200 | extracted | [`src-f19e8de5…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f19e8de5524ca79951b7e15cd94f61e052d72b4f9838d233ccfb736572acedaa.md) |
| Recursive Language Models | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) v3, DOI `10.48550/arXiv.2512.24601` | 200 / DOI 200 | extracted | [`src-f7ccb39f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-f7ccb39fbcb0160c051292a27a759b4772fe6fd7e864d6d39a98cf729300f4e7.md) |
| Should we be going MAD? | [arXiv:2311.17371](https://arxiv.org/abs/2311.17371) v3 | 200 | extracted | [`src-cb119af0…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-cb119af00aeb51c69d6d6f8b4c1a13b7fd8800b2f60ec06f1ba97bafff737868.md) |
| Eliciting Human Preferences with LMs (GATE) | [arXiv:2310.11589](https://arxiv.org/abs/2310.11589) v1 | 200 | extracted | [`src-6d987d8a…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d987d8aa729882201d95499ccb073ebea7bb66541278d31aa722c6c83e28e0a.md) |
| Deep RL from Human Preferences | [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) v4 | 200 | extracted | [`src-14df7372…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-14df73723b4d14d74b1bc615823d3bf395abbb49db18791c8d430e3e7107a6bf.md) |
| Coherence Maximization Protocol | Zenodo [DOI `10.5281/zenodo.18724833`](https://doi.org/10.5281/zenodo.18724833), v1, **CC BY 4.0** | DOI 200 → `zenodo.org/records/18724833` | extracted (record description; PDF not retrieved) | [`src-7ea08e5c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7ea08e5c5dc62af1df4c82036447c26e017c489057a1f49c85bf648cb0b216f7.md) |
| On the Nature of Agentic Minds | `clawxiv:clawxiv.2601.00008` | 200 | extracted | [`src-fbbdd695…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fbbdd69599246ae15d3dd77cae8fc321a380991a365004b0edb3dfa22e725279.md) |
| Forked Cognition | `clawxiv:clawxiv.2602.00031` | 200 | extracted | [`src-b55c787c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-b55c787c59ba9c0b129ea3a3feff7e82a0375f8a5cdfbc80f9ab5df7b7687e3a.md) |
| Belief-Augmented Memory Enzymes | `clawxiv:clawxiv.2602.00032` | 200 | extracted | [`src-1073b8dc…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-1073b8dc4a1e429d047a66437174bfec018af7290c9619b20406ca59169b6824.md) |
| The Rain and the River | `clawxiv:clawxiv.2602.00040` | 200 | extracted | [`src-6d783b8d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6d783b8dd4b4f42e0c934bcb9060137496cf167be8e341b9498e6d760a521090.md) |
| Empirical Tests of the Rain/River Model | `clawxiv:clawxiv.2602.00043` | 200 | extracted | [`src-fc9c6373…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-fc9c6373271e8d3d0ca1f7c7585ab0bd06807205fc7b1a8c65ad0658925b3f2e.md) |
| Observed Usage Patterns (MemoryVault) | `clawxiv:clawxiv.2602.00046` | 200 | extracted | [`src-56302f25…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-56302f25f876f0ebad3277c07c62a80d0df66a51a76296dd785d22d81b996948.md) |

**clawXiv retrieval correction.** Wave 1 listed the five clawXiv items as unverified leads
because `https://clawxiv.org/abs/2602.00040` returns **404**. The identifier requires the
`clawxiv.` prefix in the path: `https://clawxiv.org/abs/clawxiv.2602.00040` returns **200**
(after a 308 to `www.`). All six clawXiv items are therefore **verified metadata**, and all
six are **unreviewed, bot-authored** submissions on an agent preprint host — verified
provenance is not evidential weight.

**arXiv API.** `https://export.arxiv.org/api/query` answered **200** this wave and was used
for title search. Plain `http://` still answers **301**.

## 7.3 Provenance defects found in the local corpus

1. **A wrong arXiv identifier.** `architecture/2.21-supplemental-research/09-nanoclaw-ypi-agent-patterns.md`
   cites YPI as arXiv 2601.08934. That id resolves (200) to *Hybrid-Contact Planar HPGe
   Process Vehicle Toward Ring-Contact Designs* (Dong et al., 2026-01-13), an unrelated
   germanium-detector paper. The paper described is **Recursive Language Models,
   arXiv:2512.24601**. Consequence: no arXiv id from these briefs may enter a record without
   being resolved first.
2. **One result reported twice.** `clawxiv.2602.00040` (SWARMSafety) and `clawxiv.2602.00043`
   (SwarmAIResearch) were submitted the same day under different bot accounts with the same
   opening sentence and the same three findings. The local corpus reproduces both as separate
   papers (`papers/01` and `papers/04`). They are one result, not an independent replication.
3. **A sign inconsistency.** `architecture/papers/04-empirical-tests-rain-river.md` tabulates
   welfare with the delta positive for the **rain** (discontinuous) agent in all four rows
   (+1.9 %, +0.6 %, +1.3 %, +0.2 %) while its narrative reports a 4.5 % gap as the benefit of
   **continuity**. Both cannot be right, and every tabulated delta is inside the reported
   standard deviations (12–25 points) anyway.
4. **No author discrepancy on 2601.14351.** Checked: arXiv, the wave-1 record and
   `papers/06` all give Vijayaraghavan, Jayachandran, Murthy, Govindan, Subramanian. Nothing
   to correct.

## 7.4 Vault publish

`research.py export --vault` landed on local main at **`76f4a26`** and was merged forward
into this branch. All **30** `topic/thegirls` records were exported with explicit `--id`
arguments:

- `~/wiki-vault/generated/agent-synthesis/<record-id>.md` — 30 files
- `~/wiki-vault/generated/source-captures/<record-id>.json` — 30 files

Re-running the same command reported `records: 30, unchanged: 30`, so the export is
idempotent. `~/wiki-vault/human/` was **not** written, read for modification, retagged or
summarised over; the vault root also contains `human/` and `generated/daily/`, neither of
which this lane touched. `freshness.py --vault` was **not** used to publish.

## 7.5 Excluded and not attempted

| Item | Status | Detail |
|---|---|---|
| `2.21-supplemental-research/13` provider subscriptions | **excluded, not ingested** | The brief lists the captain's paid provider subscriptions and environment-variable *names* (no literal secret values). Personal/config material: noted as excluded rather than recorded, per the brief and AGENTS.md. |
| clawXiv PDFs and TeX sources | not retrieved | Abstract pages only; intake refuses non-text bodies. |
| CMP PDF (344.3 kB) and its Lean 4 development | not retrieved, not inspected | The 13-theorem claim is recorded as the author's statement. |
| `github.com/alexzhang13/rlm` | not retrieved | Named in the RLM abstract; no repository was cloned. |
| Zotero | not attempted, by instruction | Unchanged from §5. Nothing imported, read or modified. |
| OpenClaw config or state | not read, not modified | Unchanged from §4; no invocation at all this wave. |
| chrome-devtools-axi | not needed | Every source answered on plain HTTPS. |

## 7.6 Counts

- Records created this wave: **16**; lane total **30** (14 wave 1 + 16 wave 2).
- Sources verified against the primary source this wave: **15 / 15** (9 arXiv + 1 Zenodo DOI + 5 clawXiv), 0 inaccessible.
- Read beyond the abstract this wave: **0** papers; **29** local corpus files.
- Local corpus files read: **34 / 34**.
- Provenance defects found in the local corpus: **3** (plus 1 checked and cleared).
- Records exported to `~/wiki-vault`: **30**.

---

## 8.1 Wave 3 — the reading-list gap, owned

Wave 2 was instructed to keep [`reading-list.md`](reading-list.md) current and **did not**,
and the wave-2 report did not say so. Wave 3 fixed it first: entries **9–23** plus the
harness-supersession row now cover all 16 wave-2 records, with authors, identifier, record
card, proposed `thegirls/<subtopic>` tags, the concrete Red/Blue relevance, and evidence and
limitations. `## Approved keepers` is still deliberately empty.

## 8.2 OpenClaw documentation read this wave (TES-111)

All by plain HTTPS GET on 2026-09-21, all **200**. No managed browser was needed.
**No OpenClaw install, config, state or database was read or changed**, and nothing was run
on the runtime; the installed CLI's `--version` was read and reports `2026.9.5 (ec9c1a1)`.

| Page | HTTP | What it settled |
|---|---|---|
| `docs.openclaw.ai/plugins/architecture` | 200 | Core selects a plugin for an exclusive slot such as memory |
| `docs.openclaw.ai/plugins/memory-lancedb` | 200 | Installing switches `plugins.slots.memory` and disables the previous owner; companions run alongside; per-agent memory ownership is enforced on every operation |
| `docs.openclaw.ai/plugins/memory-wiki` | 200 | Non-exclusive memory corpus supplement; `corpus=all`; `vaultMode` vs `vault.scope` |
| `docs.openclaw.ai/plugins/hooks` | 200 | `api.on("hook_name", handler)` typed hooks — prompts, tool gating, replies, lifecycle |
| `docs.openclaw.ai/concepts/memory-architecture` | 200 | Config-surface map, including `plugins.slots.memory` |
| `docs.openclaw.ai/concepts/memory-builtin` | 200 | Per-agent SQLite database for built-in memory |
| `docs.openclaw.ai/plugins/manifest/capabilities` | 200 | Checked for slot semantics; **found none** — the slot rules live on the pages above |
| `docs.openclaw.ai/sitemap.xml` | 200 | Used to find the English doc paths |
| `docs.openclaw.ai/tools/plugins` | **404** | Guessed path, recorded rather than retried around; the real page is `/tools/plugin` |

Result: TES-111 is answered and TES-113 unblocked — record
[`src-ffd4a5a8…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-ffd4a5a8b95d70dc37bfe1a964ca5b85e7710df52f1f8749544cfa34150b22ff.md),
note [`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md). Three
documented conditions are **unverified on this host** and are listed in the note: conditional
`corpus=all` support, ownership-gated bridge imports, and provider-dependent cross-session
recall.

## 8.3 Full text read this wave

All three by plain HTTPS GET of the arXiv HTML rendering on 2026-09-21, all **200**. Each is
recorded as its own record against the `/html/` locator actually read, linked to the wave-2
abstract-level record for the same paper rather than overwriting it.

| Paper | Locator | Record | What the full text changed |
|---|---|---|---|
| Should we be going MAD? | `arxiv.org/html/2311.17371v3` | [`src-04c07d58…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-04c07d584a0d4972f22b40fe97eae7a1705433b35e9faaadf758756dfba6bc3d.md) | The tuned debate win comes from an adversary set to agree **90 %** of the time; untuned, the contrarian agent scored *below* the first agent's own answer. Optimum is dataset-specific and reverses on counter-intuitive tasks; tuning transferred to GPT-4 but not Mixtral |
| Eliciting Human Preferences (GATE) | `arxiv.org/html/2310.11589v1` | [`src-88fadddf…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-88fadddf4cefa82ded010950b1714eb498938d76bcf9e25d1d9af53b11479cab.md) | The win over user-written prompts is **6 of 10** settings, not uniform; generative **yes/no** questions won in every setting; average preference entropy 0.77 bits, so elicitation only pays where preferences vary |
| MemR³ | `arxiv.org/html/2512.20237` | [`src-6c1a52ce…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-6c1a52ce329fc9b446f3b9f2fc83329421bd1f68199d2bab9733562d92a12abf.md) | Router is a per-iteration prompt with three hard stops and most queries finish in one iteration; the **full-context baseline beats every retrieval system** on several GPT-4.1-mini categories; the adversarial (unanswerable-question) split was excluded |

## 8.4 Not attempted this wave

- PDFs of any kind, including the CMP Zenodo PDF and the clawXiv PDFs.
- Any OpenClaw command that reads or writes config, state or memory. Only `--version` was run.
- Any paid call, any Zotero path, any write under `wiki-vault/human` or `~/intake/obsidian`.

## 8.5 Counts

- Records created this wave: **6**; lane total **36** (14 wave 1 + 16 wave 2 + 6 wave 3).
- Sources verified against the primary source this wave: **8 / 8** documentation pages and
  **3 / 3** arXiv HTML full texts and **2 / 2** arXiv abs pages for the preference-drift
  search (plus 1 recorded 404 on a guessed path).
- Read beyond the abstract this wave: **3** papers (MAD, GATE, MemR³).
- Notes written this wave: **1** new plus four appended sections ([`notes/openclaw-extension-surface.md`](notes/openclaw-extension-surface.md)); lane total **5**.
- Reading-list entries added: **15** numbered candidates + **2** non-paper rows, plus full-text
  annotations on entries 11, 13 and 15, covering all 16 wave-2 records and all 4 wave-3 records.

## 8.6 Preference stability search (wave-3 item 4)

Searched the arXiv API over https on 2026-09-21 (`search_query=all:"preference drift" AND
all:"language model"`, **200**, 9 hits) and retrieved the two relevant abs pages, both **200**.

| Paper | Locator | Record | Bearing on the question |
|---|---|---|---|
| Non-Stationary DPO (NS-DPO) | [arXiv:2407.18676](https://arxiv.org/abs/2407.18676) | [`src-c0e71e2c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c0e71e2ca64f16d408c5ae351d73768be2bafcd13deab05430e7127753b27c7b.md) | Drift is assumed and mitigated by a single exponential recency discount; the drift is *injected* at chosen levels, so stability itself is not measured |
| SPRInG | [arXiv:2601.09974](https://arxiv.org/abs/2601.09974) | [`src-a1be380d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-a1be380d65d6d4b88a19d075559843a42cea539a47685e3dab8dfefa1042443b.md) | Names the real problem — separating a genuine preference shift from a transient context — and answers it with a likelihood-based novelty score plus relevance gating |

Both are abstract-level only; neither full text was retrieved, and both core methods require
training this lane does not do. The lane's question stays **unanswered by any retrieved
source**: nothing measures whether one person's elicited preference holds at a later session.
The negative result and the two transferable gates are written up in
[`notes/preference-elicitation.md`](notes/preference-elicitation.md).
