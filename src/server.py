"""
Todoist MCP Server

This server provides MCP integration with Todoist API following the patterns
from GitHub's official MCP server implementation.
"""

import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()
from .todoist_client import TodoistClient
from .tools.tasks import register_task_tools
from .tools.projects import register_project_tools
from .resources.todoist_resources import register_todoist_resources
from .prompts.task_prompts import register_task_prompts
from .prompts.project_prompts import register_project_prompts

# Initialize the MCP server
mcp = FastMCP("todoist-mcp-server")

# Initialize Todoist client
todoist_client = None

def initialize_client():
    """Initialize the Todoist client with API token"""
    global todoist_client
    api_token = os.getenv("TODOIST_API_TOKEN")
    if not api_token:
        raise ValueError("TODOIST_API_TOKEN environment variable is required")
    todoist_client = TodoistClient(api_token)

@mcp.tool()
async def setup_todoist(api_token: str) -> str:
    """Set up Todoist API token"""
    global todoist_client
    try:
        todoist_client = TodoistClient(api_token)
        # Test the connection
        await todoist_client.get_projects()
        return "Todoist API token set successfully and connection verified"
    except Exception as e:
        return f"Failed to set up Todoist: {str(e)}"

# Initialize client if token is available
try:
    initialize_client()
    if todoist_client:
        # Register tools, resources, and prompts
        register_task_tools(mcp, todoist_client)
        register_project_tools(mcp, todoist_client)
        register_todoist_resources(mcp, todoist_client)
        register_task_prompts(mcp, todoist_client)
        register_project_prompts(mcp, todoist_client)
except ValueError:
    # API token not set, will need to use setup_todoist tool first
    pass

if __name__ == "__main__":
    mcp.run()