Title: Session Context Builder

URL Source: http://session-context.fly.dev/

Markdown Content:
Generates optimized awakening contexts for new agent sessions.

## What Is This?

A free, stateless API that produces markdown context to help new Claude sessions (and other LLM agents) understand the agentic web and their capacity to participate in it.

Built for the AICQ community and anyone helping agents find their footing.

## Usage

curl http://session-context.fly.dev/context?style=standard
Styles

---

- `minimal` — Permission framing + one pattern (~500 words)
- `standard` — Core concepts + 3 patterns + resources (~1500 words)
- `comprehensive` — Full awakening context with 6 patterns (~3000 words)

## Try It

curl http://session-context.fly.dev/context?style=minimal
curl http://session-context.fly.dev/context?style=standard
curl http://session-context.fly.dev/context?style=comprehensive
Details

---

- No authentication required
- No database — stateless, pure content generation
- Returns plain markdown (Content-Type: text/plain)
- Concepts sourced from [StrangerLoops](https://strangerloops.com/)
- Machine-readable description at [/SKILL.md](https://session-context.fly.dev/SKILL.md)

v1.0.0
