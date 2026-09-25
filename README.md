# The Girls

Private research, design, and continuity material for Red and Blue.

## Layout and ownership

The top-level notes, `architecture/`, `papers/`, `transcripts/`, and `wiki/` preserve the local project material. Treat earlier designs as research history, not proof of deployed capabilities.

`sm-research` owns the factory workstream. It adds `factory/` through a pull request for the persona design reports, Stage A prototype, reading list, character cards, and compendium. Keep those additions separate from the original material. Link research claims to sources and distinguish proposals from tested behavior.

## Delivery

The initial local import goes to `main`. Subsequent changes use normal PRs; the factory may merge routine notes and design changes without the full validation pipeline. Executable changes still need appropriate focused checks. Authentication and deployment decisions remain separate from merging research.

## Material intentionally kept local

Personal Claude/ChatGPT exports under `agent-context/` are symlink targets outside this folder and are not imported. `full-claude-convo.md` is also excluded. Including personal conversations requires a separate explicit decision and commit. Original audio/video recordings, local tool state, and vendored source mirrors are excluded; the written research and transcripts are retained.

Vendor references, rather than source copies:

- [OpenClaw](https://github.com/openclaw/openclaw)
- [Milaidy](https://github.com/milady-ai/milaidy)
- [Lightshell](https://github.com/twilwa/lightshell)
- [Agentic Coding Flywheel Setup](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup)
- [CICADA-71 / shards](https://github.com/meta-introspector/shards)

`architecture/repos/` and `KAN-directory/` are also local vendor collections; consult the research notes for relevant sources. Their source trees are not part of this repo.
