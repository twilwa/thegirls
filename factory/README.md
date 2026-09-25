# Red and Blue factory archive

This folder collects the persona-design reports, research notes, SillyTavern cards, Stage A prototype, and separation report. The index below gives the production date of each set of files.

Deployment is on hold as of 2026-09-25 while the captain spends time with Red and Blue first. The current plan is to deploy them on the captain's own machine, not this fleet host. No live persona has been launched here.

Some copied reports contain absolute VPS paths. They are preserved as written and refer to the fleet host, not to this repository or the captain's machine. The Stage A command-output transcript was not copied. No conversation exports or private persona chats are included.

## Index

### `persona-design/`, produced 2026-09-25

- `captain-direction-2026-09-25.md`: concise summary of the captain's design goals. Routing metadata and worker instructions from the source were left out.
- `foundation/report.md` and `foundation/wiki-note.md`: initial foundation evaluation.
- `design/report.md`, `design/design-summary.md`, and `design/wiki-note.md`: first locked design and summary.
- `design-rev/report.md`: revision to the foundation analysis.
- `refound/report.md`, `refound/design-summary.md`, and `refound/wiki-note.md`: reopened comparison and updated recommendation.

### `stage-a/`, produced 2026-09-25

- `report.md`: offline prototype results, limitations, and Stage B gates.
- `artifact/README.md`: source and test guide.
- `artifact/src/persona_stage_a.py`: prototype implementation.
- `artifact/tests/test_stage_a.py` and `artifact/tests/golden/contexts.json`: tests and expected context fixture.
- `artifact/demo/capability-matrix.json`, `contexts.json`, `demo-result.json`, `journal.jsonl`, `operation-counts.json`, `route-ledger.json`, and `route-ledger.jsonl`: synthetic demonstration outputs.
- `artifact/deletion-manifest.txt`: disposable-tree inventory and guarded cleanup instructions.

The original test transcript is deliberately absent. From `factory/stage-a/artifact/`, `python3 -m unittest discover -s tests -v` passed all 13 tests on Python 3.12.3 with `STAGE_A_ROOT`, `HOME`, and the XDG directories pointed into a fresh disposable `/tmp/sr-persona-stage-a.factory-tests.*` tree. The same result is recorded in the PR.

### `separation/`, produced 2026-09-25

- `report.md`: Stage B isolation recommendation and host limitations.
- `vault-note.md`: concise separation note for the wiki.

### `research/`

The research-wiki wave 1 materials and Zotero import files were produced 2026-09-21. The seven `notes/*.md` files are waves 2 through 4, also dated 2026-09-21. The copied `README.md`, `coverage.md`, `reading-list.md`, `notes/`, `zotero-import.bib`, and `zotero-import.ris` form the research bundle. Links to record cards and wiki guidance point to `research-wiki` `main`, since those linked files are not part of this archive.

### `personas/`, sourced from `research-wiki` `main` on 2026-09-25

- `red.card.json` and `blue.card.json`: SillyTavern v2 character cards, copied byte-for-byte from main. Their Git blob IDs are `db239ba101aca5139a2cd7d22345769eef23f700` and `ca07656be8c3684e8c57a73387caae314596c3c2`.
- `red-and-blue-everything-so-far.md`: persona compendium from `research-wiki` `main` blob `8765fd37cbf9d707dc96f2e58f2c2a3b0760837c`. Its unavailable agentic-internet map reference is plain text because that target is not present in the upstream tree and is not included here.
