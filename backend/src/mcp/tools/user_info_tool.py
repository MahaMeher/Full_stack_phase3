"""
User Info Tool for retrieving user information in the AI chatbot system.
"""

from typing import Dict, Any
from pydantic import Field
from .base_tool import UserScopedMCPTool
from ...models.user import User


class GetUserInfoTool(UserScopedMCPTool):
    """
    Tool for retrieving the current user's information.
    """

    @property
    def name(self) -> str:
        """The name of the tool."""
        return "get_user_info"

    @property
    def description(self) -> str:
        """Description of what the tool does."""
        return "Retrieve the current user's information including name, email, and other profile details."

    @property
    def parameters(self) -> Dict[str, Any]:
        """JSON Schema for the tool's parameters."""
        return {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }

    def validate_input(self, **kwargs) -> bool:
        """
        Validate the input parameters for the tool.

        Args:
            **kwargs: Parameters passed to the tool

        Returns:
            bool: True if input is valid, False otherwise
        """
        # No parameters to validate for this tool
        return True

    def execute_with_validation(self, **kwargs) -> "ToolCallResult":
        """
        Execute the tool with user isolation and input validation.

        Args:
            **kwargs: Parameters passed to the tool

        Returns:
            ToolCallResult: Result of the tool execution
        """
        try:
            # Import the UserService to get user information
            from ...services.user_service import UserService

            # Create an instance of UserService
            user_service = UserService()

            # Get user information using the user service
            user = user_service.get_user_by_id(self.db_session, self.user_id)

            if not user:
                return self._create_result(
                    success=False,
                    error="User not found",
                    data=None
                )

            # Return user information (excluding sensitive data like password)
            user_info = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "is_active": user.is_active,
            }

            return self._create_result(
                success=True,
                error=None,
                data=user_info
            )

        except Exception as e:
            return self._create_result(
                success=False,
                error=f"Error retrieving user information: {str(e)}",
                data=None
            )

    def _create_result(self, success: bool, error: str, data: Any):
        """
        Helper method to create a ToolCallResult.

        Args:
            success: Whether the operation was successful
            error: Error message if any
            data: Data to return

        Returns:
            ToolCallResult: The result object
        """
        from ...mcp.server import ToolCallResult
        return ToolCallResult(
            success=success,
            error=error,
            data=data,
            tool_name=self.name
        )