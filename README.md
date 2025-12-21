# MDSA Framework

**Multi-Domain Small Language Model Agentic Orchestration Framework**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **✅ Development Status**: Phases 1-5 Complete! Core framework is production-ready with monitoring and logging.

## 🎯 Overview

MDSA is a production-ready Python framework for orchestrating domain-specialized small language models (SLMs). It provides cost-efficient AI system architecture with autonomous agent behavior across specialized domains.

### Key Features ✅ IMPLEMENTED

- **🚀 Beginner-Friendly**: Create domains with just 3 lines of code
- **⚡ Ultra-Fast Routing**: <50ms intent classification using TinyBERT (67M params)
- **💾 Memory Efficient**: Selective model activation with LRU cache
- **🔌 ANY HuggingFace Model**: Use 35,000+ models - zero hardcoding!
- **📊 Real-Time Monitoring**: Request logging, metrics collection, performance tracking
- **🎯 Multi-Domain Support**: Finance, medical, support, technical + custom domains
- **⚙️ Quantization Ready**: INT4/INT8/FP16 for memory efficiency
- **🌐 Production-Ready**: Comprehensive error handling, metrics, and logging

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Application                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Tier 1: Orchestration (TinyBERT 67M - CPU)                  │
│  • Intent Router: <50ms classification                        │
│  • State Machine: Workflow control                            │
│  • Selective Activation: Load only active domains             │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Tier 2: Validation (Phi-1.5 1.3B - Optional)                │
│  • Schema Validation (Pure Python)                            │
│  • Rule-Based Validation                                      │
│  • Reasoning Validation (Complex logic)                       │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Tier 3: Domain SLMs (7-13B - GPU/CPU)                       │
│  • Finance Domain    • Dev Domain    • Support Domain         │
│  • Each with independent RAG and tools                        │
└───────────────────────────────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- For GPU support: CUDA 11.8+ or ROCm 5.4+
- For domain SLMs: 8GB+ GPU VRAM or 32GB+ system RAM

### Install from PyPI (Coming Soon)

```bash
pip install mdsa-framework
```

### Install from Source (Current)

```bash
git clone https://github.com/your-org/mdsa-framework.git
cd mdsa-framework/version_1
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Verify Installation

```bash
# Show welcome page
python -m mdsa
```

### Basic Usage ✅ WORKING NOW

```python
from mdsa import ModelManager, DomainExecutor
from mdsa.domains import create_finance_domain

# Initialize (3 lines!)
manager = ModelManager()
executor = DomainExecutor(manager)
finance = create_finance_domain()

# Process query
result = executor.execute("What's my account balance?", finance)
print(result['response'])
print(f"Latency: {result['latency_ms']:.1f}ms")
print(f"Confidence: {result['confidence']:.2f}")
```

### Use ANY HuggingFace Model ✅ WORKING NOW

```python
from mdsa import DomainConfig

# Use Microsoft Phi-2
phi_domain = DomainConfig(
    domain_id="general",
    model_name="microsoft/phi-2",  # ← ANY model!
    keywords=["help", "question"]
)

result = executor.execute("Explain quantum computing", phi_domain)
```

### With Monitoring ✅ WORKING NOW

```python
from mdsa import RequestLogger, MetricsCollector
import uuid

# Setup monitoring
logger = RequestLogger(max_logs=10000)
metrics = MetricsCollector(window_size=1000)

# Execute with tracking
result = executor.execute(query, finance)

# Log request
logger.log_request(
    request_id=str(uuid.uuid4()),
    query=query,
    domain=result['domain'],
    model=result['model'],
    response=result['response'],
    status=result['status'],
    latency_ms=result['latency_ms'],
    tokens_generated=result['tokens_generated'],
    confidence=result['confidence']
)

# Get stats
stats = logger.get_stats()
print(f"Success rate: {stats['success_rate_percent']:.1f}%")

summary = metrics.get_summary()
print(f"P95 latency: {summary['p95_latency_ms']:.1f}ms")
```

## 📁 Project Structure

```
mdsa-framework/
├── mdsa/                    # Main package
│   ├── core/               # Orchestration engine (Phase 2)
│   ├── domains/            # Domain management (Phase 4)
│   ├── models/             # Model loading (Phase 3)
│   ├── rag/                # RAG system (Phase 5)
│   ├── communication/      # Message bus (Phase 6)
│   ├── validation/         # Validation pipeline (Phase 7)
│   ├── monitoring/         # Metrics & web server (Phase 8)
│   ├── ui/                 # Dashboard UI (Phase 9)
│   ├── integrations/       # MCP, tools (Phase 10)
│   └── utils/              # Hardware, config, logging
├── configs/                # Configuration templates
├── examples/               # Example scripts
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## 🎯 Use Cases

### Financial Services
```python
# Transaction processing, risk assessment, reporting
domain = SimpleDomainAPI.create_domain("finance", "meta-llama/Llama-2-7b-hf")
mdsa.register_domain(domain)

response = mdsa.process("Analyze transaction TR-12345 for fraud risk")
```

### Software Development
```python
# Code analysis, testing, integration
domain = SimpleDomainAPI.create_domain("dev", "Qwen/Qwen-7B")
mdsa.register_domain(domain)

response = mdsa.process("Review pull request #42 for security issues")
```

### Customer Support
```python
# Support ticket routing, knowledge base queries
domain = SimpleDomainAPI.create_rag_domain(
    "support",
    "mistralai/Mistral-7B-v0.1",
    ["./support_docs/"]
)
mdsa.register_domain(domain)

response = mdsa.process("User can't login - error 401")
```

## 📊 Performance Targets

| Metric | Target | Description |
|--------|--------|-------------|
| **Orchestrator Latency** | <50ms | TinyBERT intent classification (P99) |
| **Classification Accuracy** | >95% | Intent routing accuracy |
| **Domain Processing** | <500ms | SLM inference on GPU |
| **Total E2E Latency** | <700ms | Complete request (P99) |
| **Idle Memory** | <500MB | Framework overhead |
| **Active Memory** | <16GB | With 3 domains loaded |
| **Throughput** | 450 req/sec | Concurrent request handling |

## 🔧 Configuration

### Framework Configuration (`configs/framework_config.yaml`)

```yaml
framework:
  name: "MDSA Framework"
  version: "1.0.0"

orchestrator:
  model: "huawei-noah/TinyBERT_General_6L_768D"
  device: "cpu"
  confidence_threshold: 0.85

validation:
  enable_rules: true
  enable_reasoning: true
  reasoning_model: "microsoft/phi-1_5"

monitoring:
  metrics: true
  logging: true
  log_level: "INFO"
  metrics_port: 9090
```

### Domain Configuration (`configs/domains/my_domain.yaml`)

```yaml
domain:
  name: "my_domain"
  description: "Custom domain for specialized tasks"

  models:
    - name: "primary_model"
      source: "huggingface"
      path: "meta-llama/Llama-2-7b-hf"
      quantization: "8bit"
      device: "auto"

  rag:
    enabled: true
    scope: "local"
    embedding_model: "all-MiniLM-L6-v2"
    documents:
      - "./domain_docs/"

  tools: []
  validation: []
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mdsa --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m performance   # Performance benchmarks
```

## 📚 Documentation

- **[README.md](README.md)** - This file: Quick start and overview
- **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - Detailed production usage guide
  - Installation methods
  - Using ANY model from HuggingFace
  - Visualization (Streamlit, Prometheus, Grafana)
  - Project integration examples (FastAPI, chatbot, document analysis)
  - Plug and play model testing
  - Publishing to PyPI
- **[DISTRIBUTION_SUMMARY.md](DISTRIBUTION_SUMMARY.md)** - Quick reference for sharing with friends

## 🛣️ Roadmap

### Phase 1: Project Foundation ✅ COMPLETE
- [x] Package structure
- [x] setup.py and dependencies
- [x] Hardware detection
- [x] Configuration system

### Phase 2: Orchestration Core ✅ COMPLETE
- [x] TinyBERT intent router
- [x] State machine
- [x] Message bus
- [x] Workflow management

### Phase 3: Model Management ✅ COMPLETE
- [x] ModelManager with LRU cache
- [x] ANY HuggingFace model support
- [x] INT4/INT8/FP16 quantization
- [x] Thread-safe operations
- [x] Automatic model eviction

### Phase 4: Domain Execution ✅ COMPLETE
- [x] DomainConfig and DomainRegistry
- [x] 4 predefined domains (finance, medical, support, technical)
- [x] Custom domain creation
- [x] Prompt builder
- [x] Response validation

### Phase 5: Monitoring & Logging ✅ COMPLETE
- [x] RequestLogger with filtering
- [x] MetricsCollector with percentiles
- [x] Per-domain and per-model tracking
- [x] Export to JSON/CSV
- [x] Historical snapshots

### Phase 6+: Future Enhancements
- [ ] RAG system (local + global knowledge)
- [ ] Streamlit web dashboard
- [ ] Response caching
- [ ] Multi-turn conversations
- [ ] Streaming responses
- [ ] Model fine-tuning utilities

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for Transformers and model hub
- The PyTorch team
- ChromaDB for vector storage
- FastAPI for the web framework
- All contributors to the open-source AI community

## 📮 Contact

- **Issues**: [GitHub Issues](https://github.com/your-org/mdsa-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/mdsa-framework/discussions)
- **Email**: mdsa@example.com

---

## 🎁 Sharing with Friends

### Build & Share

```bash
# Build wheel file
python setup.py bdist_wheel

# Share: dist/mdsa-1.0.0-py3-none-any.whl

# Your friend installs:
pip install mdsa-1.0.0-py3-none-any.whl

# They verify:
python -m mdsa
```

See [DISTRIBUTION_SUMMARY.md](DISTRIBUTION_SUMMARY.md) for complete sharing guide.

---

**Built with ❤️ for the AI community**

*Status: Phases 1-5 Complete - Production Ready!* 🚀
