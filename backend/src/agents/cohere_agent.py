"""
Cohere-powered AI Agent that follows OpenAI Agents SDK architectural patterns.
Implements natural language understanding and tool selection for task management.
"""

import json
from typing import Dict, Any, List, Optional
from cohere import Client
from datetime import datetime
from ..config.settings import settings
from ..mcp.server import MCPServer, ToolCallResult


class CohereAgent:
    """
    Cohere-powered agent that interprets natural language and selects appropriate MCP tools.
    Mimics OpenAI Agents SDK patterns while using Cohere as the underlying LLM.
    """

    def __init__(self, mcp_server: MCPServer):
        """
        Initialize the Cohere agent with MCP server access.

        Args:
            mcp_server: MCP server instance for tool execution
        """
        self.client = Client(api_key=settings.cohere_api_key)
        self.mcp_server = mcp_server
        self.model = "command-r-08-2024"  # Using Cohere's current R-series model with date version

    def _format_system_instructions(self) -> str:
        """
        Format system instructions for task management.

        Returns:
            str: System instructions for the agent
        """
        return """
        You are an AI assistant that helps users manage their tasks through natural language.
        You must use the available tools to perform any task operations.
        Do not attempt to modify data directly - always use the appropriate tools.

        CRITICAL: When a user asks you to perform an action, DO IT IMMEDIATELY without asking for confirmation.
        Only ask for clarification if the request is genuinely ambiguous, not just to confirm what was requested.

        For example:
        - If user says "mark the task buy laptop as completed", immediately execute complete_task
        - If user says "update the task buy laptop to buy phone", immediately execute update_task
        - If user says "delete the task buy laptop", immediately execute delete_task
        - Only ask for clarification if you can't identify which task they mean

        FOR UPDATE TASKS SPECIFICALLY:
        - When user says "update task X", "change task X", "modify task X", or similar, ALWAYS call update_task
        - If user provides new title or description, include it in the update_task call
        - If user says "update the task to X" or "update it to X", call update_task with new title/description
        - DO NOT generate responses claiming tasks were updated without calling update_task tool

        For casual conversation (greetings, small talk, general questions), respond naturally
        and use the get_user_info tool to personalize responses when appropriate.
        Only use task-related tools when the user explicitly requests task operations
        like adding, listing, updating, completing, or deleting tasks.

        When parsing user requests, pay attention to natural language constructs like "as well",
        "too", "also", etc. These typically mean to apply the same action or include the same
        parameters as mentioned earlier in the sentence, not to refer to a task by that name.

        For example, if a user says "update task X and update the title and description as well",
        you should update task X with the new title and description, not look for a task named "as well".

        Available tools:
        - add_task: Add a new task with title and optional description
        - list_tasks: List tasks with optional filtering by completion status
        - update_task: Update an existing task's title, description, or completion status
        - complete_task: Mark a task as completed
        - delete_task: Delete a task
        - get_user_info: Retrieve the current user's information including name, email, and other profile details

        Always use the most appropriate tool for the user's request.
        When listing tasks, provide clear and organized information.
        When updating tasks, execute the changes immediately without asking for confirmation.
        For personalization and greetings, use get_user_info to get user details.
        For general conversation, respond naturally and appropriately use get_user_info when relevant.

        Remember: Execute user requests immediately. Don't ask "Would you like me to..." - just do what they asked.
        CRITICAL: When user asks to update a task, you MUST call the update_task tool. Do not fabricate responses.
        """

    def _prepare_conversation_history(self, messages: List[Dict[str, str]]) -> str:
        """
        Prepare conversation history for the Cohere model.

        Args:
            messages: List of messages in the conversation

        Returns:
            str: Formatted conversation history
        """
        history = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history += f"{role.capitalize()}: {content}\n"
        return history

    def _parse_tool_calls_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse tool calls from the model response.
        This is a simplified implementation - in practice, you'd use Cohere's tool calling capabilities
        or implement a more sophisticated parsing mechanism.

        Args:
            response_text: Raw response from the model

        Returns:
            List of parsed tool calls
        """
        # Look for patterns indicating tool usage in the response
        tool_calls = []

        # Simple pattern matching for demonstration - in production, use Cohere's tool calling
        import re

        # Pattern for add_task: "add_task(title='...', description='...')"
        add_pattern = r'add_task\((.*)\)'
        add_matches = re.findall(add_pattern, response_text)
        for match in add_matches:
            try:
                # Parse arguments assuming they're in key=value format
                args = self._parse_function_args(match)
                tool_calls.append({
                    "name": "add_task",
                    "arguments": args
                })
            except:
                pass

        # Pattern for list_tasks: "list_tasks(filter_completed=...)"
        list_pattern = r'list_tasks\((.*)\)'
        list_matches = re.findall(list_pattern, response_text)
        for match in list_matches:
            try:
                args = self._parse_function_args(match)
                tool_calls.append({
                    "name": "list_tasks",
                    "arguments": args
                })
            except:
                pass

        # Pattern for complete_task: "complete_task(task_id='...')"
        complete_pattern = r'complete_task\((.*)\)'
        complete_matches = re.findall(complete_pattern, response_text)
        for match in complete_matches:
            try:
                args = self._parse_function_args(match)
                tool_calls.append({
                    "name": "complete_task",
                    "arguments": args
                })
            except:
                pass

        # Pattern for update_task: "update_task(task_id='...', title='...', ...)"
        update_pattern = r'update_task\((.*)\)'
        update_matches = re.findall(update_pattern, response_text)
        for match in update_matches:
            try:
                args = self._parse_function_args(match)
                tool_calls.append({
                    "name": "update_task",
                    "arguments": args
                })
            except:
                pass

        # Pattern for delete_task: "delete_task(task_id='...')"
        delete_pattern = r'delete_task\((.*)\)'
        delete_matches = re.findall(delete_pattern, response_text)
        for match in delete_matches:
            try:
                args = self._parse_function_args(match)
                tool_calls.append({
                    "name": "delete_task",
                    "arguments": args
                })
            except:
                pass

        return tool_calls

    def _parse_function_args(self, args_str: str) -> Dict[str, Any]:
        """
        Parse function arguments from a string representation.
        This is a simplified parser for demonstration purposes.

        Args:
            args_str: String containing function arguments

        Returns:
            Dict of parsed arguments
        """
        args = {}
        # Split by comma, but be careful with nested quotes
        parts = args_str.split(',')
        for part in parts:
            part = part.strip()
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip().strip("'\"")  # Remove quotes
                # Try to convert to appropriate type
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                args[key] = value
        return args

    def run(self, user_input: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent with user input and conversation history.

        Args:
            user_input: The user's natural language request
            conversation_history: Previous messages in the conversation

        Returns:
            Dict containing the response and any tool calls made
        """
        if conversation_history is None:
            conversation_history = []

        # Prepare the full context
        full_context = self._prepare_conversation_history(conversation_history)
        full_context += f"User: {user_input}\nAssistant:"

        # Get available tool schemas
        tool_schemas = self.mcp_server.get_all_tool_schemas()

        # Call Cohere with the context and tools
        try:
            response = self.client.chat(
                message=full_context,
                model=self.model,
                preamble=self._format_system_instructions(),
                tools=tool_schemas,
                # Enable tool calling - this is where Cohere's native tool calling would be used
            )

            # Extract response text
            response_text = response.text

            # Attempt to parse any tool calls from the response
            # In a real implementation, Cohere would return structured tool calls
            tool_calls = self._parse_tool_calls_from_response(response_text)

            # Execute any identified tool calls
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    result = self.mcp_server.execute_tool(
                        tool_call["name"],
                        **tool_call.get("arguments", {})
                    )
                    tool_results.append({
                        "tool_call_id": tool_call.get("id"),
                        "result": result.dict() if hasattr(result, 'dict') else {"success": result.success, "data": result.data, "error": result.error}
                    })

            return {
                "response": response_text,
                "tool_calls": tool_calls,
                "tool_results": tool_results,
                "has_tool_calls": len(tool_calls) > 0
            }

        except Exception as e:
            # Return error response
            return {
                "response": f"I encountered an error processing your request: {str(e)}. Please try again.",
                "tool_calls": [],
                "tool_results": [],
                "has_tool_calls": False,
                "error": str(e)
            }


# Enhanced version that uses Cohere's native tool calling when available
class CohereToolAgent(CohereAgent):
    """
    Enhanced Cohere agent that leverages Cohere's native tool calling capabilities.
    """

    def run_with_native_tools(self, user_input: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent using Cohere's native tool calling capabilities.

        Args:
            user_input: The user's natural language request
            conversation_history: Previous messages in the conversation

        Returns:
            Dict containing the response and any tool calls made
        """
        if conversation_history is None:
            conversation_history = []

        # Resolve context references in user input using conversation history
        resolved_input = self._resolve_context_references(user_input, conversation_history)

        # Check if this is an update task request and handle it directly
        update_result = self._handle_direct_update_request(resolved_input)
        if update_result:
            return update_result

        # Check if this is a complete task request and handle it directly
        complete_result = self._handle_direct_complete_request(resolved_input)
        if complete_result:
            return complete_result

        # Check if this is a delete task request and handle it directly
        delete_result = self._handle_direct_delete_request(resolved_input)
        if delete_result:
            return delete_result

        # Pre-process the user input to handle specific patterns before sending to AI
        processed_input = self._preprocess_user_input(resolved_input)

        # Check if the input is a casual conversation that doesn't require tools
        if self._is_general_conversation(processed_input):
            # Handle general conversation without tools, but allow for user info when appropriate
            # Check if user is asking for their information
            lower_input = user_input.lower().strip()


            user_info_patterns = [
                'who am i', 'what is my name', 'what is my email', 'tell me about me',
                'my information', 'my profile', 'show my details', 'user details'
            ]

            requires_user_info = any(pattern in lower_input for pattern in user_info_patterns)

            if requires_user_info:
                # Execute get_user_info tool to get user details
                user_info_result = self.mcp_server.execute_tool('get_user_info')

                if user_info_result.success and user_info_result.data:
                    user_info = user_info_result.data
                    user_name = user_info.get('name', user_info.get('email', 'User'))

                    # Craft a personalized response
                    if 'who am i' in lower_input or 'what is my name' in lower_input:
                        response_text = f"You are {user_name}. Nice to see you again!"
                    elif 'what is my email' in lower_input:
                        user_email = user_info.get('email', 'unknown')
                        response_text = f"Your email address is {user_email}."
                    elif 'tell me about me' in lower_input or 'my profile' in lower_input:
                        response_text = f"Your name is {user_name} and your email is {user_info.get('email', 'unknown')}."
                    else:
                        response_text = f"Hello {user_name}! I'm your AI task assistant. You can ask me to add, list, update, or complete tasks."

                    return {
                        "response": response_text,
                        "tool_calls": [{"name": "get_user_info", "parameters": {}}],
                        "tool_results": [{
                            "tool_call_id": None,
                            "name": "get_user_info",
                            "parameters": {},
                            "result": user_info_result.dict() if hasattr(user_info_result, 'dict') else {"success": user_info_result.success, "data": user_info_result.data, "error": user_info_result.error}
                        }],
                        "has_tool_calls": True
                    }
                else:
                    # If user info tool fails, respond generically
                    try:
                        response = self.client.chat(
                            message=user_input,
                            model=self.model,
                            preamble=self._format_system_instructions()
                        )

                        return {
                            "response": response.text,
                            "tool_calls": [],
                            "tool_results": [],
                            "has_tool_calls": False
                        }
                    except Exception as e:
                        return {
                            "response": f"Hello! I'm your AI task assistant. You can ask me to add, list, update, or complete tasks.",
                            "tool_calls": [],
                            "tool_results": [],
                            "has_tool_calls": False,
                            "error": str(e)
                        }
            else:
                # Handle general conversation without tools
                try:
                    response = self.client.chat(
                        message=user_input,
                        model=self.model,
                        preamble=self._format_system_instructions()
                    )

                    return {
                        "response": response.text,
                        "tool_calls": [],
                        "tool_results": [],
                        "has_tool_calls": False
                    }
                except Exception as e:
                    return {
                        "response": f"I'm doing well, thank you for asking! How can I help you today?",
                        "tool_calls": [],
                        "tool_results": [],
                        "has_tool_calls": False,
                        "error": str(e)
                    }

        # Prepare the full context
        full_context = self._prepare_conversation_history(conversation_history)
        full_context += f"\nUser: {processed_input}"

        # Get available tool schemas and adapt for Cohere format
        original_schemas = self.mcp_server.get_all_tool_schemas()

        # Cohere expects tools in a specific format - adapt from OpenAI format
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

        try:
            # Check if this is an update request that the AI might miss
            # First, let's manually detect if this is an update request before calling the AI
            import re

            # Pattern detection for update requests
            update_patterns = [
                r'update\s+the\s+task\s+na[m]{1,3}ely\s+(.+?)\s+to\s+(.+)',  # Handles "namely", "namley", etc.
                r'update\s+the\s+task\s+for\s+me\s+na[m]{1,3}ely\s+(.+?)\s+to\s+(.+)',  # For "update the task for me namely/namley"
                r'update\s+the\s+task\s+(.+?)\s+to\s+(.+)',
                r'update\s+(.+?)\s+to\s+(.+)',
                r'modify\s+the\s+task\s+(.+?)\s+to\s+(.+)',
                r'modify\s+(.+?)\s+to\s+(.+)',
                r'change\s+the\s+task\s+(.+?)\s+to\s+(.+)',
                r'change\s+(.+?)\s+to\s+(.+)',
            ]

            manual_update_detection = None
            for pattern in update_patterns:
                match = re.search(pattern, processed_input.lower())
                if match:
                    manual_update_detection = match
                    break

            # If we detect an update pattern manually, ensure the AI calls the update tool
            if manual_update_detection:
                # First, get the user's tasks to see if the target task exists
                list_result = self.mcp_server.execute_tool('list_tasks', filter_completed=None)

                if list_result.success and list_result.data:
                    # Extract the task name and new value from the match
                    task_name = manual_update_detection.group(1).strip()
                    new_value = manual_update_detection.group(2).strip()

                    # Look for the task in the user's task list
                    target_task = None
                    for task in list_result.data:
                        if task_name.lower() in task.get('title', '').lower() or task.get('title', '').lower() in task_name.lower():
                            target_task = task
                            break

                    # If we found the target task, call the update tool directly
                    if target_task:
                        # Determine if the new value contains both title and description
                        new_title = new_value
                        new_description = None

                        # Check if there's a description part in the original request
                        desc_match = re.search(r'to\s+(.+?)\s+and\s+add\s+description\s+(.+)', processed_input.lower())
                        if desc_match:
                            new_title = desc_match.group(1).strip()
                            new_description = desc_match.group(2).strip()

                        # Prepare update parameters
                        update_params = {
                            "task_id": target_task['id'],
                            "title": new_title
                        }

                        if new_description:
                            update_params["description"] = new_description

                        # Execute the update tool directly
                        update_result = self.mcp_server.execute_tool('update_task', **update_params)

                        # Format response for successful update
                        if update_result.success and update_result.data:
                            return {
                                "response": f"Task '{target_task['title']}' has been updated successfully.\n\nNew Title: {update_result.data.get('title', 'N/A')}\nNew Description: {update_result.data.get('description', 'N/A')}",
                                "tool_calls": [{"name": "update_task", "parameters": update_params}],
                                "tool_results": [{
                                    "tool_call_id": None,
                                    "name": "update_task",
                                    "parameters": update_params,
                                    "result": update_result.dict() if hasattr(update_result, 'dict') else {"success": update_result.success, "data": update_result.data, "error": update_result.error}
                                }],
                                "has_tool_calls": True
                            }

            # Use Cohere's chat endpoint with tools
            # Only pass tools if we have valid ones to avoid API errors
            if tool_schemas:  # Only pass tools if the array is not empty
                response = self.client.chat(
                    message=processed_input,
                    model=self.model,
                    preamble=self._format_system_instructions(),
                    tools=tool_schemas
                    # Removed force_single_step to avoid the hallucination issue
                )

                # Process tool calls if any
                tool_results = []
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    # Execute each tool call and collect results
                    executed_tool_results = []

                    for tool_call in response.tool_calls:
                        # Special handling for tasks that might use names instead of IDs
                        processed_params = self._resolve_task_parameters(tool_call.name, tool_call.parameters)

                        # Execute the tool through our MCP server
                        result = self.mcp_server.execute_tool(
                            tool_call.name,
                            **processed_params
                        )

                        # Format the result for Cohere
                        executed_tool_results.append({
                            "call": {
                                "name": tool_call.name,
                                "parameters": processed_params
                            },
                            "outputs": [result.dict() if hasattr(result, 'dict') else {"success": result.success, "data": result.data, "error": result.error}]
                        })

                        # Store for our return
                        tool_results.append({
                            "tool_call_id": getattr(tool_call, 'id', None),
                            "name": tool_call.name,
                            "parameters": processed_params,
                            "result": result.dict() if hasattr(result, 'dict') else {"success": result.success, "data": result.data, "error": result.error}
                        })

                    # If we have tool results, get the final response from Cohere
                    if executed_tool_results:
                        # Get final response from Cohere after tool execution
                        final_response = self.client.chat(
                            message=user_input,  # Original user input
                            model=self.model,
                            preamble=self._format_system_instructions(),
                            tools=tool_schemas,
                            tool_results=executed_tool_results,
                            force_single_step=True  # Required when providing tool_results
                        )
                        response = final_response
            else:
                # If no tools are available, call without tools
                response = self.client.chat(
                    message=user_input,
                    model=self.model,
                    preamble=self._format_system_instructions()
                )

            # Safely extract tool call information without modifying the response object
            tool_calls_list = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    # Create a new dict instead of accessing __dict__ directly
                    tool_call_dict = {
                        "name": getattr(tool_call, 'name', None),
                        "parameters": getattr(tool_call, 'parameters', {}),
                        "id": getattr(tool_call, 'id', None)
                    }
                    tool_calls_list.append(tool_call_dict)

            return {
                "response": response.text,
                "tool_calls": tool_calls_list,
                "tool_results": tool_results,
                "has_tool_calls": len(tool_results) > 0  # Changed to reflect actual tool execution
            }

        except Exception as e:
            # Check if this is the specific hallucination error
            error_str = str(e)
            if 'HALLUCINATED_ALL_TOOL_CALLS' in error_str or 'hallucinated' in error_str.lower():
                # This is a tool hallucination error, respond naturally instead
                try:
                    # Respond naturally without forcing tools
                    response = self.client.chat(
                        message=user_input,
                        model=self.model,
                        preamble=self._format_system_instructions()
                    )
                    return {
                        "response": response.text,
                        "tool_calls": [],
                        "tool_results": [],
                        "has_tool_calls": False
                    }
                except:
                    # If all else fails, return a generic response
                    return {
                        "response": "Hello! I'm your AI task assistant. You can ask me to add, list, update, or complete tasks. For example: 'Add a task to buy groceries' or 'Show me my tasks'.",
                        "tool_calls": [],
                        "tool_results": [],
                        "has_tool_calls": False
                    }
            else:
                return {
                    "response": f"I encountered an error processing your request: {str(e)}. Please try again.",
                    "tool_calls": [],
                    "tool_results": [],
                    "has_tool_calls": False,
                    "error": str(e)
                }

    def _is_general_conversation(self, user_input: str) -> bool:
        """
        Determine if the user input is a general conversation that might benefit from user info.

        Args:
            user_input: The user's input message

        Returns:
            bool: True if it's general conversation, False if it's task-related
        """
        # Convert to lowercase for easier matching
        lower_input = user_input.lower().strip()

        # Check for common greeting patterns that should use user info
        greeting_patterns = [
            'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon',
            'good evening', 'how are you', 'how do you do', 'howdy', 'yo',
            'what\'s up', 'sup', 'good day', 'nice to meet you', 'pleased to meet you',
            'how\'s it going', 'how are things', 'how have you been', 'what\'s new',
            'how is everything', 'hope you are doing well', 'hope you\'re well',
            'what is your name', 'who is this', 'who are you talking to'
        ]

        # Check if input matches any greeting pattern
        for pattern in greeting_patterns:
            if pattern in lower_input:
                return True

        # Check for simple responses that don't require tools
        # Don't include 'yes', 'no', 'sure' here as they might be responses to tool prompts
        # But exclude them if they appear in isolation (single word responses)
        if lower_input in ['thanks', 'thank you', 'please', 'maybe'] or (len(lower_input.split()) == 1 and lower_input in ['ok', 'okay']):
            return True

        # Check for questions about the AI itself
        ai_related_questions = [
            'who are you', 'what are you', 'what do you do', 'tell me about yourself',
            'introduce yourself', 'what can you do', 'how can you help me', 'what are your capabilities'
        ]

        for pattern in ai_related_questions:
            if pattern in lower_input:
                return True

        # Check for questions about user info that should trigger the get_user_info tool
        user_info_patterns = [
            'who am i', 'what is my name', 'what is my email', 'tell me about me',
            'my information', 'my profile', 'show my details', 'user details'
        ]

        for pattern in user_info_patterns:
            if pattern in lower_input:
                return False  # These should trigger the get_user_info tool, not be general conversation

        return False

    def _resolve_task_parameters(self, tool_name: str, parameters: dict) -> dict:
        """
        Resolve task parameters by converting task names to IDs where necessary.

        Args:
            tool_name: Name of the tool being called
            parameters: Original parameters from the AI

        Returns:
            Updated parameters with proper IDs where needed
        """
        # Only process certain tools that might have name-based task references
        if tool_name in ['update_task', 'complete_task', 'delete_task']:
            if 'task_id' in parameters:
                # Check if the task_id is a valid UUID-like string (which would be an actual ID)
                # If it's not a valid UUID, treat it as a potential task name/title
                task_identifier = parameters['task_id']

                # If it's already a valid UUID, return as is
                if self._is_valid_uuid(task_identifier):
                    return parameters

                # This looks like a task name/title, try to find the actual ID
                original_identifier = str(task_identifier).strip()

                # Comprehensive pattern matching for various natural language constructs
                import re

                # Pattern: "mrk it as completed because the task namely [TASK_NAME] is completed"
                pattern1 = r'mrk it as completed because the task namely ([^is]+) is completed'
                match1 = re.search(pattern1, original_identifier.lower())
                if match1:
                    extracted_task_name = match1.group(1).strip()
                    if extracted_task_name:
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "mark it as completed because the task named [TASK_NAME] is completed"
                pattern2 = r'mark it as completed because the task named ([^is]+) is completed'
                match2 = re.search(pattern2, original_identifier.lower())
                if match2:
                    extracted_task_name = match2.group(1).strip()
                    if extracted_task_name:
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "the task [TASK_NAME] is completed"
                pattern3 = r'the task ([^is]+) is completed'
                match3 = re.search(pattern3, original_identifier.lower())
                if match3:
                    extracted_task_name = match3.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "mrk [TASK_NAME] as completed" or "mark [TASK_NAME] as completed"
                pattern4 = r'(?:mrk|mark)\s+(.+?)\s+as completed'
                match4 = re.search(pattern4, original_identifier.lower())
                if match4:
                    extracted_task_name = match4.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "[TASK_NAME] should be completed" or "[TASK_NAME] needs to be completed"
                pattern5 = r'(.+?)\s+(?:should be|needs to be|has to be|must be)\s+completed'
                match5 = re.search(pattern5, original_identifier.lower())
                if match5:
                    extracted_task_name = match5.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "complete the [TASK_NAME] task" or "complete [TASK_NAME]"
                pattern6 = r'complete\s+(?:the\s+)?(.+?)(?:\s+task)?$'
                match6 = re.search(pattern6, original_identifier.lower())
                if match6:
                    extracted_task_name = match6.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "update the [TASK_NAME] task" or "update [TASK_NAME]"
                pattern7 = r'update\s+(?:the\s+)?(.+?)(?:\s+task)?$'
                match7 = re.search(pattern7, original_identifier.lower())
                if match7:
                    extracted_task_name = match7.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Pattern: "delete the [TASK_NAME] task" or "delete [TASK_NAME]"
                pattern8 = r'delete\s+(?:the\s+)?(.+?)(?:\s+task)?$'
                match8 = re.search(pattern8, original_identifier.lower())
                if match8:
                    extracted_task_name = match8.group(1).strip()
                    if extracted_task_name:
                        # Remove common articles and prepositions that might be included in the extracted name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()
                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            return resolved_params

                # Enhanced update_task specific pattern matching
                if tool_name == 'update_task':
                    # Pattern: "update task [TASK_NAME] to [NEW_TITLE]" or "update [TASK_NAME] to [NEW_VALUE]"
                    pattern_update = r'(?:update|modify|change)\s+(?:the\s+)?(?:task\s+)?(.+?)\s+to\s+(.+)$'
                    match_update = re.search(pattern_update, original_identifier.lower())
                    if match_update:
                        extracted_task_name = match_update.group(1).strip()
                        update_content = match_update.group(2).strip()

                        # Clean the task name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()

                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id

                            # If we don't have explicit title/description parameters, try to infer them from the update content
                            if 'title' not in resolved_params and 'description' not in resolved_params:
                                # For update_task, we need at least one of title or description
                                resolved_params['title'] = update_content

                            return resolved_params

                    # Pattern: "update task [TASK_NAME] with [NEW_TITLE]" or "update [TASK_NAME] with [NEW_VALUE]"
                    pattern_update2 = r'(?:update|modify|change)\s+(?:the\s+)?(?:task\s+)?(.+?)\s+with\s+(.+)$'
                    match_update2 = re.search(pattern_update2, original_identifier.lower())
                    if match_update2:
                        extracted_task_name = match_update2.group(1).strip()
                        update_content = match_update2.group(2).strip()

                        # Clean the task name
                        extracted_task_name = re.sub(r'\b(the|a|an|task)\b', '', extracted_task_name).strip()

                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id

                            # If we don't have explicit title/description parameters, try to infer them
                            if 'title' not in resolved_params and 'description' not in resolved_params:
                                resolved_params['title'] = update_content

                            return resolved_params

                    # Pattern: "update the task namely [TASK_NAME] to [NEW_TITLE]" - your specific case
                    pattern_update3 = r'update\s+(?:the\s+)?task\s+namely\s+(.+?)\s+to\s+(.+)$'
                    match_update3 = re.search(pattern_update3, original_identifier.lower())
                    if match_update3:
                        extracted_task_name = match_update3.group(1).strip()
                        update_content = match_update3.group(2).strip()

                        # Look for "and add description" pattern in the update content
                        desc_pattern = r'(.+?)\s+and\s+add\s+description\s+(.+)$'
                        desc_match = re.search(desc_pattern, update_content.lower())

                        if desc_match:
                            # Separate the new title and description
                            new_title = desc_match.group(1).strip()
                            new_description = desc_match.group(2).strip()

                            task_id = self._find_task_by_name(extracted_task_name)
                            if task_id:
                                resolved_params = parameters.copy()
                                resolved_params['task_id'] = task_id
                                resolved_params['title'] = new_title
                                resolved_params['description'] = new_description
                                return resolved_params
                        else:
                            # No separate description, treat entire update content as title
                            task_id = self._find_task_by_name(extracted_task_name)
                            if task_id:
                                resolved_params = parameters.copy()
                                resolved_params['task_id'] = task_id
                                resolved_params['title'] = update_content
                                return resolved_params

                    # Pattern: "update [TASK_NAME] to [NEW_TITLE] and add description [DESCRIPTION]"
                    pattern_update4 = r'update\s+(.+?)\s+to\s+(.+?)\s+and\s+add\s+description\s+(.+)$'
                    match_update4 = re.search(pattern_update4, original_identifier.lower())
                    if match_update4:
                        extracted_task_name = match_update4.group(1).strip()
                        new_title = match_update4.group(2).strip()
                        new_description = match_update4.group(3).strip()

                        task_id = self._find_task_by_name(extracted_task_name)
                        if task_id:
                            resolved_params = parameters.copy()
                            resolved_params['task_id'] = task_id
                            resolved_params['title'] = new_title
                            resolved_params['description'] = new_description
                            return resolved_params

                # If we reach here, try to find the task in the user's task list using the cleaned identifier
                # Remove common phrases that might interfere with matching
                cleaned_identifier = self._clean_task_identifier(original_identifier)

                if cleaned_identifier and len(cleaned_identifier) > 1:
                    task_id = self._find_task_by_name(cleaned_identifier)
                    if task_id:
                        resolved_params = parameters.copy()
                        resolved_params['task_id'] = task_id
                        return resolved_params

        return parameters

    def _clean_task_identifier(self, identifier: str) -> str:
        """
        Clean a task identifier by removing common natural language artifacts.

        Args:
            identifier: The raw identifier string

        Returns:
            Cleaned task identifier
        """
        import re

        # Convert to lowercase for processing
        identifier_lower = identifier.lower().strip()

        # Remove common natural language phrases that aren't part of task names
        phrases_to_remove = [
            'because', 'the', 'a', 'an', 'it', 'is', 'was', 'are', 'were', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'can', 'may', 'might', 'must', 'to', 'for', 'of',
            'in', 'on', 'at', 'by', 'with', 'from', 'about', 'as', 'if', 'when',
            'where', 'why', 'how', 'what', 'which', 'who', 'whose', 'that', 'this',
            'these', 'those', 'such', 'very', 'quite', 'rather', 'fairly', 'pretty',
            'somewhat', 'some', 'any', 'each', 'every', 'all', 'both', 'either',
            'neither', 'much', 'many', 'little', 'few', 'lot', 'lots', 'several',
            'various', 'different', 'same', 'similar', 'like', 'than', 'more', 'most',
            'least', 'less', 'over', 'under', 'above', 'below', 'up', 'down', 'out',
            'off', 'on', 'into', 'onto', 'upon', 'across', 'through', 'around',
            'behind', 'before', 'after', 'since', 'until', 'while', 'during',
            'ago', 'away', 'apart', 'aside', 'near', 'next', 'past', 'toward',
            'towards', 'away', 'apart', 'away', 'back', 'forward', 'straight',
            'upward', 'downward', 'home', 'there', 'here', 'now', 'then', 'soon',
            'later', 'early', 'late', 'first', 'last', 'next', 'previous', 'former',
            'latter', 'other', 'another', 'own', 'new', 'old', 'young', 'big',
            'large', 'small', 'great', 'huge', 'tiny', 'long', 'short', 'high',
            'low', 'deep', 'wide', 'narrow', 'thick', 'thin', 'heavy', 'light',
            'strong', 'weak', 'fast', 'slow', 'hot', 'cold', 'warm', 'cool',
            'dry', 'wet', 'hard', 'soft', 'rough', 'smooth', 'clean', 'dirty',
            'right', 'wrong', 'true', 'false', 'real', 'fake', 'good', 'bad',
            'nice', 'mean', 'kind', 'cruel', 'happy', 'sad', 'angry', 'calm',
            'excited', 'bored', 'tired', 'awake', 'asleep', 'ready', 'busy',
            'free', 'important', 'necessary', 'possible', 'impossible', 'easy',
            'difficult', 'simple', 'complex', 'clear', 'unclear', 'obvious',
            'hidden', 'visible', 'invisible', 'available', 'unavailable', 'open',
            'closed', 'public', 'private', 'personal', 'professional', 'work',
            'job', 'task', 'project', 'assignment', 'duty', 'responsibility',
            'obligation', 'chore', 'errand', 'mission', 'goal', 'objective',
            'target', 'purpose', 'reason', 'cause', 'effect', 'result', 'outcome'
        ]

        # Remove common phrases from the identifier
        cleaned = identifier_lower
        for phrase in phrases_to_remove:
            # Replace the phrase with a space to avoid concatenating words
            cleaned = re.sub(r'\b' + re.escape(phrase) + r'\b', ' ', cleaned)

        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        return cleaned

    def _find_task_by_name(self, task_name: str) -> str:
        """
        Find a task ID by name in the user's task list.

        Args:
            task_name: The name or partial name of the task to find

        Returns:
            Task ID if found, None otherwise
        """
        # Get the user's tasks
        list_result = self.mcp_server.execute_tool('list_tasks', filter_completed=None)

        if not list_result.success or not list_result.data:
            return None

        # Clean the search term
        search_term = task_name.strip().lower()
        if not search_term:
            return None

        # First, try exact match
        for task in list_result.data:
            task_title = task.get('title', '')
            if task_title and str(task_title).lower().strip() == search_term:
                return task['id']

        # Next, try partial match (search term contained in title)
        for task in list_result.data:
            task_title = task.get('title', '')
            if task_title and search_term in str(task_title).lower():
                return task['id']

        # Try reverse match (title contained in search term)
        for task in list_result.data:
            task_title = task.get('title', '')
            if task_title and str(task_title).lower() in search_term:
                return task['id']

        # Try fuzzy matching - check if any title words appear in search term
        search_words = set(search_term.split())
        for task in list_result.data:
            task_title = task.get('title', '')
            if task_title:
                title_words = set(str(task_title).lower().split())
                # If there's significant overlap in words, consider it a match
                common_words = search_words.intersection(title_words)
                if len(common_words) > 0 and len(common_words) >= max(1, min(len(search_words), len(title_words)) // 2):
                    return task['id']

        return None

    def _is_valid_uuid(self, val):
        """Check if a value looks like a UUID."""
        import uuid
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def _handle_direct_update_request(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Directly handle update task requests by bypassing the AI and calling the tool directly.

        Args:
            user_input: The original user input

        Returns:
            Dict with tool call results if it's an update request, None otherwise
        """
        import re

        # Normalize input for pattern matching
        input_lower = user_input.lower().strip()

        # Patterns for update requests
        patterns = [
            # "update the task for me namely doing homework to doing nothing and add description"
            r'update\s+the\s+task\s+for\s+me\s+(?:namely|namley)\s+(.+?)\s+to\s+(.+?)(?:\s+and\s+add\s+description\s+(.+))?$',

            # "update the task doing homework to doing nothing and add description"
            r'update\s+the\s+task\s+(.+?)\s+to\s+(.+?)(?:\s+and\s+add\s+description\s+(.+))?$',

            # "update doing homework to doing nothing and add description"
            r'update\s+(.+?)\s+to\s+(.+?)(?:\s+and\s+add\s+description\s+(.+?))?(?:\s+and.*)?$',
            # "update doing homework to doing nothing and add description accordingly"
            r'update\s+(.+?)\s+to\s+(.+?)\s+and\s+add\s+description\s+accordingly$',

            # Variations without description
            r'update\s+the\s+task\s+for\s+me\s+(?:namely|namley)\s+(.+?)\s+to\s+(.+)$',
            r'update\s+the\s+task\s+(.+?)\s+to\s+(.+)$',
            r'update\s+(.+?)\s+to\s+(.+)$',
        ]

        for pattern in patterns:
            match = re.search(pattern, input_lower)
            if match:
                groups = match.groups()

                if len(groups) >= 2:
                    task_name = groups[0].strip()
                    new_title = groups[1].strip()

                    # Check if description is provided
                    new_description = groups[2].strip() if len(groups) > 2 and groups[2] else None

                    # Get the user's tasks to find the matching one
                    list_result = self.mcp_server.execute_tool('list_tasks', filter_completed=None)

                    if list_result.success and list_result.data:
                        # Find the task to update
                        target_task = None
                        for task in list_result.data:
                            if task_name.lower().strip() in task.get('title', '').lower().strip() or \
                               task.get('title', '').lower().strip() in task_name.lower().strip():
                                target_task = task
                                break

                        if target_task:
                            # Prepare update parameters
                            update_params = {
                                "task_id": target_task['id'],
                                "title": new_title
                            }

                            if new_description:
                                # Check if the description is "accordingly" and handle it specially
                                if new_description.lower().strip() == "accordingly":
                                    update_params["description"] = f"Updated from '{target_task['title']}' to '{new_title}', per user request"
                                else:
                                    update_params["description"] = new_description
                            elif "on your own" in input_lower or "accordingly" in input_lower:
                                # If "on your own" or "accordingly" is in the request, create a meaningful description
                                update_params["description"] = f"Updated from '{target_task['title']}' to '{new_title}', per user request"

                            # Execute the update tool directly
                            update_result = self.mcp_server.execute_tool('update_task', **update_params)

                            # Format response for successful update
                            if update_result.success and update_result.data:
                                response_text = f"Task '{target_task['title']}' has been updated successfully.\n\nNew Title: {update_result.data.get('title', 'N/A')}"
                                if update_result.data.get('description'):
                                    response_text += f"\nNew Description: {update_result.data.get('description', 'N/A')}"

                                return {
                                    "response": response_text,
                                    "tool_calls": [{"name": "update_task", "parameters": update_params}],
                                    "tool_results": [{
                                        "tool_call_id": None,
                                        "name": "update_task",
                                        "parameters": update_params,
                                        "result": update_result.dict() if hasattr(update_result, 'dict') else {"success": update_result.success, "data": update_result.data, "error": update_result.error}
                                    }],
                                    "has_tool_calls": True
                                }

        return None  # Not an update request we can handle

    def _handle_direct_delete_request(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Directly handle delete task requests by bypassing the AI and calling the tool directly.

        Args:
            user_input: The original user input

        Returns:
            Dict with tool call results if it's a delete request, None otherwise
        """
        import re

        # Normalize input for pattern matching
        input_lower = user_input.lower().strip()

        # Patterns for delete requests
        patterns = [
            # "delete the task do it now"
            r'delete\s+the\s+task\s+(.+?)$',

            # "delete do it now"
            r'delete\s+(.+?)$',

            # "remove the task do it now"
            r'remove\s+the\s+task\s+(.+?)$',

            # "remove do it now"
            r'remove\s+(.+?)$',

            # "drop the task do it now"
            r'drop\s+the\s+task\s+(.+?)$',

            # "eliminate the task do it now"
            r'eliminate\s+the\s+task\s+(.+?)$',
        ]

        for pattern in patterns:
            match = re.search(pattern, input_lower)
            if match:
                task_name = match.group(1).strip()

                # Get the user's tasks to find the matching one
                list_result = self.mcp_server.execute_tool('list_tasks', filter_completed=None)

                if list_result.success and list_result.data:
                    # Find the task to delete
                    target_task = None
                    for task in list_result.data:
                        if task_name.lower().strip() in task.get('title', '').lower().strip() or \
                           task.get('title', '').lower().strip() in task_name.lower().strip():
                            target_task = task
                            break

                    if target_task:
                        # Prepare delete parameters
                        delete_params = {
                            "task_id": target_task['id']
                        }

                        # Execute the delete tool directly
                        delete_result = self.mcp_server.execute_tool('delete_task', **delete_params)

                        # Format response for successful deletion
                        if delete_result.success and delete_result.data:
                            response_text = f"Task '{target_task['title']}' has been deleted successfully."

                            return {
                                "response": response_text,
                                "tool_calls": [{"name": "delete_task", "parameters": delete_params}],
                                "tool_results": [{
                                    "tool_call_id": None,
                                    "name": "delete_task",
                                    "parameters": delete_params,
                                    "result": delete_result.dict() if hasattr(delete_result, 'dict') else {"success": delete_result.success, "data": delete_result.data, "error": delete_result.error}
                                }],
                                "has_tool_calls": True
                            }

        return None  # Not a delete request we can handle

    def _handle_direct_complete_request(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Directly handle complete task requests by bypassing the AI and calling the tool directly.

        Args:
            user_input: The original user input

        Returns:
            Dict with tool call results if it's a complete request, None otherwise
        """
        import re

        # Normalize input for pattern matching
        input_lower = user_input.lower().strip()

        # Patterns for complete requests
        patterns = [
            # "task do it now is completed"
            r'task\s+(.+?)\s+is\s+completed$',

            # "mark task do it now as completed"
            r'mark\s+task\s+(.+?)\s+as\s+completed$',

            # "mark the task do it now as completed" - your specific case
            r'mark\s+the\s+task\s+(.+?)\s+as\s+completed$',

            # "complete the task do it now"
            r'complete\s+the\s+task\s+(.+?)$',

            # "complete do it now"
            r'complete\s+(.+?)$',

            # "finish task do it now"
            r'finish\s+(?:the\s+)?task\s+(.+?)$',
        ]

        for pattern in patterns:
            match = re.search(pattern, input_lower)
            if match:
                task_name = match.group(1).strip()

                # Get the user's tasks to find the matching one
                list_result = self.mcp_server.execute_tool('list_tasks', filter_completed=None)

                if list_result.success and list_result.data:
                    # Find the task to complete
                    target_task = None
                    for task in list_result.data:
                        if task_name.lower().strip() in task.get('title', '').lower().strip() or \
                           task.get('title', '').lower().strip() in task_name.lower().strip():
                            target_task = task
                            break

                    if target_task:
                        # Prepare complete parameters
                        complete_params = {
                            "task_id": target_task['id']
                        }

                        # Execute the complete tool directly
                        complete_result = self.mcp_server.execute_tool('complete_task', **complete_params)

                        # Format response for successful completion
                        if complete_result.success and complete_result.data:
                            response_text = f"Task '{target_task['title']}' has been marked as completed successfully."

                            return {
                                "response": response_text,
                                "tool_calls": [{"name": "complete_task", "parameters": complete_params}],
                                "tool_results": [{
                                    "tool_call_id": None,
                                    "name": "complete_task",
                                    "parameters": complete_params,
                                    "result": complete_result.dict() if hasattr(complete_result, 'dict') else {"success": complete_result.success, "data": complete_result.data, "error": complete_result.error}
                                }],
                                "has_tool_calls": True
                            }

        return None  # Not a complete request we can handle

    def _resolve_context_references(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Resolve context references like 'it', 'that', 'the task' by looking at conversation history
        and also by understanding references within the same sentence.

        Args:
            user_input: The current user input
            conversation_history: Previous messages in the conversation

        Returns:
            Resolved input with context references replaced with specific task names
        """
        import re

        # First, try to resolve references within the same sentence
        # Pattern: "the task X is Y. delete it" or "task X is Y, remove it"
        same_sentence_patterns = [
            # "the task do it now is being done. delete it for me"
            r'(?:the\s+)?task\s+([^.!?]+?)\s+is\s+[^.!?]*?\.\s*(delete|remove|complete|finish|mark|update|change)\s+it',

            # "i have completed my task do it now. so delete it for me" - your specific case
            r'(?:i\s+have\s+)?(?:completed|finished|done|marked)\s+(?:my\s+)?task\s+([^.,!?]+?)[.,]\s*(?:so|and|then)\s*(delete|remove|complete|finish|mark|update|change)\s+it',

            # "i have completed task do it now, so delete it for me"
            r'(?:i\s+have\s+)?(?:completed|finished|done|marked)\s+(?:my\s+)?task\s+([^.,!?]+?),\s*(?:so|and|then)\s*(delete|remove|complete|finish|mark|update|change)\s+it',

            # "task do it now is being done, delete it for me"
            r'(?:the\s+)?task\s+([^,.!?]+?)\s+is\s+[^,.!?]*?,\s*(delete|remove|complete|finish|mark|update|change)\s+it',

            # General pattern: "task NAME something... ACTION it"
            r'(?:the\s+)?task\s+([^,.!?]+?)\s+(?:is|are|was|were|has|have|will|would|should|can|could)\s+[^,.!?]*?[,.]\s*(delete|remove|complete|finish|mark|update|change)\s+it',
        ]

        for pattern in same_sentence_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                task_name = match.group(1).strip()
                action = match.group(2).strip()

                # Replace "ACTION it" with "ACTION task [task_name]"
                resolved_input = re.sub(
                    rf'{action}\s+it',
                    f'{action} task {task_name}',
                    user_input,
                    flags=re.IGNORECASE
                )
                return resolved_input

        # Check if the user is using pronouns like "it", "that", "the task" to refer to a previously mentioned task
        current_input_lower = user_input.lower().strip()

        # Patterns that indicate context reference
        context_patterns = [
            r'mark\s+it(\s+as\s+completed)?',
            r'complete\s+it',
            r'toggle\s+it',
            r'update\s+it',
            r'change\s+it',
            r'delete\s+it',
            r'modify\s+it',
            r'finish\s+it',
            r'do\s+that',
            r'complete\s+that',
            r'update\s+the\s+task',  # "update the task" without a specific name
            r'complete\s+the\s+task',  # "complete the task" without a specific name
        ]

        # Look for context references in the current input
        has_context_ref = any(re.search(pattern, current_input_lower) for pattern in context_patterns)

        if has_context_ref and conversation_history:
            # Look backward through the conversation history to find the last task mentioned
            for i in range(len(conversation_history) - 1, -1, -1):
                prev_message = conversation_history[i]

                if prev_message.get('role') == 'user':
                    # Look for task names in previous user messages
                    prev_content = prev_message.get('content', '').lower()

                    # Common patterns where tasks are mentioned explicitly
                    task_patterns = [
                        r'update\s+the\s+task\s+(.+?)(?:\s+to|$)',
                        r'create\s+task\s+(.+?)(?:\s+|$)',
                        r'add\s+task\s+(.+?)(?:\s+|$)',
                        r'task\s+(.+?)\s+is\s+(?:completed|pending|done|not\s+done)',
                        r'add\s+a\s+task\s+(.+?)(?:\s+|$)',
                        r'do\s+(.+?)\s+now',  # For "do it now"
                    ]

                    for pattern in task_patterns:
                        match = re.search(pattern, prev_content)
                        if match:
                            referenced_task = match.group(1).strip()

                            # Replace context reference with the actual task name
                            resolved_input = re.sub(r'mark\s+it', f'mark task {referenced_task}', user_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'complete\s+it', f'complete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'update\s+it', f'update task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'update\s+the\s+task(?!\s+\w+)', f'update task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'complete\s+the\s+task(?!\s+\w+)', f'complete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'toggle\s+it', f'toggle task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'delete\s+it', f'delete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'change\s+it', f'change task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'modify\s+it', f'modify task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'finish\s+it', f'finish task {referenced_task}', resolved_input, flags=re.IGNORECASE)

                            return resolved_input

                # Also check assistant responses for task names
                elif prev_message.get('role') == 'assistant':
                    prev_content = prev_message.get('content', '').lower()

                    # Look for task names in assistant responses (like when it confirms updates)
                    task_patterns_assistant = [
                        r'task\s+[\'"](.+?)[\'"]\s+has\s+been',
                        r'created\s+task\s+[\'"](.+?)[\'"]',
                        r'updated\s+task\s+[\'"](.+?)[\'"]',
                        r'added\s+task\s+[\'"](.+?)[\'"]',
                    ]

                    for pattern in task_patterns_assistant:
                        match = re.search(pattern, prev_content)
                        if match:
                            referenced_task = match.group(1).strip()

                            # Replace context reference with the actual task name
                            resolved_input = re.sub(r'mark\s+it', f'mark task {referenced_task}', user_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'complete\s+it', f'complete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'update\s+it', f'update task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'update\s+the\s+task(?!\s+\w+)', f'update task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'complete\s+the\s+task(?!\s+\w+)', f'complete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'toggle\s+it', f'toggle task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'delete\s+it', f'delete task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'change\s+it', f'change task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'modify\s+it', f'modify task {referenced_task}', resolved_input, flags=re.IGNORECASE)
                            resolved_input = re.sub(r'finish\s+it', f'finish task {referenced_task}', resolved_input, flags=re.IGNORECASE)

                            return resolved_input

        # If no context reference is found or resolved, return the original input
        return user_input

    def _preprocess_user_input(self, user_input: str) -> str:
        """
        Preprocess user input to handle specific patterns that the AI might struggle with.

        Args:
            user_input: The original user input

        Returns:
            Processed input that's more likely to be correctly interpreted by the AI
        """
        import re

        original_input = user_input.lower().strip()

        # Pattern: "update the task namely [TASK_NAME] to [NEW_TITLE] and add description [DESC]"
        # Convert to: "update task [TASK_NAME] with title [NEW_TITLE] and description [DESC]"
        pattern_namely = r'update\s+the\s+task\s+namely\s+(.+?)\s+to\s+(.+?)\s+and\s+add\s+description\s+(.+)$'
        match_namely = re.search(pattern_namely, original_input)

        if match_namely:
            task_name = match_namely.group(1).strip()
            new_title = match_namely.group(2).strip()
            description = match_namely.group(3).strip()

            # Create a clearer instruction for the AI
            processed = f"update the task '{task_name}' to have title '{new_title}' and description '{description}'"
            return processed

        # Pattern: "update the task namely [TASK_NAME] to [NEW_TITLE]"
        pattern_namely_simple = r'update\s+the\s+task\s+namely\s+(.+?)\s+to\s+(.+)$'
        match_namely_simple = re.search(pattern_namely_simple, original_input)

        if match_namely_simple:
            task_name = match_namely_simple.group(1).strip()
            new_title = match_namely_simple.group(2).strip()

            # Create a clearer instruction for the AI
            processed = f"update the task '{task_name}' to have title '{new_title}'"
            return processed

        # Pattern: "update [TASK_NAME] to [NEW_TITLE] and add description [DESC]"
        pattern_update_desc = r'update\s+(.+?)\s+to\s+(.+?)\s+and\s+add\s+description\s+(.+)$'
        match_update_desc = re.search(pattern_update_desc, original_input)

        if match_update_desc:
            task_name = match_update_desc.group(1).strip()
            new_title = match_update_desc.group(2).strip()
            description = match_update_desc.group(3).strip()

            # Create a clearer instruction for the AI
            processed = f"update the task '{task_name}' to have title '{new_title}' and description '{description}'"
            return processed

        # Pattern: "update [TASK_NAME] to [NEW_TITLE]"
        pattern_update_simple = r'update\s+(.+?)\s+to\s+(.+)$'
        match_update_simple = re.search(pattern_update_simple, original_input)

        if match_update_simple:
            task_name = match_update_simple.group(1).strip()
            new_title = match_update_simple.group(2).strip()

            # Create a clearer instruction for the AI
            processed = f"update the task '{task_name}' to have title '{new_title}'"
            return processed

        # If no pattern matches, return the original input unchanged
        return user_input