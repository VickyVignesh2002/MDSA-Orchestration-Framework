# MDSA Framework User Guide v1.0.2

## Multi-Domain Small Language Model Agentic Orchestration Framework

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Quick Start](#3-quick-start)
4. [Core Components](#4-core-components)
5. [Domain Management](#5-domain-management)
6. [RAG System](#6-rag-system)
7. [Tools Integration](#7-tools-integration)
8. [Dashboard & Monitoring](#8-dashboard--monitoring)
9. [Configuration Guide](#9-configuration-guide)
10. [Examples](#10-examples)
11. [Troubleshooting](#11-troubleshooting)
12. [API Reference](#12-api-reference)

---

## 1. Introduction

### What is MDSA?

MDSA (Multi-Domain Small Language Model Agentic Orchestration) is a production-ready Python framework for orchestrating domain-specialized small language models. It enables you to build intelligent applications that can:

- **Route queries** to specialized domain experts automatically
- **Manage multiple AI models** with efficient resource utilization
- **Integrate RAG** (Retrieval-Augmented Generation) for knowledge-enhanced responses
- **Connect external tools** like APIs and databases
- **Monitor performance** in real-time through a web dashboard

### Key Features

| Feature | Description |
|---------|-------------|
| Smart Routing | TinyBERT-based intent classification (67M params, <50ms) |
| Multi-Domain | Finance, Medical, Technical, Support domains out-of-the-box |
| RAG System | Dual-tier RAG with local and global knowledge stores |
| Tool Integration | Built-in tool registry for external API connections |
| Monitoring | Real-time Flask dashboard with metrics visualization |
| Auto GPU | Automatic GPU/CPU device detection and optimization |

### Architecture Overview

```
User Query
    |
    v
+-------------------+
| TinyBERT Router   |  <- Tier 1: Fast classification (<50ms)
+-------------------+
    |
    v
+-------------------+
| Domain Selection  |  <- Identifies: Finance, Medical, Technical, Support
+-------------------+
    |
    v
+-------------------+
| RAG Enhancement   |  <- Retrieves relevant context from knowledge base
+-------------------+
    |
    v
+-------------------+
| Domain SLM        |  <- Tier 3: Specialized response generation
+-------------------+
    |
    v
Response
```

---

## 2. Installation

### Basic Installation

```bash
pip install mdsa-framework
```

### Full Installation (with RAG support)

```bash
pip install mdsa-framework[rag]
```

### Development Installation

```bash
git clone https://github.com/yourusername/mdsa-framework.git
cd mdsa-framework
pip install -e ".[dev]"
```

### Verify Installation

```python
from mdsa import MDSA, __version__
print(f"MDSA Framework v{__version__} installed successfully!")
```

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.9+ | 3.11+ |
| RAM | 4GB | 16GB+ |
| Disk | 2GB | 10GB+ |
| GPU | Optional | NVIDIA RTX 3050+ |

---

## 3. Quick Start

### Basic Usage (5 minutes)

```python
from mdsa import MDSA

# Initialize the orchestrator
orchestrator = MDSA()

# Process a query
response = orchestrator.process("What are the symptoms of diabetes?")
print(response)
```

### With Domain Configuration

```python
from mdsa import MDSA
from mdsa.domains import create_medical_domain, create_finance_domain

# Create an orchestrator with specific domains
orchestrator = MDSA()

# Add domains
orchestrator.add_domain(create_medical_domain())
orchestrator.add_domain(create_finance_domain())

# Process queries - automatically routed to the right domain
medical_response = orchestrator.process("What is hypertension?")
finance_response = orchestrator.process("How do I calculate compound interest?")
```

### With RAG Enhancement

```python
from mdsa import MDSA, DualRAG

# Initialize RAG system
rag = DualRAG()
rag.register_domain("medical")

# Add knowledge documents
rag.add_to_local(
    domain="medical",
    content="Diabetes is a chronic condition affecting blood sugar levels...",
    metadata={"source": "medical_guide.pdf"}
)

# Create orchestrator with RAG
orchestrator = MDSA(rag=rag)

# Queries now use knowledge base
response = orchestrator.process("What is diabetes?")
```

---

## 4. Core Components

### 4.1 MDSA Orchestrator

The main entry point for the framework.

```python
from mdsa import MDSA

# Basic initialization
orchestrator = MDSA()

# With configuration
orchestrator = MDSA(
    config_path="config.yaml",  # Load from config file
    device="auto",              # Auto-detect GPU/CPU
    enable_monitoring=True      # Enable metrics collection
)

# Process a single query
response = orchestrator.process("Your question here")

# Process multiple queries
responses = orchestrator.process_batch([
    "Question 1",
    "Question 2",
    "Question 3"
])

# Async processing
import asyncio
response = asyncio.run(orchestrator.process_async("Async question"))
```

### 4.2 Intent Router

Routes queries to appropriate domains using TinyBERT.

```python
from mdsa import IntentRouter

# Initialize router
router = IntentRouter()

# Classify a query
domain, confidence = router.classify("What are stock market trends?")
print(f"Domain: {domain}, Confidence: {confidence:.2f}")
# Output: Domain: finance, Confidence: 0.92
```

### 4.3 State Machine

Manages conversation flow and context.

```python
from mdsa import StateMachine, WorkflowState

# Create a state machine
sm = StateMachine()

# Define workflow states
sm.add_state(WorkflowState(
    name="greeting",
    next_states=["query", "help"]
))

sm.add_state(WorkflowState(
    name="query",
    next_states=["response", "clarification"]
))

# Transition between states
sm.transition("greeting", "query")
```

### 4.4 Message Bus

Enables communication between components.

```python
from mdsa import MessageBus

# Create message bus
bus = MessageBus()

# Subscribe to events
def on_query_received(data):
    print(f"Query received: {data}")

bus.subscribe("query_received", on_query_received)

# Publish events
bus.publish("query_received", {"query": "Hello!"})
```

### 4.5 Hardware Detector

Automatically detects available compute resources.

```python
from mdsa import HardwareDetector

# Initialize detector
hw = HardwareDetector()

# Check available resources
print(f"CPU Cores: {hw.cpu_count}")
print(f"Memory: {hw.memory_gb:.1f} GB")
print(f"CUDA Available: {hw.has_cuda}")
print(f"MPS Available: {hw.has_mps}")

# Get recommended device for each tier
tier1_device = hw.best_device_for_tier1()  # Router - usually CPU
tier2_device = hw.best_device_for_tier2()  # Intermediate models
tier3_device = hw.best_device_for_tier3()  # Large domain models
```

---

## 5. Domain Management

### 5.1 Built-in Domains

MDSA includes 4 pre-configured domains:

```python
from mdsa.domains import (
    create_medical_domain,
    create_finance_domain,
    create_support_domain,
    create_technical_domain
)

# Create domain instances
medical = create_medical_domain()
finance = create_finance_domain()
support = create_support_domain()
technical = create_technical_domain()

print(f"Medical domain keywords: {medical.keywords}")
# Output: ['symptom', 'diagnosis', 'treatment', 'medication', ...]
```

### 5.2 Creating Custom Domains

```python
from mdsa import DomainConfig

# Create a custom domain
ecommerce = DomainConfig(
    domain_id="ecommerce",
    name="E-Commerce Support",
    description="Handles product and order queries",
    keywords=[
        "order", "product", "shipping", "return",
        "payment", "cart", "checkout", "delivery"
    ],
    model_name="microsoft/phi-2",  # Or any HuggingFace model
    temperature=0.7,
    max_tokens=512,
    device="auto"  # Auto-detect GPU/CPU
)

# Add to orchestrator
orchestrator.add_domain(ecommerce)
```

### 5.3 Domain Registry

Manage multiple domains centrally.

```python
from mdsa import DomainRegistry

# Create registry
registry = DomainRegistry()

# Register domains
registry.register(create_medical_domain())
registry.register(create_finance_domain())

# Get a domain by ID
medical = registry.get("medical")

# List all domains
for domain in registry.list_domains():
    print(f"- {domain.name}: {domain.description}")
```

### 5.4 Domain Executor

Execute queries within a specific domain.

```python
from mdsa import DomainExecutor
from mdsa.domains import create_medical_domain

# Create executor for medical domain
executor = DomainExecutor(create_medical_domain())

# Execute a query
response = executor.execute("What causes high blood pressure?")
print(response)
```

---

## 6. RAG System

### 6.1 Dual RAG Architecture

MDSA uses a dual-tier RAG system:

- **Local RAG**: Domain-specific knowledge (fast, focused)
- **Global RAG**: Cross-domain knowledge (comprehensive)

```python
from mdsa import DualRAG

# Initialize
rag = DualRAG()

# Register domains
rag.register_domain("medical")
rag.register_domain("finance")
```

### 6.2 Adding Documents

```python
# Add to domain-specific (local) knowledge
rag.add_to_local(
    domain="medical",
    content="Hypertension, or high blood pressure, is a condition...",
    metadata={
        "source": "medical_handbook.pdf",
        "chapter": "Cardiovascular Diseases",
        "page": 45
    }
)

# Add to global knowledge (accessible by all domains)
rag.add_to_global(
    content="Health insurance typically covers preventive care...",
    tags=["insurance", "healthcare", "coverage"]
)
```

### 6.3 Retrieving Context

```python
# Search within a specific domain
results = rag.search(
    query="blood pressure symptoms",
    domain="medical",
    top_k=5,
    include_global=True  # Also search global knowledge
)

for result in results:
    print(f"Score: {result.score:.2f}")
    print(f"Content: {result.content[:100]}...")
    print(f"Source: {result.metadata.get('source', 'Unknown')}")
    print("---")
```

### 6.4 Local RAG (Standalone)

```python
from mdsa.rag import LocalRAG

# Create local RAG for a single domain
local_rag = LocalRAG(max_documents=1000)

# Add documents
local_rag.add_document(
    doc_id="doc_001",
    content="Document content here...",
    metadata={"type": "article"}
)

# Retrieve
results = local_rag.retrieve("search query", top_k=3)
```

### 6.5 Global RAG (Standalone)

```python
from mdsa.rag import GlobalRAG

# Create global RAG
global_rag = GlobalRAG()

# Add with tags
global_rag.add_document(
    content="Cross-domain content...",
    tags=["general", "faq"]
)

# Retrieve
results = global_rag.retrieve("query", top_k=5)
```

---

## 7. Tools Integration

### 7.1 Built-in Tool System

```python
from mdsa import Tool, ToolResult, ToolRegistry

# Create a custom tool
class WeatherTool(Tool):
    name = "weather"
    description = "Get current weather for a location"

    def execute(self, location: str) -> ToolResult:
        # Your API call logic here
        weather_data = {"temp": 72, "condition": "sunny"}
        return ToolResult(
            success=True,
            data=weather_data,
            message=f"Weather in {location}: {weather_data}"
        )

# Register the tool
registry = ToolRegistry()
registry.register(WeatherTool())

# Use the tool
result = registry.execute("weather", location="New York")
print(result.data)
```

### 7.2 Tool Manager for External APIs

```python
from mdsa import ToolManager

# Create tool manager
manager = ToolManager()

# Add an API integration
manager.add_tool(
    name="stock_api",
    api_url="https://api.example.com/stocks",
    api_key="your_api_key",  # Encrypted automatically
    headers={"Content-Type": "application/json"}
)

# Execute API call
result = manager.execute(
    tool_name="stock_api",
    endpoint="/quote",
    params={"symbol": "AAPL"}
)
```

### 7.3 Smart Tool Executor

Automatically selects and executes appropriate tools.

```python
from mdsa import SmartToolExecutor

# Initialize with registry
executor = SmartToolExecutor(registry)

# Let the executor decide which tool to use
result = executor.execute(
    query="What's the weather in Tokyo?",
    context={"user_location": "Japan"}
)
```

---

## 8. Dashboard & Monitoring

### 8.1 Starting the Dashboard

```python
from mdsa.ui.dashboard import DashboardServer

# Create and start dashboard
dashboard = DashboardServer(
    host="127.0.0.1",
    port=5000,
    debug=False
)

# Start in background
dashboard.start()

# Access at http://127.0.0.1:5000
print("Dashboard running at http://127.0.0.1:5000")
```

### 8.2 Dashboard Features

| Feature | Description |
|---------|-------------|
| Real-time Metrics | View request counts, latency, error rates |
| Domain Statistics | Per-domain performance breakdown |
| Request Timeline | Visualize request flow over time |
| System Health | CPU, memory, GPU utilization |
| Authentication | Built-in user authentication |

### 8.3 Monitoring Service

```python
from mdsa import MonitoringService, RequestMetric

# Initialize monitoring
monitor = MonitoringService()

# Track a request manually
metric = RequestMetric(
    domain="medical",
    latency_ms=45.2,
    success=True,
    tokens_used=256
)
monitor.record(metric)

# Get statistics
stats = monitor.get_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Average latency: {stats['avg_latency_ms']:.1f}ms")
print(f"Success rate: {stats['success_rate']:.1%}")
```

### 8.4 Dashboard Authentication

```python
from mdsa.ui.dashboard import DashboardServer

# Create dashboard with authentication
dashboard = DashboardServer(
    host="0.0.0.0",  # Allow external access
    port=5000
)

# Users are managed through environment variables:
# MDSA_ADMIN_PASSWORD=your_secure_password
# MDSA_JWT_SECRET=your_jwt_secret
```

---

## 9. Configuration Guide

### 9.1 YAML Configuration

Create a `config.yaml` file:

```yaml
# MDSA Framework Configuration

orchestrator:
  name: "My MDSA Application"
  version: "1.0.0"
  device: "auto"
  enable_monitoring: true

domains:
  - id: "medical"
    name: "Medical Information"
    model: "microsoft/phi-2"
    temperature: 0.7
    max_tokens: 512

  - id: "finance"
    name: "Financial Services"
    model: "microsoft/phi-2"
    temperature: 0.5
    max_tokens: 1024

rag:
  enabled: true
  local_max_documents: 10000
  global_max_documents: 50000
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"

monitoring:
  enabled: true
  dashboard_port: 5000
  log_level: "INFO"
```

### 9.2 Loading Configuration

```python
from mdsa import MDSA, ConfigLoader

# Load from YAML
config = ConfigLoader.load("config.yaml")

# Create orchestrator with config
orchestrator = MDSA(config=config)
```

### 9.3 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MDSA_DEVICE` | Default device (cpu/cuda/auto) | auto |
| `MDSA_LOG_LEVEL` | Logging level | INFO |
| `MDSA_ADMIN_PASSWORD` | Dashboard admin password | Required |
| `MDSA_JWT_SECRET` | JWT signing secret | Required |
| `MDSA_ENCRYPTION_KEY` | API key encryption | Generated |

```bash
# Set environment variables
export MDSA_DEVICE=cuda
export MDSA_LOG_LEVEL=DEBUG
export MDSA_ADMIN_PASSWORD=your_password
```

---

## 10. Examples

### 10.1 Medical Chatbot

```python
from mdsa import MDSA, DualRAG
from mdsa.domains import create_medical_domain

# Initialize RAG with medical knowledge
rag = DualRAG()
rag.register_domain("medical")

# Add medical knowledge
rag.add_to_local(
    domain="medical",
    content="""
    Diabetes mellitus is a group of metabolic disorders characterized
    by high blood sugar levels over a prolonged period. Symptoms include
    frequent urination, increased thirst, and unexplained weight loss.
    """,
    metadata={"source": "medical_textbook", "chapter": "Endocrinology"}
)

# Create orchestrator
orchestrator = MDSA(rag=rag)
orchestrator.add_domain(create_medical_domain())

# Interactive chat
print("Medical Assistant Ready! Type 'quit' to exit.")
while True:
    query = input("\nYou: ")
    if query.lower() == 'quit':
        break
    response = orchestrator.process(query)
    print(f"\nAssistant: {response}")
```

### 10.2 Finance Assistant with Tools

```python
from mdsa import MDSA, ToolRegistry, Tool, ToolResult
from mdsa.domains import create_finance_domain

# Create a stock price tool
class StockPriceTool(Tool):
    name = "stock_price"
    description = "Get real-time stock price"

    def execute(self, symbol: str) -> ToolResult:
        # Mock data - replace with real API
        prices = {"AAPL": 178.50, "GOOGL": 140.25, "MSFT": 378.90}
        price = prices.get(symbol.upper(), None)
        if price:
            return ToolResult(True, {"symbol": symbol, "price": price})
        return ToolResult(False, message=f"Symbol {symbol} not found")

# Setup
registry = ToolRegistry()
registry.register(StockPriceTool())

orchestrator = MDSA(tools=registry)
orchestrator.add_domain(create_finance_domain())

# Query with tool execution
response = orchestrator.process(
    "What is Apple's stock price?",
    use_tools=True
)
print(response)
```

### 10.3 Multi-Domain Customer Support

```python
from mdsa import MDSA, DualRAG
from mdsa.domains import (
    create_support_domain,
    create_technical_domain
)

# Setup RAG for FAQ
rag = DualRAG()
rag.register_domain("support")
rag.register_domain("technical")

# Add FAQ content
rag.add_to_global(
    content="Returns must be initiated within 30 days of purchase.",
    tags=["returns", "policy"]
)

rag.add_to_local(
    domain="technical",
    content="To reset your password, click 'Forgot Password' on the login page.",
    metadata={"category": "account"}
)

# Create multi-domain orchestrator
orchestrator = MDSA(rag=rag)
orchestrator.add_domain(create_support_domain())
orchestrator.add_domain(create_technical_domain())

# Process various queries
queries = [
    "How do I return a product?",     # -> Support domain
    "Reset my password please",        # -> Technical domain
    "My order hasn't arrived",         # -> Support domain
    "App keeps crashing on startup"    # -> Technical domain
]

for query in queries:
    response = orchestrator.process(query)
    print(f"Q: {query}")
    print(f"A: {response}\n")
```

---

## 11. Troubleshooting

### 11.1 Common Issues

#### Issue: "CUDA not available"

**Symptoms**: GPU not being used, slow performance

**Solution**:
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify CUDA installation
python -c "import torch; print(torch.cuda.is_available())"
```

#### Issue: "Module not found: chromadb"

**Symptoms**: RAG features not working

**Solution**:
```bash
# Install RAG dependencies
pip install chromadb sentence-transformers
```

#### Issue: "Dashboard not loading"

**Symptoms**: Cannot access web dashboard

**Solution**:
```python
# Check if Flask is installed
pip install flask flask-login flask-limiter

# Verify dashboard can start
from mdsa.ui.dashboard import DashboardServer
dashboard = DashboardServer(port=5000)
dashboard.start()
```

#### Issue: "Out of memory"

**Symptoms**: OOM errors when loading models

**Solution**:
```python
from mdsa import MDSA

# Force CPU to reduce memory usage
orchestrator = MDSA(device="cpu")

# Or use quantization
from mdsa.models import ModelConfig, QuantizationType
config = ModelConfig(
    model_name="microsoft/phi-2",
    tier="tier3",
    quantization=QuantizationType.INT8  # Reduce memory by ~4x
)
```

### 11.2 Debugging

Enable debug logging:

```python
from mdsa import setup_logger
import logging

# Set debug level
setup_logger(level=logging.DEBUG)
```

### 11.3 Performance Tips

1. **Use GPU when available**: Set `device="auto"` to auto-detect
2. **Enable caching**: Use `use_cache=True` in model configs
3. **Batch requests**: Process multiple queries together
4. **Quantize models**: Use INT8/INT4 for lower memory
5. **Optimize RAG**: Limit `top_k` to reduce retrieval time

---

## 12. API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `MDSA` | Main orchestrator class |
| `IntentRouter` | Query classification |
| `StateMachine` | Conversation flow management |
| `MessageBus` | Event communication |
| `HardwareDetector` | Device detection |

### Domain Classes

| Class | Description |
|-------|-------------|
| `DomainConfig` | Domain configuration |
| `DomainRegistry` | Domain management |
| `DomainExecutor` | Query execution |
| `PromptBuilder` | Prompt construction |
| `ResponseValidator` | Response validation |

### RAG Classes

| Class | Description |
|-------|-------------|
| `DualRAG` | Dual-tier RAG system |
| `LocalRAG` | Domain-specific RAG |
| `GlobalRAG` | Cross-domain RAG |
| `RAGDocument` | Document structure |
| `RAGResult` | Retrieval result |

### Tool Classes

| Class | Description |
|-------|-------------|
| `Tool` | Base tool class |
| `ToolResult` | Tool execution result |
| `ToolRegistry` | Tool management |
| `ToolManager` | External API management |
| `SmartToolExecutor` | Auto tool selection |

### Monitoring Classes

| Class | Description |
|-------|-------------|
| `MonitoringService` | Metrics collection |
| `RequestMetric` | Request metrics |
| `DashboardServer` | Web dashboard |

---

## Getting Help

- **Documentation**: [https://mdsa-framework.readthedocs.io](https://mdsa-framework.readthedocs.io)
- **GitHub Issues**: [https://github.com/mdsa-framework/mdsa/issues](https://github.com/mdsa-framework/mdsa/issues)
- **Examples**: See `examples/` directory in the repository

---

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

---

*MDSA Framework v1.0.2 - Built with precision for production AI applications*
