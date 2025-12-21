# MDSA Phase 4 - Domain Execution

## Overview

Phase 4 implements the domain execution layer, bringing together Phases 1-3 to enable actual query processing with domain-specific Small Language Models (SLMs).

## Objectives

1. **Domain Configuration**: Define domain-specific models and prompts
2. **Domain Executor**: Load and execute domain SLMs
3. **Prompt Engineering**: Create domain-specific prompt templates
4. **Response Generation**: Generate and validate responses
5. **End-to-End Integration**: Complete MDSA workflow from query to response

## Components to Implement

### 1. Domain Configuration (`mdsa/domains/config.py`)

**Purpose**: Define domain-specific settings and models

```python
@dataclass
class DomainConfig:
    """Configuration for a domain."""
    domain_id: str
    name: str
    description: str
    keywords: List[str]

    # Model configuration
    model_name: str  # HuggingFace model or local path
    model_tier: ModelTier = ModelTier.TIER3
    quantization: QuantizationType = QuantizationType.INT4

    # Prompt configuration
    system_prompt: str = ""
    prompt_template: str = "{query}"
    max_tokens: int = 512
    temperature: float = 0.7

    # Execution settings
    timeout_seconds: int = 30
    max_retries: int = 2
```

**Predefined Domains**:
```python
# Finance domain
FINANCE_DOMAIN = DomainConfig(
    domain_id="finance",
    name="Financial Services",
    description="Banking, transactions, and financial queries",
    keywords=["money", "transfer", "payment", "balance", "account"],
    model_name="meta-llama/Llama-2-7b-chat-hf",
    system_prompt="You are a financial assistant...",
    prompt_template="User query: {query}\n\nProvide a helpful financial response:"
)

# Medical domain
MEDICAL_DOMAIN = DomainConfig(
    domain_id="medical",
    name="Medical Information",
    description="Health, symptoms, and medical guidance",
    keywords=["health", "symptom", "doctor", "medicine", "pain"],
    model_name="microsoft/BioGPT-Large",
    system_prompt="You are a medical information assistant...",
    prompt_template="Patient query: {query}\n\nProvide medical information:"
)
```

### 2. Domain Registry (`mdsa/domains/registry.py`)

**Purpose**: Track registered domains and their configurations

```python
class DomainRegistry:
    """Registry for managing domains."""

    def register(self, config: DomainConfig) -> None:
        """Register a domain configuration."""

    def get(self, domain_id: str) -> Optional[DomainConfig]:
        """Get domain configuration."""

    def list_domains(self) -> List[str]:
        """List all registered domain IDs."""

    def get_stats(self) -> Dict[str, Any]:
        """Get domain statistics."""
```

### 3. Prompt Builder (`mdsa/domains/prompts.py`)

**Purpose**: Build domain-specific prompts with context

```python
class PromptBuilder:
    """Build prompts for domain SLMs."""

    def build_prompt(
        self,
        query: str,
        domain_config: DomainConfig,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build a complete prompt."""

    def format_system_prompt(self, domain_config: DomainConfig) -> str:
        """Format system prompt for domain."""

    def format_user_prompt(
        self,
        query: str,
        template: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format user prompt with template."""
```

**Example Prompts**:
```python
# Finance domain
"""
System: You are a financial assistant helping users with banking and transactions.
Provide accurate, helpful responses about financial matters.

User query: Transfer $100 to John's account

Provide a helpful financial response:
"""

# Medical domain
"""
System: You are a medical information assistant. Provide general health information
and always recommend consulting with healthcare professionals for specific medical advice.

Patient query: I have a headache and fever

Provide medical information:
"""
```

### 4. Domain Executor (`mdsa/domains/executor.py`)

**Purpose**: Execute queries using domain-specific SLMs

```python
class DomainExecutor:
    """Execute queries with domain SLMs."""

    def __init__(
        self,
        model_manager: ModelManager,
        prompt_builder: PromptBuilder
    ):
        self.model_manager = model_manager
        self.prompt_builder = prompt_builder

    def execute(
        self,
        query: str,
        domain_config: DomainConfig,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a query with domain SLM.

        Returns:
            {
                'response': str,  # Generated response
                'domain': str,  # Domain ID
                'model': str,  # Model name
                'latency_ms': float,
                'tokens_generated': int,
                'confidence': float
            }
        """

    def _load_model(self, domain_config: DomainConfig):
        """Load domain model using ModelManager."""

    def _generate_response(
        self,
        model,
        tokenizer,
        prompt: str,
        config: DomainConfig
    ) -> Tuple[str, int]:
        """Generate response from model."""

    def _validate_response(
        self,
        response: str,
        domain_config: DomainConfig
    ) -> bool:
        """Validate generated response."""
```

### 5. Response Validator (`mdsa/domains/validator.py`)

**Purpose**: Validate and filter generated responses

```python
class ResponseValidator:
    """Validate domain SLM responses."""

    def validate(
        self,
        response: str,
        domain_config: DomainConfig
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate response.

        Returns:
            (is_valid, error_message)
        """

    def check_length(self, response: str, max_length: int) -> bool:
        """Check response length."""

    def check_toxicity(self, response: str) -> bool:
        """Check for toxic content."""

    def check_relevance(
        self,
        response: str,
        domain_config: DomainConfig
    ) -> bool:
        """Check domain relevance."""
```

### 6. Updated Orchestrator (`mdsa/core/orchestrator.py`)

**Purpose**: Integrate domain execution into workflow

**Updates to `TinyBERTOrchestrator`**:
```python
class TinyBERTOrchestrator:
    def __init__(self, ...):
        # Existing components
        self.hardware = HardwareDetector()
        self.router = IntentRouter()
        self.state_machine = StateMachine()
        self.bus = MessageBus()

        # NEW: Phase 3 & 4 components
        self.model_manager = ModelManager(max_models=5)
        self.domain_registry = DomainRegistry()
        self.domain_executor = DomainExecutor(
            model_manager=self.model_manager,
            prompt_builder=PromptBuilder()
        )

    def register_domain(
        self,
        domain_id: str,
        description: str,
        keywords: List[str],
        model_name: Optional[str] = None,  # NEW
        system_prompt: Optional[str] = None,  # NEW
        prompt_template: Optional[str] = None  # NEW
    ):
        """Register domain with optional execution config."""

    def process_request(self, query: str) -> Dict[str, Any]:
        """
        Complete request processing with domain execution.

        Workflow:
        1. ROUTE: Classify query to domain (TinyBERT)
        2. LOAD_SLM: Load domain SLM via ModelManager
        3. EXECUTE: Generate response with domain SLM
        4. VALIDATE: Check response quality
        5. RETURN: Return response to user
        """
```

## Implementation Steps

### Step 1: Domain Configuration
- [ ] Create `mdsa/domains/__init__.py`
- [ ] Implement `DomainConfig` dataclass
- [ ] Add predefined domain configurations
- [ ] Add configuration validation

### Step 2: Domain Registry
- [ ] Implement `DomainRegistry` class
- [ ] Add thread-safe registration
- [ ] Add domain lookup methods
- [ ] Add statistics tracking

### Step 3: Prompt Engineering
- [ ] Implement `PromptBuilder` class
- [ ] Create prompt templates
- [ ] Add context injection
- [ ] Test prompt formatting

### Step 4: Domain Execution
- [ ] Implement `DomainExecutor` class
- [ ] Integrate with `ModelManager`
- [ ] Add response generation
- [ ] Add timeout handling
- [ ] Add retry logic

### Step 5: Response Validation
- [ ] Implement `ResponseValidator` class
- [ ] Add length validation
- [ ] Add basic content filtering
- [ ] Add relevance checking

### Step 6: Orchestrator Integration
- [ ] Update `TinyBERTOrchestrator.__init__`
- [ ] Update `register_domain` method
- [ ] Update `process_request` workflow
- [ ] Update state machine steps
- [ ] Add error handling

### Step 7: Testing
- [ ] Create Phase 4 manual test
- [ ] Test each domain type
- [ ] Test full end-to-end workflow
- [ ] Test error cases
- [ ] Performance testing

## Testing Strategy

### Unit Tests
```python
# Test domain configuration
def test_domain_config():
    config = DomainConfig(
        domain_id="test",
        name="Test",
        description="Test domain",
        keywords=["test"],
        model_name="test-model"
    )
    assert config.domain_id == "test"

# Test domain registry
def test_domain_registry():
    registry = DomainRegistry()
    registry.register(config)
    assert registry.get("test") == config

# Test prompt builder
def test_prompt_builder():
    builder = PromptBuilder()
    prompt = builder.build_prompt("query", config)
    assert "query" in prompt
```

### Integration Tests
```python
# Test end-to-end workflow
def test_end_to_end():
    orchestrator = MDSA()
    orchestrator.register_domain(
        "test",
        "Test domain",
        ["test"],
        model_name="gpt2",  # Small model for testing
        system_prompt="You are a test assistant."
    )

    result = orchestrator.process_request("test query")

    assert result['status'] == 'success'
    assert 'response' in result
    assert result['metadata']['domain'] == 'test'
```

### Manual Testing
```bash
python manual_test_phase4.py
```

**Expected Output**:
```
======================================================================
MDSA Phase 4 - Domain Execution Test
======================================================================

[1] Registering domains...
[OK] Registered 'finance' domain
[OK] Registered 'medical' domain
[OK] Registered 'support' domain

[2] Testing domain execution...

Query: "Transfer $100 to savings account"
Domain: finance
Model: Loading meta-llama/Llama-2-7b-chat-hf (INT4)...
Response: "To transfer $100 to your savings account, you can:
1. Log into your online banking
2. Select 'Transfer Funds'
3. Choose checking to savings
4. Enter $100
5. Confirm the transfer

The transfer typically completes within minutes."

Latency: 2,450ms
Tokens: 67

[3] Testing validation...
[OK] Response length valid (67 tokens < 512 max)
[OK] No toxic content detected
[OK] Domain relevance confirmed

[4] Testing Phase 1+2+3+4 integration...
[OK] Hardware detection working
[OK] Intent routing working
[OK] Model management working
[OK] Domain execution working

[SUCCESS] All Phase 4 tests passed!
```

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Domain SLM Load Time | < 10s | First load with INT4 quantization |
| Response Generation | < 5s | For most queries |
| End-to-End Latency | < 7s | Route + Load + Execute |
| Memory Usage | < 4GB | Per domain SLM (INT4) |
| Concurrent Domains | 2-3 | Based on 16GB RAM |

## Integration with Previous Phases

### Phase 1: Hardware Detection
- Informs device placement for domain SLMs
- Determines quantization level based on available memory

### Phase 2: Orchestration
- Uses TinyBERT for fast intent classification
- State machine coordinates domain execution workflow
- MessageBus publishes execution events

### Phase 3: Model Management
- ModelManager loads domain SLMs on-demand
- ModelRegistry tracks loaded domain models
- Automatic LRU eviction when memory constrained

## File Structure

```
mdsa/
├── domains/
│   ├── __init__.py          # Domain exports
│   ├── config.py            # DomainConfig
│   ├── registry.py          # DomainRegistry
│   ├── prompts.py           # PromptBuilder
│   ├── executor.py          # DomainExecutor
│   └── validator.py         # ResponseValidator
├── core/
│   └── orchestrator.py      # Updated with domain execution
└── __init__.py              # Add domain exports

tests/
├── unit/
│   ├── test_domain_config.py
│   ├── test_domain_registry.py
│   ├── test_prompt_builder.py
│   ├── test_domain_executor.py
│   └── test_validator.py
└── integration/
    └── test_phase4_integration.py

manual_test_phase4.py        # Manual testing script
```

## Success Criteria

Phase 4 is complete when:

- [x] All components implemented
- [x] Unit tests passing (>80% coverage)
- [x] Integration tests passing
- [x] Manual test demonstrates end-to-end workflow
- [x] Performance targets met
- [x] Documentation complete
- [x] Example domains working (finance, medical, support)

## Next Steps After Phase 4

After Phase 4 completion, the MDSA framework will be feature-complete with:

1. **Optimization Phase** (Optional):
   - Model fine-tuning for specific domains
   - Response caching
   - Batch processing
   - Advanced prompt engineering

2. **Production Readiness**:
   - API server implementation
   - Monitoring and logging
   - Rate limiting
   - Authentication

3. **Advanced Features**:
   - Multi-turn conversations
   - Context memory
   - Tool/function calling
   - RAG integration

---

**Phase 4 Status**: 🚧 **PLANNING COMPLETE - READY FOR IMPLEMENTATION**
**Estimated Time**: 4-6 hours
**Next Action**: Begin implementation with Step 1 (Domain Configuration)
