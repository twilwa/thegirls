# PIHub - Package Documentation

## Overview

**PIHub** is a Python package (version 0.0.0) that is currently under active development. It is designed to integrate with the Recursive Language Models (RLM) paradigm and provide utilities for working with language model inference strategies that process unbounded-length context through recursive decomposition.

The package is authored by Will Brown (williambrown97@gmail.com) and is licensed under the MIT License. The project homepage is located at https://pihub.ai.

### Purpose

PIHub appears designed as a hub or integration layer for:
- Interfacing with recursive language model environments
- Managing model context and REPL-based inference
- Supporting hierarchical or distributed LLM calls
- Providing utilities for unbounded context processing

As stated in the official package metadata: "Coming soon, under development."

---

## Package Status

| Property | Value |
|----------|-------|
| **Current Version** | 0.0.0 (Pre-release) |
| **Python Requirement** | >= 3.11 |
| **License** | MIT |
| **Status** | In Development |
| **Repository** | https://pihub.ai |

### Current State

The current distribution contains only:
- `pihub/__init__.py` - Package initialization file with version string
- Package metadata in `pihub-0.0.0.dist-info/`

The package is a minimal skeleton, suggesting that active development is underway to implement core functionality.

---

## Integration with RLM Paradigm

### What are Recursive Language Models?

Recursive Language Models (RLMs) represent an inference strategy where:

1. **Root Model** - A primary language model interacts with a Python REPL environment
2. **Context Storage** - Input context of unbounded length is stored as variables within the REPL
3. **Recursive Decomposition** - The model can break down large problems into smaller chunks
4. **Sub-LLM Spawning** - The root model can trigger parallel or sequential sub-LLM calls to process context chunks
5. **Hierarchical Interaction** - Sub-models recursively process portions of context and return results to the parent

### PIHub's Role in RLM Architecture

Based on the ecosystem context, PIHub is positioned as:

- **Integration Layer** - Connect RLM environments with various model backends
- **Context Management** - Handle storage and routing of unbounded context through REPL environments
- **Model Coordination** - Manage spawning and orchestration of sub-LLM calls
- **Protocol Handler** - Likely work with MCP (Model Context Protocol) and other standards

The related `RLMEnv` class in the `verifiers` package demonstrates the practical application of RLMs. PIHub likely provides complementary utilities and abstractions for this paradigm.

---

## Key Classes and Functions

### Current API

Currently, the package exposes only:

```python
from pihub import __version__

# Access version string
print(__version__)  # "0.0.0"
```

### Expected Future Components

Based on the RLM paradigm and the package purpose, anticipated future components may include:

#### Core Model Classes
- **ModelHub** - Central registry for available language models
- **RLMClient** - Client for interacting with RLM environments
- **ContextManager** - Handle large context storage and routing
- **SubLLMOrchestrator** - Coordinate parallel/sequential sub-model calls

#### Protocol Handlers
- **REPLInterface** - Communication with Python REPL for context storage
- **MCPAdapter** - Integration with Model Context Protocol servers
- **ToolRegistry** - Management of available tools for LLM interaction

#### Utilities
- **ContextChunker** - Decompose large inputs into manageable pieces
- **ResponseAggregator** - Combine results from multiple sub-LLM calls
- **CallTracker** - Monitor and log hierarchical LLM interactions

---

## Example Usage Patterns

Given the package's intended purpose, future usage would likely follow these patterns:

### Pattern 1: Basic RLM Client Initialization

```python
from pihub import RLMClient

# Initialize RLM client with root model
client = RLMClient(
    root_model="claude-opus-4.6",
    sub_model="claude-haiku-4.5",
    max_parallelism=5
)

# Process large context
result = client.process(
    context=large_document,
    task="Summarize the key findings"
)
```

### Pattern 2: Context Management

```python
from pihub import ContextManager

# Create manager for unbounded context
ctx_mgr = ContextManager(repl_timeout=300)

# Store context in REPL
ctx_id = ctx_mgr.store_context(large_text)

# Process context chunks
chunks = ctx_mgr.get_chunks(ctx_id, chunk_size=4096)

for chunk in chunks:
    result = process_chunk(chunk)  # Sub-LLM call
```

### Pattern 3: Model Coordination

```python
from pihub import SubLLMOrchestrator

# Create orchestrator for parallel processing
orchestrator = SubLLMOrchestrator(
    max_workers=5,
    timeout_per_call=60
)

# Spawn multiple sub-LLM calls
results = orchestrator.map(
    fn=analyze_chunk,
    chunks=context_chunks
)
```

### Pattern 4: Tool Integration

```python
from pihub import ToolRegistry, MCPAdapter

# Register available tools
tools = ToolRegistry()
tools.register_mcp_server("web_search", mcp_uri)
tools.register_function(retrieve_document)

# Provide tools to RLM
adapter = MCPAdapter(tools)
client.set_tool_adapter(adapter)
```

---

## Dependencies and Integration Points

### Python Requirements
- **Python >= 3.11** (per package specification)
- Standard library modules for:
  - `subprocess` - REPL interaction
  - `asyncio` - Parallel sub-LLM calls
  - `json` - Configuration and serialization

### Expected External Dependencies

The package likely depends on:

#### Core Dependencies
- **anthropic** or similar - Language model API clients
- **asyncio** - Asynchronous request handling

#### Optional Ecosystem Integration
- **verifiers** - RLM environment implementations (`RLMEnv` class)
- **huggingface_hub** - Model access and management (present in same environment)
- **mcp** - Model Context Protocol implementation
- **pydantic** - Data validation and configuration

### Integration Points

#### 1. Language Model Providers
- Anthropic (Claude models)
- OpenAI (GPT models)
- Local models via llama.cpp or similar

#### 2. REPL Environments
- Python REPL with context variables
- Jupyter kernel backends
- Custom sandboxed execution environments

#### 3. MCP Servers
- Web search tools
- File system access
- Database queries
- Custom tool implementations

#### 4. Storage Backends
- In-memory context storage
- Redis for distributed context
- Local file system
- Cloud object storage (S3, etc.)

#### 5. Monitoring & Observability
- Logging frameworks (logging, structlog)
- Tracing systems (OpenTelemetry)
- Metrics collection

---

## Development Status and Roadmap

### Current Phase
**Skeleton Phase** - Core package structure and metadata established, awaiting implementation.

### Next Steps (Inferred)
1. Implement core `RLMClient` for basic model interaction
2. Develop `ContextManager` for unbounded context handling
3. Create `SubLLMOrchestrator` for parallel processing
4. Add MCP integration layer
5. Implement tool registry and discovery
6. Add comprehensive error handling and logging
7. Create extensive documentation and examples

### Community and Contributions
For contributions or updates, refer to:
- Homepage: https://pihub.ai
- Author: Will Brown (williambrown97@gmail.com)
- License: MIT (permissive for modifications)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│          PIHub Integration Layer                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────────┐    ┌──────────────────┐    │
│  │   RLMClient   │───▶│ ContextManager   │    │
│  └───────────────┘    └──────────────────┘    │
│         │                      │               │
│         ▼                       ▼               │
│  ┌──────────────────────────────────────┐     │
│  │  SubLLMOrchestrator                  │     │
│  │  (Parallel Processing & Spawning)    │     │
│  └──────────────────────────────────────┘     │
│         │              │              │        │
│         ▼              ▼              ▼        │
│    ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│    │  Tool   │   │   MCP   │   │  REPL   │   │
│    │Registry │   │ Adapter │   │Interface│   │
│    └─────────┘   └─────────┘   └─────────┘   │
│         │              │              │        │
└─────────┼──────────────┼──────────────┼────────┘
          │              │              │
          ▼              ▼              ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ LLM Backends │ │MCP Servers  │ │   Python     │
│  (Claude,    │ │ (Search,    │ │   REPL       │
│   GPT, etc)  │ │  Tools)     │ │  Environment │
└──────────────┘ └─────────────┘ └──────────────┘
```

---

## Related Resources

### RLM Paradigm
- **Reference Paper/Blog**: https://alexzhang13.github.io/blog/2025/rlm/
- **Practical Implementation**: `verifiers.envs.experimental.RLMEnv`

### Ecosystem Context
- **Verifiers Library** - Provides `RLMEnv` class for implementing RLM inference
- **HuggingFace Hub** - Model access and management
- **MCP Standard** - Tool and service integration protocol

### Author Contact
- **Email**: williambrown97@gmail.com
- **Project Homepage**: https://pihub.ai

---

## Conclusion

PIHub is positioned as a critical integration and coordination layer for Recursive Language Models. While currently in pre-release (v0.0.0), it represents an important abstraction for managing:

- Unbounded-length context processing
- Hierarchical language model calls
- Tool and service integration
- Parallel sub-model coordination

The package's minimal current state reflects early-stage development, with the full feature set expected to be substantial once implementation begins. Developers interested in RLM paradigms should monitor this package for future releases and integration opportunities with their language model applications.
