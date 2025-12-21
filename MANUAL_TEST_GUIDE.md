# Manual Testing Guide - Phase 1 & 2

## Quick Start Testing

### Option 1: Test Smart Tools Directly (Framework)

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
python
```

```python
# Import framework tools
from mdsa.tools import ToolRegistry, SmartToolExecutor
from mdsa.tools.builtin import get_default_tools

# Register all tools
registry = ToolRegistry()
for tool in get_default_tools():
    registry.register(tool)

# Create executor
executor = SmartToolExecutor(registry)

# Test queries
queries = [
    "What time is it?",
    "Calculate 50 + 75",
    "Convert 100 fahrenheit to celsius",
    "How many words are in this sentence?"
]

for query in queries:
    results = executor.detect_and_execute(query)
    if results:
        print(f"\nQuery: {query}")
        print(f"Tool: {results[0].tool_name}")
        print(f"Result: {results[0].result}")
    else:
        print(f"\nQuery: {query}")
        print("No tools detected")
```

### Option 2: Test Through Chatbot

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
python
```

```python
from chatbot_app.chatbot import MDSAChatbot

# Initialize chatbot
chatbot = MDSAChatbot(
    model_name="gpt2",
    max_models=2,
    enable_rag=False,   # Disable RAG for faster testing
    enable_tools=True   # Enable smart tools
)

# Test queries
test_queries = [
    "What time is it right now?",
    "Calculate 25 plus 37 for me",
    "Convert 100 celsius to fahrenheit",
]

for query in test_queries:
    print(f"\n{'='*70}")
    print(f"Query: {query}")
    print('-'*70)

    response = chatbot.chat(query, use_tools=True, use_rag=False)

    print(f"Domain: {response['domain']}")
    print(f"Status: {response['status']}")

    if 'tool_results' in response and response['tool_results']:
        print(f"Tools used: {[t['tool_name'] for t in response['tool_results']]}")

    print(f"\nResponse:")
    print(response['response'])
```

### Option 3: Run Comprehensive Test Script

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
python test_integration_phase1_2.py
```

## What to Look For

### ✅ Phase 1 Success Indicators:
- Tools detected for relevant queries
- Tool execution results shown
- No errors like "Tool not found"
- Execution time < 50ms for tools

### ✅ Phase 2 Success Indicators:
- Model configured as "microsoft/phi-2"
- Device set to "cpu"
- Temperature: 0.3
- Max tokens: 256
- CPU optimizations applied in logs
- Responses are coherent (not gibberish)
- No hallucination warnings

## Test Queries by Category

### Time Queries (get_current_time tool):
- "What time is it?"
- "What's the current date?"
- "Tell me the time right now"

### Math Queries (calculate tool):
- "Calculate 15 + 20"
- "What is 50 times 3?"
- "Compute 100 minus 45"

### Unit Conversion (convert_units tool):
- "Convert 100 celsius to fahrenheit"
- "Convert 10 km to miles"
- "Convert 150 pounds to kg"

### Word Count (word_count tool):
- "Count words in this sentence"
- "How many words: Hello world this is a test"

## Expected Results

### Tool Detection:
```
Query: 'What time is it?'
  Detected: get_current_time
  Result: 2025-12-02 21:14:12
  Success: True
  Status: PASS
```

### Chatbot Integration:
```
Query: Calculate 25 plus 37 for me
Domain: support
Status: success
Tools used: ['calculate']
Result: Result: 62

Response: [Response includes the calculation result]
```

## Configuration Verification

### Check Phi-2 Configuration:
```python
from mdsa.domains.config import get_predefined_domain

for domain in ['finance', 'medical', 'support', 'technical']:
    config = get_predefined_domain(domain)
    print(f"\n{domain}:")
    print(f"  Model: {config.model_name}")  # Should be microsoft/phi-2
    print(f"  Device: {config.device}")     # Should be cpu
    print(f"  Temp: {config.temperature}")  # Should be 0.3
    print(f"  Tokens: {config.max_tokens}") # Should be 256
```

### Check Tool Registration:
```python
from mdsa.tools import ToolRegistry
from mdsa.tools.builtin import get_default_tools

registry = ToolRegistry()
for tool in get_default_tools():
    registry.register(tool)

print(f"Registered tools: {len(registry)}")  # Should be 7
print(f"Tool names: {registry.list_tools()}")
```

## Troubleshooting

### If tools don't detect:
1. Check query keywords match detection patterns
2. Verify tools are registered: `len(chatbot.executor.tool_registry) == 7`
3. Check enable_tools=True in chat() call

### If model fails to load:
1. Check internet connection (first download)
2. Verify 16GB RAM available
3. Check disk space for model cache (~5.4GB)

### If responses are gibberish:
1. Verify Phi-2 configured (not GPT-2)
2. Check temperature is 0.3 (not 0.7)
3. Verify repetition_penalty=2.5

## Next Steps

After verifying Phase 1 & 2:
- **Phase 3**: Authentication & Rate Limiting
- **Phase 4**: Async support for concurrency
- **Phase 5**: Comprehensive test suite
- **Phase 6**: UI redesign with visualizations
- **Phase 7**: Final documentation

## Quick Health Check

Run this to verify everything:
```bash
python test_phase2.py          # Phase 2 verification
python test_integration_phase1_2.py  # Full integration test
```

Both should show "PASS" for all tests.
