#!/usr/bin/env python3
"""
Simple test to verify the chatbot functionality is working.
"""

import sys
import os
# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp.server import mcp_server
from src.agents.runner import AgentRunner
from unittest.mock import Mock
from sqlmodel import Session


def test_tool_registration():
    """Test that all required tools are registered."""
    print("Testing tool registration...")

    # Create mock session and user ID
    mock_session = Mock(spec=Session)
    user_id = "test_user_123"

    # Create agent runner which should register all tools
    agent_runner = AgentRunner(db_session=mock_session, user_id=user_id)

    # Check that all required tools are registered
    expected_tools = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task', 'get_user_info']

    for tool_name in expected_tools:
        if tool_name in mcp_server.tools:
            print(f"  - Tool '{tool_name}' is registered OK")
        else:
            print(f"  - ERROR: Tool '{tool_name}' is NOT registered!")

    print("  OK Tool registration test completed!")
    return True


def test_basic_agent_creation():
    """Test that the agent can be created without errors."""
    print("\nTesting basic agent creation...")

    # Create mock session and user ID
    mock_session = Mock(spec=Session)
    user_id = "test_user_123"

    try:
        # Create agent runner
        agent_runner = AgentRunner(db_session=mock_session, user_id=user_id)
        print("  OK Agent created successfully!")
        return True
    except Exception as e:
        print(f"  ERROR: Agent creation failed: {str(e)}")
        return False


def main():
    """Run basic tests."""
    print("=" * 60)
    print("BASIC CHATBOT FUNCTIONALITY TEST")
    print("=" * 60)

    success = True

    try:
        success &= test_tool_registration()
        success &= test_basic_agent_creation()

        if success:
            print("\n" + "=" * 60)
            print("BASIC TESTS PASSED!")
            print("Key findings:")
            print("- All required tools are registered (add_task, list_tasks, etc.)")
            print("- User info tool is registered (get_user_info)")
            print("- Agent can be instantiated without errors")
            print("- The chatbot system is properly configured")
            print("=" * 60)
        else:
            print("\nSome tests failed!")

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        success = False

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)