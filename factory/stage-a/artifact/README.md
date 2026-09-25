# Stage A artifact

This is the retained source, tests and golden context fixture for the offline synthetic persona simulation. It uses Python 3.11+ and the standard library only. It does not implement a live runtime or contact a provider, connector or channel.

The policy checks use inert `/MOCK_ONLY/...` path strings. They test policy logic only, not operating-system isolation. GPT-6 Astra subscription and OpenRouter promo choices, per-channel/task assignments, the Claude Opus external-advice stub, costs and the clock are synthetic.

## Files

- `../report.md`: standalone result, stop-condition evidence, limitations and Stage B gates.
- `src/persona_stage_a.py`: append-only episodes and journals, summaries, bounded context, mock policy, model choice/use log, fake clock, change control, child task and stop gate.
- `tests/test_stage_a.py`: 13 offline `unittest` cases.
- `tests/golden/contexts.json`: frozen expected context output.
- `demo/`: final synthetic context, capability, operation-count and route-ledger artifacts.
- The source command-output transcript is intentionally not included in this archive under the no-transcripts rule.
- `deletion-manifest.txt`: inventory and exact disposable-tree cleanup target.

## Re-run

Copy this directory's `src/` and `tests/` into a fresh directory created with `mktemp -d`. Redirect `HOME` and each `XDG_*` directory into that same temporary root, set `STAGE_A_ROOT` to the root, then run:

```sh
python3 -m unittest discover -s tests -v
STAGE_A_DATA="$STAGE_A_ROOT/project/demo-data" python3 src/persona_stage_a.py
```

Use a new empty `STAGE_A_DATA` directory for each demo run. The demo refuses to reuse a populated path so it cannot silently append a second fixture set. Remove only the exact temporary root after retaining any output you need. The source includes a guarded `teardown_disposable_tree(root, expected_root)` helper that refuses a different target.

A passing test run is not authorization to deploy Red or Blue. Stage B must test real OS boundaries, connectors, model continuity and billing before live state or credentials are considered.
