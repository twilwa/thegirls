# OpenClaw host-conditions check: the three conditions, run against the install

Wave 4 note, 2026-09-21. This is the on-host counterpart to
[`openclaw-extension-surface.md`](openclaw-extension-surface.md), which read the vendor
documentation and closed by naming **three conditions that must be checked before TES-113
relies on this**. Those three are checked here.

**Read-only, and nothing was changed.** No login, no config write, no agent turn, no gateway
start, no plugin enable, no memory index, no import. The check ran only inspection surfaces:
`--version`, `--help` on the relevant command groups, `plugins list`, `plugins inspect`,
`config get` on four paths, `config schema`, `docs <query>`, and `doctor --lint --json
--non-interactive` — which OpenClaw's own `doctor --help` documents as "Run read-only health
checks and report findings". `openclaw memory status`, `memory index`, `doctor --fix` and
anything under `wiki`, `agent` or `gateway` were deliberately **not** run.

Install under test: `~/.local/bin/openclaw` → `../lib/node_modules/openclaw/openclaw.mjs`,
reporting `OpenClaw 2026.9.5 (ec9c1a1)`.

## Host baseline

`openclaw plugins list` reports **39 of 61 plugins enabled** from the stock source root
`~/.local/lib/node_modules/openclaw/dist/extensions`. The three that decide these conditions:

| Plugin | ID | Status on this host |
| --- | --- | --- |
| OpenClaw Memory | `memory-core` | **enabled** (bundled, 2026.9.5) |
| Memory Wiki | `memory-wiki` | **disabled** |
| Active Memory | `active-memory` | **disabled** |

`memory-lancedb` is **not installed at all** — it does not appear in `plugins list`. That
matters, because two of the three documented conditions are stated about LanceDB.

## Condition 1 — `corpus=all` is conditional

**Does not hold as installed.** The capability exists in 2026.9.5; it is not available here.

The docs said `corpus=all` works "when the active memory plugin supports corpus selection"
without asserting that support for either builtin or `memory-lancedb`. `openclaw config
schema` resolves that ambiguity: the setting exists at exactly one path,

```
plugins.entries.memory-wiki.config.search.corpus   enum: ["wiki", "memory", "all"]
```

alongside `…config.search.backend` (`shared` | `local`). Corpus selection is therefore a
**`memory-wiki` setting**, not a property of the builtin engine and not a LanceDB feature —
which is why the docs could not assert it for either. On this host `memory-wiki` is disabled,
and `openclaw wiki --help` refuses outright: *"The `openclaw wiki` command is provided by the
"memory-wiki" plugin, but that bundled plugin is disabled by default."* The path is also
unset: `config get plugins` reports "valid but unset".

Note separately that the CLI has no corpus flag — `openclaw memory search --help` offers only
`--agent`, `--json`, `--max-results`, `--min-score`, `--query`. Corpus selection is a config
and tool-level surface, not a CLI one, so a shell-level check of cross-corpus recall is not
available even once the plugin is on.

**What this means for the design.** Cross-corpus recall spanning session memory and the wiki
is a real 2026.9.5 feature behind two steps that are state changes and were not taken here:
enable `memory-wiki`, then set `plugins.entries.memory-wiki.config.search.corpus`. Until
someone does that deliberately, any design that assumes one `memory_search` reaches both
layers is assuming a capability this host does not currently have.

## Condition 2 — bridge-mode imports are ownership-gated

**Could not be determined.** The surface is confirmed present; the gate is runtime behaviour
that cannot be observed without changing state.

`config schema` confirms the bridge surface exists under `plugins.entries.memory-wiki.config`:

- `vaultMode` — enum `["isolated", "bridge", "unsafe-local"]`
- `bridge` — `enabled`, `readMemoryArtifacts`, `indexDreamReports`, `indexDailyNotes`,
  `indexMemoryRoot`, `followMemoryEvents`

So bridge mode is real and its read surface is granular. But the documented gate — that an
agent-scoped import accepts a public memory artifact "only when it carries ownership
metadata", skipping artifacts with missing or unknown owners — is a property of what the
importer *does* with an artifact. Observing it requires enabling `memory-wiki` and running an
import against artifacts with and without ownership metadata. Both are state changes and
outside this check's authority, and `openclaw wiki bridge --help` is unreachable while the
plugin is disabled. The documentation's statement therefore stands unchallenged and
unconfirmed.

**What this means for the design.** Unchanged from the wave-3 note: treat silent
under-import as the expected failure and verify ownership metadata is present on anything fed
to a shared wiki. This check neither strengthened nor weakened that.

## Condition 3 — cross-session recall is provider-dependent

**Could not be determined, and it is moot as this host is configured.**

The documented check is `openclaw doctor`, which the vendor troubleshooting page says will
"verify the current memory provider supports protected transcript recall".
`doctor --lint --json --non-interactive` ran **35 checks and skipped 30**, and returned four
findings, none about memory:

- `core/doctor/gateway-auth` — gateway auth off or missing a token
- `core/doctor/gateway-config` — `gateway.mode` unset, so gateway start is blocked
- `core/doctor/heartbeat-cadence-migration` — heartbeat monitor not materialised in cron
- `core/doctor/node-hosting-preconditions` — gateway bound to loopback only

The memory-provider check is among the 30 that did not run, and the reason is visible in the
baseline: `config get memory.search.rememberAcrossConversations` is unset, and the
`active-memory` plugin — which `plugins list` describes as the component that "implements
per-agent Remember across conversations for eligible private conversations" — is disabled.
There is no configured memory provider for doctor to interrogate.

The condition is also moot in its literal form. It was stated about LanceDB's `memory_recall`
not receiving the protected private transcript authorization used by
`memory.search.rememberAcrossConversations`. `memory-lancedb` is not installed, so that
specific gap is not live on this host.

**What this means for the design.** The wave-3 conclusion survives intact and is now sharper:
continuity across sessions is a property of a provider that has to be chosen and enabled, not
something the memory slot supplies. On this host nothing supplies it yet. A design that
assumes Red and Blue remember across sessions is, today, assuming a plugin that is switched
off.

## Summary

| Condition | Verdict | Decided by |
| --- | --- | --- |
| 1. `corpus=all` is conditional | **Does not hold as installed** | `config schema` locates the setting under the disabled `memory-wiki` plugin |
| 2. Bridge imports are ownership-gated | **Could not be determined** | Runtime import behaviour; checking it requires enabling a plugin and importing |
| 3. Cross-session recall is provider-dependent | **Could not be determined** | The doctor check did not run; `active-memory` disabled and no provider configured |

One condition resolved, two left open — and both remain open for the same reason: the
capabilities they describe are behind plugins that are off, and turning them on is a decision
for whoever owns this host, not something a read-only check may do. The practical finding for
TES-113 is blunter than any of the three: **all three memory capabilities the persona design
leans on are currently inert on this install.** `memory-core` is the only memory plugin
enabled. That is a smaller problem than a capability that does not exist, and a larger one
than the wave-3 note implied, which read the documentation as describing a surface that was
present and merely conditional.

## Limitations of this note

A read-only inspection of an install is not a test of its behaviour. Everything above is
either a configuration fact (`plugins list`, `config get`, `config schema`) or an absence of a
finding (`doctor --lint`), and an absence of a finding is weak evidence: the memory check may
have been skipped for a reason other than the one inferred here, since `doctor --lint` reports
the skip count but not which checks were skipped or why. Nothing here observed an import, a
recall, or a search actually running. Conditions 2 and 3 are recorded as undetermined rather
than as holding or failing precisely because determining them requires running the system, and
the two verdicts of "could not be determined" should not be read as leaning either way.
