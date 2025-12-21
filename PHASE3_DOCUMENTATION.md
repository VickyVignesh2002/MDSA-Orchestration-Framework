# MDSA Phase 3 - Model Management

## Overview

Phase 3 implements the model management infrastructure for MDSA, providing loading, caching, quantization, and lifecycle management for machine learning models across all three tiers.

## What Was Implemented

### 1. Model Configuration (`mdsa/models/config.py`)

**Purpose**: Define model specifications and loading parameters

**Components**:
- `ModelTier` enum: TIER1 (TinyBERT), TIER2 (Phi), TIER3 (Domain SLMs)
- `QuantizationType` enum: NONE, INT4, INT8, FP16, BFLOAT16
- `ModelConfig` dataclass: Complete model specifications

**Predefined Configurations**:
```python
# Tier 1: TinyBERT (67M params, <50ms latency)
config = ModelConfig.for_tier1()
# - Device: Always CPU
# - Quantization: None (not needed for small models)
# - Max length: 128 tokens

# Tier 2: Phi-1.5 (1.3B params, optional)
config = ModelConfig.for_tier2()
# - Device: Auto-detected
# - Quantization: INT8 (8-bit for memory efficiency)
# - Max length: 512 tokens

# Tier 3: Domain SLMs (7-13B params)
config = ModelConfig.for_tier3("meta-llama/Llama-2-7b-hf")
# - Device: Auto-detected (GPU if available)
# - Quantization: INT4 (4-bit for large models)
# - Max length: 2048 tokens
```

**Custom Configuration**:
```python
config = ModelConfig(
    model_name="custom-model",
    tier=ModelTier.TIER3,
    device="cuda",
    quantization=QuantizationType.INT4,
    max_length=2048,
    batch_size=1
)
```

### 2. Model Registry (`mdsa/models/registry.py`)

**Purpose**: Thread-safe tracking of loaded models with LRU eviction

**Features**:
- **Thread-Safe Operations**: All operations protected with locks
- **LRU Eviction**: Automatically unloads least-recently-used models when limit reached
- **Usage Tracking**: Counts model accesses and tracks memory
- **Statistics**: Provides comprehensive model usage statistics

**Key Methods**:
```python
# Register a model
model_info = registry.register(
    model_id="llama-7b",
    config=config,
    model=model_obj,
    tokenizer=tokenizer_obj,
    memory_mb=3500.0
)

# Retrieve model (increments use count)
model_info = registry.get("llama-7b")

# Check if loaded
is_loaded = registry.is_loaded("llama-7b")

# Get statistics
stats = registry.get_stats()
# Returns: {
#     'models_loaded': 3,
#     'total_memory_mb': 7500.0,
#     'total_uses': 42,
#     'models': {'llama-7b': {...}, ...}
# }

# List all loaded models
models = registry.list_models()  # ['llama-7b', 'phi-1.5', 'tinybert']

# Unregister model
success = registry.unregister("llama-7b")

# Clear all models
registry.clear()
```

**LRU Eviction Example**:
```python
# Create registry with max 2 models
registry = ModelRegistry(max_models=2)

# Register 2 models - both loaded
registry.register("model1", config, model1, None, 100.0)
registry.register("model2", config, model2, None, 100.0)

# Register 3rd model - model1 (LRU) is automatically evicted
registry.register("model3", config, model3, None, 100.0)
# Now loaded: ['model2', 'model3']
```

### 3. Model Loader (`mdsa/models/loader.py`)

**Purpose**: Load models from HuggingFace with quantization and optimization

**Features**:
- **HuggingFace Integration**: Uses AutoModel and AutoTokenizer
- **Quantization Support**: 4-bit and 8-bit via BitsAndBytes
- **Device Placement**: Automatic CPU/CUDA/MPS detection
- **Model Caching**: Downloads to `~/.mdsa/models` by default
- **Memory Estimation**: Calculates model size before loading

**Quantization Configurations**:
```python
# 4-bit quantization (25% original size)
BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,  # Double quantization
    bnb_4bit_quant_type="nf4"        # Normal Float 4-bit
)

# 8-bit quantization (50% original size)
BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)
```

**Usage**:
```python
loader = ModelLoader(cache_dir="~/.mdsa/models")

# Load model with quantization
model, tokenizer = loader.load(config)

# Estimate memory before loading
estimated_mb = loader.estimate_memory(config)
```

**Memory Estimates**:
- Tier 1 (TinyBERT): ~250 MB
- Tier 2 (Phi-1.5): ~1,300 MB (unquantized), ~650 MB (INT8)
- Tier 3 (7B model): ~14,000 MB (unquantized), ~3,500 MB (INT4)

### 4. Model Manager (`mdsa/models/manager.py`)

**Purpose**: High-level interface combining Loader and Registry

**Features**:
- **Cached Loading**: `get_or_load()` returns cached models or loads new ones
- **Automatic Lifecycle**: Handles registration, memory tracking, eviction
- **Simple API**: One-line model access
- **Statistics**: Comprehensive usage and memory tracking

**Usage**:
```python
# Initialize manager
manager = ModelManager(max_models=10)

# Get or load model (cached)
model, tokenizer = manager.get_or_load("llama-7b", tier3_config)
# First call: Loads from HuggingFace, registers, returns
# Second call: Returns from cache (fast!)

# Check if loaded
if manager.is_loaded("llama-7b"):
    print("Model in cache")

# Get model info
info = manager.get_info("llama-7b")
# Returns: {
#     'model_id': 'llama-7b',
#     'tier': 'tier3',
#     'memory_mb': 3500.0,
#     'use_count': 5,
#     'loaded_at': '2025-01-15T10:30:00',
#     'last_used': '2025-01-15T11:45:00'
# }

# Get statistics
stats = manager.get_stats()
# Returns: {
#     'models_loaded': 3,
#     'max_models': 10,
#     'total_memory_mb': 5000.0,
#     'total_uses': 15,
#     'models': {...}
# }

# List loaded models
models = manager.list_models()  # ['llama-7b', 'phi-1.5', 'tinybert']

# Unload specific model
manager.unload("llama-7b")

# Clear all models
manager.clear_all()
```

## Architecture Integration

### Phase 1: Hardware Detection
- Detects available devices (CPU, CUDA, MPS)
- Informs model device placement in ModelConfig
- Used by ModelLoader for automatic device selection

### Phase 2: Orchestration
- TinyBERTOrchestrator can use ModelManager for intent classification
- State machine coordinates model loading based on workflow
- Domain routing determines which Tier 3 model to load

### Phase 3: Model Management
- ModelConfig defines specifications for all tiers
- ModelLoader handles actual loading with quantization
- ModelRegistry tracks all loaded models
- ModelManager provides simple API for phases 2 and 4

### Phase 4: Domain Execution (Next)
- Will use ModelManager to load domain-specific SLMs
- Each domain can specify its Tier 3 model
- ModelManager handles lifecycle and memory constraints

## Testing

### Quick Verification
```bash
# Test imports and basic functionality
python -c "
from mdsa import ModelConfig, QuantizationType, ModelTier
from mdsa.models import ModelRegistry, ModelManager

# Test Config
config = ModelConfig.for_tier1()
print(f'Config: {config.model_name}')

# Test Registry
registry = ModelRegistry(max_models=2)
registry.register('model1', config, {'data': 1}, None, 100.0)
print(f'Registered: {registry.list_models()}')

# Test Manager
manager = ModelManager()
stats = manager.get_stats()
print(f'Manager: models={stats[\"models_loaded\"]}, max={stats[\"max_models\"]}')

print('Phase 3 OK!')
"
```

### Expected Output
```
Config: huawei-noah/TinyBERT_General_6L_768D
Registered: ['model1']
Manager: models=0, max=10
Phase 3 OK!
```

## Troubleshooting

### Test Hangs When Loading Models

**Issue**: Tests hang when trying to download models from HuggingFace

**Cause**:
- First-time model downloads can take 5-30 minutes
- Network issues or slow connection
- Large model files (TinyBERT is ~250MB)

**Solution**:
1. Use the simplified test that doesn't download models:
   ```bash
   python -c "from mdsa import ModelManager; ..."  # Quick test
   ```

2. Or download models separately first:
   ```python
   from transformers import AutoModel, AutoTokenizer

   # Download TinyBERT (one-time, ~250MB)
   model = AutoModel.from_pretrained("huawei-noah/TinyBERT_General_6L_768D")
   tokenizer = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_6L_768D")
   ```

3. For testing without downloads, use dummy models:
   ```python
   # Use mock objects instead of real models
   dummy_model = {"type": "test"}
   registry.register("test", config, dummy_model, None, 100.0)
   ```

### Import Errors

**Issue**: `ModuleNotFoundError: No module named 'mdsa.models'`

**Solution**:
1. Ensure you're in the project root directory
2. Install in development mode: `pip install -e .`
3. Check `mdsa/models/__init__.py` exists and has exports

### Memory Issues

**Issue**: Out of memory when loading large models

**Solution**:
1. Use quantization for Tier 2 and 3:
   ```python
   config = ModelConfig.for_tier3("model", quantization=QuantizationType.INT4)
   ```

2. Reduce max_models limit:
   ```python
   manager = ModelManager(max_models=2)  # Only keep 2 models loaded
   ```

3. Monitor memory usage:
   ```python
   stats = manager.get_stats()
   print(f"Total memory: {stats['total_memory_mb']} MB")
   ```

## File Reference

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `mdsa/models/__init__.py` | Package exports | 22 | ✅ Complete |
| `mdsa/models/config.py` | Model configuration | 149 | ✅ Complete |
| `mdsa/models/registry.py` | Model tracking | 224 | ✅ Complete |
| `mdsa/models/loader.py` | Model loading | 190 | ✅ Complete |
| `mdsa/models/manager.py` | High-level API | 154 | ✅ Complete |
| `mdsa/__init__.py` | Main exports (updated) | 48 | ✅ Complete |

## Next Steps: Phase 4

Phase 4 will implement Domain Execution, which includes:

1. **Domain Registry**: Track registered domains and their models
2. **Domain Executor**: Load and execute domain-specific SLMs
3. **Prompt Templates**: Domain-specific prompts for consistent behavior
4. **Response Generation**: Generate domain-specific responses
5. **Integration**: Connect Phases 1-3 with domain execution

See `PHASE4_PLAN.md` for detailed implementation plan.

---

**Phase 3 Status**: ✅ **COMPLETE**
**Date Completed**: 2025-01-15
**Next Phase**: Phase 4 - Domain Execution
