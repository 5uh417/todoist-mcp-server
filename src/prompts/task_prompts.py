"""
Task-related prompts for Todoist MCP server
"""

from typing import Dict, Any, Optional


def register_task_prompts(mcp, todoist_client):
    """Register task-related prompts with the MCP server"""
    
    @mcp.prompt()
    async def daily_planning() -> str:
        """Generate a daily planning prompt with current tasks"""
        try:
            tasks = await todoist_client.get_tasks()
            projects = await todoist_client.get_projects()
            
            # Get project names for reference
            project_map = {p['id']: p['name'] for p in projects}
            
            # Organize tasks by project
            tasks_by_project = {}
            for task in tasks:
                project_id = task.get('project_id')
                project_name = project_map.get(project_id, 'Inbox')
                if project_name not in tasks_by_project:
                    tasks_by_project[project_name] = []
                tasks_by_project[project_name].append(task)
            
            prompt = """# Daily Planning Session

## Current Tasks Overview
"""
            
            for project_name, project_tasks in tasks_by_project.items():
                prompt += f"\n### {project_name}\n"
                for task in project_tasks:
                    priority_indicator = "🔴" if task['priority'] == 4 else "🟡" if task['priority'] == 3 else "🟢" if task['priority'] == 2 else "⚪"
                    due_info = f" (Due: {task['due']['string']})" if task.get('due') else ""
                    prompt += f"- {priority_indicator} {task['content']}{due_info}\n"
            
            prompt += """
## Planning Questions
1. What are your top 3 priorities for today?
2. Which tasks can be completed quickly (< 15 minutes)?
3. Are there any tasks that should be rescheduled or delegated?
4. What new tasks need to be added for today?

Please help me prioritize and organize these tasks for maximum productivity."""
            
            return prompt
            
        except Exception as e:
            return f"Error generating daily planning prompt: {str(e)}"
    
    @mcp.prompt()
    async def task_breakdown(task_description: str) -> str:
        """Generate a prompt for breaking down a complex task"""
        return f"""# Task Breakdown Analysis

## Original Task
{task_description}

## Breakdown Framework
Please help me break down this task into smaller, actionable steps:

1. **Identify Components**: What are the main parts of this task?
2. **Sequence Steps**: What order should these be completed in?
3. **Estimate Time**: How long might each step take?
4. **Identify Dependencies**: What needs to be done before other steps?
5. **Define Success**: What does completion look like for each step?

## Output Format
Please provide:
- A list of 3-7 concrete, actionable subtasks
- Time estimates for each subtask
- Any dependencies between subtasks
- Priority level for each subtask

This breakdown will help me create individual tasks in Todoist for better tracking and completion."""
    
    @mcp.prompt()
    async def weekly_review() -> str:
        """Generate a weekly review prompt with task completion analysis"""
        try:
            tasks = await todoist_client.get_tasks()
            projects = await todoist_client.get_projects()
            
            prompt = f"""# Weekly Review

## Current Status
- **Active Tasks**: {len(tasks)}
- **Active Projects**: {len(projects)}

## Review Questions

### Completion Analysis
1. What tasks did I complete this week?
2. What tasks are still pending and why?
3. Which projects made the most progress?

### Process Improvement
1. What patterns do I notice in my task completion?
2. Are there tasks that consistently get postponed?
3. How can I better estimate task duration?

### Planning Ahead
1. What are the priorities for next week?
2. Are there any upcoming deadlines I need to prepare for?
3. Should any projects be restructured or broken down differently?

## Current Task Summary
"""
            
            # Group tasks by priority
            high_priority = [t for t in tasks if t['priority'] == 4]
            medium_priority = [t for t in tasks if t['priority'] == 3]
            low_priority = [t for t in tasks if t['priority'] <= 2]
            
            if high_priority:
                prompt += f"\n### High Priority ({len(high_priority)} tasks)\n"
                for task in high_priority[:5]:  # Limit to first 5
                    prompt += f"- {task['content']}\n"
            
            if medium_priority:
                prompt += f"\n### Medium Priority ({len(medium_priority)} tasks)\n"
                for task in medium_priority[:5]:  # Limit to first 5
                    prompt += f"- {task['content']}\n"
            
            prompt += f"\n### Other Tasks: {len(low_priority)} remaining\n"
            
            return prompt
            
        except Exception as e:
            return f"Error generating weekly review prompt: {str(e)}"