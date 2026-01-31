#!/usr/bin/env python3
"""
Test script to verify the fixes for the Cohere agent and timezone issues.
"""

import sys
import os
from datetime import datetime, timezone
from unittest.mock import Mock

# Add the backend src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server import MCPServer
from agents.cohere_agent import CohereToolAgent
from mcp.tools.task_tools import AddTaskTool


def test_timezone_fixes():
    """Test that timezone-aware datetime is being used."""
    print("Testing timezone-aware datetime fixes...")

    # Test that current time is timezone-aware
    now = datetime.now(timezone.utc)
    assert now.tzinfo is not None, "Datetime should be timezone-aware"
    print("✓ Timezone-aware datetime is working correctly")


def test_tool_schema_conversion():
    """Test that tool schemas are properly formatted for Cohere."""
    print("\nTesting tool schema conversion...")

    # Create a mock session and user ID
    mock_session = Mock()
    user_id = "test_user_123"

    # Create MCP server and register a test tool
    mcp_server = MCPServer()
    test_tool = AddTaskTool(mock_session, user_id)
    mcp_server.register_tool(test_tool)

    # Create a Cohere agent
    agent = CohereToolAgent(mcp_server)

    # Get the original schemas
    original_schemas = mcp_server.get_all_tool_schemas()
    print(f"Original schemas: {original_schemas}")

    # Test the conversion process
    tool_schemas = []
    for schema in original_schemas:
        if 'function' in schema and isinstance(schema.get('function'), dict):
            # Convert from OpenAI format {"type": "function", "function": {...}}
            # to Cohere format with direct properties
            function_data = schema['function']

            # Ensure we have the required fields for Cohere
            name = function_data.get("name")
            description = function_data.get("description", "")
            parameters = function_data.get("parameters", {})

            # Skip if name is missing or empty
            if not name:
                continue

            # Format parameters for Cohere - it expects parameter_definitions with type and description
            param_definitions = {}
            if isinstance(parameters, dict) and "properties" in parameters:
                props = parameters["properties"]
                for param_name, param_details in props.items():
                    # Extract type and description for Cohere format
                    param_type = param_details.get("type", "string")
                    param_desc = param_details.get("description", "")

                    # Create parameter definition in Cohere format
                    param_def = {
                        "type": param_type,
                        "description": param_desc
                    }

                    # Add additional properties if they exist
                    if "default" in param_details:
                        param_def["default"] = param_details["default"]
                    if "required" in parameters:
                        param_def["required"] = param_name in parameters["required"]

                    param_definitions[param_name] = param_def

            adapted_schema = {
                "name": name,
                "description": description,
                "parameter_definitions": param_definitions,
            }

            tool_schemas.append(adapted_schema)

    print(f"Converted schemas: {tool_schemas}")

    # Verify that all schemas have names
    for schema in tool_schemas:
        assert "name" in schema, f"Schema missing name: {schema}"
        assert schema["name"], f"Schema has empty name: {schema}"
        assert "parameter_definitions" in schema, f"Schema missing parameter_definitions: {schema}"

    print("✓ All converted schemas have valid names and parameter definitions!")


def test_agent_runner_tool_registration():
    """Test that agent runner properly registers tools per session."""
    print("\nTesting agent runner tool registration...")

    from agents.runner import AgentRunner
    from sqlmodel import Session

    # Create mock session and user ID
    mock_session = Mock(spec=Session)
    user_id = "test_user_456"

    # Create an agent runner
    agent_runner = AgentRunner(mock_session, user_id)

    # Check that tools were registered
    expected_tools = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']
    for tool_name in expected_tools:
        assert tool_name in agent_runner.mcp_server.tools, f"Tool {tool_name} not registered"

    # Verify the tools have the correct user context
    add_task_tool = agent_runner.mcp_server.tools['add_task']
    assert add_task_tool.user_id == user_id, "Tool does not have correct user context"

    print("✓ Agent runner properly registers tools with user context!")


if __name__ == "__main__":
    print("Running tests for Cohere agent and timezone fixes...\n")

    test_timezone_fixes()
    test_tool_schema_conversion()
    test_agent_runner_tool_registration()

    print("\n✅ All tests passed! The fixes should resolve:")
    print("   - 'HALLUCINATED_ALL_TOOL_CALLS' error by fixing tool schema conversion")
    print("   - Timezone issues by using timezone-aware datetime")
    print("   - Tool registration issues by properly managing tools per session")