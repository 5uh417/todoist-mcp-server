# Todoist MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with Todoist, enabling AI assistants to manage tasks and projects through the Todoist API.

## Features

### 🔧 Core Tools
- **Task Management**
  - `get_tasks` - Retrieve tasks from Todoist (with optional project filtering)
  - `create_task` - Create new tasks with full customization (priority, labels, due dates)
  - `complete_task` - Mark tasks as completed

- **Project Management**
  - `get_projects` - Retrieve all projects from your Todoist account
  - `create_project` - Create new projects with optional color customization

- **Setup & Configuration**
  - `setup_todoist` - Dynamic API token configuration and connection verification

### 🏗️ Architecture

- **FastMCP Framework**: Built on the modern FastMCP server framework for optimal performance
- **Async Operations**: Full async/await support for non-blocking API calls
- **Modular Design**: Clean separation of concerns with dedicated modules for:
  - Task operations (`src/tools/tasks.py`)
  - Project operations (`src/tools/projects.py`)
  - API client (`src/todoist_client.py`)
  - Resource management (`src/resources/`)
  - Prompt management (`src/prompts/`)

### 🔐 Security & Configuration

- **Environment Variables**: Secure API token management via `.env` files
- **Token Validation**: Built-in connection testing and validation
- **Error Handling**: Comprehensive error handling with meaningful error messages

## Installation

### Prerequisites
- Python 3.10 or higher
- Todoist account with API access

### Setup

1. **Install the package**
   ```bash
   pip install -e .
   ```

2. **Set up your Todoist API token**
   
   Create a `.env` file in the project root:
   ```bash
   TODOIST_API_TOKEN=your_api_token_here
   ```
   
   Or set it as an environment variable:
   ```bash
   export TODOIST_API_TOKEN=your_api_token_here
   ```

3. **Configure Claude Desktop** (if using with Claude Desktop)
   
   Add to your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "todoist": {
         "url": "http://127.0.0.1:8000",
         "env": {
           "TODOIST_API_TOKEN": "your_api_token_here"
         }
       }
     }
   }
   ```

## Usage

### Running the Server

```bash
# Direct execution
python main.py

# Or using the module
python -m src.server
```

### HTTP Server Mode

The server also supports HTTP mode for web-based integrations:

```bash
python -m uvicorn src.http_server:app --reload --port 8000
```

## API Integration

### Task Operations

```python
# Get all tasks
tasks = await get_tasks()

# Get tasks from specific project
project_tasks = await get_tasks(project_id="12345")

# Create a new task
task = await create_task(
    content="Review quarterly reports",
    project_id="work_project_id",
    priority=3,
    due_string="tomorrow at 9am",
    labels=["urgent", "review"]
)

# Complete a task
result = await complete_task(task_id="67890")
```

### Project Operations

```python
# Get all projects
projects = await get_projects()

# Create a new project
project = await create_project(
    name="Q4 Planning",
    color="blue"
)
```

## Development

### Project Structure

```
todoist-mcp-server/
├── src/
│   ├── __main__.py              # Module entry point
│   ├── server.py                # Main MCP server setup
│   ├── http_server.py           # HTTP server variant
│   ├── todoist_client.py        # Todoist API client
│   ├── tools/
│   │   ├── tasks.py            # Task management tools
│   │   └── projects.py         # Project management tools
│   ├── resources/
│   │   └── todoist_resources.py # MCP resources
│   └── prompts/
│       ├── task_prompts.py     # Task-related prompts
│       └── project_prompts.py  # Project-related prompts
├── main.py                      # Simple entry point
├── pyproject.toml              # Project configuration
├── claude_desktop_config.json  # Claude Desktop configuration
└── CLAUDE.md                   # Development guidelines
```

### Dependencies

- **mcp[cli]** (≥1.4.0) - Model Context Protocol framework
- **httpx** (≥0.25.0) - Modern HTTP client for API calls
- **uvicorn** (≥0.23.0) - ASGI server for HTTP mode
- **python-dotenv** (≥1.1.1) - Environment variable management

### Development Commands

```bash
# Install in development mode
pip install -e .

# Run with auto-reload (development)
python -m uvicorn src.http_server:app --reload

# Test API connection
python -c "from src.todoist_client import TodoistClient; import asyncio; asyncio.run(TodoistClient().get_projects())"
```

## Contributing

This project follows clean architecture principles:

1. **API Client Layer** (`todoist_client.py`) - Handles all Todoist API interactions
2. **Tools Layer** (`tools/`) - MCP tool implementations
3. **Server Layer** (`server.py`) - MCP server setup and configuration
4. **Resources & Prompts** - MCP resources and prompt management

When contributing:
- Follow the existing async patterns
- Add proper error handling
- Update documentation for new features
- Test with both environment variable and dynamic token setup

## License

This project is open source and available under standard licensing terms.