"""
Entry point for running todoist_mcp_server as a module
"""

from .server import mcp

if __name__ == "__main__":
    mcp.run()