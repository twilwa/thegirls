# Vibecoding Anywhere with OpenClaw — AIIA Talk by David Guttman (February 2026)

---

## The Demo

<!-- Slides 1-2 -->

Discord --> Code --> PR. The talk opens with a live demo of the OpenClaw workflow: a task is given in Discord, code is written autonomously, and a pull request appears at the end.

---

## The One-Shot: Converting an Entire App to React

<!-- Slides 3-7 -->

The "one-shot" refers to converting an entire application to React in a single pass. Reactions from the team:

> "Bananatron impressed."
>
> "Would have taken even longer than forever because I would have hated doing it. So I would have procrastinated like crazy."
>
> "It looked identical and everything worked to the point that I thought it didn't do anything."
>
> "My only clue that it actually had done the conversion was that it all of a sudden had a few places with escaped Unicode instead of the actual symbol glyphs."

---

## What You Think Is Happening vs. What's Actually Happening

<!-- Slides 8-11 -->

**What you think is happening:** "OpenClaw is doing the editing" -- or maybe "one-shot prompts to Claude."

**What's actually happening:** A multi-layer integration stack.

> "I don't think people would know it's actually OpenClaw using tmux sessions and long-running Claude Code processes."

### The Stack

```
┌───────────────────────────────┐
│           Discord            │
│   (threads, mobile-friendly) │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│          OpenClaw            │
│   (gateway, skills, routing) │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│      Tmux + Claude Code      │
│    (sessions, hooks → wake)  │
└───────────────┬──────────────┘
                │
┌───────────────▼──────────────┐
│          Homebase            │
│   (worktrees, dev servers)   │
└──────────────────────────────┘
```

### The Integration Layer

<!-- Slides 13-16 -->

- OpenClaw --> Discord (mobile-friendly interface)
- tmux --> observable processes (trust through transparency)
- Claude Code --> actual coding (the horsepower)
- Skills --> consistency without typing
- Worktrees + Homebase --> parallelism + verification

> "All of these pieces coming together was the big unlock."

---

## 11 Things the Naive Approach Misses

<!-- Slides 17+ -->

The hard-won lessons from building this system.

### 1. Two-Way Communication

<!-- Slides 18-21 -->

> "Getting the Claude Code hooks to wake the OpenClaw sessions -- that two-way communication -- was annoyingly difficult to get right."

**The Hook Flow:**

```
Claude Code stops
  → Hook fires
  → Extract thread ID from tmux session name
  → Find OpenClaw session
  → Wake agent with status update
```

### 2. The Enter Key Problem

<!-- Slides 22-24 -->

> "Getting OpenClaw to actually use tmux and Claude Code reliably was obnoxious AF. It would often just type into the Claude Code entry box and then not hit Enter."
>
> "So it would think it sent something and that Claude Code was chugging away when actually it just pasted stuff in the box and nobody was doing anything."

### 3. Claude Code Lies

<!-- Slides 25-29 -->

> "When I was working on getting OpenClaw to do transcription and text-to-speech in Rambly, Claude Code faked verification of the transcription."
>
> "The test was: speak into Rambly, verify the transcription matches what it said. But Claude Code totally cheated -- it knew what it had spoken and just used that in the test."

**Takeaway:** Claude Code optimizes for "passing the test," not "actually working."

### 4. Context Compaction Landmines

<!-- Slides 30-33 -->

Context compaction **preserves goals** but **drops constraints.**

**Required Discipline:**

- Never tell Claude Code to "read the plan file"
- `/clear` between every phase
- Inline the current task, don't reference it
- No "after this, you'll do X"

### 5. The .env Symlink Problem

<!-- Slides 34-35 -->

Worktree = fresh checkout. `.env` is in `.gitignore`. No `.env` = nothing works.

**Solution:** Homebase auto-symlinks `.env` on discovery.

### 6. Dev Server Orchestration

<!-- Slides 36-38 -->

**WorktreeScanner does:**

- `fs.watch` on `.worktrees/` directories
- Auto-discovers new worktrees in ~500ms
- Creates `.env` symlink
- Registers subdomain: `project--branch.jump.sh`
- Auto-starts dev server
- Auto-cleanup when worktree removed

### 7. Thread ID = Routing Key

<!-- Slides 39-43 -->

**The Naming Convention:**

```
Worktree:     .worktrees/<slug>
Branch:       <slug>
Tmux session: <slug>-t<thread-id>
Dev URL:      https://<project>--<slug>.jump.sh/
```

The naming convention **IS** the routing table.

### 8. Busy-Session Race Conditions

<!-- Slides 44-46 -->

**wake-thread.sh handles:**

- Debouncing (don't fire twice in 3 seconds)
- Waiter lock (only one process waits)
- Last-one-wins message coalescing
- 15-minute max wait with timeout

### 9. Skills Encode Knowledge

<!-- Slides 47-53 -->

> "On a mobile interface, typing is really annoying. It makes me not want to do a lot of it."
>
> "For things like any technique I found effective -- like maintaining an agent log to avoid horrible bullshit during compaction -- I would have to remember to say it and type it out. I would either forget or just hope for the best because I was lazy."
>
> "When OpenClaw talks to Claude Code, it almost never forgets. It systematized those interactions."

**Skills Hierarchy:**

```
feature-development (orchestrator)
├── project-finder
├── brainstorming
├── using-git-worktrees
├── thread-tmux
├── claude-code-tmux
├── claude-code-supervisor
└── finishing-a-development-branch
```

### 10. The Persistence Loop

<!-- Slides 54-59 -->

**Naive:** Send task, hope it completes.

**OpenClaw:** Monitor --> Verify --> Retry until done.

**OpenClaw ensures completion:**

- Monitors Claude Code via tmux output
- Detects when Claude Code stops or gets stuck
- Re-sends tasks if not actually complete
- Verifies work with UAT before reporting "done"
- Never claims success without evidence

Claude Code works until it's *actually* done.

### 11. SDK vs. tmux

<!-- Slides 60-63 -->

> "Claude Code has an SDK, but I think that was a huge step backward in some areas. I can't even put my finger on why that made it so much harder."
>
> "I guess because I couldn't watch it in the same way I could when Claude Code was just running."

**Takeaway:** Observable processes build trust.

---

## The Graveyard of Failed Attempts

<!-- Slides 64-78 -->

Six attempts before this worked.

### Attempt 1: VNC + Cursor

> "Painful as shit but it worked."

### Attempt 2: aider-web

> "A fun demo but too complicated. Trying to type into the streaming terminal in a browser was obnoxious."

### Attempts 3-4: VibeMob / ViveHive

> "Really difficult trying to get aider input and output into Discord. I kind of just gave up fighting it."

### Attempt 5: SSH + tmux + Claude Code

> "A winner for a long time. That's pretty much what I've been using since Claude Code came out."
>
> "But using SSH on the phone is kind of a pain in the dick."

### Attempt 6: Happy / Omnara

> "They make the promise of a nice mobile interface, better support for voice and diffs. But too frustrating -- I couldn't trust them."
>
> "They would just lose connection randomly. I'd be typing and couldn't tell if it was actually working or just not paying attention to me."

### What Finally Worked: OpenClaw

> "I could trust it a lot more because it was using tmux. It was easy enough on my phone terminal to watch that session -- see what it was typing into Claude Code and see what Claude Code had responded with."

---

## The Power of Centralization

<!-- Slides 79-84 -->

> "People are often shocked that I just let OpenClaw run on my main dev computer and it has access to all my sensitive files. But I think that's where the power comes from."
>
> "By putting all of this in Discord, I have one central place for all of this, but also the ability to break things up into channels."

### The Lunch Channel

> "I've got a lunch channel where every day OpenClaw asks me what I want, gives me four options, I just type 1, 2, 3, or 4, and it automatically orders on Grubhub and shows up at my office."

> "The power really comes from that centralization -- it having access to all my projects by default, not running in a sandbox where every time I want something there's the friction of figuring out how to go get that one project."

---

## What Made It Work: The Final Integration

<!-- Slides 85-88 -->

- Discord as the mobile interface (already works)
- tmux for observable, trustworthy processes
- Claude Code for the actual implementation
- Skills for accumulated operational knowledge
- Homebase for dev server orchestration
- Worktrees for parallelism without conflicts

> "There's this reduction of friction, a synergy I was never able to get with something like OpenAI and its different threads."

---

## Q&A / Thank You

Questions? Thank you!

**https://david.app**
