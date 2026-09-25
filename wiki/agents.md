# OpenAI Agents Framework

## Overview

The **OpenAI Agents** framework (package: `openai-agents`, version 0.8.1) is a comprehensive Python SDK for building AI agent applications using OpenAI's latest language models. It provides a structured, type-safe approach to creating autonomous agents capable of reasoning, making decisions, using tools, and collaborating with other agents.

The framework extends the concept of tool-use and function-calling beyond simple LLM interactions by introducing:
- **Agentic orchestration** with multi-turn loops
- **Tool ecosystems** supporting various domains (shell, code interpretation, web search, computer vision)
- **Agent hierarchies** through handoffs between specialized agents
- **Guardrails and safety mechanisms** for input/output validation
- **Memory persistence** across sessions
- **Distributed tracing** for observability

This aligns with modern LLM paradigms where models are positioned as reasoning engines that can delegate to tools and coordinate with other agents to solve complex tasks.

---

## Core Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────┐
│                   Agent Framework                       │
├─────────────────────────────────────────────────────────┤
│  Runner          (Orchestrates agent execution)         │
│    ├─ Agent      (LLM + tools + configuration)          │
│    ├─ Tool       (Function/Shell/Computer/MCP tools)    │
│    ├─ Guardrails (Input/output validation)              │
│    ├─ Handoffs   (Agent-to-agent delegation)            │
│    └─ Memory     (Session persistence)                  │
├─────────────────────────────────────────────────────────┤
│  Supporting Infrastructure:                             │
│    ├─ Models     (OpenAI API, Responses, Chat)          │
│    ├─ Tracing    (Observability and logging)            │
│    ├─ MCP        (Model Context Protocol integration)   │
│    ├─ Voice      (Audio I/O for voice agents)           │
│    ├─ Realtime   (WebSocket-based real-time agents)     │
│    └─ Items      (Type definitions for messages/tools)  │
└─────────────────────────────────────────────────────────┘
```

---

## Key Classes and Functions

### 1. Agent and Runner

**`Agent[TContext]`** - The core agent class
- Represents an autonomous AI agent with a specific purpose
- Generic over context type for state management
- Contains: system prompt, tools, output schema, guardrails, lifecycle hooks
- Supports streaming and batch execution

**`Runner`** - Orchestrates agent execution
- Main entry point for running agents
- Manages multi-turn conversation loops
- Handles tool invocations, guardrails, error recovery
- Returns `RunResult` or `RunResultStreaming` for tracking outcomes

**Related types:**
- `RunConfig` - Configuration for agent execution (max turns, error handlers, session settings)
- `RunState` - Current execution state (history, tool calls, guardrails)
- `RunContext[TContext]` - Runtime context available during execution

### 2. Tools System

**`Tool` (base class)**
- Abstract interface for tools agents can invoke
- All tools implement `name`, `description`, and invocation methods

**Built-in Tool Types:**

| Tool Type | Purpose | Example |
|-----------|---------|---------|
| `FunctionTool` | Wraps Python functions | `@function_tool` decorator |
| `ShellTool` | Execute shell commands | bash, python scripts |
| `CodeInterpreterTool` | Python code execution | Data processing, computation |
| `ComputerTool` | GUI automation via computer vision | Browser control, UI testing |
| `WebSearchTool` | Internet search capability | Research, fact-checking |
| `FileSearchTool` | Document/file search | Knowledge base queries |
| `ImageGenerationTool` | Generate images | DALL-E integration |
| `HostedMCPTool` | Model Context Protocol tools | External tool ecosystems |
| `ApplyPatchTool` | Structured code editing | Diff-based modifications |
| `LocalShellTool` | Advanced shell execution | Complex command chains |

**Tool Definition:**
```python
@function_tool
async def my_tool(search_query: str) -> str:
    """Search for information about a topic."""
    return f"Results for {search_query}"
```

### 3. Guardrails System

**Input Guardrails** - Validate/filter agent input
- Run before or in parallel with agent
- Can intercept and redirect control flow
- Example: reject off-topic requests, detect malicious input

**Output Guardrails** - Validate agent output
- Run after agent produces a result
- Can reject, modify, or accept output
- Example: ensure responses meet quality/policy standards

**Tool Guardrails** - Validate tool invocations
- `ToolInputGuardrail` - Check tool inputs before execution
- `ToolOutputGuardrail` - Check tool outputs before returning to agent
- Example: prevent calling sensitive commands

**Interface:**
```python
@input_guardrail
async def check_input(context, agent_input):
    if is_spam(agent_input):
        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info={"reason": "Spam detected"}
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)
```

### 4. Handoffs

**`Handoff[TContext, TAgent]`** - Delegate work to another agent
- Enables agent hierarchies and specialization
- Example: triage agent → billing/support agent
- Can filter input data passed to next agent
- Maintains conversation history with optional summarization

**Use case:**
```python
billing_handoff = Handoff(
    target=billing_agent,
    input_filter=lambda data: HandoffInputData(...)
)
```

### 5. Memory and Sessions

**`Session` (abstract base)**
- Persists conversation history across runs
- Implementations:
  - `SQLiteSession` - Local file-based storage
  - `OpenAIConversationsSession` - OpenAI API storage
  - `OpenAIResponsesCompactionSession` - Compact OpenAI storage

**`SessionSettings`** - Configuration for persistence

**Features:**
- Automatic conversation tracking
- Optional response compaction for efficiency
- Callback hooks for custom handling

### 6. Models Interface

**`Model` (abstract base)**
- Abstract interface for LLM providers
- Methods: `get_response()`, `stream_response()`

**Implementations:**

| Provider | Model Class | Notes |
|----------|-------------|-------|
| OpenAI (Responses API) | `OpenAIResponsesModel` | Primary, newest API |
| OpenAI (Chat Completions) | `OpenAIChatCompletionsModel` | Legacy, still supported |
| Multi-provider | `MultiProvider` | Route to different providers |

**`ModelSettings`** - Control model behavior
- Temperature, max_tokens, top_p, etc.
- Provider-specific parameters

### 7. Tracing and Observability

**`Trace` and `Span`** - Distributed tracing primitives
- Track execution flow across agent boundaries
- Create custom spans with `@trace` or `@custom_span`

**`TracingProcessor`** - Custom trace handling
- Export to external systems
- Filter or transform trace data

**Span Types:**
- `AgentSpanData` - Agent invocation
- `GenerationSpanData` - LLM calls
- `FunctionSpanData` - Function execution
- `GuardrailSpanData` - Guardrail execution
- `HandoffSpanData` - Agent handoffs
- `SpeechSpanData` - Voice I/O (realtime agents)

**Configuration:**
```python
set_trace_provider(provider)
add_trace_processor(processor)
set_tracing_disabled(False)  # Enable/disable
```

### 8. Items and Message Format

**Run Items** - Structured representation of execution events:
- `MessageOutputItem` - LLM responses
- `ToolCallItem` - Tool invocations
- `ToolCallOutputItem` - Tool results
- `HandoffCallItem` - Agent handoffs
- `ReasoningItem` - Extended thinking (GPT-5 reasoning)

**Response Types:**
- `TResponseInputItem` - Input to model (OpenAI Responses format)
- `TResponseOutputItem` - Output from model
- `ModelResponse` - Complete response with metadata

### 9. Lifecycle Hooks

**`RunHooks[TContext]`** - Global execution events
- `on_llm_start()` - Before LLM call
- `on_llm_end()` - After LLM call
- `on_agent_start()` - Before agent invocation
- `on_agent_end()` - After agent completes
- `on_tool_start()` / `on_tool_end()` - Tool execution
- `on_handoff()` - Agent handoff

**`AgentHooks[TContext]`** - Per-agent lifecycle events

---

## RLM (Recursive Language Models) Paradigm

The OpenAI Agents framework aligns with Recursive Language Model principles:

### 1. **Hierarchical Decomposition**
- Agents can delegate to other agents via `Handoff`
- Creates recursive task decomposition
- Each agent can maintain its own context and specialization

### 2. **Tool-Augmented Reasoning**
- Models access external tools for computation/information
- Tools are not just functions—they're integrated into the agentic loop
- Extended with MCP protocol for distributed tool ecosystems

### 3. **Multi-Turn Agentic Loops**
- `Runner` implements the core agentic loop:
  1. Call LLM with context
  2. Parse response for tool calls or final output
  3. Execute tools and collect results
  4. Feed results back to LLM (recursive)
  5. Repeat until final output

### 4. **Safety and Guardrails**
- Input/output/tool guardrails enforce constraints
- Prevents execution of forbidden actions
- Aligns with model behavior verification

### 5. **Context and Memory**
- Sessions persist conversation history
- Models work with full context for reasoning
- Supports long-horizon problem solving

### 6. **Observability via Tracing**
- Traces capture recursive call stacks
- Enable debugging of complex agentic behaviors
- Support post-hoc analysis of model decisions

---

## Example Usage Patterns

### Basic Agent with Tools

```python
import agents as ag
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="your-key")

@ag.function_tool
async def search(query: str) -> str:
    """Search for information"""
    return f"Results for: {query}"

agent = ag.Agent(
    name="researcher",
    instructions="You are a research assistant",
    tools=[search],
    model=ag.OpenAIProvider().get_model("gpt-4o"),
)

runner = ag.Runner(agent=agent)
result = await runner.run(input="Find information about AI")
print(result.final_output)
```

### Agent Hierarchies with Handoffs

```python
# Specialist agents
billing_agent = ag.Agent(
    name="billing_specialist",
    instructions="Handle billing questions",
    tools=[lookup_invoice, process_refund],
    model=model,
)

support_agent = ag.Agent(
    name="support_specialist",
    instructions="Handle general support",
    tools=[create_ticket, search_kb],
    model=model,
)

# Triage agent with handoffs
triage_agent = ag.Agent(
    name="triage",
    instructions="Route to appropriate specialist",
    handoffs=[
        ag.Handoff(target=billing_agent),
        ag.Handoff(target=support_agent),
    ],
    model=model,
)

runner = ag.Runner(agent=triage_agent)
result = await runner.run(input="I have a billing question")
```

### Guardrails for Safety

```python
@ag.input_guardrail
async def content_filter(context, user_input):
    if contains_prohibited_content(user_input):
        return ag.GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info={"reason": "Prohibited content"}
        )
    return ag.GuardrailFunctionOutput(tripwire_triggered=False)

agent = ag.Agent(
    instructions="Helpful assistant",
    tools=[...],
    input_guardrails=[content_filter],
    model=model,
)
```

### Custom Tool with Approval

```python
@ag.function_tool
async def delete_file(filepath: str) -> str:
    """Delete a file from disk"""
    os.remove(filepath)
    return f"Deleted {filepath}"

# Require approval for deletion
agent = ag.Agent(
    tools=[delete_file],
    tool_approval=lambda tool_name: tool_name == "delete_file",
)
```

### Session Persistence

```python
session = ag.SQLiteSession(
    db_path="conversations.db",
    table_name="agent_history"
)

config = ag.RunConfig(
    session=session,
    max_turns=10,
)

# Conversation persists across runs
result = await runner.run(
    input="Remember: my account is 12345",
    config=config,
    session_id="user-123",
)

# Later...
result2 = await runner.run(
    input="What's my account number?",
    config=config,
    session_id="user-123",
)
```

### Tracing and Observability

```python
class CustomExporter(ag.TracingProcessor):
    async def process(self, trace: ag.Trace) -> None:
        # Export traces to custom backend
        await send_to_datadog(trace)

processor = CustomExporter()
ag.add_trace_processor(processor)

with ag.trace("my_workflow") as span:
    span.set_attribute("user_id", "123")
    result = await runner.run(input="...")
```

---

## Dependencies and Integration Points

### Core Dependencies
- **openai** (2.17+) - OpenAI API client
- **pydantic** - Data validation and schema
- **typing-extensions** - Advanced type hints

### Integration Patterns

#### 1. **OpenAI API Integration**
- Native support for OpenAI models (GPT-4, GPT-4 Turbo)
- Responses API (primary), Chat Completions API (legacy)
- Conversation persistence via OpenAI's conversation endpoint

#### 2. **Model Context Protocol (MCP)**
- Located in `agents.mcp` submodule
- `HostedMCPTool` for integrating MCP servers
- `MCPUtil` for server management
- Enables tool discovery from external MCP providers

#### 3. **Realtime API**
- Located in `agents.realtime` submodule
- WebSocket-based real-time agent communication
- Currently in **beta**—expect breaking changes
- Voice-capable agents via WebRTC

#### 4. **Voice Capabilities**
- Located in `agents.voice` submodule
- Audio transcription and generation
- Integrate with realtime agents for voice interaction

#### 5. **Computer/GUI Automation**
- `Computer` and `AsyncComputer` classes
- Vision-based UI control
- Screenshot capture and action execution
- Browser automation, testing workflows

#### 6. **Code Execution**
- `CodeInterpreterTool` for Python code
- `ApplyPatchTool` for structured code editing
- Diff-based modifications with validation

#### 7. **External Services**
- Web search integration
- File search for knowledge bases
- Image generation (DALL-E)
- Custom service integration via `FunctionTool`

---

## Architecture Highlights

### Type Safety
- Generic types throughout: `Agent[TContext]`, `Handoff[TContext, TAgent]`
- Pydantic schemas for strict validation
- Type hints for all public APIs

### Async-First Design
- All I/O operations are async
- Supports concurrent tool execution
- Streaming responses via AsyncIterator

### Composability
- Tools, guardrails, and hooks compose freely
- Mix built-in and custom implementations
- Agents combine with other agents via handoffs

### Extensibility Points
- Custom `Model` implementations
- Custom `Tool` subclasses
- Custom `TracingProcessor` for observability
- Custom `Session` for persistence
- Custom guardrails and lifecycle hooks

### Error Handling
- `RunErrorHandlers` for custom error recovery
- Tool approval workflows for safety-critical operations
- Input/output guardrails for validation
- Detailed error context in `RunErrorDetails`

---

## Configuration and Setup

### Basic Setup

```python
import agents as ag

# Optional: Set default OpenAI configuration
ag.set_default_openai_key("sk-...")
# Or use a client
ag.set_default_openai_client(client, use_for_tracing=True)

# Optional: Set API version (responses vs chat completions)
ag.set_default_openai_api("responses")  # or "chat_completions"

# Enable debugging
ag.enable_verbose_stdout_logging()
```

### Model Configuration

```python
model = ag.OpenAIProvider().get_model("gpt-4o")

settings = ag.ModelSettings(
    temperature=0.7,
    max_tokens=2000,
    top_p=0.9,
)

agent = ag.Agent(
    instructions="...",
    model=model,
    model_settings=settings,
)
```

---

## Related Packages

The agents framework appears distinct from but related to:
- **openai** - Core API client (dependency)
- **agencies** / **institutions** / **empires** - Other agentic frameworks (not this package)

The `openai-agents` package is the official OpenAI implementation of agent orchestration, tightly integrated with their API and models.

---

## Summary

The OpenAI Agents framework is a sophisticated, production-ready SDK for building autonomous AI agents. It combines:
1. **Tool-based reasoning** with comprehensive tool ecosystem
2. **Agent hierarchies** through handoffs
3. **Safety mechanisms** via guardrails
4. **Persistence** through session management
5. **Observability** via distributed tracing
6. **Type safety** through generics and Pydantic

It exemplifies the RLM paradigm by enabling recursive task decomposition, multi-turn reasoning, and tool-augmented intelligence at scale. The framework is designed for both interactive prototyping (REPL support) and production deployments (streaming, session persistence, error handling).
