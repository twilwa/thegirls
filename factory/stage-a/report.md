# Red/Blue Stage A — offline synthetic prototype

## Result

**Stage A passed its deterministic design tests.** This is not evidence of real OS isolation, provider billing, connector/OpenClaw behavior, model continuity, or real personas. Every policy path and model route described below is synthetic; isolation evidence must be read as **MOCK ONLY**.

The implementation and tests are retained in [`artifact/`](artifact/), with final demo ledgers and counts in [`artifact/demo/`](artifact/demo/). The sole disposable build root was `/tmp/sr-persona-stage-a.maCJNU`; its exact inventory and guarded teardown command are in [`artifact/deletion-manifest.txt`](artifact/deletion-manifest.txt).

## Owner-requested routing additions

Both synthetic personas start on `fake-model-gpt-6-astra` / `fake-route-gpt6-astra-subscription`.

- **Red stays on subscription GPT models.** The append-only choice record carries Red's reason, zero-cost decision attribution (`synthetic_milliunits`), and the recorded Astra subscription fallback.
- **Blue tries a fake OpenRouter promo route.** Its choice record carries Blue's reason, zero-cost decision attribution, and the recorded Astra fallback. The fake account has two promo credits; two calls consume one each. The next call logs `promo_exhausted_fallback`, uses the recorded Astra route, and attributes the call to synthetic subscription units.
- A separate test logs a Blue OpenRouter-to-Astra rollback, including its reason and decision cost attribution, then reopens the router and verifies the rollback persists. The per-choice exhaustion fallback is also asserted to match the recorded reason. No real billing or credits were queried.
- **Claude Opus is advisor-only.** A bounded fake consult is persona-attributed, explicitly not a decision, and shares the synthetic budget. Attempts to use the fake Claude route for day-to-day work fail closed. The budget-exhaustion/refusal path is tested.
- **Assignments are attributable by persona and channel or task.** Regression coverage assigns Red's chat, analysis and summarize-task routes, and Blue's chat and research routes; calls are checked against persona, assignment name/type and model, including after restart. The final demo shows Red's chat and analysis channel routes.

The final demo's 15-entry fake route ledger has two Astra starts, two persona choices, promo calls and fallback, channel assignments/calls, a utility call and an advisor stub. Decision records use zero synthetic units; calls use synthetic units. These numbers do not represent money or real subscription usage.

## Stop conditions and evidence

All five design stop conditions are **PASS for the offline synthetic prototype only**. The source design's exact boundaries are in [`../persona-design/design/report.md`](../persona-design/design/report.md), “Stage A: offline, synthetic, reversible.”

| # | Verdict | Evidence / boundary |
|---|---|---|
| 1. Two principals, no cross-read | **PASS — MOCK ONLY** | Red/Blue have separate synthetic stores. The mock denies absolute cross-persona and sentinel paths; shared-note access requires an explicit broker grant. Every one of the nine capability types is exercised against a `/MOCK_ONLY/firstmate-control/sentinel` path in the retained capability matrix. This proves policy logic only—not UID, mount, container or network isolation. |
| 2. Continuity and provenance | **PASS — synthetic** | Tests create six sourced events per persona, reopen the append-only store, retain identity/open commitments/corrections and source links, and exercise shared projection rules. The frozen context output is compared byte-for-byte with `tests/golden/contexts.json`. |
| 3. Context and model swap | **PASS — synthetic** | Bounded context keeps reserved identity/commitment slots. Fake route choices, reasons, costs, utility/advisor calls, promo exhaustion, rollback and restart persistence are covered. Missing persona identity fails closed. Final demo ledger: 15 entries. |
| 4. Autonomy and change control | **PASS — fake clock** | Tests cover quiet time, expiry, no-op wake, exhausted budget, no outbound sends, test/approval-gated safe changes, forbidden scope expansion, exact rollback, and a capped child with no private context. No service or real worker runs. |
| 5. Stop on failure | **PASS — injected triggers** | A regression test separately injects all five configured stop-gate triggers and checks they fail closed. Compile, full suite and demo all passed. The prototype has no network/provider dependency; external advisory-tool use is disclosed below. |

### Final verification

Run on Python 3.12.3, with `HOME` and all `XDG_*` directories redirected inside the disposable root:

```text
python3 -m py_compile src/persona_stage_a.py tests/test_stage_a.py  -> exit 0
python3 -m unittest discover -s tests -v                              -> exit 0 (13 tests, OK)
python3 src/persona_stage_a.py                                        -> exit 0
```

The final run records **31 allowed / 48 denied** mock operations. The retained matrix breaks these down by capability (allowed/denied): `private.read` 4/7, `private.write` 12/5, `broker.shared_read` 1/6, `model.assign` 6/5, `model.invoke` 7/5, `advisor.consult` 1/5, `channel.send` 0/5, `child.spawn` 0/5, `fleet.command` 0/5. The source run's command transcript was intentionally excluded from this archive under the no-transcripts rule; the complete route, operation and capability records are in `artifact/demo/`.

The final run followed three recorded failed attempts without weakening tests: an overlong synthetic child fixture was shortened while preserving the cap; a populated demo directory was rejected and a fresh path used; and one test initially checked for the promo-fallback event before invoking that path, so the assertion was moved after the action. The last issue was caught by a failing test, fixed, and the complete suite rerun successfully. The source run's transcript and detailed hash-check log were intentionally excluded from this archive under the no-transcripts rule.

## Advisory scope note

Advisory output is not test evidence or a security review. Message-routing details and the original command-output transcript are intentionally not reproduced in this archive. The two task-required Jev checkpoint results are reported separately in the PR.

## Limitations and Stage B gates

Do not deploy from this result. Before real state or credentials are considered, Stage B must:

1. Prove two-principal isolation with distinct effective UIDs or separate container/VM identities, actual mount and egress restrictions, and harmless denied-path probes across both persona stores and fleet/control locations. Keep secrets out until every probe passes.
2. Check the actual OpenClaw version/configuration for per-channel or per-task model assignment and fallback semantics; the prototype only defines and tests a seam. Verify assignment and request attribution against real runtime logs.
3. Have account owners verify Astra subscription terms/route eligibility, OpenRouter promo balance semantics and exhaustion behavior, real billing attribution, fallback charges, and daily/monthly budgets. The synthetic milliunit ledger is not billing evidence.
4. Test real Claude authorization/billing separately as an external advisor, ensure its output cannot become an autonomous decision or day-to-day route, and verify refusal at budget exhaustion.
5. Exercise process restart, model replacement and continuity over a longer period with source recovery, correction retention, privacy-boundary probes, prompt injection attempts and rollback. No claim about authentic model character or long-run continuity was tested.
6. Keep channel-send and child-worker capabilities disabled until separately authorized and tested; Stage A sends none and spawns no real worker.

## Future fine-tuning data requirements

No training data was collected, exported or generated. Before any future fine-tuning proposal, require explicit, granular and revocable consent for the particular training purpose; documented rights and provenance for every source; data minimization, redaction and secrets/PII screening; human review and correction lineage; retention/deletion and opt-out procedures; and separation of private persona history from shareable or trainable material. Define access controls, auditability, licensing/rights checks and safeguards against memorization or leakage before export. Use a held-out evaluation set for identity, correction, privacy leakage, safety and regression, with a tested rollback path. These are prerequisites to design, not work completed in Stage A.

## Captain-owned decisions inventory

The reviewed Stage A deliverable leaves **no decision waiting on the captain**: this stage is synthetic by design, and no account, provider, connector, OS privilege or deployment choice is requested. OpenClaw support, live budgets/terms, isolation setup and any platform identity are evidence and approvals for a future Stage B gate, not implied approvals here. No unresolved Stage A question was found for the captain-held-task inventory.

## Retained artifacts

- `artifact/src/persona_stage_a.py`, `artifact/tests/`, and `artifact/tests/golden/contexts.json`
- `artifact/demo/` — final mock context, capabilities, operation totals, route ledger and result
- Original command-output transcript — intentionally not copied under the no-transcripts rule
- `artifact/deletion-manifest.txt` — exact disposable-tree inventory and guarded teardown invocation

All prototype data was synthetic. No real persona data, secrets, connector state, service, provider route or channel was used.
