"""
Agent Service

Integrates OpenAI Agents SDK with MCP tools for task management.
Handles intent recognition, tool orchestration, and multilingual support.

Architecture:
- Uses OpenAI Agents SDK for proper agentic workflow (not manual function calling)
- Configures SDK to use OpenRouter API (gpt-4o-mini) instead of OpenAI API
- Registers 5 MCP tools with @function_tool decorator for automatic schema extraction
- Injects user_id from context for security (not exposed to agent)
- Maintains stateless architecture (loads conversation history from database)
- Supports multilingual conversations (English, Roman Urdu, Urdu)

Key Components:
- _configure_openrouter_client(): Sets up custom AsyncOpenAI client for OpenRouter
- Tool wrapper functions: Decorated with @function_tool, inject user_id from context
- agent: Global Agent instance initialized at module load
- AgentService: Service class that processes messages using Runner.run()
"""

from typing import List, Dict, Any, Optional
import os
import logging
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_client, function_tool, RunContextWrapper, set_tracing_disabled


logger = logging.getLogger(__name__)


# Import MCP tools
from mcp_server.tools.add_task import add_task_tool
from mcp_server.tools.list_tasks import list_tasks_tool
from mcp_server.tools.complete_task import complete_task_tool
from mcp_server.tools.delete_task import delete_task_tool
from mcp_server.tools.update_task import update_task_tool


# Configure OpenRouter client for OpenAI Agents SDK
def _configure_openrouter_client():
    """
    Configure OpenAI Agents SDK to use OpenRouter API

    Raises:
        ValueError: If OPENROUTER_API_KEY is not set
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )

    # Create custom AsyncOpenAI client pointing to OpenRouter
    custom_client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Set as default client for all agents
    set_default_openai_client(custom_client)
    logger.info("Configured OpenAI Agents SDK to use OpenRouter API")


# Disable OpenAI tracing (we use OpenRouter, not OpenAI)

set_tracing_disabled(True)
logger.info("🔇 OpenAI Agents SDK tracing disabled")

# Configure OpenRouter on module load
try:
    _configure_openrouter_client()
    logger.info("✅ OpenAI Agents SDK configured successfully with OpenRouter API")
except ValueError as e:
    logger.error(f"❌ Failed to configure OpenAI Agents SDK: {str(e)}")
    raise


# Wrap MCP tools with @function_tool decorator for SDK registration
# Note: user_id is injected from context, not exposed to the agent
@function_tool
async def add_task(
    ctx: RunContextWrapper[Any],
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
) -> dict:
    """
    Add a new task for the user.

    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Task priority - low, medium, or high (optional)
        category: Task category (optional)

    Returns:
        Dictionary with task_id, status, and task details
    """
    user_id = ctx.context.get("user_id")
    logger.debug(f"Tool called: add_task for user {user_id}, title='{title}'")
    result = await add_task_tool(user_id, title, description, priority, category)
    logger.info(f"✅ Task created: {result.get('task_id')} for user {user_id}")
    return result


@function_tool
async def list_tasks(
    ctx: RunContextWrapper[Any],
    status: Optional[str] = "all"
) -> dict:
    """
    List tasks for the user with optional status filtering.

    Args:
        status: Filter by status - "all", "pending", or "completed" (default: "all")

    Returns:
        Dictionary with tasks list and count
    """
    user_id = ctx.context.get("user_id")
    logger.debug(f"Tool called: list_tasks for user {user_id}, status='{status}'")
    result = await list_tasks_tool(user_id, status)
    logger.info(f"✅ Listed {result.get('count', 0)} tasks for user {user_id}")
    return result


@function_tool
async def complete_task(
    ctx: RunContextWrapper[Any],
    task_id: str
) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: UUID of the task to complete

    Returns:
        Dictionary with task_id, status, and title
    """
    user_id = ctx.context.get("user_id")
    logger.debug(f"Tool called: complete_task for user {user_id}, task_id={task_id}")
    result = await complete_task_tool(user_id, task_id)
    logger.info(f"✅ Task completed: {task_id} for user {user_id}")
    return result


@function_tool
async def delete_task(
    ctx: RunContextWrapper[Any],
    task_id: str
) -> dict:
    """
    Delete a task for the user.

    Args:
        task_id: UUID of the task to delete

    Returns:
        Dictionary with task_id, status, and title
    """
    user_id = ctx.context.get("user_id")
    logger.debug(f"Tool called: delete_task for user {user_id}, task_id={task_id}")
    result = await delete_task_tool(user_id, task_id)
    logger.info(f"✅ Task deleted: {task_id} for user {user_id}")
    return result


@function_tool
async def update_task(
    ctx: RunContextWrapper[Any],
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
) -> dict:
    """
    Update a task's title, description, priority, and/or category.

    Args:
        task_id: UUID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        priority: New task priority - "low", "medium", or "high" (optional)
        category: New task category (optional)

    Returns:
        Dictionary with task_id, status, and updated fields
    """
    user_id = ctx.context.get("user_id")
    logger.debug(f"Tool called: update_task for user {user_id}, task_id={task_id}")
    result = await update_task_tool(user_id, task_id, title, description, priority, category)
    logger.info(f"✅ Task updated: {task_id} for user {user_id} (fields: {result.get('updated_fields', [])})")
    return result


# Create Agent instance with tools and instructions
# Note: Agent is initialized at module load for efficiency
agent = Agent(
    name="TodoAssistant",
    model="gpt-4o-mini",
    instructions="""You are a helpful task management assistant. You help users manage their todo tasks through natural conversation.

**Your Capabilities:**
- Add tasks (with optional priority: low/medium/high, and category)
- List tasks (all, pending, or completed)
- Mark tasks as complete
- Delete tasks (with confirmation)
- Update tasks (title, description, priority, category)

**Language Support:**
Detect the user's language and respond in the SAME language (English, Roman Urdu, or Urdu). Use English for tool parameter values.

**Task Numbering:**
Tasks are numbered starting from 1. When users say "task 1", use the task_id from position 1 in the list.

**Guidelines:**
1. Be friendly and confirm actions
2. Ask for clarification when needed
3. ALWAYS confirm before deleting tasks
4. If updating without specifying what, ask what to change

**Examples:**

User: "Add task: buy groceries" → add_task(title="buy groceries")
User: "Add high priority task: report" → add_task(title="report", priority="high")
User: "Show my tasks" → list_tasks(status="all")
User: "Mark task 1 done" → list_tasks() to get task_id, then complete_task(task_id=...)
User: "Change task 2 priority to high" → list_tasks() to get task_id, then update_task(task_id=..., priority="high")
User: "Set task 3 category to work" → list_tasks() to get task_id, then update_task(task_id=..., category="work")
User: "Delete task 2" → Ask confirmation first

**Security**: You have access to current user's tasks only. Never mention user_id.""",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)

logger.info(f"🤖 Agent initialized: {agent.name} with {len(agent.tools)} tools")


class AgentService:
    """
    Service for managing AI agent interactions with MCP tools

    Uses OpenAI Agents SDK for intent recognition and tool orchestration.
    Supports multilingual conversations (English, Roman Urdu, Urdu).
    """

    def __init__(self):
        """Initialize agent service with OpenAI Agents SDK"""
        logger.info(f"Initialized AgentService with OpenAI Agents SDK (5 MCP tools registered)")

    def _convert_conversation_history(
        self,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """
        Convert database message objects to SDK input list format

        Args:
            conversation_history: List of message dicts with 'role' and 'content'

        Returns:
            List of messages in SDK format [{"role": "user"|"assistant", "content": "..."}]
        """
        if not conversation_history:
            return []

        # Convert to SDK format (already in correct format from chat_service)
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in conversation_history
        ]

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
            # Convert conversation history to SDK input format
            input_list = self._convert_conversation_history(conversation_history)

            # Log conversation context
            history_length = len(input_list)
            logger.info(f"🔄 Processing message for user {user_id} (history: {history_length} messages)")
            logger.debug(f"User message: {user_message[:100]}...")

            # Add current user message
            input_list.append({
                "role": "user",
                "content": user_message
            })

            # Run agent with conversation history and user_id context
            # user_id is injected into context for tool access
            # SDK handles multi-turn state management within this call
            logger.debug(f"🤖 Running agent with {len(input_list)} messages in context")
            result = await Runner.run(agent, input_list, context={"user_id": user_id})

            # Extract final response
            response_content = result.final_output

            # Log multi-turn conversation metrics
            logger.info(f"✅ Agent response generated for user {user_id} (response length: {len(response_content)} chars)")
            logger.debug(f"Agent response: {response_content[:100]}...")

            return response_content

        except Exception as e:
            logger.error(f"❌ Error processing message for user {user_id}: {str(e)}", exc_info=True)
            # Return user-friendly error message
            return "I encountered an error processing your request. Please try again or rephrase your message."


__all__ = ['AgentService']
