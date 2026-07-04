# ============================================================
# server.py — FastMCP Server Example
# ============================================================
# FastMCP is a high-level Python framework that handles all
# MCP (Model Context Protocol) protocol details under the hood:
#   - Message formatting
#   - JSON-RPC handling
#   - Schema generation from type hints
#   - stdio transport layer (how Claude talks to this server)
# ============================================================

from fastmcp import FastMCP

# Initialize the MCP server with a name.
# This name is visible to any MCP client that connects,
# including Claude-based agents and Claude Desktop.
mcp = FastMCP("MyServer")


# ============================================================
# TOOL — A callable function exposed to MCP clients
# ============================================================
# Tools are actions the client can trigger (like calling an API).
# The @mcp.tool decorator registers this function as a tool.
#
# Type annotations (int, int -> int) are REQUIRED — FastMCP
# uses them to auto-generate strict JSON schemas so the client
# knows exactly what parameters to pass and what to expect back.
# ============================================================

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two integers and returns the result."""
    return a + b


# ============================================================
# STATIC RESOURCE — A read-only data endpoint
# ============================================================
# Resources expose data to clients (not actions, just data).
# They are read-only — the client can read but not modify them.
#
# URI: "notes://list"
# In real apps, this could load from:
#   - A local file or folder
#   - A document store or CMS
#   - A database query
# ============================================================

@mcp.resource("notes://list")
def list_notes() -> list[str]:
    """Returns a static list of all available notes."""
    return ["Note 1", "Note 2"]


# ============================================================
# PARAMETERIZED RESOURCE — A dynamic resource with a URI variable
# ============================================================
# The {note_id} in the URI is a path parameter.
# FastMCP automatically extracts it and passes it as an argument.
#
# Example: A client requesting "notes://42" will call
#          get_note(note_id="42") automatically.
#
# Ideal for: lookups, queries, or fetching a specific item by ID.
# ============================================================

@mcp.resource("notes://{note_id}")
def get_note(note_id: str) -> str:
    """Fetches a single note by its ID from the URI path."""
    return f"Note {note_id}"


# ============================================================
# ENTRY POINT — Start the server
# ============================================================
# mcp.run() does three things:
#   1. Launches the async event loop
#   2. Binds stdin/stdout streams for JSON-RPC communication
#   3. Listens continuously for incoming messages from the client
#
# The `if __name__ == "__main__"` guard ensures the server only
# starts when this file is run directly (e.g. python server.py),
# not when it's imported as a module by another script.
# ============================================================

if __name__ == "__main__":
    mcp.run()