"""
Project management tools for Todoist MCP server
"""

from typing import Dict, List, Optional, Any


def register_project_tools(mcp, todoist_client):
    """Register project-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_projects() -> List[Dict[str, Any]]:
        """Get all projects from Todoist"""
        try:
            projects = await todoist_client.get_projects()
            return projects
        except Exception as e:
            raise Exception(f"Failed to get projects: {str(e)}")
    
    @mcp.tool()
    async def create_project(
        name: str,
        color: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new project in Todoist"""
        try:
            project = await todoist_client.create_project(name=name, color=color)
            return project
        except Exception as e:
            raise Exception(f"Failed to create project: {str(e)}")