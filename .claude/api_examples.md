
# MDSA Framework - API Examples

## Basic Usage

### Initialize Framework

```python
from mdsa import mdsa

mdsa = mdsa()
# or with config
mdsa = mdsa("path/to/config.yaml")
```

### Create Domain - Simple

```python
from mdsa import SimpleDomainAPI

# Absolute simplest
domain = SimpleDomainAPI.create_domain("my_domain", "gpt2")
mdsa.register_domain(domain)
```

### Create Domain - With RAG

```python
domain = SimpleDomainAPI.create_rag_domain(
    "support",
    "microsoft/DialoGPT-medium",
    ["./docs/faq.txt", "./docs/policies/"]
)
mdsa.register_domain(domain)
```

### Create Domain - Advanced

```python
from mdsa.domains import DomainBuilder

domain = DomainBuilder.from_dict({
    "domain": {
        "name": "finance",
        "models": [{
            "source": "huggingface",
            "path": "meta-llama/Llama-2-7b-hf",
            "quantization": "8bit"
        }],
        "rag": {
            "enabled": True,
            "documents": [{"path": "./finance_docs/"}]
        }
    }
})
mdsa.register_domain(domain)
```

### Process Request

```python
# Synchronous
response = mdsa.process(
    "What is my account balance?",
    context={"user_id": "123"}
)

# Asynchronous
response = await mdsa.process_async(
    "Transfer $100",
    domain="finance"
)
```

### RAG Usage

```python
from mdsa.rag import LocalRAG

rag = LocalRAG("my_domain")
rag.add_documents(["Doc 1", "Doc 2"])
rag.add_from_directory("./docs/")

results = rag.retrieve("my query", n_results=5)
```

### Model Management

```python
from mdsa.models import ModelManager

manager = ModelManager()

# Load from different sources
manager.load_model("m1", "huggingface", "gpt2")
manager.load_model("m2", "ollama", "llama2:7b")
manager.load_model("m3", "local", "/path/to/model.bin")
manager.load_model("m4", "github", "user/repo/model.bin")

# Unload when done
manager.unload_model("m1")
```

### Monitoring

```python
# Start monitoring server
mdsa.start_monitoring(port=8000)
# Visit http://localhost:8000/monitor
```

## Advanced Features

### Model-to-Model Communication

```python
from mdsa.communication import SLMBridge

bridge = SLMBridge(mdsa.message_bus)
bridge.connect_models("finance_model", "risk_model")

response = await bridge.send_to_model(
    "finance_model",
    "risk_model",
    {"action": "assess_risk", "amount": 10000}
)
```

### Custom Validation

```python
from mdsa.validation import RuleValidator

validator = RuleValidator()
validator.add_rule("amount <= available_budget")
validator.add_rule("user.role in ['manager', 'admin']")

is_valid = validator.validate(context, rules)
```

### MCP Integration

```python
from mdsa.integrations import MCPManager

mcp = MCPManager()
await mcp.connect_server("tools", "http://localhost:8000", "api_key")
result = await mcp.call_tool("tools", "database_query", {"sql": "SELECT ..."})
```
