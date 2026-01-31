"""
MCP (Model Context Protocol) Server Implementation
Acts as the single interface for all task operations in the AI chatbot system.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolCallResult(BaseModel):
    """Represents the result of a tool call."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    tool_name: str


class MCPTool(ABC):
    """Abstract base class for MCP tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON Schema for the tool's parameters."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> ToolCallResult:
        """Execute the tool with the given parameters."""
        pass


class MCPServer:
    """MCP Server that manages and executes tools."""

    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}

    def register_tool(self, tool: MCPTool) -> None:
        """Register a new tool with the server."""
        self.tools[tool.name] = tool

    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a specific tool."""
        if tool_name not in self.tools:
            return None

        tool = self.tools[tool_name]
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        }

    def get_all_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all registered tools."""
        schemas = []
        for tool_name in self.tools:
            schema = self.get_tool_schema(tool_name)
            if schema:
                schemas.append(schema)
        return schemas

    def execute_tool(self, tool_name: str, **kwargs) -> ToolCallResult:
        """Execute a tool by name with the given arguments."""
        if tool_name not in self.tools:
            return ToolCallResult(
                success=False,
                error=f"Tool '{tool_name}' not found",
                tool_name=tool_name
            )

        tool = self.tools[tool_name]
        return tool.execute(**kwargs)

    def execute_multiple_tools(self, tool_calls: List[Dict[str, Any]]) -> List[ToolCallResult]:
        """Execute multiple tools in sequence."""
        results = []
        for call in tool_calls:
            if "name" not in call or "arguments" not in call:
                results.append(ToolCallResult(
                    success=False,
                    error="Invalid tool call format: missing name or arguments",
                    tool_name="unknown"
                ))
                continue

            tool_name = call["name"]
            arguments = call.get("arguments", {})

            # If arguments is a string, parse it as JSON
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    results.append(ToolCallResult(
                        success=False,
                        error=f"Invalid JSON in arguments: {arguments}",
                        tool_name=tool_name
                    ))
                    continue

            result = self.execute_tool(tool_name, **arguments)
            results.append(result)

        return results


# Global MCP Server instance
mcp_server = MCPServer()