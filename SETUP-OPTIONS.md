# OpenClaw Setup Options

> Given: Hetzner gateway running, macOS paired, need to do onboarding

---

## The Core Question

**Where does onboarding run?**

Onboarding configures:
- Model/Auth (API keys, OAuth)
- Workspace (where agent files live)
- Gateway settings
- Channels (WhatsApp, Telegram, Discord, Signal)
- Daemon (auto-start service)
- Skills

---

## Option A: Everything on Hetzner (Simplest Start)

**Setup:**
```bash
# SSH into Hetzner, run onboarding in container
docker compose exec -it openclaw-gateway openclaw onboard
```

**Access:** SSH tunnel or Tailscale from macOS

**Pros:**
- Single source of truth
- Girls run where their files are
- No sync needed

**Cons:**
- CLI commands require `docker exec` or SSH
- No local file access from macOS apps
- OAuth flows tricky in headless container (use API keys instead)

**Best for:** Getting started fast, server-first workflow

---

## Option B: Local macOS Client → Remote Hetzner Gateway

**Setup:**
1. Install OpenClaw locally on macOS:
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```

2. Run onboarding in **remote mode**:
   ```bash
   openclaw onboard
   # Choose "Remote (over SSH/Tailnet)" when asked
   # Point to Hetzner gateway (via Tailscale or SSH tunnel)
   ```

3. Gateway stays on Hetzner, macOS is just a client

**Access:** Local CLI commands, local file editing, talks to remote gateway

**Pros:**
- Local CLI convenience
- OAuth flows work (browser on macOS)
- Can edit workspace files locally if you mount/sync them

**Cons:**
- Still need to manage files on Hetzner
- Two-machine complexity
- Onboarding on remote doesn't configure channels (must do via docker exec)

**Best for:** If you want local CLI + OAuth convenience, but gateway runs remotely

---

## Option C: Two Gateways (Local + Remote)

**Setup:**
1. Hetzner: Gateway for Red/Blue (production)
2. macOS: Gateway for you (personal/dev)

**Both connected via Tailscale mesh**

**Pros:**
- Full local development environment
- Girls run isolated on Hetzner
- Can experiment locally without affecting remote

**Cons:**
- Most complex
- Two configs to maintain
- Resource usage on both machines

**Best for:** Long-term, once things are stable

---

## Recommended Path: Option A + Incremental

**Right now (today):**
```bash
# On Hetzner, run interactive onboarding
docker compose exec -it openclaw-gateway openclaw onboard

# When prompted for model auth, choose "Claude subscription (setup-token)"
# This works for Max/Pro plans without per-token API charges
```

**For Max/Pro subscription auth (setup-token flow):**
```bash
# If onboarding doesn't offer it directly, run:
docker compose exec -it openclaw-gateway claude setup-token
```

1. It prints a URL (console.anthropic.com/setup-token)
2. Visit that URL in your Mac browser
3. Log in with your Anthropic account
4. Copy the displayed token
5. Paste it back into the SSH terminal

**No tunneling or Tailscale needed** — `setup-token` is copy/paste, not a localhost callback. Your existing SSH session works.

**What onboarding will do:**
1. Ask for model provider (choose subscription auth for Max plan)
2. Set up workspace (`~/.openclaw/workspace` in container = mounted on host)
3. Configure gateway auth (already done via token)
4. Optionally add channels (can skip for now)
5. Health check

**After onboarding, add Red and Blue:**
```bash
docker compose exec -it openclaw-gateway openclaw agents add red
docker compose exec -it openclaw-gateway openclaw agents add blue
```

This creates:
- `~/.openclaw/workspace-red/` with SOUL.md, IDENTITY.md, etc.
- `~/.openclaw/workspace-blue/` with SOUL.md, IDENTITY.md, etc.
- Isolated sessions per agent

**Later (once stable):**
- Add local macOS OpenClaw if you want
- Set up Tailscale for mesh access
- Consider Radicle for workspace sync

---

## Multi-Agent Config Preview

After adding agents, your config will look like:

```json5
{
  agents: {
    list: [
      {
        id: "red",
        name: "Red",
        workspace: "~/.openclaw/workspace-red",
        agentDir: "~/.openclaw/agents/red/agent",
      },
      {
        id: "blue",
        name: "Blue",
        workspace: "~/.openclaw/workspace-blue",
        agentDir: "~/.openclaw/agents/blue/agent",
      },
    ],
  },
  // Route channels to agents
  bindings: [
    { agentId: "red", match: { channel: "signal", peer: { kind: "dm" } } },
    { agentId: "blue", match: { channel: "discord" } },
  ],
}
```

---

## On Radicle

You mentioned Radicle for "passing back and forth."

**What Radicle does:** Decentralized git hosting. Seed-and-follow model.

**How it could help:**
- Red/Blue workspaces as Radicle repos
- Changes sync without central server
- You could seed from macOS, girls pull from Hetzner
- Or vice versa

**But:** This adds complexity. I'd suggest starting without it, then adding once the basic flow works.

---

## TL;DR

1. **Today:** `docker compose exec -it openclaw-gateway openclaw onboard` on Hetzner
2. Use Anthropic API key (not OAuth) for headless
3. After onboarding: `openclaw agents add red` and `openclaw agents add blue`
4. Edit SOUL.md files in mounted workspace
5. Later: consider local macOS install, Tailscale, Radicle

Want me to walk through the onboarding prompts, or are you good to run it?
