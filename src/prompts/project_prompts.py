"""
Project management prompts for Todoist MCP server
"""

from typing import Dict, Any, Optional


def register_project_prompts(mcp, todoist_client):
    """Register project-related prompts with the MCP server"""
    
    @mcp.prompt()
    async def project_planning(project_name: str) -> str:
        """Generate a project planning prompt for a new or existing project"""
        try:
            projects = await todoist_client.get_projects()
            existing_project = next((p for p in projects if p['name'].lower() == project_name.lower()), None)
            
            if existing_project:
                # Get tasks for this project
                tasks = await todoist_client.get_tasks(project_id=existing_project['id'])
                
                prompt = f"""# Project Planning: {project_name}

## Current Project Status
- **Project ID**: {existing_project['id']}
- **Active Tasks**: {len(tasks)}

### Existing Tasks
"""
                for task in tasks[:10]:  # Limit to first 10 tasks
                    priority_indicator = "🔴" if task['priority'] == 4 else "🟡" if task['priority'] == 3 else "🟢" if task['priority'] == 2 else "⚪"
                    due_info = f" (Due: {task['due']['string']})" if task.get('due') else ""
                    prompt += f"- {priority_indicator} {task['content']}{due_info}\n"
                
                if len(tasks) > 10:
                    prompt += f"... and {len(tasks) - 10} more tasks\n"
                
                prompt += """
## Project Review Questions
1. What is the current status of this project?
2. What are the next key milestones?
3. Are there any blockers or dependencies?
4. What tasks can be completed this week?
5. Should any tasks be reprioritized or rescheduled?
"""
            else:
                prompt = f"""# New Project Planning: {project_name}

## Project Setup Framework
Since this is a new project, let's plan it thoroughly:

### 1. Project Definition
- What is the main goal of this project?
- What does success look like?
- What is the expected timeline?

### 2. Task Breakdown
- What are the major phases or milestones?
- What specific tasks need to be completed?
- What is the logical sequence of tasks?

### 3. Resource Planning
- What resources (time, tools, people) are needed?
- Are there any external dependencies?
- What is the priority level of this project?

### 4. Implementation Strategy
- What tasks should be created first?
- How should tasks be prioritized?
- What labels or due dates should be applied?

Please help me structure this project with specific, actionable tasks that can be created in Todoist."""
            
            return prompt
            
        except Exception as e:
            return f"Error generating project planning prompt: {str(e)}"
    
    @mcp.prompt()
    async def project_review() -> str:
        """Generate a comprehensive project review prompt"""
        try:
            projects = await todoist_client.get_projects()
            all_tasks = await todoist_client.get_tasks()
            
            # Analyze tasks by project
            project_stats = {}
            for project in projects:
                project_tasks = [t for t in all_tasks if t.get('project_id') == project['id']]
                high_priority_tasks = [t for t in project_tasks if t['priority'] >= 3]
                overdue_tasks = [t for t in project_tasks if t.get('due') and 'overdue' in str(t.get('due', {}))]
                
                project_stats[project['name']] = {
                    'total_tasks': len(project_tasks),
                    'high_priority': len(high_priority_tasks),
                    'overdue': len(overdue_tasks),
                    'id': project['id']
                }
            
            prompt = """# Project Portfolio Review

## Overview
"""
            
            for project_name, stats in project_stats.items():
                status_emoji = "🔴" if stats['overdue'] > 0 else "🟡" if stats['high_priority'] > 0 else "🟢"
                prompt += f"- {status_emoji} **{project_name}**: {stats['total_tasks']} tasks"
                
                if stats['high_priority'] > 0:
                    prompt += f" ({stats['high_priority']} high priority)"
                if stats['overdue'] > 0:
                    prompt += f" ({stats['overdue']} overdue)"
                prompt += "\n"
            
            prompt += """
## Review Framework

### Health Check
1. Which projects are progressing well?
2. Which projects have stalled or need attention?
3. Are there any projects with too many overdue tasks?

### Resource Allocation
1. Which projects deserve more focus this week?
2. Are there projects that should be paused or cancelled?
3. How is my workload distributed across projects?

### Strategic Alignment
1. Do these projects align with my current goals?
2. Are there any projects that are no longer relevant?
3. What new projects should I consider starting?

### Action Items
1. Which projects need immediate attention?
2. What tasks should be reprioritized across projects?
3. How can I better balance my project portfolio?

Please help me analyze this project portfolio and suggest improvements to my project management approach."""
            
            return prompt
            
        except Exception as e:
            return f"Error generating project review prompt: {str(e)}"
    
    @mcp.prompt()
    async def project_completion(project_name: str) -> str:
        """Generate a project completion and retrospective prompt"""
        return f"""# Project Completion: {project_name}

## Completion Checklist
- [ ] All planned tasks completed
- [ ] Deliverables reviewed and approved
- [ ] Documentation updated
- [ ] Stakeholders notified
- [ ] Resources cleaned up
- [ ] Lessons learned documented

## Retrospective Questions

### What Went Well?
1. What aspects of this project were successful?
2. What processes or approaches worked effectively?
3. What tools or resources were particularly helpful?

### What Could Be Improved?
1. What challenges did we encounter?
2. What would I do differently next time?
3. Were there any missed opportunities?

### Lessons Learned
1. What insights can I apply to future projects?
2. What new skills or knowledge did I gain?
3. How can I improve my project planning process?

### Next Steps
1. Are there any follow-up tasks or maintenance items?
2. Should this project lead to new initiatives?
3. How should I archive or organize project materials?

Please help me conduct a thorough review of this completed project and extract valuable lessons for future work."""