"""
Resource handlers for Todoist MCP server
"""

from typing import Dict, List, Any


def register_todoist_resources(mcp, todoist_client):
    """Register Todoist resources with the MCP server"""
    
    @mcp.resource("todoist://tasks")
    async def get_tasks_resource() -> str:
        """Get all tasks as a resource"""
        try:
            tasks = await todoist_client.get_tasks()
            if not tasks:
                return "No tasks found"
            
            task_list = []
            for task in tasks:
                task_info = f"- {task['content']} (ID: {task['id']}, Priority: {task['priority']})"
                if task.get('due'):
                    task_info += f" - Due: {task['due']['string']}"
                task_list.append(task_info)
            
            return f"Todoist Tasks ({len(tasks)} total):\n" + "\n".join(task_list)
        except Exception as e:
            return f"Error fetching tasks: {str(e)}"
    
    @mcp.resource("todoist://projects")
    async def get_projects_resource() -> str:
        """Get all projects as a resource"""
        try:
            projects = await todoist_client.get_projects()
            if not projects:
                return "No projects found"
            
            project_list = [f"- {project['name']} (ID: {project['id']})" for project in projects]
            return f"Todoist Projects ({len(projects)} total):\n" + "\n".join(project_list)
        except Exception as e:
            return f"Error fetching projects: {str(e)}"
    
    @mcp.resource("todoist://project/{project_id}/tasks")
    async def get_project_tasks_resource(project_id: str) -> str:
        """Get tasks for a specific project"""
        try:
            tasks = await todoist_client.get_tasks(project_id=project_id)
            if not tasks:
                return f"No tasks found for project {project_id}"
            
            task_list = []
            for task in tasks:
                task_info = f"- {task['content']} (ID: {task['id']}, Priority: {task['priority']})"
                if task.get('due'):
                    task_info += f" - Due: {task['due']['string']}"
                task_list.append(task_info)
            
            return f"Tasks for Project {project_id} ({len(tasks)} total):\n" + "\n".join(task_list)
        except Exception as e:
            return f"Error fetching tasks for project {project_id}: {str(e)}"