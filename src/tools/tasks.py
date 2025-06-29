"""
Task management tools for Todoist MCP server
"""

from typing import Dict, List, Optional, Any


def register_task_tools(mcp, todoist_client):
    """Register task-related tools with the MCP server"""
    
    @mcp.tool()
    async def get_tasks(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks from Todoist, optionally filtered by project"""
        try:
            tasks = await todoist_client.get_tasks(project_id)
            return tasks
        except Exception as e:
            raise Exception(f"Failed to get tasks: {str(e)}")
    
    @mcp.tool()
    async def create_task(
        content: str,
        project_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
        priority: int = 1,
        due_string: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new task in Todoist"""
        try:
            task = await todoist_client.create_task(
                content=content,
                project_id=project_id,
                labels=labels,
                priority=priority,
                due_string=due_string
            )
            return task
        except Exception as e:
            raise Exception(f"Failed to create task: {str(e)}")
    
    @mcp.tool()
    async def complete_task(task_id: str) -> Dict[str, str]:
        """Mark a task as completed"""
        try:
            success = await todoist_client.complete_task(task_id)
            return {"status": "completed", "task_id": task_id} if success else {"status": "failed", "task_id": task_id}
        except Exception as e:
            raise Exception(f"Failed to complete task: {str(e)}")