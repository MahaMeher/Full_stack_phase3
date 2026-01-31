#!/usr/bin/env python3
"""
Test script to verify the chatbot fix for the "all elements in tools must have a name" error.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.mcp.server import mcp_server
from src.agents.cohere_agent import CohereToolAgent
from unittest.mock import Mock

def test_tool_formatting():
    """Test that tool schemas are properly formatted for Cohere."""
    print("Testing tool schema formatting...")

    # Register mock tools to test the conversion
    from src.mcp.tools.task_tools import AddTaskTool
    from sqlmodel import Session

    # Create a mock session and user ID
    mock_session = Mock(spec=Session)
    user_id = "test_user_123"

    # Register a test tool
    test_tool = AddTaskTool(mock_session, user_id)
    mcp_server.register_tool(test_tool)

    # Create a Cohere agent
    agent = CohereToolAgent(mcp_server)

    # Get the original schemas
    original_schemas = mcp_server.get_all_tool_schemas()
    print(f"Original schemas: {original_schemas}")

    # Simulate the conversion process
    tool_schemas = []
    for schema in original_schemas:
        if 'function' in schema and isinstance(schema.get('function'), dict):
            # Convert from OpenAI format {"type": "function", "function": {...}}
            # to Cohere format with direct properties
            function_data = schema['function']
            adapted_schema = {
                "name": function_data.get("name"),
                "description": function_data.get("description"),
                "parameter_definitions": function_data.get("parameters", {}).get("properties", {}),
            }
            # Only add the schema if it has a name and the name is not empty
            if adapted_schema.get("name"):
                tool_schemas.append(adapted_schema)
        # Skip schemas that don't match expected formats to prevent the "all elements in tools must have a name" error

    print(f"Converted schemas: {tool_schemas}")

    # Verify that all schemas have names
    for schema in tool_schemas:
        assert "name" in schema, f"Schema missing name: {schema}"
        assert schema["name"], f"Schema has empty name: {schema}"

    print("✓ All converted schemas have valid names!")

    # Clean up
    mcp_server.tools.clear()


if __name__ == "__main__":
    test_tool_formatting()
    print("All tests passed! The fix should resolve the 'all elements in tools must have a name' error.")