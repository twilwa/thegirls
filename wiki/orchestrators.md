# Orchestrators Package

## Overview and Purpose

The **orchestrators** package is a foundational utility library designed for building Python orchestration flows within the Recursive Language Models (RLM) paradigm. Currently at version 0.1.0, it serves as the initial PyPI package scaffold for orchestration capabilities, with support for asynchronous batch generation and training coordination.

The primary purpose of orchestrators is to:
- Manage asynchronous workflows and parallel execution patterns
- Coordinate batch generation with reinforcement learning training
- Provide abstraction layers for complex multi-stage processing pipelines
- Enable efficient resource utilization through async/await patterns and worker thread management

## Key Architecture Components

### Core Pattern: Worker Thread Architecture

The orchestrators package implements a producer-consumer pattern with dedicated worker threads for background processing. The primary implementation follows this architecture:

#### Orchestrator Class
The `Orchestrator` class (found in `verifiers.rl.trainer.orchestrator`) represents the reference implementation pattern:

**Key Responsibilities:**
- Manages asynchronous batch generation in parallel with RL training
- Handles thread-safe communication via queue-based message passing
- Coordinates environment interactions and sampling
- Processes trajectory data and computes advantages for training

**Critical Components:**
- **Request/Result Queues**: Thread-safe FIFO queues for submitting batch generation requests and retrieving completed results
- **Worker Thread**: Dedicated asyncio event loop running in background thread for non-blocking I/O operations
- **State Management**: Completed batch cache to allow out-of-order result retrieval
- **Timeout Handling**: Configurable generation timeouts with proper resource cleanup

### Data Models

#### Microbatch Structure
```python
class Microbatch(BaseModel):
    input_ids: list[list[int]]          # Tokenized input sequences
    loss_mask: list[list[int]]          # Binary mask for valid loss positions
    sampling_logprobs: list[list[float]] # Log probabilities from sampling
    advantages: list[list[float]]        # Advantage estimates for RL
    items: int                           # Total tokens in microbatch
```

#### Batch Structure
```python
class Batch(BaseModel):
    batch_id: int                       # Unique batch identifier
    microbatches: list[list[Microbatch]] # Per-process partitioned microbatches
    items_per_process: list[int]        # Token count per process
    global_item_count: int              # Total tokens across all processes
    generation_time: float              # Wall-clock generation duration
    prompts: list[Any]                  # Original prompts (for logging)
    completions: list[Any]              # Model completions (for logging)
    errors: list[Any]                   # Error tracking
    metrics_dict: dict[str, float]      # Computed metrics (rewards, timing)
    rewards_dict: dict[str, list[float]] # Per-rollout rewards
```

## Integration with RLM Paradigm

The orchestrators package fits into the Recursive Language Models (RLM) paradigm through several key mechanisms:

### 1. Asynchronous Generation During Training

RLM systems require continuous generation of training data while model parameters are being updated. The orchestrator decouples these two processes:

- **Training Process**: Synchronously performs backward passes and parameter updates
- **Generation Process**: Asynchronously generates new trajectories via background worker thread
- **Result Exchange**: Batches are queued and retrieved on-demand, allowing training to proceed while generation happens concurrently

### 2. Multi-Rollout Support

The RLM paradigm often requires multiple rollouts per training example to estimate advantages and compute policy gradients:

```
Each prompt generates N rollouts (controlled by rollouts_per_example)
↓
Each rollout produces a complete trajectory with tokens and scores
↓
Trajectories are decomposed horizontally into step-level training examples
↓
Steps are aggregated into microbatches partitioned across training processes
```

### 3. Advantage Computation and Trajectory Processing

The orchestrator implements sophisticated trajectory processing:

- **Trajectory Decomposition**: Each rollout trajectory is decomposed into individual steps, where each step becomes a separate training example
- **Advantage Computation**: Rewards and step-level advantages are extracted and broadcast across token positions within each step
- **Loss Masking**: Binary masks delineate valid training positions (typically excluding prompt tokens or special positions)
- **Log Probability Tracking**: Sampling log probabilities are tracked and paired with advantages for policy gradient computation

### 4. Recursive Feedback Loop

The orchestrator supports the recursive nature of RLM:

1. **Initialization**: Start with base model and initial dataset
2. **Batch Generation**: Environment executes model with sampling to generate trajectories
3. **Scoring**: Trajectories are scored (reward signals)
4. **Processing**: Scores and trajectories are converted to training microbatches
5. **Training**: Models are fine-tuned on processed microbatches
6. **Iteration**: Process repeats with updated model parameters

## Key Classes and Functions

### Orchestrator

**Primary Class**: Core orchestration engine managing asynchronous batch generation.

**Constructor Parameters**:
- `env: Environment` - The evaluation environment (provides dataset and generation capability)
- `client_base_url: str` - API endpoint for model inference
- `client_api_key: str` - Authentication credentials
- `client_limit: int` - Maximum concurrent HTTP connections
- `client_timeout: float` - Network timeout (seconds)
- `model_name: str` - Model identifier for generation
- `sampling_args: dict[str, Any]` - Generation hyperparameters (temperature, top_p, etc.)
- `rollouts_per_example: int` - Number of completions per prompt
- `batch_size: int` - Total batch size (prompts × rollouts)
- `micro_batch_size: int` - Training microbatch size for gradient accumulation
- `num_processes: int` - Number of training processes for sharding
- `generation_timeout: float` - Maximum time for batch generation (seconds)
- `processing_class: PreTrainedTokenizerBase` - Tokenizer for encoding/masking
- `mask_env_responses: bool` - Whether to mask environment response tokens
- `max_seq_len: int` - Maximum sequence length (padded/truncated)
- `max_prompt_len: int` - Maximum prompt length filter
- `mask_truncated_completions: bool` - Exclude loss on truncated tokens
- `zero_truncated_completions: bool` - Zero out truncated token embeddings
- `max_concurrent: int` - Maximum concurrent generation requests

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `start()` | Initialize worker thread and begin accepting batch requests |
| `stop()` | Gracefully shutdown worker thread and cleanup resources |
| `submit_batch(batch_id: int)` | Queue a batch for asynchronous generation |
| `get_batch(batch_id: int) -> Batch` | Blocking retrieval of completed batch (waits if not ready) |
| `generation_worker()` | Worker thread main loop (internal) |
| `generate_batch(batch_id: int) -> Batch` | Async batch generation implementation |
| `get_dataset_slice(batch_id: int) -> Dataset` | Retrieve dataset portion for batch |

### Data Classes

**Microbatch**: Represents tokenized training data for a single gradient update step, partitioned for per-process training.

**Batch**: Complete result of batch generation including trajectories, rewards, metrics, and error information.

## Example Usage Patterns

### Basic Orchestrator Setup and Training Loop

```python
from verifiers import Environment, Orchestrator
from transformers import AutoTokenizer

# Initialize environment with dataset
env = Environment(dataset=train_dataset)

# Configure tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Create orchestrator
orchestrator = Orchestrator(
    env=env,
    client_base_url="http://localhost:8000/v1",
    client_api_key="sk-xxx",
    client_limit=100,
    client_timeout=120.0,
    model_name="meta-llama/Llama-2-7b-hf",
    sampling_args={
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 256
    },
    rollouts_per_example=4,
    batch_size=32,  # 8 prompts × 4 rollouts
    micro_batch_size=8,
    num_processes=4,
    generation_timeout=300.0,
    processing_class=tokenizer,
    mask_env_responses=True,
    max_seq_len=2048,
    max_prompt_len=1024,
    mask_truncated_completions=True,
    zero_truncated_completions=False,
    max_concurrent=100
)

# Start background generation worker
orchestrator.start()

# Training loop
for epoch in range(num_epochs):
    for batch_id in range(num_batches):
        # Submit batch for generation while previous batch trains
        orchestrator.submit_batch(batch_id)

        # Retrieve completed batch (blocks if not ready)
        batch = orchestrator.get_batch(batch_id)

        # Process microbatches for training
        for process_idx, microbatches in enumerate(batch.microbatches):
            for mb in microbatches:
                # Train on microbatch
                logits = model(input_ids=mb.input_ids)
                loss = compute_loss(logits, mb.input_ids, mb.loss_mask, mb.advantages)
                loss.backward()

        # Log metrics
        print(f"Batch {batch_id}: {batch.metrics_dict}")

# Cleanup
orchestrator.stop()
```

### Pipelined Generation and Training

The key pattern is **pipelining**: submit batch N while training on batch N-1:

```python
orchestrator.start()

# Pre-fetch first batch
orchestrator.submit_batch(0)

for batch_id in range(1, num_batches):
    # Get results from previous batch
    batch = orchestrator.get_batch(batch_id - 1)

    # Train on it (while next batch generates in parallel)
    train_on_batch(batch)

    # Submit next batch generation
    orchestrator.submit_batch(batch_id)

# Don't forget final batch
final_batch = orchestrator.get_batch(num_batches - 1)
train_on_batch(final_batch)

orchestrator.stop()
```

### Multi-Process Training Integration

Batches are automatically partitioned for multi-GPU/multi-process training:

```python
batch = orchestrator.get_batch(batch_id)

# Distribute microbatches across processes
for process_rank in range(num_processes):
    microbatches = batch.microbatches[process_rank]
    items_for_process = batch.items_per_process[process_rank]

    # Scatter to worker process
    send_to_gpu(process_rank, microbatches)

    # Each process trains independently on its microbatches
    # Synchronize gradients via distributed training framework
```

### Error Handling and Monitoring

```python
batch = orchestrator.get_batch(batch_id)

# Check for generation errors
if batch.errors:
    for error in batch.errors:
        if error:
            logger.warning(f"Generation error: {error}")

# Monitor metrics
for metric_name, metric_value in batch.metrics_dict.items():
    if metric_name.startswith("timing/"):
        logger.info(f"{metric_name}: {metric_value}ms")
    elif metric_name.startswith("reward/"):
        logger.info(f"{metric_name}: {metric_value:.4f}")

# Handle timeout gracefully
try:
    batch = orchestrator.get_batch(batch_id)
except TimeoutError:
    logger.error(f"Batch {batch_id} generation timed out")
    # Implement fallback logic
```

## Dependencies and Integration Points

### Core Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| `asyncio` | Async event loop for non-blocking I/O | Python stdlib |
| `threading` | Background worker thread management | Python stdlib |
| `queue` | Thread-safe inter-process communication | Python stdlib |
| `httpx` | Async HTTP client for LLM API calls | External |
| `openai` | LLM API client (AsyncOpenAI) | External |
| `pydantic` | Data validation via Pydantic models | External |
| `transformers` | Tokenizer and model loading | External |
| `datasets` | HuggingFace Dataset interface | External |
| `numpy` | Numerical computations for metrics | External |

### Integration with Verifiers Package

The orchestrators pattern is deeply integrated with the `verifiers` package:

- **Environment**: Orchestrator accepts a `verifiers.Environment` instance that provides:
  - Dataset access and sampling
  - Evaluation/generation interface
  - Reward computation logic

- **Tokenizer**: Uses `transformers.PreTrainedTokenizerBase` for prompt encoding and length filtering

- **RLTrainer**: The output batches feed directly into training loops that use:
  - `RLConfig` for hyperparameter management
  - `RLTrainer` or `GRPOTrainer` for gradient computation and parameter updates

### Async HTTP Client Architecture

```
Orchestrator.client (AsyncOpenAI)
    ↓
httpx.AsyncClient (connection pooling, limits)
    ↓
LLM API (OpenAI-compatible endpoint)
```

This architecture enables:
- Connection pooling with configurable limits
- Custom timeout management
- Proper resource cleanup via context managers
- Non-blocking I/O in worker thread

### Environment Integration

The orchestrator uses the environment for:

```python
dataset = env.get_dataset()           # Fetch data slice
results = await env.generate(         # Execute generation
    dataset,
    client=self.client,
    model=model_name,
    sampling_args=sampling_args,
    max_concurrent=max_concurrent
)
```

The environment handles:
- Dataset management and slicing
- Model invocation with sampling
- Trajectory recording (prompts, completions, intermediate states)
- Optional reward computation

### Tokenization and Masking

Integration points with the tokenizer:

```python
# Prompt length filtering (during initialization)
prompt_ids = tokenizer.encode(prompt_text)
if len(prompt_ids) > max_prompt_len:
    skip_example = True

# Encoding and masking (during batch processing)
# Binary masks mark valid loss positions (typically completion tokens only)
mask = [0] * len(prompt_ids) + [1] * len(completion_ids)
```

## Configuration and Tuning

### Key Hyperparameters

**Batch Sizing**:
- `batch_size`: Total tokens per batch = `prompts_per_batch × rollouts_per_example`
- `micro_batch_size`: Sub-batch size for gradient accumulation (smaller = less memory per step)
- `rollouts_per_example`: Multiple samples per prompt for advantage estimation

**Concurrency**:
- `num_processes`: Number of training processes (affects microbatch partitioning)
- `client_limit`: Max concurrent HTTP connections for generation (tune based on API limits)
- `max_concurrent`: Max concurrent environment requests

**Timeouts**:
- `generation_timeout`: How long to wait for a batch before raising TimeoutError
- `client_timeout`: Individual HTTP request timeout

**Filtering and Masking**:
- `max_seq_len`: Hard limit on total sequence length
- `max_prompt_len`: Filter examples with longer prompts
- `mask_env_responses`: Whether to exclude environment response tokens from loss
- `mask_truncated_completions`: Don't train on tokens beyond max_seq_len

## Performance Considerations

### Throughput Optimization

1. **Pipelined Execution**: Generate batch N+1 while training on batch N
2. **Connection Pooling**: Reuse HTTP connections via httpx client
3. **Async I/O**: Non-blocking generation allows CPU-bound training to proceed
4. **Micro-batching**: Smaller microbatches enable gradient accumulation without loading full batch

### Memory Management

1. **Batch Caching**: Only completed batches stored in memory
2. **Dataset Slicing**: Load only required data slice per batch
3. **Tokenization Caching**: Consider caching encoded prompts if reusing dataset

### Monitoring and Debugging

Available metrics in `batch.metrics_dict`:
- `reward` / `reward/std`: Rollout-level rewards
- `advantage/absmean`: Mean absolute advantage values
- `tokens/completion`: Average completion length
- `tokens/masked_fraction`: Fraction of tokens excluded from loss
- `timing/generation_ms`: Model inference latency
- `timing/scoring_ms`: Reward computation latency
- `wall_clock/generate_s`: Total batch wall time

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Training Process                         │
│  (Synchronous - updates model parameters)                   │
└──────────────────────────────────────────────────────────────┘
                           ↑ (get_batch)
                           │
                    ┌──────────────┐
                    │ Orchestrator │
                    │  Result      │
                    │  Queue       │
                    └──────────────┘
                           ↑ (put result)
                           │
┌──────────────────────────────────────────────────────────────┐
│ Worker Thread (Async Event Loop)                             │
│                                                               │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐  │
│  │ Request      │  →   │ generate_    │ →  │  AsyncOpenAI│  │
│  │ Queue        │      │ batch()      │    │   Client    │  │
│  └──────────────┘      └──────────────┘    └─────────────┘  │
│  (submit_batch)             │                                 │
│                              │                                │
│                         Process Results:                      │
│                         - Extract trajectories               │
│                         - Decompose into steps               │
│                         - Compute advantages                 │
│                         - Create microbatches                │
│                         - Partition per-process              │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Future Development

The 0.1.0 version is a scaffold. Potential extensions include:

1. **Batch Prioritization**: Urgent batches skipped to front of queue
2. **Adaptive Batch Sizing**: Dynamic batch size based on available GPU memory
3. **Fallback Strategies**: Cached generations if API fails
4. **Multi-Model Support**: Generate from different models in same orchestrator
5. **Distributed Orchestration**: Multi-machine batch generation coordination
6. **Streaming Microbatches**: Begin training on microbatches as they complete (before entire batch ready)

## See Also

- **verifiers**: Package providing `Environment` abstraction and RLM training infrastructure
- **RLTrainer**: Training loop implementation that consumes Orchestrator batches
- **Environment**: Dataset and generation interface used by Orchestrator
