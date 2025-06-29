"""
HTTP-based Todoist MCP Server
"""

import uvicorn
from mcp.server.fastmcp import FastMCP

# Import your existing server setup
from .server import mcp

def run_http_server():
    """Run the MCP server over HTTP"""
    # Run FastMCP with HTTP transport
    uvicorn.run(
        "todoist_mcp_server.http_server:app",
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

# Get the HTTP app from FastMCP
app = mcp.streamable_http_app

if __name__ == "__main__":
    run_http_server()