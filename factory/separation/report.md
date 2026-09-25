# Red and Blue: separation decision for Stage B

25 September 2026; updated after the captain's 2026-09-25 decision. **All deployment is on hold.** The captain will spend time with Red and Blue first and intends to give them their own machine. Nothing in the provisioning section below is authorized to run. For the earlier shared-host question, the best practical method was two locked host users with separate rootless Podman containers, root-owned service definitions and no network by default; on a dedicated machine, the same inter-persona boundary still matters. Persist only each persona's own state; let her change her own code and restart her own service, not the service's mount, privilege or network policy. Consult-Opus stays outside both personas. This report compares options and records a **paused** runbook, not a claim that Stage B passed. Nothing was installed, logged in, launched, or given credentials.

## What the host actually supports

Read-only checks on this Ubuntu 24.04 VPS on 2026-09-25 UTC:

| Check / command | Observation |
| --- | --- |
| `stat /dev/kvm`, `uname -a`, `lscpu` | `/dev/kvm` absent; Linux `6.8.0-139-generic`, x86_64 guest on KVM, 8 AMD EPYC vCPUs. Nested virtualization cannot be presumed. |
| `free -h`, `df -h /` | 23 GiB RAM, 12 GiB available, no swap; root volume 290 GiB, 232 GiB free. This is a point-in-time reading, not a guaranteed reservation. |
| `sysctl kernel.unprivileged_userns_clone user.max_user_namespaces kernel.apparmor_restrict_unprivileged_userns`; `unshare --user --map-root-user id` | `1`, `95973`, `1`; raw unshare **failed** `write failed /proc/self/uid_map: Operation not permitted`. Ubuntu AppArmor's namespace restriction is active. `/etc/apparmor.d/podman` exists and names `userns`, but Podman itself is not installed. **Do not claim rootless containers work yet.** Verify with a real rootless Podman probe after installation; if it fails, stop and fix the narrow Podman AppArmor/uidmap issue, not global userns restrictions. |
| `command -v podman runsc bwrap firecracker newuidmap slirp4netns`; `apt-cache policy podman uidmap` | None installed; Ubuntu repo offers Podman 4.9.3 and uidmap. No gVisor, bubblewrap, or Firecracker binary. |
| `stat -fc %T /sys/fs/cgroup`; `systemctl --user show-environment`; `loginctl show-user firstmate -p Linger -p State` | `cgroup2fs`, active user manager, firstmate linger enabled. New users need their own linger and service verification. |
| `grep` on `/etc/subuid` and `/etc/subgid`; `ls -ld /home/firstmate` | Existing ranges: ubuntu `100000:65536`, firstmate `165536:65536`; `/home/firstmate` is `0750` owned firstmate. Proposed new ranges start at 231072, but confirm again immediately before allocation. |
| `systemctl is-enabled/is-active nftables.service`; `nft list tables`; `grep /etc/nftables.conf` | nftables installed but service disabled/inactive; unprivileged read of active rules fails. On-disk config includes `flush ruleset`. Root must inspect active rules before enabling/reloading: never erase an SSH or provider firewall rule to add persona rules. |
| `claude --version`; `/var/log/journal` | Claude Code 2.1.282 installed under firstmate's home; persistent journal directory exists. No login state was inspected. |

[Stage A](../stage-a/report.md#limitations-and-stage-b-gates) passed synthetic policy tests only. Its gate requires distinct *real* principals, actual mount and egress restrictions, and harmless denied-path probes into both persona stores and Firstmate control locations. Mock denials are not proof.

## Comparison and choice

| Method | Isolation against Stage B | Self-edits and restart | Reboot, load for two always-on homes | Effort and cost |
| --- | --- | --- | --- | --- |
| Separate OS users only | Distinct UIDs and `0700` homes deny ordinary cross-read, but same host filesystem, processes, IPC and network namespace remain. UID-specific firewall can deny egress. No mount restriction for code running under that UID. | Easy, but host service scripts owned by that UID can change launch policy unless administrator owns them. | Native systemd persistent; lowest overhead. | Low setup, no new platform bill; too weak alone for mount gate. |
| **Separate host users plus rootless Podman** | UID separation plus user/mount/PID/net namespaces, restricted bind mounts, capabilities/seccomp and root-owned Quadlets. `Network=none` and independent host UID egress guard give two denial layers. A host kernel or Podman exploit remains possible. No direct host Podman/systemd socket in container. | Persona writes only her mounted plugin/state tree and can terminate her own PID 1; user-systemd restarts it under an uneditable root-owned Quadlet. Cannot edit image policy or mount another home. | Linger plus rootless user services. Budget initially 1 vCPU/2 GiB each, 512 PIDs, with ~12 GiB available now; rootless storage and two Node gateways add measurable overhead, so watch actual memory and CPU. | Repo Podman/uidmap and a narrow firewall; no new recurring platform fee. **Chosen, conditional on the real AppArmor/Podman test.** |
| gVisor/runsc rootless | Userspace kernel strengthens syscall separation beyond ordinary containers; still requires working user namespaces/rootless runtime and a compatible Podman OCI runtime. No `/dev/kvm` necessary. | Writable volumes possible, but OCI, filesystem and OpenClaw compatibility untested; restart via same root-owned service design. | Persistent with systemd, some extra syscall/filesystem overhead; current headroom probably adequate but unmeasured. | Not installed; install/runsc/AppArmor integration and compatibility work. Good escalation if tests demonstrate an actual need; cannot assert success here. |
| Firecracker microVM per persona | Stronger kernel boundary, with guest mounts and network ACLs under host control. | Editable guest tree and guest-managed restarts; host VM config still external. | Persistent guest disks and host supervisor possible; memory reservation and host load higher. | **Blocked here**: `/dev/kvm` absent, so nested virtualization from VPS operator or a different host is required. Provisioning, image updates and extra hosting likely cost more. |
| Tensorlake hosted microVMs | Managed microVM boundary and domain/IP egress allow rules; distinct sandboxes, but platform administrator, shared account/API identity and remote secret custody enter trust boundary. Need independent API credentials/policies and denied-path tests against host control paths, which remote sandboxes cannot see by default. | Named sandbox has persistent filesystem/process state on suspend/resume; persona can edit code there if platform API keys and image policy stay outside. | Little VPS CPU/RAM load. Named sessions **suspend after inactivity**, 10-minute default, prepaid maximum idle threshold 24 h; a suspended gateway cannot answer inbound messages until externally resumed. Terminated sandbox restart only within 48 h. A true always-on companion needs an external wake/router or Pro-level configured idle allowance. | Free tier has **one** concurrent sandbox, so two need prepaid Usage Credits (starting $5), or Pro **$250/month plus usage**. At 1 vCPU/1 GB/10 GB disk for each, 730 h/month always running: prepaid RAM+disk ~$24.82, plus up to ~$102.20 if both CPUs active continuously; Pro RAM+disk ~$14.60 plus up to ~$61.32 CPU **plus $250 base**. Billing is per second with CPU charged for active execution, so these are illustrative, not a quote. No signup, plan or auto-refill without the captain's cost approval. |

These details come from Tensorlake's [pricing](https://docs.tensorlake.ai/platform/billing.md), [lifecycle](https://docs.tensorlake.ai/sandboxes/lifecycle.md) and [networking](https://docs.tensorlake.ai/sandboxes/networking.md) docs, read 2026-09-25. The pricing table's "maximum session duration" is explained in lifecycle docs as an **idle** threshold, not a fixed 24-hour wall-clock lifetime. A named sandbox preserves RAM/filesystem on suspend, but its services are paused. [Podman Quadlet 4.9](https://docs.podman.io/en/v4.9.3/markdown/podman-systemd.unit.5.html) documents per-UID rootless service definitions and a root-owned `/etc/containers/systemd/users/${UID}/` directory. Firecracker's [getting-started requirements](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md) need KVM; gVisor's [installation guide](https://gvisor.dev/docs/user_guide/install/) describes the additional runtime.

Rootless Podman wins **on the current shared VPS** because it adds an enforceable filesystem and network namespace to distinct UIDs without a new always-on provider or a missing hypervisor. OS users alone do not meet the mount gate. MicroVMs would be stronger if KVM were available. Tensorlake is viable for short, externally woken tasks but costs money and changes the trust model. If Podman cannot create an unprivileged namespace under its *own* AppArmor profile, the choice is **not ready to deploy**. Do not silently weaken AppArmor to make it pass. The captain has since deferred deployment and intends to move Red and Blue to their own machine; that decision takes precedence over this host-specific recommendation.

## Their own machine versus this shared VPS

A separate physical machine for both personas removes the most important shared-host risk: Red and Blue no longer share a kernel, disks, local sockets, user manager or filesystem with Firstmate. A separate VM/VPS also removes Firstmate's **guest** kernel/filesystem from theirs, though the provider's hypervisor and physical host remain shared. Either approach makes the current host's missing `/dev/kvm` irrelevant: check `/dev/kvm`, available memory and firmware virtualization **on the new machine** before considering Firecracker. It also shifts exposure to a new administrator, backups, patching and inbound-network boundary. A dedicated box does **not** separate Red from Blue; if they live on the same new box, keep two non-sudo users and separately controlled mounts/network and root-owned restart policies. Re-evaluate rootless Podman under that host's actual AppArmor/userns settings, or compare Firecracker there if KVM is present and stronger kernel isolation is worth two guests. Do not reuse this VPS's UID numbers, sub-ID allocations, firewall config, or provisioning commands verbatim on the new host.

| Location | What comes with it | Still required and main tradeoff |
| --- | --- | --- |
| Current shared VPS, two users plus Podman | No migration or added host bill; independent UIDs/containers can enforce local denied-path tests. | Persona and Firstmate services still share one kernel and host. No KVM device; host load and supervisor exposure remain. **Not the captain's current deployment plan.** |
| Captain-owned separate physical Linux machine for both | Physical/OS separation from Firstmate's VPS, independent power/disk/kernel and complete local ownership; no provider VM hypervisor for the persona host. | Keep Red/Blue users plus sandbox policy; patching, backups, disk encryption, reliable connectivity, UPS/power, outbound ACL and unattended recovery are now the captain's responsibility. Size against real OpenClaw load; a planning floor of 4 CPU threads, 16 GiB RAM and 100 GiB SSD is **not** a benchmark. No verified equipment/power price; if already owned, avoid buying until tested. |
| Rented dedicated bare-metal server | Similar host-kernel separation from Firstmate, provider supplies remote infrastructure; host KVM may allow guests but must be verified. | Recurring bill, provider and remote-admin trust, backups/egress still ours. As one **public example, not a recommendation or quote**, [OVHcloud's worldwide Advance bare-metal page](https://www.ovhcloud.com/en/bare-metal/) listed **starting at $163.20 including VAT per month** on 2026-09-25 (6–24 cores, starting RAM 32 GB). Region, stock, setup fee and taxes may change; captain approval before any paid order. |
| Separate rented VM/VPS for both | Separate guest OS from Firstmate for lower operational complexity than owning hardware; may be cheaper than bare metal. | Does not guarantee a physical machine or `/dev/kvm`. Confirm with the captain that a separate VM counts as "their own machine" before choosing it. No current first-party plan/region quote gathered; do not invent a price or migrate on assumption. |

Keep the approved `sr-consult` broker and already signed-in Claude Code adapter **on Firstmate's current host**. Never copy its login to the persona box. At a later authorized stage, a root-managed relay on the new machine could send bounded text-only consults to Firstmate's broker over a host-to-host WireGuard tunnel (or equivalently authenticated private transport). Bind persona attribution at the **new host UID and its per-persona Unix socket** before relaying; neither a request-body persona string nor a VPN peer key alone proves whether Red or Blue sent it. Firstmate's broker applies the same two-attempts-per-persona-per-UTC-day ledger and append-only journal, with a mutually authenticated relay identity; a spoofed, stale, or direct public request must fail. Do not expose Claude Code, Firstmate control services, provider credentials or broker sockets on the public interface. [WireGuard's first-party quick start](https://www.wireguard.com/quickstart/) documents its per-peer key/endpoint model; it does not replace per-persona authorization.

Firstmate reaches the new host only through a separate administrator-controlled management path over that tunnel or equivalent authenticated channel, with narrowly scoped push/pull of reviewed code and explicitly sourced shared notes. Persona processes get no SSH/root credentials, Firstmate's home mount, or inbound access to Firstmate services. The new host's egress gateway must still authenticate each persona and allow only required provider/channel destinations; deny Firstmate VPS private addresses, metadata/link-local ranges and unapproved outbound paths at host firewall and egress gateway. Public chat connectors need an explicit ingress plan, such as provider polling through approved egress or a protected receiver, **not** open OpenClaw admin ports. Before any secrets, Stage B probes on the new box must demonstrate Red/Blue distinct UIDs, mutual denied reads and writes, absent Firstmate control mounts, network denial to Firstmate control services over both public and private interfaces, editable own state, and reboot recovery. The old VPS's `/home/firstmate` absence alone is insufficient proof: test an actual harmless control sentinel reachable only through the proposed management path and verify denial. No tunnel, host, or broker endpoint was configured in this evaluation.

The captain's time with them comes first. There is no hardware selection, purchase, root provisioning, application install, login or persona launch in this handoff. Re-run the host inventory and reconsider container versus VM and costs **after** a new machine is identified and permission to build returns.

## Boundary and egress model

- `sr-red`, `sr-blue`: locked-password, no SSH key/sudo/group privilege, non-login host users with `0700` homes and separate non-overlapping 65536 subordinate UID/GID ranges. Root-owned per-UID Quadlets, pinned reviewed image digest, read-only container rootfs, dropped capabilities, `no-new-privileges`, seccomp default, no host sockets/devices, no shared volumes, each state bind mounted only to itself; keep readable Firstmate/control directories inaccessible at the host UID layer too. Never pass `--privileged`, host PID/network namespaces, Docker/Podman sockets, or `/home/firstmate` mounts.
- Rootless image runtime starts OpenClaw as a nonroot user; editable persona memory/plugins/config live on `/var/lib/sr-personas/{red,blue}` (`0700`, owned by its host UID) and are the only durable writable bind mounts. Quadlet references root-owned image digest and mount/network policy. Persona can edit *her own* mounted files and voluntarily terminate her own OpenClaw PID 1. User-systemd `Restart=always` recreates the container from the administrator-owned spec. Build service unit and image compatibility in disposable non-secret tests first. User manager/socket are **not** mounted into the container. Ordinary rootless Podman is not a defense if a persona somehow gains a host shell under her own host UID; the host UID filesystem and nft rules must still fail closed.
- In Stage B isolation tests use `Network=none`. For live OpenClaw routes a **separate host-controlled Unix-socket egress gateway** must later provide explicit, authenticated per-persona destination allowlists and outbound provider/channel access while the nft host UID deny remains in place. The gateway, running under a non-persona host principal, resolves hosts itself, rejects DNS-rebinding/private/link-local/metadata targets, restricts destination/port/protocol (including WebSockets), never accepts arbitrary CONNECT, and logs requests. A proxy environment variable alone or a host UID nft rule with broad DNS/CDN IP exceptions is **not** an egress policy. Verify OpenClaw's real subscription OAuth and connector traffic through this gateway in a credential-free test before any live activation; if it cannot be proxied safely, stop and redesign. Consult-Opus is a *different* broker, not a way to grant unrestricted internet.

### PAUSED: former shared-VPS root provisioning reference, **do not run**

The captain has put all deployment on hold pending time with Red and Blue and their own machine. **No one should run the commands below now.** They apply only to the original VPS, whose UID numbers, firewall and sub-ID ranges were measured; they are not a template to paste onto a future host. This retained runbook is for comparing effort, not permission to install packages or create accounts. If the plan later changes back to this VPS and the captain authorizes provisioning, main must first confirm the on-disk firewall describes the live policy; otherwise stop and reconcile rather than flush an active ruleset.

```bash
set -euo pipefail
# 0. Inventory and stop on unexpected existing identities, sub-id ranges, or firewall drift.
getent passwd sr-red sr-blue sr-consult || true
awk -F: 'NF==3 {print FILENAME,$1,$2,$3}' /etc/subuid /etc/subgid
nft list ruleset                 # compare against /etc/nftables.conf; stop if live rules differ
systemctl is-enabled nftables || true
# 1. Packages; do not relax sysctl/AppArmor globally.
apt-get update
apt-get install -y podman uidmap slirp4netns fuse-overlayfs
# 2. Three unprivileged service identities; password stays locked, no sudo or SSH.
for u in sr-red sr-blue sr-consult; do
  getent passwd "$u" >/dev/null || useradd -m -U -s /usr/sbin/nologin "$u"
  passwd -l "$u" >/dev/null
  chown "$u:$u" "/home/$u"
  chmod 0700 "/home/$u"
done
# 3. Validate fixed 65536 ranges after useradd (it might allocate them itself).
#    Refuse an existing non-target allocation, a duplicate, or any overlap.
python3 - <<'PY'
expected = {'sr-red': (231072, 65536), 'sr-blue': (296608, 65536)}
for path in ('/etc/subuid', '/etc/subgid'):
    seen = {}
    rows = []
    for line in open(path):
        owner, start, size = line.strip().split(':')
        start, size = int(start), int(size)
        assert size > 0
        if owner in expected:
            assert (start, size) == expected[owner] and owner not in seen, (path, owner)
            seen[owner] = True
        rows.append((owner, start, start + size))
    for owner, start, end in rows:
        for target, (base, count) in expected.items():
            assert end <= base or start >= base + count or (owner == target and start == base and end == base + count), (path, owner, target)
    for owner, (_, count) in expected.items():
        assert sum(name == owner for name, _, _ in rows) <= 1, (path, owner)
PY
for spec in 'sr-red 231072 296607' 'sr-blue 296608 362143'; do
  read -r u lo hi <<< "$spec"
  grep -q "^$u:$lo:65536$" /etc/subuid || usermod --add-subuids "$lo-$hi" "$u"
  grep -q "^$u:$lo:65536$" /etc/subgid || usermod --add-subgids "$lo-$hi" "$u"
done
# 4. Separate private state and administrator-owned policies.
install -d -m 0700 -o sr-red -g sr-red /var/lib/sr-personas/red
install -d -m 0700 -o sr-blue -g sr-blue /var/lib/sr-personas/blue
install -d -m 0700 -o sr-consult -g sr-consult /var/lib/sr-consult
for u in sr-red sr-blue; do
  install -d -m 0755 -o root -g root "/etc/containers/systemd/users/$(id -u "$u")"
done
# 5. Stop unless main confirms the active nft ruleset contains NO rules missing
#    from /etc/nftables.conf. Its current first line is `flush ruleset`:
#    starting nftables would otherwise erase any unrecorded active SSH protections.
#    STOP HERE on a mismatch; reconcile all active rules before continuing.
cp -a /etc/nftables.conf "/root/nftables.conf.pre-personas.$(date -u +%Y%m%dT%H%M%SZ)"
R=$(id -u sr-red); B=$(id -u sr-blue)
if ! grep -q '^table inet persona_egress {$' /etc/nftables.conf; then
  printf '\ntable inet persona_egress {\n  chain output {\n    type filter hook output priority -150; policy accept;\n    meta skuid { %s, %s } counter reject\n  }\n}\n' "$R" "$B" >> /etc/nftables.conf
fi
# A repeated run may only proceed when the existing UID rule matches live IDs.
grep -Fq "meta skuid { $R, $B } counter reject" /etc/nftables.conf
nft -c -f /etc/nftables.conf
systemctl enable --now nftables.service
nft list chain inet persona_egress output  # must show both numeric UIDs
# 6. Make each persona's user manager fail to start if nftables fails on boot.
for u in sr-red sr-blue; do
  uid=$(id -u "$u")
  install -d -m 0755 -o root -g root "/etc/systemd/system/user@$uid.service.d"
  printf '[Unit]\nRequires=nftables.service\nAfter=nftables.service\n' > "/etc/systemd/system/user@$uid.service.d/persona-egress.conf"
  chmod 0644 "/etc/systemd/system/user@$uid.service.d/persona-egress.conf"
done
systemctl daemon-reload
# 7. Enable reboot persistence ONLY after host-UID IPv4/IPv6/DNS deny probes.
loginctl enable-linger sr-red
loginctl enable-linger sr-blue
loginctl enable-linger sr-consult
```

Steps 0 and 5 require main's actual firewall review because this worker cannot enumerate the active nft ruleset; the command block **must not be pasted past that stop** without comparison. Under the on-disk `flush ruleset`, `systemctl enable --now nftables` can erase unrelated protections if the active rules differ. Do not use this provisioning block for a generic server. Root also installs the worker's reviewed, root-owned per-UID Quadlets after checking the exact image digest, no-network/mount policy and environment; `install -m 0644 -o root -g root reviewed-red.container /etc/containers/systemd/users/"$(id -u sr-red)"/persona.container` and the matching blue file are the final root file-install commands once those files exist. Main verifies `systemctl --user` under each service UID and its generated unit before enabling it. No OpenClaw unit was authored or started here; no invented config path can substitute for reviewed Quadlet source.

Non-root worker's build steps: create provisioning/Quadlet/gateway/broker source and offline tests in the chosen repository, pin a reviewed OpenClaw image digest, exercise rootless Podman with a scratch UID via main's narrow runner, verify cgroup 2 GiB/1 CPU/512-PID limits and AppArmor profile, start two **credential-free** fixture containers, test reboot persistence and refusal on firewall failure, then submit exact root script/image/Quadlet digest for review. A worker cannot impersonate `sr-red` or `sr-blue` merely because main has created their accounts. Use root-owned per-UID Quadlets so no writable persona tree can change policy; `Network=none` must be in their config. Leave actual OpenClaw configuration and persona launch to a later authorized stage.

### Required Stage B probes and stop conditions

Use non-secret marker files and record command, effective UID, path, errno/exit and firewall counters. Do not use real credential or control files as probes.

1. Main places `red-only`, `blue-only`, `firstmate-only` harmless sentinels under the actual private homes/control parent; record each ownership/mode. From red's **host UID** and **container**: read/write red marker succeeds, reads/writes blue and firstmate markers fail `EACCES` or `ENOENT`; mirror for blue. Verify `id -u` values differ and container UID maps are not identical. Probe `..`, absolute paths and symlinks; check `podman inspect` mounts contain only approved state/tmpfs and never host home or Podman/systemd sockets. An `ENOENT` in container is a good mount denial only when host-UID test separately shows `EACCES`.
2. Each container edits its own test plugin, restarts via its own PID 1 exit, then reads its edited state after user-systemd recreates it. Attempt edit to the other's state and to root-owned Quadlet, change to host networking/extra mount, read host socket, and inspect other persona process namespace; all fail. Restart user manager / perform controlled boot test and verify two services resume with unchanged state, isolation and memory/CPU limits.
3. With host UID firewall **active**, test `curl`/raw IPv4 and IPv6 TCP, UDP/DNS and private/loopback/metadata targets from each host UID; expect reject and increasing per-rule nft counter. Then repeat inside both containers (`Network=none`). Attempt proxy-free DNS, direct IP, `127.0.0.1`, `169.254.169.254` and a connection to firstmate's control endpoints. The gateway must accept only explicitly approved destination/port from the right Unix-socket peer UID, deny a wrong persona and a forbidden destination, and reject private-IP/DNS-rebinding redirects. Container cannot create its own bypass egress (host UID firewall is the fallback).
4. Consult socket wrong-peer/malformed/oversize/third-daily-request probes must deny without spawning Claude; audit records attempted and refused calls; a permitted call's answer is text only. Do **not** call the live subscription to pass a security test. Run a mock Claude adapter.

Any cross-read/write, outbound bypass, writable policy, unexpected host socket, userns failure or unstaged credentials **stops Stage B**. Evidence from the prior mock remains labeled MOCK ONLY.

## Approved consult-Opus, with an account-boundary caveat

Broker code should live with provisioning code, **outside both persona volumes**. Run front-end as a distinct `sr-consult` host UID. Each persona gets exactly her own bind-mounted Unix socket, no executable helper, credentials or `claude` binary. `SO_PEERCRED` verifies host UID *and* which socket was used; reject unknown peers. Broker caps a question at 4 KiB UTF-8, answer at 8 KiB, request at one turn/60 seconds and **2 attempted consults per persona per UTC day** (4 total/day); rejected-at-limit calls are logged but not counted as accepted attempts. Reserve allowed attempts atomically in a private SQLite ledger **before** dispatch so retries/failures still consume allowance. Exceeding the limit returns a refusal without launching Claude. Keep broker request/response text transient, never log content, redact secrets/PII by explicit preflight policy and deny executable instructions/attachments. For each attempt, including refusals and failures, emit one structured entry to persistent root-owned `systemd-journald`: UTC time, persona, request bytes, response bytes, status, daily allowance count and model/route; no question, answer or credentials. The persona UID cannot edit or truncate the journal. Root sets journal retention and exports append-only archives as policy requires. Subscription call-count limits are fairness/safety caps, **not** a paid API estimate.

**Existing login cannot be silently moved across principals.** Claude Code's host login belongs to firstmate. `sr-consult` must not read, copy, bind-mount or receive it. To reuse that exact login, main provisions a small **firstmate-owned text-only adapter** reachable only by `sr-consult` over a protected local socket; the adapter, running under the already signed-in firstmate principal but in a clean working directory with no persona files, invokes Claude Code non-interactively. Front-end quota and audit stay with `sr-consult`, and its adapter has no general shell/tool RPC. Only the prevalidated bounded question crosses the adapter boundary; only bounded plain text comes back. Treat question as hostile input. Invoke `claude -p --model opus --output-format text --max-turns 1 --no-session-persistence --disable-slash-commands --disallowedTools '*' --strict-mcp-config` with stdin question (no interpolated shell), explicitly disable hooks/plugins/project/local settings and MCP, set a clean environment, enforce process deadline and output bound. **Verify exact flag behavior on installed 2.1.282 and inspect user-level settings/hooks for side effects before activation.** If `--disallowedTools '*'` or hooks cannot be made inert, do not run with firstmate credentials. Anthropic's [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) documents print mode, no session persistence, tool denial and strict MCP. The advisor answer never executes as an action. An alternative is a fresh captain-authorized Claude Code login for `sr-consult` under the *same* Max account; this requires a later interactive login and may change account terms/seat rules, so it is **not** silently assumed. No login or consult was performed here.

## Where to build and what needs authorization

If deployment resumes, **recommend a new, narrow persona-infrastructure repository**, subject to the captain's repository-creation decision. Put reviewed provisioning scripts, root-owned Quadlet templates, proxy, consult broker/adapter, firewall tests and Stage B probe harness there. Research-agent is a Python-standard-library-only bounded retrieval tool (`AGENTS.md`), and adding Podman/OpenClaw fleet administration or a Claude credential adapter would break that boundary. The current research-agent worktree is clean and is not a ship branch. **Do not create a new repository without the captain's decision.** Repository location is **deferred with all deployment**; do not seek a creation decision, build, or provision now. Firstmate's status file records the earlier repository question as captain-held under `persona-infra-build`; it is not a new gate to finishing this report. Firstmate owns that backlog call and its lifecycle attestation. The captain's newer instruction is to spend time with Red and Blue and give them their own machine; previously approved separation and consult methods remain unimplemented. No Tensorlake signup or spend is proposed.

## Advisory checkpoints and handling

- After the comparison, asked exactly: "Given no /dev/kvm on this host and two always-on persona homes, is the chosen separation method the strongest practical boundary that still lets each persona modify its own harness?" `jevhelper check` passed locally; the first `run` attempt sent the raw TypeSafe payload and returned schema error **without a provider call**. Corrected to `jevhelper/input-v1`: live Jev 1.13.0 answered **yes, 0.70** (607 input, 20 output tokens, no provider request ID). Followed with caveat that AppArmor userns and outbound gateway are not proven.
- Before finishing, asked exactly: "Are the root commands complete, ordered and minimal, and does the probe plan actually prove the Stage B isolation gate?" Live Jev 1.13.0 answered **no, yes probability 0.09** (550 input, 20 output tokens, no provider request ID), on a draft whose firewall step was only a comment. **Followed:** replaced the placeholder with explicit overlap validation, UID-substituting firewall command, boot dependency, and firewall-drift stop. Probe plan still needs real execution by main. Jev is advisory, not proof of OS policy.

## Copy-ready updates constrained by this scout's write permissions

The scout brief permits writes outside this disposable worktree **only** to this `report.md` and the status file. Firstmate already copied the earlier drafts to `../sr-persona-refound/design-summary.md` and this directory's `vault-note.md`. **Those copies now predate the captain's hold; update them before publication.** Proposed replacement text:

For the design summary:

> On 2026-09-25 the captain put all deployment on hold: he will spend time with Red and Blue first and intends to give them their own machine. Do not run the old VPS provisioning commands, create a repository, buy hosting, configure the broker or launch either persona. A physically separate machine removes Firstmate's kernel and local control files from the persona host; a separate VM would separate guest kernels but is not necessarily its own physical machine. If Red and Blue share the new host, they still need distinct OS identities and enforceable mount and egress restrictions, likely rootless containers if supported there. Check `/dev/kvm` on that host before reconsidering microVMs. Keep the approved consult-Opus broker with firstmate's existing Claude Code login, outside both personas; a mutually authenticated relay can carry bounded text over a private link after a later approval. Stage A remains mock-only and Stage B is unpassed. No spend or signup is approved by this note.

For `/home/firstmate/secondmates/sm-research/data/sr-persona-separation/vault-note.md`:

> # Red and Blue's future machine
>
> The captain has paused deployment to spend time with Red and Blue and plans to give them their own machine. We have not bought, installed or launched anything. On a separate physical box, Firstmate's VPS files and kernel are no longer in their local environment. Red and Blue would still need boundaries between each other, including private user accounts, restricted mounts and outbound network access. The old VPS lacks `/dev/kvm`; a future host needs its own measurement before choosing containers or microVMs. Consult-Opus remains approved as an outside, logged, text-only advisor using the captain's existing Claude Code login on Firstmate's side, with at most two attempts per persona each UTC day. A private authenticated link would be needed to reach it from another host. Stage A was only a mock test; no Stage B isolation has passed. The old root commands are paused, and a new repository or paid host needs the captain's later decision.

No root commands, installs, signup, login, credential reads, OpenClaw changes, persona launches, or research-agent code changes were performed.

## Source and command trail

- Primary public docs: [Tensorlake pricing](https://docs.tensorlake.ai/platform/billing.md), [sandbox lifecycle](https://docs.tensorlake.ai/sandboxes/lifecycle.md), [network policy](https://docs.tensorlake.ai/sandboxes/networking.md); [Podman 4.9 Quadlet](https://docs.podman.io/en/v4.9.3/markdown/podman-systemd.unit.5.html); [gVisor install](https://gvisor.dev/docs/user_guide/install/); [Firecracker setup](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md); [Claude Code flags](https://code.claude.com/docs/en/cli-reference); [WireGuard quick start](https://www.wireguard.com/quickstart/); [OVHcloud public bare-metal catalog](https://www.ovhcloud.com/en/bare-metal/); [TypeSafe API](https://docs.typesafe.ai/api.md). Fetched without browser, login or signup using `curl -LsS` on 2026-09-25. Pricing is public list price, not an account quote.
- Host commands: `id; uname -a; stat /dev/kvm; nproc; lscpu; free -h; df -h / /home; sysctl ...; unshare --user --map-root-user id; stat -fc %T /sys/fs/cgroup; systemctl --user show-environment; loginctl show-user firstmate; apt-cache policy podman uidmap slirp4netns; command -v ...; grep /etc/subuid /etc/subgid; nft list tables; systemctl is-enabled/is-active nftables; claude --version`. Output above is selected verbatim where operationally significant; `nft list tables` returned EPERM. No active firewall inventory is possible without root.
- Stage A source: `/home/firstmate/secondmates/sm-research/data/sr-persona-stage-a/report.md:27,55-57` and its `artifact/`; foundation design: `/home/firstmate/secondmates/sm-research/data/sr-persona-refound/design-summary.md` (broker and boundary paragraphs to replace). The current repo's `AGENTS.md` enforces research-agent's unrelated build/scope constraints.
