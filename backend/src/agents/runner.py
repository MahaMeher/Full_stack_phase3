"""
Agent runner responsible for executing the Cohere agent with proper context management.
Manages conversation state, tool registration, and execution flow.
"""

from typing import Dict, Any, List
from sqlmodel import Session
from ..mcp.server import mcp_server
from .cohere_agent import CohereToolAgent
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..services.task_service import TaskService


class AgentRunner:
    """
    Manages the execution of the AI agent with conversation context and tool integration.
    """

    def __init__(self, db_session: Session, user_id: str):
        """
        Initialize the agent runner with database session and user context.

        Args:
            db_session: Database session for operations
            user_id: ID of the authenticated user
        """
        self.db_session = db_session
        self.user_id = user_id
        self.conversation_service = ConversationService
        self.message_service = MessageService
        self.task_service = TaskService

        # Initialize the Cohere agent with the MCP server
        self.agent = CohereToolAgent(mcp_server)

        # Register all task tools with the MCP server for this user session
        self._register_user_specific_tools()

    def _register_user_specific_tools(self):
        """
        Register user-scoped tools with the MCP server for the current user session.
        """
        from ..mcp.tools.task_tools import AddTaskTool, ListTasksTool, UpdateTaskTool, CompleteTaskTool, DeleteTaskTool
        from ..mcp.tools.user_info_tool import GetUserInfoTool

        # Clear any existing tools for this session to avoid conflicts
        # This ensures each agent runner has fresh tools with the correct user context
        tool_names = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task', 'get_user_info']
        for name in tool_names:
            if name in mcp_server.tools:
                del mcp_server.tools[name]

        # Register tools with the current user context
        mcp_server.register_tool(AddTaskTool(self.db_session, self.user_id))
        mcp_server.register_tool(ListTasksTool(self.db_session, self.user_id))
        mcp_server.register_tool(UpdateTaskTool(self.db_session, self.user_id))
        mcp_server.register_tool(CompleteTaskTool(self.db_session, self.user_id))
        mcp_server.register_tool(DeleteTaskTool(self.db_session, self.user_id))
        mcp_server.register_tool(GetUserInfoTool(self.db_session, self.user_id))

    def run_conversation(self, user_message: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Run a conversation step with the AI agent.

        Args:
            user_message: The message from the user
            conversation_id: Optional conversation ID (creates new if not provided)

        Returns:
            Dict containing the AI response and any tool execution results
        """
        # Get or create conversation
        if conversation_id:
            conversation = self.conversation_service.get_conversation_by_id(self.db_session, conversation_id)
            if not conversation:
                # Create new conversation if ID not found
                conversation = self.conversation_service.create_conversation(self.db_session, self.user_id)
        else:
            conversation = self.conversation_service.create_conversation(self.db_session, self.user_id)

        conversation_id = conversation.id

        # Save user message to database
        try:
            self.message_service.create_message(
                self.db_session,
                conversation_id=conversation_id,
                role="user",
                content=user_message
            )
        except Exception as e:
            # If we can't save the user message, the conversation is compromised
            try:
                self.db_session.rollback()
            except:
                pass
            raise

        # Get conversation history for context
        try:
            conversation_history = self.message_service.get_messages_by_conversation(self.db_session, conversation_id)

            # Format history for the agent
            formatted_history = [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in conversation_history
            ]
        except Exception as e:
            # If getting history fails, create minimal history
            formatted_history = []

        # Run the agent - this may execute tools that use the same session
        # Wrap in try-catch to ensure any tool execution errors don't break the session
        try:
            result = self.agent.run_with_native_tools(
                user_input=user_message,
                conversation_history=formatted_history[:-1]  # Exclude current user message
            )

            # Only apply safety checks for update requests, not completion requests
            user_input_lower = user_message.lower()
            update_keywords = ['update', 'change', 'modify', 'rename', 'alter']
            has_update_intent = any(keyword in user_input_lower for keyword in update_keywords)

            # Only apply this safety check if the AI response contains definitive language about updating without any tools
            # Don't apply this check if the AI is asking for more information (like asking to list tasks)
            if has_update_intent and 'task' in user_input_lower and \
               result.get("has_tool_calls", False) == False and \
               result.get("tool_calls", []) == [] and \
               any(phrase in result.get("response", "").lower() for phrase in ['task updated', 'has been updated', 'updated successfully', 'updated the task']) and \
               not any(phrase in result.get("response", "").lower() for phrase in ['need to know', 'which specific task', 'list your tasks', 'be more specific']):

                # The AI claimed to update a task without calling the update tool
                result["response"] = "I heard your request to update a task, but I need to know which specific task to update. Could you please list your tasks first or be more specific about which task you want to update? For example: 'Update the task buy groceries to say buy organic groceries'."
                result["has_tool_calls"] = False
                result["tool_calls"] = []
                result["tool_results"] = []
            # For completion requests, don't apply the same aggressive safety check
            # Let the AI handle completion requests naturally

            # Check if there were any errors in tool results
            for tool_result in result.get("tool_results", []):
                if tool_result.get("result", {}).get("success") == False:
                    error_msg = tool_result.get("result", {}).get("error", "Unknown error")

                    # Check if this is the specific UUID parsing error
                    if "invalid input syntax for type uuid" in error_msg.lower():
                        # This is likely a parsing error where the AI mistook natural language for a task ID
                        enhanced_response = "I'm sorry, I had trouble understanding which task you wanted to modify. Could you please specify the task more directly? For example: 'Complete the task going home' or 'Mark going home as completed'."
                        result["response"] = enhanced_response
                    else:
                        # Enhance the response with specific error information
                        enhanced_response = f"I'm sorry, I encountered an error with your request: {error_msg}. Please make sure you're referring to the correct task."
                        result["response"] = enhanced_response
        except Exception as e:
            # If tool execution fails, ensure session is clean for message saving
            try:
                self.db_session.rollback()
            except:
                pass  # Ignore rollback errors
            # Create a result with an error message
            result = {
                "response": "I'm sorry, I was unable to process your request. Please try again or be more specific with your task management request.",
                "tool_calls": [],
                "tool_results": [],
                "has_tool_calls": False
            }

        # Commit any changes from tool executions before saving the response
        try:
            self.db_session.commit()
        except Exception:
            # If commit fails, rollback and continue
            try:
                self.db_session.rollback()
            except:
                pass

        # Save AI response to database
        try:
            self.message_service.create_message(
                self.db_session,
                conversation_id=conversation_id,
                role="assistant",
                content=result["response"],
                metadata_json=None  # Could store tool call info here if needed
            )
        except Exception as e:
            # If saving the response fails, try once more with a simpler message
            # BUT we should NOT rollback here as it will undo tool operations that happened earlier
            try:
                # Just save the simpler message without rolling back previous operations
                self.message_service.create_message(
                    self.db_session,
                    conversation_id=conversation_id,
                    role="assistant",
                    content="I'm sorry, I encountered an issue processing your request.",
                    metadata_json=None
                )
            except:
                # If all else fails, at least don't crash the entire request
                # Any previous tool operations remain committed
                pass

        # Commit the final state
        try:
            self.db_session.commit()
        except Exception:
            try:
                self.db_session.rollback()
            except:
                pass

        # Update conversation timestamp
        try:
            self.conversation_service.update_conversation_timestamp(self.db_session, conversation_id)
        except:
            # If timestamp update fails, try to rollback
            try:
                self.db_session.rollback()
            except:
                pass  # Ignore rollback errors

        # Return the complete result
        return {
            "response": result["response"],
            "conversation_id": conversation_id,
            "tool_calls": result["tool_calls"],
            "tool_results": result["tool_results"],
            "has_tool_calls": result["has_tool_calls"]
        }

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve the conversation history for a specific conversation.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            List of messages in the conversation
        """
        messages = self.message_service.get_messages_by_conversation(self.db_session, conversation_id)

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata_json
            }
            for msg in messages
        ]