from mdsa.tools import ToolRegistry, SmartToolExecutor
from mdsa.tools.builtin import get_default_tools

registry = ToolRegistry()
for tool in get_default_tools():
    registry.register(tool)

executor = SmartToolExecutor(registry)
results = executor.detect_and_execute("What is the GMT timenow?")
print(results[0].result)  # Shows current time