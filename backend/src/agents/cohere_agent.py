"""
Cohere-powered AI Agent that follows OpenAI Agents SDK architectural patterns.
Implements natural language understanding and tool selection for task management.
"""

import json
from typing import Dict, Any, List, Optional
from cohere import Client
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

        For casual conversation (greetings, small talk, general questions), respond naturally
        without attempting to use any tools. Only use tools when the user explicitly requests
        task-related operations like adding, listing, updating, completing, or deleting tasks.

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

        Always use the most appropriate tool for the user's request.
        When listing tasks, provide clear and organized information.
        When updating tasks, confirm the changes with the user.
        For general conversation, respond naturally without using tools.
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

        # Check if the input is a casual conversation that doesn't require tools
        if self._is_general_conversation(user_input):
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
        full_context += f"User: {user_input}"

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
            # Use Cohere's chat endpoint with tools
            # Only pass tools if we have valid ones to avoid API errors
            if tool_schemas:  # Only pass tools if the array is not empty
                response = self.client.chat(
                    message=user_input,
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
                            tools=tool_schemas,
                            tool_results=executed_tool_results
                            # Removed force_single_step to avoid the hallucination issue
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
        Determine if the user input is a general conversation that doesn't require tools.

        Args:
            user_input: The user's input message

        Returns:
            bool: True if it's general conversation, False if it's task-related
        """
        # Convert to lowercase for easier matching
        lower_input = user_input.lower().strip()

        # Check for common greeting patterns
        greeting_patterns = [
            'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon',
            'good evening', 'how are you', 'how do you do', 'howdy', 'yo',
            'what\'s up', 'sup', 'good day', 'nice to meet you', 'pleased to meet you',
            'how\'s it going', 'how are things', 'how have you been', 'what\'s new',
            'how is everything', 'hope you are doing well', 'hope you\'re well'
        ]

        # Check if input matches any greeting pattern
        for pattern in greeting_patterns:
            if pattern in lower_input:
                return True

        # Check for simple responses that don't require tools
        if lower_input in ['thanks', 'thank you', 'please', 'ok', 'okay', 'sure', 'yes', 'no', 'maybe']:
            return True

        # Check for questions about the AI itself
        ai_related_questions = [
            'who are you', 'what are you', 'what do you do', 'tell me about yourself',
            'introduce yourself', 'what can you do', 'how can you help me', 'what are your capabilities'
        ]

        for pattern in ai_related_questions:
            if pattern in lower_input:
                return True

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
                if not self._is_valid_uuid(parameters['task_id']):
                    # This looks like a task name/title, try to find the actual ID
                    task_identifier = parameters['task_id']

                    # First, let's clean the identifier by removing common natural language patterns
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
                            task_id = self._find_task_by_name(extracted_task_name)
                            if task_id:
                                resolved_params = parameters.copy()
                                resolved_params['task_id'] = task_id
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