# Complete MDSA Orcherstration Framework Development Prompt - Production-Grade Enterprise AI Orchestration System

Build a comprehensive, production-ready Python framework called **MDSA Orcherstartion (Multi-Domain Small Language Model Agentic Orchestration)** that is beginner-friendly, highly configurable, and enterprise-grade with complete monitoring capabilities.

---

## 🎯 CORE OBJECTIVES

Create a framework that:

1. **Beginner-Friendly** : Simple domain creation with minimal code
2. **Multi-Source Model Support** : GitHub, HuggingFace, local files, cloud APIs, custom endpoints
3. **Flexible RAG** : Both local (per-domain/per-model) and global (cross-domain) RAG capabilities
4. **Advanced Communication** : Easy SLM-to-SLM, SLM-to-tool, and domain-to-domain communication
5. **Visual Monitoring** : Real-time web UI for system visualization and monitoring
6. **Production-Ready** : Scalable, secure, and deployable in enterprise environments

---

## 📁 PROJECT STRUCTURE

```
mdsa-framework/
├── mdsa/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # TinyBERT orchestration engine
│   │   ├── state_machine.py         # Workflow state management
│   │   ├── router.py                # Intent classification & routing
│   │   └── communication_bus.py     # Inter-model communication layer
│   │
│   ├── domains/
│   │   ├── __init__.py
│   │   ├── base.py                  # BaseDomain abstract class
│   │   ├── registry.py              # Domain registration & discovery
│   │   ├── builder.py               # Domain builder from configs
│   │   ├── templates/               # Domain templates for quick start
│   │   │   ├── simple_domain.yaml
│   │   │   ├── rag_enabled_domain.yaml
│   │   │   └── multi_model_domain.yaml
│   │   └── examples/                # Pre-built domain examples
│   │       ├── finance_domain.py
│   │       ├── dev_domain.py
│   │       └── customer_service_domain.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_manager.py         # Model lifecycle management
│   │   ├── loaders/
│   │   │   ├── huggingface_loader.py
│   │   │   ├── github_loader.py
│   │   │   ├── local_loader.py
│   │   │   ├── ollama_loader.py
│   │   │   ├── openai_loader.py
│   │   │   └── custom_loader.py
│   │   ├── bundled/
│   │   │   └── tinybert/            # Bundled TinyBERT model
│   │   └── downloader.py            # Auto-download & caching
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── vector_store.py          # Vector database interface
│   │   ├── embeddings.py            # Embedding generation
│   │   ├── local_rag.py             # Per-domain/per-model RAG
│   │   ├── global_rag.py            # Cross-domain RAG
│   │   ├── chunking.py              # Document chunking strategies
│   │   └── retrieval.py             # Retrieval strategies
│   │
│   ├── communication/
│   │   ├── __init__.py
│   │   ├── message_bus.py           # Event-driven message bus
│   │   ├── slm_bridge.py            # SLM-to-SLM communication
│   │   ├── tool_adapter.py          # SLM-to-tool integration
│   │   └── protocols.py             # Communication protocols
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── rules.py                 # Rule-based validation
│   │   ├── reasoning.py             # Phi-1.5 reasoning validator
│   │   ├── schemas.py               # JSON schema validation
│   │   └── validators/              # Custom validators
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── mcp.py                   # Model Context Protocol
│   │   ├── api_manager.py           # API key management
│   │   ├── tools/                   # Tool integrations
│   │   │   ├── github_tools.py
│   │   │   ├── database_tools.py
│   │   │   └── custom_tools.py
│   │   └── adapters/
│   │       ├── langchain_adapter.py
│   │       └── llamaindex_adapter.py
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── metrics_collector.py     # Real-time metrics
│   │   ├── event_tracker.py         # Event tracking
│   │   ├── resource_monitor.py      # RAM/GPU/CPU monitoring
│   │   ├── flow_analyzer.py         # Data flow analysis
│   │   └── web_server.py            # Monitoring web server
│   │
│   ├── ui/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── main.css
│   │   │   │   ├── monitor.css
│   │   │   │   └── components.css
│   │   │   ├── js/
│   │   │   │   ├── main.js
│   │   │   │   ├── monitor.js
│   │   │   │   ├── graph-renderer.js
│   │   │   │   ├── metrics-dashboard.js
│   │   │   │   └── websocket-client.js
│   │   │   └── assets/
│   │   │       └── icons/
│   │   └── templates/
│   │       ├── monitor.html
│   │       ├── domain_view.html
│   │       └── model_details.html
│   │
│   └── utils/
│       ├── __init__.py
│       ├── hardware.py              # Hardware detection
│       ├── config_loader.py         # Configuration management
│       ├── logger.py                # Logging utilities
│       └── helpers.py               # Common utilities
│
├── configs/
│   ├── framework_config.yaml        # Main framework config
│   ├── domains/                     # Domain configurations
│   │   ├── finance.yaml
│   │   ├── development.yaml
│   │   └── customer_service.yaml
│   └── templates/
│       └── domain_template.yaml     # Template for new domains
│
├── examples/
│   ├── quickstart.py
│   ├── beginner_domain_creation.py
│   ├── advanced_multi_domain.py
│   ├── rag_integration.py
│   ├── custom_model_source.py
│   └── monitoring_demo.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── docs/
│   ├── getting_started.md
│   ├── domain_creation_guide.md
│   ├── rag_setup.md
│   ├── monitoring_guide.md
│   └── api_reference.md
│
├── scripts/
│   ├── setup_dev.sh
│   └── start_monitoring.sh
│
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── README.md
├── LICENSE
└── .env.example
```

---

## 🔧 DETAILED IMPLEMENTATION REQUIREMENTS

### 1. BEGINNER-FRIENDLY DOMAIN CREATION SYSTEM

#### 1.1 Simple Domain Template (YAML-Based)

**File: `configs/templates/domain_template.yaml`**

```yaml
# Simple Domain Template - Beginner Friendly
domain:
  name: "my_domain"
  description: "Description of what this domain handles"
  
  # Model Configuration - Multiple Sources Supported
  models:
    - name: "primary_model"
      source: "huggingface"  # huggingface, github, local, ollama, openai, custom
      path: "meta-llama/Llama-2-7b-hf"
      quantization: "8bit"  # Optional: 4bit, 8bit, none
      device: "auto"  # auto, cpu, cuda, mps
  
    - name: "secondary_model"
      source: "local"
      path: "/path/to/local/model"
  
    - name: "reasoning_model"
      source: "ollama"
      path: "codellama:7b"
  
  # RAG Configuration
  rag:
    enabled: true
    scope: "local"  # local (domain-specific) or global (cross-domain)
    vector_store: "chroma"  # chroma, faiss, pinecone, weaviate
    embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
    documents:
      - path: "./data/domain_docs/"
      - url: "https://example.com/api/docs"
    chunk_size: 512
    chunk_overlap: 50
  
  # Tools & Integrations
  tools:
    - name: "database_query"
      type: "sql"
      connection: "postgresql://localhost/mydb"
  
    - name: "api_call"
      type: "rest"
      endpoint: "https://api.example.com"
      auth: "${API_KEY}"
  
    - name: "custom_tool"
      type: "mcp"
      server: "custom_mcp_server"
  
  # Validation Rules
  validation:
    pre_execution:
      - rule: "user.has_permission('domain_access')"
      - rule: "query_length < 1000"
  
    post_execution:
      - schema: "./schemas/response.json"
      - reasoning: true  # Use Phi-1.5 for complex validation
  
  # Communication Settings
  communication:
    can_communicate_with:
      - "finance_domain"
      - "dev_domain"
    protocols:
      - "message_bus"
      - "direct"
```

#### 1.2 Python Domain Builder API

**File: `mdsa/domains/builder.py`**

```python
from typing import Dict, List, Optional, Union
import yaml
from pathlib import Path

class DomainBuilder:
    """
    Beginner-friendly domain builder with multiple creation methods
    """
  
    @staticmethod
    def from_yaml(config_path: str) -> 'Domain':
        """
        Create domain from YAML configuration
    
        Example:
            domain = DomainBuilder.from_yaml("configs/domains/my_domain.yaml")
        """
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return DomainBuilder._build_from_config(config)
  
    @staticmethod
    def from_dict(config: Dict) -> 'Domain':
        """
        Create domain from dictionary
    
        Example:
            domain = DomainBuilder.from_dict({
                "name": "my_domain",
                "models": [{"source": "huggingface", "path": "gpt2"}],
                "rag": {"enabled": True}
            })
        """
        return DomainBuilder._build_from_config(config)
  
    @staticmethod
    def quick_start(
        name: str,
        model_source: str,
        model_path: str,
        enable_rag: bool = False,
        rag_documents: List[str] = None
    ) -> 'Domain':
        """
        Quick start method for absolute beginners
    
        Example:
            domain = DomainBuilder.quick_start(
                name="customer_service",
                model_source="huggingface",
                model_path="microsoft/DialoGPT-medium",
                enable_rag=True,
                rag_documents=["./docs/faq.txt"]
            )
        """
        config = {
            "domain": {
                "name": name,
                "models": [{
                    "name": "primary",
                    "source": model_source,
                    "path": model_path
                }]
            }
        }
    
        if enable_rag:
            config["domain"]["rag"] = {
                "enabled": True,
                "scope": "local",
                "documents": [{"path": doc} for doc in (rag_documents or [])]
            }
    
        return DomainBuilder._build_from_config(config)
  
    @staticmethod
    def interactive_builder():
        """
        Interactive CLI builder for creating domains
    
        Guides user through domain creation with prompts
        """
        print("🚀 MDSA Interactive Domain Builder")
        print("=" * 50)
    
        name = input("Domain name: ")
        description = input("Domain description: ")
    
        print("\n📦 Model Configuration")
        print("Select model source:")
        print("1. HuggingFace")
        print("2. Local file")
        print("3. Ollama")
        print("4. GitHub")
        print("5. OpenAI API")
    
        source_choice = input("Choice (1-5): ")
        source_map = {
            "1": "huggingface",
            "2": "local",
            "3": "ollama",
            "4": "github",
            "5": "openai"
        }
    
        source = source_map.get(source_choice, "huggingface")
        model_path = input(f"Model path/ID for {source}: ")
    
        enable_rag = input("\n🔍 Enable RAG? (y/n): ").lower() == 'y'
    
        config = {
            "domain": {
                "name": name,
                "description": description,
                "models": [{
                    "name": "primary",
                    "source": source,
                    "path": model_path
                }]
            }
        }
    
        if enable_rag:
            rag_scope = input("RAG scope (local/global): ")
            doc_path = input("Path to documents: ")
            config["domain"]["rag"] = {
                "enabled": True,
                "scope": rag_scope,
                "documents": [{"path": doc_path}]
            }
    
        # Save configuration
        output_path = f"configs/domains/{name}.yaml"
        Path("configs/domains").mkdir(parents=True, exist_ok=True)
    
        with open(output_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
        print(f"\n✅ Domain configuration saved to {output_path}")
        return DomainBuilder.from_dict(config)

class SimpleDomainAPI:
    """
    Ultra-simple API for absolute beginners
    """
  
    @staticmethod
    def create_domain(name: str, model: str):
        """
        Create domain with single line
    
        Example:
            domain = SimpleDomainAPI.create_domain("my_domain", "gpt2")
        """
        return DomainBuilder.quick_start(name, "huggingface", model)
  
    @staticmethod
    def create_rag_domain(name: str, model: str, documents: List[str]):
        """
        Create RAG-enabled domain with single line
    
        Example:
            domain = SimpleDomainAPI.create_rag_domain(
                "support", "gpt2", ["./docs/"]
            )
        """
        return DomainBuilder.quick_start(
            name, "huggingface", model, True, documents
        )
```

### 2. MULTI-SOURCE MODEL LOADER SYSTEM

**File: `mdsa/models/model_manager.py`**

```python
from typing import Dict, Any, Optional, Union
import importlib
from pathlib import Path
import torch

class ModelManager:
    """
    Unified model management supporting multiple sources
    """
  
    SUPPORTED_SOURCES = [
        "huggingface",
        "github",
        "local",
        "ollama",
        "openai",
        "anthropic",
        "custom"
    ]
  
    def __init__(self):
        self.loaded_models = {}
        self.model_registry = {}
        self.loaders = self._initialize_loaders()
  
    def _initialize_loaders(self) -> Dict[str, Any]:
        """Initialize all available model loaders"""
        loaders = {}
    
        for source in self.SUPPORTED_SOURCES:
            try:
                module = importlib.import_module(
                    f"mdsa.models.loaders.{source}_loader"
                )
                loaders[source] = module.Loader()
            except ImportError:
                print(f"⚠️  Loader for {source} not available")
    
        return loaders
  
    def load_model(
        self,
        name: str,
        source: str,
        path: str,
        **kwargs
    ) -> Any:
        """
        Load model from any supported source
    
        Args:
            name: Unique model identifier
            source: Model source (huggingface, github, local, etc.)
            path: Model path/ID
            **kwargs: Additional configuration
        
        Returns:
            Loaded model instance
        
        Example:
            # HuggingFace
            model = manager.load_model(
                "finance_model",
                "huggingface",
                "meta-llama/Llama-2-7b-hf",
                quantization="8bit"
            )
        
            # Local file
            model = manager.load_model(
                "custom_model",
                "local",
                "/path/to/model",
                device="cuda"
            )
        
            # GitHub repository
            model = manager.load_model(
                "github_model",
                "github",
                "username/repo/model.bin",
                branch="main"
            )
        
            # Ollama
            model = manager.load_model(
                "ollama_model",
                "ollama",
                "codellama:7b"
            )
        """
        if source not in self.loaders:
            raise ValueError(f"Unsupported source: {source}")
    
        print(f"📦 Loading {name} from {source}...")
    
        loader = self.loaders[source]
        model = loader.load(path, **kwargs)
    
        self.loaded_models[name] = {
            "model": model,
            "source": source,
            "path": path,
            "config": kwargs
        }
    
        print(f"✅ {name} loaded successfully")
        return model
  
    def unload_model(self, name: str):
        """Unload model from memory"""
        if name in self.loaded_models:
            del self.loaded_models[name]["model"]
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            print(f"🗑️  {name} unloaded")
  
    def get_model(self, name: str) -> Any:
        """Get loaded model instance"""
        if name not in self.loaded_models:
            raise ValueError(f"Model {name} not loaded")
        return self.loaded_models[name]["model"]
  
    def list_loaded_models(self) -> List[str]:
        """List all currently loaded models"""
        return list(self.loaded_models.keys())
```

**File: `mdsa/models/loaders/github_loader.py`**

```python
import requests
import tempfile
from pathlib import Path
from typing import Dict, Any

class Loader:
    """Load models from GitHub repositories"""
  
    def load(self, repo_path: str, **kwargs) -> Any:
        """
        Load model from GitHub
    
        Args:
            repo_path: Format "username/repo/path/to/model"
            branch: Git branch (default: main)
        
        Example:
            loader = Loader()
            model = loader.load(
                "myuser/my-models/finance-model.bin",
                branch="main"
            )
        """
        branch = kwargs.get("branch", "main")
    
        # Parse repo path
        parts = repo_path.split("/")
        username = parts[0]
        repo = parts[1]
        file_path = "/".join(parts[2:])
    
        # Download from GitHub
        url = f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{file_path}"
    
        print(f"📥 Downloading from GitHub: {url}")
    
        response = requests.get(url)
        response.raise_for_status()
    
        # Save to temp file
        temp_path = Path(tempfile.gettempdir()) / f"mdsa_{repo}_{file_path.replace('/', '_')}"
        temp_path.write_bytes(response.content)
    
        # Load model (assuming PyTorch format)
        import torch
        model = torch.load(temp_path, map_location=kwargs.get("device", "cpu"))
    
        return model
```

### 3. FLEXIBLE RAG SYSTEM (Local & Global)

**File: `mdsa/rag/local_rag.py`**

```python
from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

class LocalRAG:
    """
    Domain-specific or model-specific RAG system
    """
  
    def __init__(
        self,
        domain_name: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        vector_store_path: Optional[str] = None
    ):
        self.domain_name = domain_name
        self.embedding_model = SentenceTransformer(embedding_model)
    
        # Initialize ChromaDB
        if vector_store_path is None:
            vector_store_path = f"~/.mdsa/rag/{domain_name}"
    
        self.client = chromadb.PersistentClient(
            path=str(Path(vector_store_path).expanduser())
        )
    
        self.collection = self.client.get_or_create_collection(
            name=f"{domain_name}_documents"
        )
  
    def add_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Add documents to local RAG
    
        Example:
            rag = LocalRAG("finance")
            rag.add_documents(
                ["Document 1 text", "Document 2 text"],
                metadata=[{"source": "doc1"}, {"source": "doc2"}]
            )
        """
        embeddings = self.embedding_model.encode(documents).tolist()
    
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
    
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata or [{}] * len(documents),
            ids=ids
        )
    
        print(f"✅ Added {len(documents)} documents to {self.domain_name} RAG")
  
    def add_from_directory(
        self,
        directory: str,
        file_extensions: List[str] = [".txt", ".md", ".pdf"],
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        """
        Add all documents from directory
    
        Example:
            rag.add_from_directory("./data/finance_docs/")
        """
        from mdsa.rag.chunking import chunk_documents
    
        documents = []
        metadata = []
    
        for ext in file_extensions:
            for file_path in Path(directory).rglob(f"*{ext}"):
                content = file_path.read_text()
                chunks = chunk_documents(content, chunk_size, chunk_overlap)
            
                documents.extend(chunks)
                metadata.extend([
                    {"source": str(file_path), "chunk": i}
                    for i in range(len(chunks))
                ])
    
        self.add_documents(documents, metadata)
  
    def retrieve(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents
    
        Returns:
            List of {"content": str, "metadata": dict, "score": float}
        """
        query_embedding = self.embedding_model.encode([query]).tolist()
    
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
    
        documents = []
        for i in range(len(results["documents"][0])):
            documents.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            })
    
        return documents
```

**File: `mdsa/rag/global_rag.py`**

```python
class GlobalRAG:
    """
    Cross-domain RAG system for shared knowledge
    """
  
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
    
        self.client = chromadb.PersistentClient(
            path=str(Path("~/.mdsa/rag/global").expanduser())
        )
    
        self.collection = self.client.get_or_create_collection(
            name="global_knowledge"
        )
  
    def add_domain_knowledge(
        self,
        domain_name: str,
        documents: List[str],
        metadata: Optional[List[Dict]] = None
    ):
        """Add knowledge that can be shared across domains"""
        # Add domain tag to metadata
        if metadata is None:
            metadata = [{}] * len(documents)
    
        for meta in metadata:
            meta["domain"] = domain_name
    
        embeddings = self.embedding_model.encode(documents).tolist()
        ids = [f"{domain_name}_global_{i}" for i in range(len(documents))]
    
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
            ids=ids
        )
  
    def retrieve_cross_domain(
        self,
        query: str,
        n_results: int = 5,
        filter_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve from global knowledge base, optionally filtering by domains
        """
        query_embedding = self.embedding_model.encode([query]).tolist()
    
        where_filter = None
        if filter_domains:
            where_filter = {"domain": {"$in": filter_domains}}
    
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where_filter
        )
    
        return self._format_results(results)
```

### 4. ADVANCED COMMUNICATION SYSTEM

**File: `mdsa/communication/message_bus.py`**

```python
import asyncio
from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    """Types of messages in the system"""
    QUERY = "query"
    RESPONSE = "response"
    TOOL_CALL = "tool_call"
    VALIDATION = "validation"
    RAG_REQUEST = "rag_request"
    MODEL_TO_MODEL = "model_to_model"
    ERROR = "error"

@dataclass
class Message:
    """Message structure for inter-component communication"""
    type: MessageType
    sender: str
    receiver: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = None
    correlation_id: str = None

class MessageBus:
    """
    Event-driven message bus for all component communication
    Enables SLM-to-SLM, SLM-to-tool, domain-to-domain communication
    """
  
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
        self.active_conversations: Dict[str, List[Message]] = {}
  
    def subscribe(self, channel: str, callback: Callable):
        """
        Subscribe to message channel
    
        Example:
            bus.subscribe("finance_domain", finance_handler)
            bus.subscribe("model_to_model", inter_model_handler)
        """
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
  
    async def publish(self, channel: str, message: Message):
        """
        Publish message to channel
    
        Example:
            await bus.publish("finance_domain", Message(
                type=MessageType.QUERY,
                sender="user",
                receiver="finance_model",
                payload={"query": "What's my balance?"}
            ))
        """
        # Store in history
        self.message_history.append(message)
    
        # Track conversation
        if message.correlation_id:
            if message.correlation_id not in self.active_conversations:
                self.active_conversations[message.correlation_id] = []
            self.active_conversations[message.correlation_id].append(message)
    
        # Notify subscribers
        if channel in self.subscribers:
            tasks = [
                callback(message)
                for callback in self.subscribers[channel]
            ]
            await asyncio.gather(*tasks)
  
    def get_conversation_history(self, correlation_id: str) -> List[Message]:
        """Get full conversation thread"""
        return self.active_conversations.get(correlation_id, [])

class SLMBridge:
    """
    Facilitates direct SLM-to-SLM communication
    """
  
    def __init__(self, message_bus: MessageBus):
        self.bus = message_bus
        self.model_connections: Dict[str, List[str]] = {}
  
    def connect_models(self, model_a: str, model_b: str):
        """
        Establish bidirectional communication between two models
    
        Example:
            bridge.connect_models("finance_model", "risk_model")
        """
        if model_a not in self.model_connections:
            self.model_connections[model_a] = []
        if model_b not in self.model_connections:
            self.model_connections[model_b] = []
    
        self.model_connections[model_a].append(model_b)
        self.model_connections[model_b].append(model_a)
    
        print(f"🔗 Connected {model_a} ↔️ {model_b}")
  
    async def send_to_model(
        self,
        sender_model: str,
        receiver_model: str,
        payload: Dict[str, Any],
        correlation_id: str = None
    ) -> Dict[str, Any]:
        """
        Send message from one model to another
    
        Example:
            response = await bridge.send_to_model(
                "finance_model",
                "risk_model",
                {"action": "assess_risk", "amount": 10000}
            )
        """
        if receiver_model not in self.model_connections.get(sender_model, []):
            raise ValueError(f"{sender_model} not connected to {receiver_model}")
    
        message = Message(
            type=MessageType.MODEL_TO_MODEL,
            sender=sender_model,
            receiver=receiver_model,
            payload=payload,
            correlation_id=correlation_id
        )
    
        # Publish and wait for response
        response_future = asyncio.Future()
    
        async def response_handler(response_msg: Message):
            if response_msg.sender == receiver_model:
                response_future.set_result(response_msg.payload)
    
        self.bus.subscribe(f"response_{correlation_id}", response_handler)
        await self.bus.publish(f"model_{receiver_model}", message)
    
        return await response_future
```

### 5. COMPREHENSIVE MONITORING UI

**File: `mdsa/monitoring/web_server.py`**

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncio
import json
from typing import List, Dict, Any

app = FastAPI(title="MDSA Monitoring Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="mdsa/ui/static"), name="static")
templates = Jinja2Templates(directory="mdsa/ui/templates")

class MonitoringServer:
    """
    Real-time monitoring web server
    Accessible at localhost:8000/monitor
    """
  
    def __init__(self, framework):
        self.framework = framework
        self.active_connections: List[WebSocket] = []
        self.metrics_collector = framework.monitoring.metrics_collector
        self.flow_analyzer = framework.monitoring.flow_analyzer
    
    async def start(self, host: str = "localhost", port: int = 8000):
        """Start monitoring server"""
        import uvicorn
        uvicorn.run(app, host=host, port=port)

@app.get("/monitor", response_class=HTMLResponse)
async def monitor_dashboard(request: Request):
    """Main monitoring dashboard"""
    return templates.TemplateResponse("monitor.html", {
        "request": request,
        "title": "MDSA Monitoring Dashboard"
    })

@app.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    WebSocket endpoint for real-time metrics
    """
    await websocket.accept()
    monitoring_server.active_connections.append(websocket)
  
    try:
        while True:
            # Collect current metrics
            metrics = {
                "timestamp": time.time(),
                "domains": monitoring_server.metrics_collector.get_domain_metrics(),
                "models": monitoring_server.metrics_collector.get_model_metrics(),
                "resources": monitoring_server.metrics_collector.get_resource_metrics(),
                "flows": monitoring_server.flow_analyzer.get_active_flows()
            }
        
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
        
    except WebSocketDisconnect:
        monitoring_server.active_connections.remove(websocket)

@app.get("/api/domains")
async def get_domains():
    """Get all registered domains"""
    return {
        "domains": [
            {
                "name": domain.name,
                "models": [model.name for model in domain.models],
                "status": domain.status,
                "active": domain.is_active()
            }
            for domain in monitoring_server.framework.domains.get_all()
        ]
    }

@app.get("/api/models/{model_name}/metrics")
async def get_model_metrics(model_name: str):
    """Get detailed metrics for specific model"""
    return monitoring_server.metrics_collector.get_model_details(model_name)

@app.get("/api/flow/graph")
async def get_flow_graph():
    """Get current data flow graph"""
    return monitoring_server.flow_analyzer.get_graph_data()
```

**File: `mdsa/ui/static/js/monitor.js`**

```javascript
// Real-time monitoring dashboard JavaScript

class MDSAMonitor {
    constructor() {
        this.ws = null;
        this.graphs = {};
        this.init();
    }
  
    init() {
        this.connectWebSocket();
        this.setupGraphs();
        this.setupEventHandlers();
    }
  
    connectWebSocket() {
        this.ws = new WebSocket('ws://localhost:8000/ws/metrics');
    
        this.ws.onopen = () => {
            console.log('✅ Connected to monitoring server');
            this.updateConnectionStatus(true);
        };
    
        this.ws.onmessage = (event) => {
            const metrics = JSON.parse(event.data);
            this.updateDashboard(metrics);
        };
    
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
    
        this.ws.onclose = () => {
            console.log('Disconnected. Reconnecting...');
            setTimeout(() => this.connectWebSocket(), 3000);
        };
    }
  
    setupGraphs() {
        // Domain visualization graph
        this.graphs.domainFlow = new DomainFlowGraph('domain-flow-canvas');
    
        // Resource usage charts
        this.graphs.cpuChart = new ResourceChart('cpu-chart', 'CPU Usage');
        this.graphs.memoryChart = new ResourceChart('memory-chart', 'Memory Usage');
        this.graphs.gpuChart = new ResourceChart('gpu-chart', 'GPU Usage');
    
        // Model activity timeline
        this.graphs.activityTimeline = new ActivityTimeline('activity-timeline');
    }
  
    updateDashboard(metrics) {
        // Update domain cards
        this.updateDomainCards(metrics.domains);
    
        // Update model status
        this.updateModelStatus(metrics.models);
    
        // Update resource graphs
        this.graphs.cpuChart.addDataPoint(metrics.resources.cpu);
        this.graphs.memoryChart.addDataPoint(metrics.resources.memory);
        this.graphs.gpuChart.addDataPoint(metrics.resources.gpu);
    
        // Update flow visualization
        this.graphs.domainFlow.update(metrics.flows);
    
        // Update activity timeline
        this.graphs.activityTimeline.addEvent(metrics.flows.latest);
    }
  
    updateDomainCards(domains) {
        const container = document.getElementById('domains-container');
        container.innerHTML = '';
    
        domains.forEach(domain => {
            const card = this.createDomainCard(domain);
            container.appendChild(card);
        });
    }
  
    createDomainCard(domain) {
        const card = document.createElement('div');
        card.className = 'domain-card';
        card.innerHTML = `
            <div class="domain-header">
                <h3>${domain.name}</h3>
                <span class="status-badge ${domain.active ? 'active' : 'inactive'}">
                    ${domain.active ? '🟢 Active' : '⚫ Inactive'}
                </span>
            </div>
            <div class="domain-body">
                <div class="models-list">
                    <h4>Models (${domain.models.length})</h4>
                    ${domain.models.map(model => `
                        <div class="model-item">
                            <span class="model-name">${model.name}</span>
                            <span class="model-status">
                                ${this.getModelStatusIcon(model.status)}
                            </span>
                        </div>
                    `).join('')}
                </div>
                <div class="domain-metrics">
                    <div class="metric">
                        <span class="metric-label">Requests</span>
                        <span class="metric-value">${domain.metrics.requests}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Avg Latency</span>
                        <span class="metric-value">${domain.metrics.latency}ms</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Memory</span>
                        <span class="metric-value">${domain.metrics.memory}GB</span>
                    </div>
                </div>
            </div>
        `;
    
        card.addEventListener('click', () => {
            this.showDomainDetails(domain);
        });
    
        return card;
    }
  
    showDomainDetails(domain) {
        // Show detailed view in modal
        const modal = document.getElementById('domain-details-modal');
        // ... populate modal with detailed information
        modal.style.display = 'block';
    }
}

class DomainFlowGraph {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.edges = [];
        this.setupCanvas();
    }
  
    setupCanvas() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }
  
    update(flows) {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
        // Extract nodes and edges from flow data
        this.processFlows(flows);
    
        // Draw edges
        this.edges.forEach(edge => this.drawEdge(edge));
    
        // Draw nodes
        this.nodes.forEach(node => this.drawNode(node));
    
        // Draw labels
        this.nodes.forEach(node => this.drawLabel(node));
    }
  
    processFlows(flows) {
        // Convert flow data to graph structure
        const nodeMap = new Map();
        this.edges = [];
    
        flows.forEach(flow => {
            // Add sender node
            if (!nodeMap.has(flow.sender)) {
                nodeMap.set(flow.sender, {
                    id: flow.sender,
                    x: Math.random() * (this.canvas.width - 100) + 50,
                    y: Math.random() * (this.canvas.height - 100) + 50,
                    type: flow.sender_type,
                    active: true
                });
            }
        
            // Add receiver node
            if (!nodeMap.has(flow.receiver)) {
                nodeMap.set(flow.receiver, {
                    id: flow.receiver,
                    x: Math.random() * (this.canvas.width - 100) + 50,
                    y: Math.random() * (this.canvas.height - 100) + 50,
                    type: flow.receiver_type,
                    active: true
                });
            }
        
            // Add edge
            this.edges.push({
                from: flow.sender,
                to: flow.receiver,
                label: flow.message_type,
                active: flow.active,
                latency: flow.latency
            });
        });
    
        this.nodes = Array.from(nodeMap.values());
    }
  
    drawNode(node) {
        const radius = 30;
        const colors = {
            'domain': '#4CAF50',
            'model': '#2196F3',
            'tool': '#FF9800',
            'validator': '#9C27B0'
        };
    
        // Draw circle
        this.ctx.beginPath();
        this.ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
        this.ctx.fillStyle = colors[node.type] || '#666';
        this.ctx.fill();
    
        // Draw border
        this.ctx.strokeStyle = node.active ? '#FFF' : '#888';
        this.ctx.lineWidth = node.active ? 3 : 1;
        this.ctx.stroke();
    }
  
    drawEdge(edge) {
        const fromNode = this.nodes.find(n => n.id === edge.from);
        const toNode = this.nodes.find(n => n.id === edge.to);
    
        if (!fromNode || !toNode) return;
    
        // Draw line
        this.ctx.beginPath();
        this.ctx.moveTo(fromNode.x, fromNode.y);
        this.ctx.lineTo(toNode.x, toNode.y);
        this.ctx.strokeStyle = edge.active ? '#4CAF50' : '#CCC';
        this.ctx.lineWidth = edge.active ? 2 : 1;
        this.ctx.stroke();
    
        // Draw arrow
        this.drawArrow(fromNode, toNode);
    
        // Draw latency label if active
        if (edge.active && edge.latency) {
            const midX = (fromNode.x + toNode.x) / 2;
            const midY = (fromNode.y + toNode.y) / 2;
        
            this.ctx.fillStyle = '#FFF';
            this.ctx.fillRect(midX - 20, midY - 10, 40, 20);
        
            this.ctx.fillStyle = '#000';
            this.ctx.font = '12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(`${edge.latency}ms`, midX, midY + 5);
        }
    }
  
    drawArrow(from, to) {
        const angle = Math.atan2(to.y - from.y, to.x - from.x);
        const headLength = 10;
    
        this.ctx.beginPath();
        this.ctx.moveTo(to.x, to.y);
        this.ctx.lineTo(
            to.x - headLength * Math.cos(angle - Math.PI / 6),
            to.y - headLength * Math.sin(angle - Math.PI / 6)
        );
        this.ctx.moveTo(to.x, to.y);
        this.ctx.lineTo(
            to.x - headLength * Math.cos(angle + Math.PI / 6),
            to.y - headLength * Math.sin(angle + Math.PI / 6)
        );
        this.ctx.strokeStyle = '#4CAF50';
        this.ctx.stroke();
    }
  
    drawLabel(node) {
        this.ctx.fillStyle = '#FFF';
        this.ctx.font = 'bold 12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(node.id, node.x, node.y + 5);
    }
}

// Initialize monitor on page load
document.addEventListener('DOMContentLoaded', () => {
    window.monitor = new MDSAMonitor();
});
```

**File: `mdsa/ui/static/css/monitor.css`**

```css
/* MDSA Monitoring Dashboard Styles */

:root {
    --primary-color: #2196F3;
    --success-color: #4CAF50;
    --warning-color: #FF9800;
    --danger-color: #F44336;
    --dark-bg: #1a1a1a;
    --card-bg: #2d2d2d;
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --border-color: #404040;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--dark-bg);
    color: var(--text-primary);
    line-height: 1.6;
}

.dashboard-container {
    display: grid;
    grid-template-columns: 250px 1fr;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    background: var(--card-bg);
    border-right: 1px solid var(--border-color);
    padding: 20px;
}

.sidebar-header {
    margin-bottom: 30px;
}

.sidebar-header h1 {
    font-size: 24px;
    color: var(--primary-color);
}

.sidebar-header .connection-status {
    margin-top: 10px;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--success-color);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.nav-menu {
    list-style: none;
}

.nav-item {
    padding: 12px 15px;
    margin-bottom: 5px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.nav-item.active {
    background: var(--primary-color);
}

/* Main Content */
.main-content {
    padding: 30px;
    overflow-y: auto;
}

.page-header {
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.page-header h2 {
    font-size: 28px;
}

.refresh-button {
    padding: 10px 20px;
    background: var(--primary-color);
    border: none;
    border-radius: 6px;
    color: white;
    cursor: pointer;
    transition: background 0.2s;
}

.refresh-button:hover {
    background: #1976D2;
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.metric-label {
    font-size: 14px;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.metric-icon {
    font-size: 24px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: var(--primary-color);
}

.metric-trend {
    margin-top: 10px;
    font-size: 12px;
    color: var(--success-color);
}

.metric-trend.negative {
    color: var(--danger-color);
}

/* Domains Section */
#domains-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.domain-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s;
}

.domain-card:hover {
    border-color: var(--primary-color);
    box-shadow: 0 0 20px rgba(33, 150, 243, 0.3);
}

.domain-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}

.domain-header h3 {
    font-size: 18px;
}

.status-badge {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.status-badge.active {
    background: rgba(76, 175, 80, 0.2);
    color: var(--success-color);
}

.status-badge.inactive {
    background: rgba(128, 128, 128, 0.2);
    color: var(--text-secondary);
}

.models-list {
    margin-bottom: 15px;
}

.models-list h4 {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 10px;
}

.model-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    margin-bottom: 5px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 6px;
}

.model-name {
    font-size: 13px;
}

.model-status {
    font-size: 16px;
}

.domain-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.metric {
    text-align: center;
}

.metric-label {
    display: block;
    font-size: 11px;
    color: var(--text-secondary);
    margin-bottom: 5px;
}

.metric-value {
    display: block;
    font-size: 16px;
    font-weight: bold;
    color: var(--primary-color);
}

/* Flow Visualization */
.flow-visualization {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 30px;
}

.flow-visualization h3 {
    margin-bottom: 20px;
}

#domain-flow-canvas {
    width: 100%;
    height: 500px;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.2);
}

/* Resource Charts */
.resource-charts {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.chart-container {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

.chart-container h4 {
    margin-bottom: 15px;
    color: var(--text-secondary);
    font-size: 14px;
    text-transform: uppercase;
}

.chart-canvas {
    width: 100%;
    height: 200px;
}

/* Activity Timeline */
.activity-timeline {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

.activity-timeline h3 {
    margin-bottom: 20px;
}

.timeline-container {
    max-height: 400px;
    overflow-y: auto;
}

.timeline-event {
    display: flex;
    gap: 15px;
    padding: 15px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid var(--primary-color);
    border-radius: 6px;
    transition: background 0.2s;
}

.timeline-event:hover {
    background: rgba(255, 255, 255, 0.05);
}

.timeline-time {
    font-size: 12px;
    color: var(--text-secondary);
    min-width: 80px;
}

.timeline-content {
    flex: 1;
}

.timeline-title {
    font-weight: bold;
    margin-bottom: 5px;
}

.timeline-details {
    font-size: 13px;
    color: var(--text-secondary);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
}

.modal-content {
    background: var(--card-bg);
    margin: 5% auto;
    padding: 30px;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    width: 80%;
    max-width: 800px;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}

.close-button {
    font-size: 28px;
    font-weight: bold;
    color: var(--text-secondary);
    cursor: pointer;
    transition: color 0.2s;
}

.close-button:hover {
    color: var(--text-primary);
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--dark-bg);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
}

/* Responsive Design */
@media (max-width: 1024px) {
    .dashboard-container {
        grid-template-columns: 1fr;
    }
  
    .sidebar {
        display: none;
    }
  
    .metrics-grid {
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }
}
```

**File: `mdsa/ui/templates/monitor.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MDSA Monitoring Dashboard</title>
    <link rel="stylesheet" href="/static/css/monitor.css">
</head>
<body>
    <div class="dashboard-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>🎯 MDSA</h1>
                <div class="connection-status">
                    <span class="status-indicator"></span>
                    <span id="connection-text">Connected</span>
                </div>
            </div>
        
            <nav>
                <ul class="nav-menu">
                    <li class="nav-item active" data-view="overview">
                        📊 Overview
                    </li>
                    <li class="nav-item" data-view="domains">
                        🏢 Domains
                    </li>
                    <li class="nav-item" data-view="models">
                        🤖 Models
                    </li>
                    <li class="nav-item" data-view="flows">
                        🔄 Data Flows
                    </li>
                    <li class="nav-item" data-view="resources">
                        💻 Resources
                    </li>
                    <li class="nav-item" data-view="logs">
                        📝 Logs
                    </li>
                </ul>
            </nav>
        </aside>
    
        <!-- Main Content -->
        <main class="main-content">
            <div class="page-header">
                <h2>Dashboard Overview</h2>
                <button class="refresh-button">🔄 Refresh</button>
            </div>
        
            <!-- Metrics Summary -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-label">Total Requests</span>
                        <span class="metric-icon">📈</span>
                    </div>
                    <div class="metric-value" id="total-requests">0</div>
                    <div class="metric-trend">↑ 12% from last hour</div>
                </div>
            
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-label">Avg Latency</span>
                        <span class="metric-icon">⚡</span>
                    </div>
                    <div class="metric-value" id="avg-latency">0ms</div>
                    <div class="metric-trend">↓ 5% improvement</div>
                </div>
            
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-label">Active Domains</span>
                        <span class="metric-icon">🏢</span>
                    </div>
                    <div class="metric-value" id="active-domains">0</div>
                    <div class="metric-trend">3 total domains</div>
                </div>
            
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-label">Memory Usage</span>
                        <span class="metric-icon">💾</span>
                    </div>
                    <div class="metric-value" id="memory-usage">0GB</div>
                    <div class="metric-trend">of 16GB available</div>
                </div>
            </div>
        
            <!-- Domain Cards -->
            <section class="domains-section">
                <h3>Active Domains</h3>
                <div id="domains-container">
                    <!-- Domain cards will be dynamically inserted -->
                </div>
            </section>
        
            <!-- Flow Visualization -->
            <section class="flow-visualization">
                <h3>Data Flow Visualization</h3>
                <canvas id="domain-flow-canvas"></canvas>
            </section>
        
            <!-- Resource Charts -->
            <section class="resource-charts">
                <div class="chart-container">
                    <h4>CPU Usage</h4>
                    <canvas id="cpu-chart" class="chart-canvas"></canvas>
                </div>
                <div class="chart-container">
                    <h4>Memory Usage</h4>
                    <canvas id="memory-chart" class="chart-canvas"></canvas>
                </div>
                <div class="chart-container">
                    <h4>GPU Usage</h4>
                    <canvas id="gpu-chart" class="chart-canvas"></canvas>
                </div>
            </section>
        
            <!-- Activity Timeline -->
            <section class="activity-timeline">
                <h3>Recent Activity</h3>
                <div class="timeline-container" id="activity-timeline">
                    <!-- Timeline events will be dynamically inserted -->
                </div>
            </section>
        </main>
    </div>
  
    <!-- Domain Details Modal -->
    <div id="domain-details-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-domain-name"></h2>
                <span class="close-button">×</span>
            </div>
            <div id="modal-domain-content">
                <!-- Domain details will be dynamically inserted -->
            </div>
        </div>
    </div>
  
    <script src="/static/js/monitor.js"></script>
    <script src="/static/js/graph-renderer.js"></script>
    <script src="/static/js/metrics-dashboard.js"></script>
</body>
</html>
```

### 6. COMPLETE USAGE EXAMPLES

**File: `examples/quickstart.py`**

```python
"""
MDSA Framework - Quickstart Example
Demonstrates basic usage and domain creation
"""

from mdsa import MDSA, SimpleDomainAPI

# Initialize framework
print("🚀 Initializing MDSA Framework...")
mdsa = MDSA()

# Method 1: Ultra-simple domain creation (for absolute beginners)
print("\n📦 Method 1: Simple domain creation")
finance_domain = SimpleDomainAPI.create_domain(
    name="finance",
    model="meta-llama/Llama-2-7b-hf"
)

# Method 2: Quick start with RAG
print("\n📚 Method 2: Domain with RAG")
support_domain = SimpleDomainAPI.create_rag_domain(
    name="customer_support",
    model="microsoft/DialoGPT-medium",
    documents=["./data/faq.txt", "./data/policies.pdf"]
)

# Method 3: From YAML config
print("\n⚙️  Method 3: From configuration file")
dev_domain = mdsa.load_domain_from_yaml("configs/domains/development.yaml")

# Process a query
print("\n💬 Processing query...")
response = mdsa.process(
    "What is the current budget for Q4?",
    context={"user_id": "usr_123", "role": "manager"}
)

print(f"Response: {response}")

# Start monitoring
print("\n📊 Starting monitoring dashboard...")
print("Visit http://localhost:8000/monitor to view real-time metrics")
mdsa.start_monitoring(port=8000)
```

**File: `examples/beginner_domain_creation.py`**

```python
"""
Step-by-step guide for creating custom domains
Perfect for beginners
"""

from mdsa import MDSA
from mdsa.domains import DomainBuilder

# Initialize framework
mdsa = MDSA()

print("=" * 60)
print("MDSA Framework - Beginner's Domain Creation Guide")
print("=" * 60)

# Example 1: Local model
print("\n📦 Example 1: Creating domain with local model")
local_domain = DomainBuilder.quick_start(
    name="my_local_domain",
    model_source="local",
    model_path="/path/to/my/model"
)
mdsa.register_domain(local_domain)
print("✅ Local domain registered!")

# Example 2: HuggingFace model with RAG
print("\n📚 Example 2: HuggingFace model with RAG")
rag_domain = DomainBuilder.quick_start(
    name="docs_assistant",
    model_source="huggingface",
    model_path="gpt2",
    enable_rag=True,
    rag_documents=["./data/documentation/"]
)
mdsa.register_domain(rag_domain)
print("✅ RAG-enabled domain registered!")

# Example 3: GitHub model
print("\n🌐 Example 3: Model from GitHub repository")
github_domain = DomainBuilder.quick_start(
    name="github_domain",
    model_source="github",
    model_path="username/repo/model.bin"
)
mdsa.register_domain(github_domain)
print("✅ GitHub domain registered!")

# Example 4: Ollama model
print("\n🦙 Example 4: Ollama local server")
ollama_domain = DomainBuilder.quick_start(
    name="code_assistant",
    model_source="ollama",
    model_path="codellama:7b"
)
mdsa.register_domain(ollama_domain)
print("✅ Ollama domain registered!")

# Example 5: Interactive builder
print("\n🎨 Example 5: Interactive domain builder")
print("Follow the prompts to create a custom domain...")
interactive_domain = DomainBuilder.interactive_builder()
mdsa.register_domain(interactive_domain)

# List all registered domains
print("\n📋 All registered domains:")
for domain in mdsa.list_domains():
    print(f"  • {domain.name} ({domain.model_source})")

# Test a domain
print("\n🧪 Testing domain...")
result = mdsa.process(
    "Hello, how can you help?",
    domain="docs_assistant"
)
print(f"Response: {result}")

print("\n✨ Domain creation complete!")
```

**File: `examples/rag_integration.py`**

```python
"""
Advanced RAG integration examples
Both local and global RAG systems
"""

from mdsa import MDSA
from mdsa.rag import LocalRAG, GlobalRAG

mdsa = MDSA()

# Example 1: Local RAG (domain-specific)
print("📚 Setting up local RAG for finance domain")
finance_rag = LocalRAG("finance")

# Add documents
finance_rag.add_documents([
    "Company policy: Budget approvals require manager signature",
    "Q4 budget allocation: $500,000 for operations",
    "Travel expenses must be under $5,000 per trip"
])

# Add from directory
finance_rag.add_from_directory("./data/finance_docs/")

# Retrieve relevant information
query = "What is the travel expense limit?"
results = finance_rag.retrieve(query, n_results=3)

print(f"Query: {query}")
print("Retrieved documents:")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc['content'][:100]}...")
    print(f"   Score: {doc['score']:.3f}")

# Example 2: Global RAG (cross-domain)
print("\n🌐 Setting up global RAG")
global_rag = GlobalRAG()

# Add knowledge from multiple domains
global_rag.add_domain_knowledge(
    "finance",
    ["Financial planning best practices", "Budget management guidelines"]
)

global_rag.add_domain_knowledge(
    "legal",
    ["Compliance requirements", "Contract review procedures"]
)

# Cross-domain retrieval
query = "What are the compliance requirements for budget approvals?"
results = global_rag.retrieve_cross_domain(
    query,
    filter_domains=["finance", "legal"],
    n_results=5
)

print(f"\nCross-domain query: {query}")
print("Retrieved from multiple domains:")
for doc in results:
    print(f"• [{doc['metadata']['domain']}] {doc['content'][:80]}...")

# Example 3: RAG-enhanced domain processing
print("\n🔗 Creating RAG-enhanced domain")
from mdsa.domains import DomainBuilder

support_domain = DomainBuilder.from_dict({
    "domain": {
        "name": "customer_support",
        "models": [{
            "source": "huggingface",
            "path": "microsoft/DialoGPT-medium"
        }],
        "rag": {
            "enabled": True,
            "scope": "local",
            "documents": [
                {"path": "./data/faq.txt"},
                {"path": "./data/kb/"}
            ],
            "chunk_size": 512
        }
    }
})

mdsa.register_domain(support_domain)

# Query with RAG context
response = mdsa.process(
    "How do I reset my password?",
    domain="customer_support",
    use_rag=True
)

print(f"Response (with RAG context): {response}")
```

**File: `examples/monitoring_demo.py`**

```python
"""
Monitoring and observability features
"""

import asyncio
from mdsa import MDSA

async def main():
    # Initialize framework
    mdsa = MDSA()
  
    # Register multiple domains
    mdsa.load_domain_from_yaml("configs/domains/finance.yaml")
    mdsa.load_domain_from_yaml("configs/domains/development.yaml")
    mdsa.load_domain_from_yaml("configs/domains/customer_service.yaml")
  
    # Start monitoring server
    print("🚀 Starting monitoring dashboard...")
    print("Visit http://localhost:8000/monitor")
  
    # Start processing queries to generate metrics
    queries = [
        ("What's my account balance?", "finance"),
        ("Review code in PR #123", "development"),
        ("How do I track my order?", "customer_service")
    ]
  
    print("\n💬 Processing sample queries...")
    for query, domain in queries:
        response = await mdsa.process_async(query, domain=domain)
        print(f"✅ [{domain}] {query[:30]}... → {response['status']}")
        await asyncio.sleep(2)  # Simulate real usage
  
    # Keep monitoring server running
    print("\n📊 Monitoring dashboard running...")
    print("Press Ctrl+C to stop")
  
    await mdsa.monitoring.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🎯 CRITICAL IMPLEMENTATION REQUIREMENTS

### Must-Have Features Checklist

#### ✅ Domain Management

* [ ] YAML-based configuration
* [ ] Python API for programmatic creation
* [ ] Interactive CLI builder
* [ ] Template library (simple, RAG, multi-model)
* [ ] Hot-reload domain configs
* [ ] Domain versioning

#### ✅ Model Loading

* [ ] HuggingFace integration
* [ ] GitHub repository support
* [ ] Local file loading
* [ ] Ollama integration
* [ ] OpenAI API compatibility
* [ ] Custom endpoint support
* [ ] Automatic quantization (4bit/8bit)
* [ ] LoRA/QLoRA adapter support
* [ ] Model caching
* [ ] Auto-download with progress bars

#### ✅ RAG System

* [ ] Local RAG (per-domain/per-model)
* [ ] Global RAG (cross-domain)
* [ ] Multiple vector stores (Chroma, FAISS, Pinecone)
* [ ] Document chunking strategies
* [ ] Embedding model selection
* [ ] Incremental updates
* [ ] RAG metrics tracking

#### ✅ Communication

* [ ] Event-driven message bus
* [ ] SLM-to-SLM direct communication
* [ ] Domain-to-domain messaging
* [ ] Tool adapter interface
* [ ] Async/await support
* [ ] Message persistence
* [ ] Communication logging

#### ✅ Monitoring UI

* [ ] Real-time WebSocket updates
* [ ] Domain status cards
* [ ] Model activity visualization
* [ ] Data flow graph
* [ ] Resource usage charts (CPU/Memory/GPU)
* [ ] Activity timeline
* [ ] Detailed model metrics
* [ ] Export monitoring data
* [ ] Alert system
* [ ] Dark mode (default)

#### ✅ Production Features

* [ ] Comprehensive error handling
* [ ] Graceful degradation
* [ ] Connection pooling
* [ ] Rate limiting
* [ ] Circuit breakers
* [ ] Health checks
* [ ] Prometheus metrics
* [ ] Structured logging
* [ ] API authentication
* [ ] Docker support
* [ ] Kubernetes manifests

---

## 📚 DOCUMENTATION REQUIREMENTS

### README.md Structure

```markdown
# MDSA Framework

## Quick Start (3 lines of code)
## Features
## Installation
## Basic Usage
## Advanced Usage
## Configuration
## Monitoring
## Contributing
```

### Required Documentation Files

1. `docs/getting_started.md` - Complete beginner tutorial
2. `docs/domain_creation_guide.md` - Step-by-step domain creation
3. `docs/model_sources.md` - All supported model sources
4. `docs/rag_setup.md` - RAG configuration guide
5. `docs/communication.md` - Inter-component communication
6. `docs/monitoring_guide.md` - Using the monitoring dashboard
7. `docs/api_reference.md` - Complete API documentation
8. `docs/deployment.md` - Production deployment guide
9. `docs/troubleshooting.md` - Common issues and solutions

---

## 🚀 GETTING STARTED QUICKSTART

The final framework must support this 5-line quickstart:

```python
from mdsa import MDSA, SimpleDomainAPI

mdsa = MDSA()
mdsa.register_domain(SimpleDomainAPI.create_domain("my_domain", "gpt2"))
response = mdsa.process("Hello!")
mdsa.start_monitoring()  # Visit localhost:8000/monitor
```

---

## 🎨 UI/UX REQUIREMENTS

### Monitoring Dashboard Must Show:

1. **Overview Page** : Summary metrics, active domains, system health
2. **Domains Page** : All domains with models, status, metrics
3. **Models Page** : Individual model details, performance, resource usage
4. **Flows Page** : Real-time data flow visualization with animated connections
5. **Resources Page** : CPU/Memory/GPU charts with historical data
6. **Logs Page** : Searchable, filterable log viewer

### Design Principles:

* Clean, modern dark theme
* Intuitive navigation
* Real-time updates (no manual refresh needed)
* Responsive design (works on tablets)
* Color-coded status indicators
* Tooltips for all metrics
* Export capabilities (PDF/CSV)

---

## 🔧 TESTING & QUALITY

### Required Tests:

* Unit tests for all core modules (>80% coverage)
* Integration tests for domain workflows
* Performance benchmarks
* Load testing (1000+ concurrent requests)
* Mock tests for external APIs
* RAG retrieval accuracy tests

### Performance Targets:

* Orchestrator: <50ms on CPU
* Intent classification: 95%+ accuracy
* Domain processing: <500ms on GPU
* Memory: <500MB idle, <16GB with 3 active domains
* Monitoring UI: 60 FPS, <100ms WebSocket latency

---

## 📦 PACKAGE DISTRIBUTION

### Requirements:

* `setup.py` with proper dependencies
* `requirements.txt` for pip
* `requirements-dev.txt` for development
* PyPI package publishing
* Conda package (optional)
* Docker image on Docker Hub
* GitHub releases with changelog

---

**Build this framework focusing on:**

1. **Beginner-friendliness** : Anyone can create domains in minutes
2. **Flexibility** : Support any model from any source
3. **Visibility** : Beautiful monitoring UI showing everything
4. **Production-ready** : Scalable, secure, well-tested
5. **Documentation** : Comprehensive guides and examples

This should be the **easiest** multi-domain SLM orchestration framework to use while being **powerful** enough for enterprise deployments.
