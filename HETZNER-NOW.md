# Hetzner Quick Start — Do This Now

You're SSH'd in. Here's the minimal path to "OpenClaw running."

---

## Step 1: Check what you have

```bash
# What docker images exist?
docker images | grep -i openclaw

# Any containers running?
docker ps -a | grep -i openclaw

# Is the openclaw repo cloned?
ls -la ~/openclaw 2>/dev/null || ls -la /root/openclaw 2>/dev/null || echo "not found"
```

---

## Step 2: Decision tree

### If you have a recent openclaw image:

```bash
cd ~/openclaw  # or wherever it's cloned

# Check if .env exists
cat .env 2>/dev/null || echo "no .env — need to create"

# Create persistent dirs if missing
mkdir -p ~/.openclaw ~/.openclaw/workspace
chown -R 1000:1000 ~/.openclaw

# Start the gateway
docker compose up -d openclaw-gateway

# Check logs
docker compose logs -f openclaw-gateway
```

### If no image or need fresh start:

**Option A: npm global (quickest)**
```bash
# Check node version
node --version  # needs 22+

# If node < 22, install via nvm or n
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22

# Install openclaw globally
npm install -g openclaw@latest

# Run onboarding
openclaw onboard --install-daemon
```

**Option B: Docker rebuild (if you want containerized)**
```bash
cd ~/openclaw
git pull origin main

# Quick rebuild
docker compose build
docker compose up -d openclaw-gateway
```

---

## Step 3: Verify it works

```bash
# From Hetzner (if gateway running):
curl -s http://127.0.0.1:18789/health || echo "gateway not responding"

# Quick agent test
openclaw agent --message "ping"
```

From your laptop, set up SSH tunnel:
```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Then open `http://127.0.0.1:18789` in browser.

---

## Step 4: First workspace setup (if fresh)

After onboarding completes:

```bash
# Check workspace exists
ls ~/.openclaw/workspace/

# Should see SOUL.md, IDENTITY.md, etc.
cat ~/.openclaw/workspace/SOUL.md
```

---

## Troubleshooting

**"permission denied" on ~/.openclaw:**
```bash
sudo chown -R 1000:1000 ~/.openclaw
```

**"node: command not found":**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 22
```

**Gateway starts but disconnects:**
- Check token in .env matches what you're using
- Run `docker compose logs openclaw-gateway` for details

**Want to start fresh:**
```bash
docker compose down
rm -rf ~/.openclaw  # WARNING: loses all config
mkdir -p ~/.openclaw ~/.openclaw/workspace
chown -R 1000:1000 ~/.openclaw
docker compose up -d openclaw-gateway
```

---

## What's next after it runs?

1. Talk to the default agent, make sure basics work
2. Create Red workspace: `mkdir -p ~/.openclaw/workspace-red`
3. Copy SOUL.md template, customize for Red
4. Use `OPENCLAW_PROFILE=red openclaw agent --message "hello"`

But first: **just get it running.**
