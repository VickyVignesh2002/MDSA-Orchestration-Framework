"""
MDSA Framework Tool System

This module provides intelligent tool detection and execution capabilities
for the MDSA framework. It includes:

- ToolRegistry: Central registry for managing tools
- SmartToolExecutor: Semantic tool detection from queries
- Tool: Base class for creating custom tools
- ToolResult: Standardized tool execution result

The smart tool system works by detecting tool needs from query semantics
rather than relying on models to generate specific output formats.
This makes it model-agnostic and works with any LLM (GPT-2, Phi-2, Llama, etc.).

Example:
    from mdsa.tools import ToolRegistry, SmartToolExecutor

    # Create registry and executor
    registry = ToolRegistry()
    executor = SmartToolExecutor(registry)

    # Detect and execute tools from a query
    results = executor.detect_and_execute("What time is it?")
"""

from .base import Tool, ToolResult
from .registry import ToolRegistry
from .smart_executor import SmartToolExecutor

__all__ = [
    'Tool',
    'ToolResult',
    'ToolRegistry',
    'SmartToolExecutor',
]

__version__ = '1.0.0'
