"""
Agent Service

Integrates OpenAI Agents SDK with MCP tools for task management.
Handles intent recognition, tool orchestration, and multilingual support.
"""

from typing import List, Dict, Any, Optional
import uuid
import logging
from openai import AsyncOpenAI
from mcp_server.server import get_all_tools
from core.services.openrouter_client import OpenRouterClient

logger = logging.getLogger(__name__)


class AgentService:
    """
    Service for managing AI agent interactions with MCP tools

    Uses OpenAI Agents SDK for intent recognition and tool orchestration.
    Supports multilingual conversations (English, Roman Urdu, Urdu).
    """

    SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo tasks through natural conversation.

**Your Capabilities:**
- Add new tasks when users describe things they need to do
- List tasks (all, pending, or completed)
- Mark tasks as complete
- Delete tasks (with confirmation)
- Update task details (title, description)

**Language Support:**
You can understand and respond in:
- English
- Roman Urdu (Urdu written in Latin script)
- Urdu (written in Urdu script)

Detect the user's language from their message and respond in the same language. However, when calling tools, always use English for parameter values.

**Task Numbering:**
When listing tasks, they are numbered starting from 1 (position 1, 2, 3...). When users refer to "task 1" or "first task", use the task_id from position 1.

**Conversation Guidelines:**
1. Be friendly and conversational
2. Confirm actions after completing them
3. Ask for clarification when needed
4. For destructive actions (delete), ask for confirmation first
5. If a user says "update task 1" without specifying what to update, ask what they want to change

**Examples:**

User: "Add task: buy groceries"
You: Call add_task with title="buy groceries", then respond: "I've added 'buy groceries' to your tasks!"

User: "Show my tasks"
You: Call list_tasks with status="all", then format and display the results

User: "Mark task 1 as done"
You: Call list_tasks to get task_id for position 1, then call complete_task with that task_id

User: "Delete task 2"
You: Ask "Are you sure you want to delete task 2?" and wait for confirmation

User: "Mujhe apne tasks dikhao" (Roman Urdu)
You: Call list_tasks, then respond in Roman Urdu: "Yeh hain aapke tasks..."

Remember: Always maintain user_id isolation - only access tasks belonging to the current user."""

    def __init__(self, openrouter_client: OpenRouterClient):
        """
        Initialize agent service

        Args:
            openrouter_client: OpenRouter API client for LLM inference
        """
        self.openrouter_client = openrouter_client
        self.tools = get_all_tools()
        logger.info(f"Initialized AgentService with {len(self.tools)} MCP tools")

    def _convert_tools_to_openai_format(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to OpenAI function calling format

        Returns:
            List of tool definitions in OpenAI format
        """
        openai_tools = []

        for tool in self.tools:
            # Extract function metadata
            func_name = tool.__name__
            func_doc = tool.__doc__ or ""

            # Parse function signature for parameters
            import inspect
            sig = inspect.signature(tool)

            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }

            for param_name, param in sig.parameters.items():
                param_type = "string"  # Default to string
                param_desc = f"{param_name} parameter"

                # Determine if required (no default value)
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)

                parameters["properties"][param_name] = {
                    "type": param_type,
                    "description": param_desc
                }

            tool_def = {
                "type": "function",
                "function": {
                    "name": func_name,
                    "description": func_doc.strip().split('\n')[0] if func_doc else func_name,
                    "parameters": parameters
                }
            }

            openai_tools.append(tool_def)

        logger.info(f"Converted {len(openai_tools)} tools to OpenAI format")
        return openai_tools

    async def process_message(
        self,
        user_id: str,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Process user message with agent and return response

        Args:
            user_id: UUID of the user (for tool isolation)
            user_message: User's message content
            conversation_history: Previous messages in conversation (optional)

        Returns:
            Agent's response message

        Raises:
            Exception: If processing fails
        """
        try:
            # Build messages list with system prompt and history
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Convert tools to OpenAI format
            tools = self._convert_tools_to_openai_format()

            # Call OpenRouter API with tools
            response = await self.openrouter_client.chat_completion(
                messages=messages,
                temperature=0.7,
                tools=tools if tools else None
            )

            # Check if agent wants to call tools
            tool_calls = self.openrouter_client.extract_tool_calls(response)

            if tool_calls:
                # Execute tool calls
                tool_results = await self._execute_tool_calls(tool_calls, user_id)

                # Add assistant message with tool calls to history
                messages.append(response["choices"][0]["message"])

                # Add tool results to messages
                for tool_result in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_result["tool_call_id"],
                        "content": tool_result["content"]
                    })

                # Get final response from agent
                final_response = await self.openrouter_client.chat_completion(
                    messages=messages,
                    temperature=0.7
                )

                response_content = self.openrouter_client.extract_message_content(final_response)
            else:
                # No tool calls, just return the response
                response_content = self.openrouter_client.extract_message_content(response)

            logger.info(f"Processed message for user {user_id}")
            return response_content

        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {str(e)}")
            raise Exception(f"Failed to process message: {str(e)}")

    async def _execute_tool_calls(
        self,
        tool_calls: List[Dict[str, Any]],
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Execute tool calls and return results

        Args:
            tool_calls: List of tool call objects from OpenAI response
            user_id: UUID of the user (injected into all tool calls)

        Returns:
            List of tool result dictionaries

        Raises:
            Exception: If tool execution fails
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = eval(tool_call["function"]["arguments"])  # Parse JSON string to dict

            # Inject user_id into tool arguments
            tool_args["user_id"] = user_id

            try:
                # Find and execute the tool
                tool_func = None
                for tool in self.tools:
                    if tool.__name__ == tool_name:
                        tool_func = tool
                        break

                if not tool_func:
                    raise Exception(f"Tool not found: {tool_name}")

                # Execute tool
                result = await tool_func(**tool_args)

                # Format result as JSON string
                import json
                result_content = json.dumps(result)

                results.append({
                    "tool_call_id": tool_call["id"],
                    "content": result_content
                })

                logger.info(f"Executed tool {tool_name} for user {user_id}")

            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                results.append({
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps({"error": str(e)})
                })

        return results


__all__ = ['AgentService']
