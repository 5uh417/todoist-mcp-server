"""
Todoist API Client

This module handles all interactions with the Todoist API.
"""

import os
from typing import Dict, List, Optional, Any
import httpx


class TodoistClient:
    """Client for interacting with the Todoist API"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("TODOIST_API_TOKEN")
        self.base_url = "https://api.todoist.com/rest/v2"
        
        if not self.api_token:
            raise ValueError("Todoist API token is required. Set TODOIST_API_TOKEN environment variable.")
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def get_tasks(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks from Todoist"""
        params = {}
        if project_id:
            params["project_id"] = project_id
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tasks",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    
    async def create_task(
        self, 
        content: str, 
        project_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
        priority: int = 1,
        due_string: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new task"""
        task_data = {
            "content": content,
            "priority": priority
        }
        
        if project_id:
            task_data["project_id"] = project_id
        if labels:
            task_data["labels"] = labels
        if due_string:
            task_data["due_string"] = due_string
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks",
                headers=self.headers,
                json=task_data
            )
            response.raise_for_status()
            return response.json()
    
    async def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks/{task_id}/close",
                headers=self.headers
            )
            response.raise_for_status()
            return True
    
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/projects",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_project(self, name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """Create a new project"""
        project_data = {"name": name}
        if color:
            project_data["color"] = color
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/projects",
                headers=self.headers,
                json=project_data
            )
            response.raise_for_status()
            return response.json()