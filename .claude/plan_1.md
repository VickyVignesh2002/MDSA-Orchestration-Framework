# MDSA Framework - Product Requirements Document & Implementation Guide

## Executive Summary

MDSA (Multi-Domain Small Language Model Agentic Orchestration) is a production-grade Python framework for building cost-efficient enterprise AI systems. It uses a three-tier architecture with tiny orchestration models, lightweight validation reasoning, and domain-specialized SLMs with selective activation.

## 1. Updated Architecture Plan

```yaml
Framework Name: MDSA (pip install mdsa-framework)
Version: 1.0.0
License: Apache 2.0

Three-Tier Architecture:

Tier 1 - Orchestration Core (Bundled):
  Model: TinyBERT-6L (pre-downloaded with framework)
  Size: 67M parameters
  Memory: 250MB
  Role: Intent routing, classification, state management
  Hardware: CPU (x86_64, ARM64, Apple Silicon supported)
  Bundled: Yes (downloads on pip install)

Tier 2 - Validation & Reasoning:
  Model A: Pure Python Rules (bundled)
    Size: 0 parameters
    Memory: <10MB
    Role: Deterministic validation, schema checking
  
  Model B: Phi-1.5 or StableLM-2-1.6B (optional, auto-download)
    Size: 1.3-1.6B parameters  
    Memory: 2-3GB
    Role: Complex validation reasoning, edge case handling
    Hardware: CPU with 4GB RAM or basic GPU
    Auto-download: On first use

Tier 3 - Domain SLMs (User Configured):
  Models: Any 7-13B model (Llama, Qwen, Mistral, etc.)
  Memory: 8-15GB (only when active)
  Role: Domain expertise and reasoning
  Hardware: GPU required (or CPU with 16GB+ RAM)
  User Provides: Model paths or HuggingFace IDs
```

## 2. Complete PRD & Implementation Blueprint

### 2.1 Framework Features

```python
"""
MDSA Framework Features:
- Plug-and-play domain creation
- Dynamic SLM loading/unloading
- MCP (Model Context Protocol) support
- API key management
- Multi-backend support (HuggingFace, Ollama, OpenAI, local)
- CPU/GPU automatic detection
- Distributed deployment ready
"""
```

### 2.2 Project Structure

```
mdsa-framework/
├── mdsa/
│   ├── __init__.py
│   ├── core/
│   │   ├── orchestrator.py       # TinyBERT orchestration
│   │   ├── state_machine.py      # Workflow management
│   │   └── router.py             # Intent classification
│   ├── validation/
│   │   ├── rules.py              # Deterministic validation
│   │   ├── reasoning.py          # Phi-1.5 reasoning validator
│   │   └── schemas.py            # JSON schemas
│   ├── domains/
│   │   ├── base.py               # BaseDomain class
│   │   ├── registry.py           # Domain registration
│   │   └── examples/             # Pre-built domains
│   ├── integrations/
│   │   ├── mcp.py                # Model Context Protocol
│   │   ├── api_manager.py        # API key management
│   │   ├── huggingface.py        # HF integration
│   │   └── ollama.py             # Ollama integration
│   ├── models/
│   │   ├── tiny_bert/            # Bundled TinyBERT
│   │   └── downloader.py         # Model auto-download
│   └── utils/
│       ├── hardware.py           # CPU/GPU detection
│       └── monitoring.py         # Metrics and logging
├── configs/
│   └── default_config.yaml
├── examples/
│   ├── quickstart.py
│   └── enterprise_demo.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

### 2.3 Core Implementation Code

```python
# mdsa/__init__.py
"""
MDSA - Multi-Domain Small Language Model Agentic Orchestration Framework
A production-grade framework for efficient enterprise AI systems
"""

from mdsa.core import MDSAFramework
from mdsa.domains import Domain, DomainRegistry
from mdsa.validation import Validator, ReasoningValidator

__version__ = "1.0.0"

class MDSA:
    """Main framework entry point"""
  
    def __init__(self, config_path=None):
        """
        Initialize MDSA Framework
      
        Args:
            config_path: Path to YAML config (optional)
        """
        self.config = self._load_config(config_path)
        self._initialize_components()
  
    def _initialize_components(self):
        # Auto-detect hardware
        self.hardware = HardwareDetector()
      
        # Initialize orchestrator with bundled TinyBERT
        self.orchestrator = TinyBERTOrchestrator(
            model_path="mdsa/models/tiny_bert",
            device=self.hardware.best_device_for_tier1()
        )
      
        # Initialize validation
        self.validator = ValidationPipeline(
            use_reasoning=self.config.get('enable_reasoning_validation', True)
        )
      
        # Initialize domain registry
        self.domains = DomainRegistry()
      
        # Initialize integrations
        self.mcp = MCPManager()
        self.api_manager = APIKeyManager()

# mdsa/core/orchestrator.py
import torch
from transformers import AutoModel, AutoTokenizer
from typing import Dict, Any, Tuple, Optional
import json

class TinyBERTOrchestrator:
    """
    Lightweight orchestrator using TinyBERT
    Runs on CPU, handles routing and state management
    """
  
    def __init__(self, model_path: str = None, device: str = "cpu"):
        """
        Initialize TinyBERT orchestrator
      
        Args:
            model_path: Path to TinyBERT model (uses bundled if None)
            device: Device to run on (cpu/cuda/mps)
        """
        if model_path is None:
            model_path = self._download_bundled_model()
      
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path).to(device)
        self.model.eval()
      
        # State machine for workflow
        self.state_machine = WorkflowStateMachine()
      
        # Domain router
        self.router = IntentRouter(self.model, self.tokenizer)
      
        # Active domain tracking
        self.active_domain = None
        self.active_slm = None
      
    def process_request(self, query: str, context: Dict = None) -> Dict[str, Any]:
        """
        Main orchestration pipeline
      
        Args:
            query: User query
            context: Optional context
          
        Returns:
            Response dictionary
        """
        # Step 1: Route query to domain
        domain, confidence = self.router.classify(query)
      
        if confidence < 0.85:
            return self._escalate_to_human(query, confidence)
      
        # Step 2: State machine workflow
        workflow = self.state_machine.create_workflow(domain, query)
      
        # Step 3: Execute workflow
        result = self._execute_workflow(workflow, query, context)
      
        return result
  
    def _execute_workflow(self, workflow, query, context):
        """Execute workflow with selective SLM activation"""
      
        for step in workflow.steps:
            if step.type == "LOAD_SLM":
                self._activate_domain_slm(step.domain)
          
            elif step.type == "VALIDATE":
                if not self.validator.validate(step.data):
                    return {"error": f"Validation failed: {step.name}"}
          
            elif step.type == "EXECUTE":
                result = self.active_slm.process(query, context)
          
            elif step.type == "UNLOAD_SLM":
                self._deactivate_slm()
      
        return result

# mdsa/domains/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import yaml

class Domain(ABC):
    """Base class for all domains"""
  
    def __init__(self, name: str, config: Dict):
        """
        Initialize domain
      
        Args:
            name: Domain name
            config: Domain configuration
        """
        self.name = name
        self.config = config
        self.slm_model = None
        self.tools = []
        self.validators = []
      
    @abstractmethod
    def initialize_slm(self):
        """Initialize domain-specific SLM"""
        pass
  
    @abstractmethod
    def process(self, query: str, context: Dict = None) -> Dict:
        """Process query in this domain"""
        pass
  
    def add_tool(self, tool):
        """Add tool to domain"""
        self.tools.append(tool)
  
    def add_validator(self, validator):
        """Add validator to domain"""
        self.validators.append(validator)

class DomainBuilder:
    """Builder for creating domains dynamically"""
  
    @staticmethod
    def from_config(config_path: str) -> Domain:
        """
        Create domain from YAML config
      
        Example config:
        ```yaml
        name: finance
        slm:
          model: "meta-llama/Llama-2-7b-hf"
          adapter: "finance-lora-adapter"
        tools:
          - name: "get_budget"
            endpoint: "http://api/budget"
        validators:
          - type: "schema"
            schema_path: "schemas/finance.json"
        ```
        """
        with open(config_path) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
      
        domain = CustomDomain(config['name'], config)
      
        # Configure SLM
        if 'slm' in config:
            domain.set_slm(config['slm'])
      
        # Add tools
        for tool_config in config.get('tools', []):
            domain.add_tool(Tool.from_config(tool_config))
      
        # Add validators  
        for val_config in config.get('validators', []):
            domain.add_validator(Validator.from_config(val_config))
      
        return domain

# mdsa/validation/reasoning.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ReasoningValidator:
    """
    Lightweight reasoning validator using Phi-1.5 or similar
    Handles complex validation that rules can't cover
    """
  
    def __init__(self, model_name: str = "microsoft/phi-1_5"):
        """
        Initialize reasoning validator
      
        Args:
            model_name: Model to use (Phi-1.5 default)
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
      
        # Auto-download on first use
        print(f"Loading reasoning validator: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )
      
    def validate_complex(self, query: str, response: Dict, rules: List[str]) -> Tuple[bool, str]:
        """
        Validate complex business logic using reasoning
      
        Args:
            query: Original query
            response: SLM response
            rules: Business rules to check
          
        Returns:
            (is_valid, reasoning)
        """
        prompt = self._build_validation_prompt(query, response, rules)
      
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
      
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=200,
                temperature=0.1,  # Low temperature for deterministic validation
                do_sample=False
            )
      
        reasoning = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
      
        # Parse validation result
        is_valid = "VALID" in reasoning.upper()
      
        return is_valid, reasoning

# mdsa/integrations/mcp.py
from typing import Dict, Any, List
import json
import aiohttp

class MCPManager:
    """
    Model Context Protocol (MCP) integration
    Enables tool usage across domains
    """
  
    def __init__(self):
        self.servers = {}
        self.tools = {}
  
    async def connect_server(self, name: str, url: str, api_key: str = None):
        """
        Connect to MCP server
      
        Args:
            name: Server name
            url: Server URL
            api_key: Optional API key
        """
        self.servers[name] = {
            "url": url,
            "api_key": api_key,
            "session": aiohttp.ClientSession()
        }
      
        # Discover available tools
        tools = await self._discover_tools(name)
        self.tools[name] = tools
  
    async def call_tool(self, server: str, tool: str, params: Dict) -> Any:
        """
        Call tool via MCP
      
        Args:
            server: Server name
            tool: Tool name
            params: Tool parameters
          
        Returns:
            Tool response
        """
        server_info = self.servers[server]
      
        headers = {"Content-Type": "application/json"}
        if server_info["api_key"]:
            headers["Authorization"] = f"Bearer {server_info['api_key']}"
      
        async with server_info["session"].post(
            f"{server_info['url']}/tools/{tool}",
            headers=headers,
            json=params
        ) as response:
            return await response.json()

# mdsa/integrations/api_manager.py
import os
from typing import Dict, Optional
from cryptography.fernet import Fernet

class APIKeyManager:
    """
    Secure API key management
    """
  
    def __init__(self, key_file: str = ".mdsa_keys"):
        """
        Initialize API key manager
      
        Args:
            key_file: Path to encrypted key file
        """
        self.key_file = key_file
        self.cipher = self._get_cipher()
        self.keys = self._load_keys()
  
    def add_key(self, service: str, key: str):
        """Add API key for service"""
        encrypted = self.cipher.encrypt(key.encode())
        self.keys[service] = encrypted
        self._save_keys()
  
    def get_key(self, service: str) -> Optional[str]:
        """Get decrypted API key"""
        if service not in self.keys:
            # Check environment variables
            env_key = f"{service.upper()}_API_KEY"
            return os.environ.get(env_key)
      
        encrypted = self.keys[service]
        return self.cipher.decrypt(encrypted).decode()
```

### 2.4 Configuration System

```yaml
# configs/default_config.yaml
framework:
  name: "MDSA Framework"
  version: "1.0.0"
  
orchestrator:
  model: "bundled:tinybert-6l"  # Uses bundled model
  device: "auto"  # auto, cpu, cuda, mps
  confidence_threshold: 0.85
  
validation:
  enable_rules: true
  enable_reasoning: true
  reasoning_model: "microsoft/phi-1_5"  # Auto-downloads
  reasoning_device: "auto"
  
domains:
  registry_path: "~/.mdsa/domains"
  auto_discover: true
  
  # Example domain configs
  finance:
    slm:
      provider: "huggingface"  # huggingface, ollama, openai, local
      model: "meta-llama/Llama-2-7b-hf"
      quantization: "8bit"  # Optional: 4bit, 8bit, none
    tools:
      - name: "budget_check"
        type: "mcp"
        server: "finance_server"
    validators:
      - type: "schema"
        path: "schemas/finance.json"
      - type: "rules"
        rules:
          - "amount <= available_budget"
          - "user.role in ['manager', 'admin']"
  
  development:
    slm:
      provider: "ollama"
      model: "codellama:7b"
    tools:
      - name: "github"
        type: "api"
        endpoint: "https://api.github.com"
      
integrations:
  mcp:
    servers:
      - name: "finance_server"
        url: "http://localhost:8000"
      - name: "dev_server"
        url: "http://localhost:8001"
  
  api_keys:
    openai: "${OPENAI_API_KEY}"
    anthropic: "${ANTHROPIC_API_KEY}"
    github: "${GITHUB_TOKEN}"
  
monitoring:
  metrics: true
  logging: true
  log_level: "INFO"
  metrics_port: 9090
```

### 2.5 Usage Examples

```python
# examples/quickstart.py
from mdsa import MDSA

# Initialize framework
mdsa = MDSA("config.yaml")

# Register a domain dynamically
mdsa.register_domain({
    "name": "customer_service",
    "slm": {
        "provider": "huggingface",
        "model": "microsoft/DialoGPT-medium"
    },
    "tools": [
        {"name": "ticket_system", "type": "api", "url": "http://tickets.api"}
    ]
})

# Process request
response = mdsa.process(
    "Check the status of ticket #1234",
    context={"user_id": "usr_123", "role": "support"}
)

print(response)

# examples/enterprise_demo.py
from mdsa import MDSA, Domain, Tool, Validator

class FinanceDomain(Domain):
    """Custom finance domain implementation"""
  
    def initialize_slm(self):
        """Initialize finance-specific SLM"""
        from transformers import AutoModelForCausalLM
      
        self.slm_model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-7b-hf",
            load_in_8bit=True,
            device_map="auto"
        )
      
        # Load LoRA adapter if available
        if self.config.get("lora_adapter"):
            from peft import PeftModel
            self.slm_model = PeftModel.from_pretrained(
                self.slm_model,
                self.config["lora_adapter"]
            )
  
    def process(self, query: str, context: Dict = None) -> Dict:
        """Process finance query"""
        # Pre-validation
        for validator in self.validators:
            if not validator.validate(query, context):
                return {"error": "Validation failed"}
      
        # Tool execution
        if self._needs_tool(query):
            tool_result = self._execute_tool(query)
            context = {**context, "tool_result": tool_result}
      
        # SLM processing
        response = self.slm_model.generate(
            self._build_prompt(query, context),
            max_length=200,
            temperature=0.7
        )
      
        # Post-validation
        if not self._validate_response(response):
            return {"error": "Response validation failed"}
      
        return {"response": response, "domain": "finance"}

# Initialize and use
mdsa = MDSA()

# Register custom domain
finance_domain = FinanceDomain("finance", {
    "slm": {"model": "llama-2-7b"},
    "lora_adapter": "path/to/finance/adapter"
})

mdsa.register_domain(finance_domain)

# Add MCP integration
await mdsa.mcp.connect_server(
    "finance_tools",
    "http://localhost:8000",
    api_key="secret_key"
)

# Process with MCP tools
response = await mdsa.process_async(
    "Transfer $5000 from account A to account B",
    use_tools=True
)
```

## 3. Complete Implementation Prompt for Claude Code

```markdown
# Build MDSA Framework - Production Grade Python Implementation

Create a complete production-ready Python framework called MDSA (Multi-Domain Small Language Model Agentic Orchestration) with the following specifications:

## Framework Structure
Create a pip-installable package with this structure:
- mdsa/ (main package)
  - core/ (orchestration, routing, state management)  
  - validation/ (rules and reasoning validators)
  - domains/ (domain management and registry)
  - integrations/ (MCP, API keys, HuggingFace, Ollama)
  - models/ (bundled TinyBERT and model management)
  - utils/ (hardware detection, monitoring)

## Core Requirements

### 1. Orchestrator Module (mdsa/core/orchestrator.py)
- Implement TinyBERTOrchestrator class that:
  - Auto-downloads TinyBERT-6L on first use (67M parameters)
  - Runs on CPU (supports x86_64, ARM64, Apple Silicon)
  - Provides intent classification with 95%+ accuracy
  - Manages state machine workflow (INIT → CLASSIFY → LOAD_SLM → VALIDATE → EXECUTE → UNLOAD_SLM → RETURN)
  - Implements selective SLM activation (only loads needed domain model)
  - Tracks active domains and automatic cleanup

### 2. Validation System (mdsa/validation/)
Create two-tier validation:

**Rule-based Validator (rules.py):**
- JSON schema validation
- Business rule checking (preconditions/postconditions)
- Pure Python, no ML required

**Reasoning Validator (reasoning.py):**
- Use Phi-1.5 (1.3B params) or StableLM-2-1.6B
- Auto-download on first use
- Handle complex validation logic
- Run on CPU with 4GB RAM or basic GPU

### 3. Domain Management (mdsa/domains/)
**Base Domain Class (base.py):**
- Abstract base class with initialize_slm() and process() methods
- Support for tools and validators
- Configuration via YAML

**Domain Registry (registry.py):**
- Dynamic domain registration
- Domain discovery from configs
- Plug-and-play domain addition
- Support any 7-13B model (Llama, Qwen, Mistral, etc.)

**Domain Builder:**
- Create domains from YAML configs
- Support multiple SLM providers (HuggingFace, Ollama, OpenAI, local)
- Handle LoRA/QLoRA adapters

### 4. Integrations (mdsa/integrations/)

**MCP Manager (mcp.py):**
- Async MCP server connections
- Tool discovery and execution
- Support multiple MCP servers

**API Key Manager (api_manager.py):**
- Secure encrypted storage
- Environment variable fallback
- Support for multiple services

**Model Providers:**
- HuggingFace integration with transformers library
- Ollama integration via REST API
- OpenAI API compatibility
- Local model loading

### 5. Hardware Management (mdsa/utils/hardware.py)
```python
class HardwareDetector:
    - Detect available devices (CPU, CUDA, MPS, ROCm)
    - Automatic device selection based on tier
    - Memory availability checking
    - Optimization recommendations
```

### 6. Monitoring (mdsa/utils/monitoring.py)

* Request latency tracking
* Memory usage monitoring
* Token usage counting
* Error rate tracking
* Prometheus metrics export

## Configuration System

Implement YAML-based configuration with:

* Framework settings
* Orchestrator configuration
* Domain definitions
* Integration settings
* API key management
* Monitoring preferences

## Key Features to Implement

1. **Auto-download Models:**
   * Bundle TinyBERT with package
   * Auto-download Phi-1.5 for reasoning on first use
   * Cache models in ~/.mdsa/models/
2. **Dynamic Domain Creation:**

```python
mdsa.register_domain({
    "name": "custom_domain",
    "slm": {"provider": "huggingface", "model": "any-7b-model"},
    "tools": [...],
    "validators": [...]
})
```

3. **Selective Activation:**
   * Load only active domain SLM
   * Automatic unloading after use
   * Memory-efficient operation
4. **Multi-Backend Support:**
   * HuggingFace Transformers
   * Ollama local server
   * OpenAI API
   * Custom model endpoints
5. **Production Features:**
   * Async/await support
   * Thread safety
   * Connection pooling
   * Retry logic
   * Circuit breakers
   * Rate limiting

## Testing Requirements

Create comprehensive tests:

* Unit tests for each module
* Integration tests for workflows
* Performance benchmarks
* Mock SLM responses for testing

## Documentation

Include:

* README with quickstart
* API documentation (docstrings)
* Configuration examples
* Domain creation guide
* MCP integration guide

## Performance Targets

* Orchestrator: <50ms latency on CPU
* Validation: <100ms with reasoning
* Domain SLM: <500ms on GPU
* Memory: <500MB idle, <16GB active
* Accuracy: 94%+ routing, 90%+ domain processing

## Error Handling

* Graceful degradation
* Comprehensive error messages
* Fallback mechanisms
* Human escalation when confidence low

## Deployment Support

* Docker support with Dockerfile
* Kubernetes manifests
* Environment-based configuration
* Health checks and readiness probes

## Example Usage Files

Create working examples:

1. quickstart.py - Basic usage
2. enterprise_demo.py - Advanced features
3. custom_domain.py - Domain creation
4. mcp_integration.py - MCP usage

## Package Metadata (setup.py)

```python
setup(
    name="mdsa-framework",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "peft>=0.4.0",
        "pyyaml>=6.0",
        "fastapi>=0.100.0",
        "prometheus-client>=0.17.0",
        "cryptography>=41.0.0",
        "aiohttp>=3.8.0"
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
        "gpu": ["accelerate", "bitsandbytes"]
    }
)
```

Build this as a production-ready framework that can be deployed in enterprise environments. Focus on:

* Clean, maintainable code
* Comprehensive error handling
* Performance optimization
* Security best practices
* Extensive documentation
* Easy configuration
* Plug-and-play architecture

The framework should work out-of-the-box with minimal configuration while allowing advanced customization for enterprise users.

```

## Summary

This PRD provides:

1. **Complete Architecture**: Three-tier system with tiny orchestration, lightweight validation reasoning, and domain SLMs
2. **Production Features**: Dynamic domains, MCP support, API management, multi-backend support
3. **Hardware Flexibility**: Runs on any CPU for orchestration, optional GPU for domain SLMs
4. **Easy Integration**: Plug-and-play domains, YAML configs, auto-downloading models
5. **Enterprise Ready**: Security, monitoring, error handling, deployment support

The framework bundles TinyBERT for orchestration (250MB), optionally uses Phi-1.5 for reasoning validation (2GB), and supports any 7-13B model for domains. It's designed to be pip-installable and work immediately with minimal configuration while supporting advanced enterprise customization.
```
