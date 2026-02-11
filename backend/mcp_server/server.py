"""
MCP Server for AI Chatbot Task Management Tools

This module provides the MCP server entry point with tool registration
for task management operations (add, list, complete, delete, update).

Uses OpenAI Agents SDK's function_tool decorator for tool definitions.
All tools enforce user_id isolation for multi-user security.
"""

from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.todo import TodoTask
from database.session import get_session
import logging

logger = logging.getLogger(__name__)


class MCPToolError(Exception):
    """Base exception for MCP tool errors"""
    pass


class TaskNotFoundError(MCPToolError):
    """Raised when a task is not found"""
    pass


class UnauthorizedAccessError(MCPToolError):
    """Raised when user tries to access another user's task"""
    pass


# Tool implementations will be imported from tools/ directory
from mcp_server.tools.add_task import add_task_tool
from mcp_server.tools.list_tasks import list_tasks_tool
from mcp_server.tools.complete_task import complete_task_tool
from mcp_server.tools.delete_task import delete_task_tool
from mcp_server.tools.update_task import update_task_tool


# Export all tools for agent registration
ALL_TOOLS = [
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
]


def get_all_tools():
    """
    Get all registered MCP tools for agent integration

    Returns:
        List of tool functions decorated with @function_tool
    """
    return ALL_TOOLS


__all__ = [
    'get_all_tools',
    'ALL_TOOLS',
    'MCPToolError',
    'TaskNotFoundError',
    'UnauthorizedAccessError'
]
