# Hands-On — Creating Your First MCP Tool

## 🎯 What This Demo Covers

- Adding a meaningful MCP tool to an existing MCP server
- Understanding what makes a tool more than just a Python function
- Verifying tool registration using the FastMCP inspector
- Builds on the previous demo (server already created with FastMCP)

## 🧠 What Is an MCP Tool?

An MCP tool is a clearly defined **action** — not just a Python function. It is a capability that an AI system like Claude can reliably call.

It's designed to reflect real-world agent behavior:

- **Typed inputs** — the AI knows exactly what to pass
- **Deterministic processing** — predictable behavior every time
- **Structured output** — returns parseable data, not free-form text

## 📄 The Tool — `analyze_task`

### What It Does

- Accepts a task description (`string`) and a priority number (`integer`)
- Normalizes the text (strips whitespace, capitalizes)
- Converts the numeric priority into a human-friendly priority label
- Returns a dictionary (structured JSON) with three fields:
  - `original` — the raw input text
  - `summary` — the cleaned/normalized version
  - `priority_level` — the label derived from the number

### Why the Return Type Matters

- Returns a dictionary → structured JSON (not free-form text)
- The agent can parse and use this for planning
- Predictable output = more reliable agent reasoning

### How FastMCP Registers It

```python
@mcp.tool
def analyze_task(description: str, priority: int) -> dict:
    ...
```

- `@mcp.tool` decorator → registers the function as an MCP tool
- FastMCP inspects the function signature and auto-generates a JSON schema
- The schema tells the AI model what inputs to expect and what type is returned

## ▶️ Running & Verifying the Tool

### Run the Server

```bash
python server.py
```

- Server starts, prints a confirmation message
- Enters waiting state — listens for MCP messages via stdio
- Appears to "hang" — this is expected behavior

### Inspect in a Second Terminal

```bash
fastmcp inspect server.py
```

- Open a new terminal, activate the virtual environment again
- Inspector output shows:
  - Server name, MCP version, FastMCP version
  - Component summary: tools, resources, templates
  - Confirms `analyze_task` tool is registered with correct schema

> ⚠️ **Note:** This version of FastMCP does not execute tools directly from the CLI — the inspector is used only to confirm schemas and registration.

## 🔮 What's Next

- In an upcoming demo, this MCP server will be connected to a Claude-based agent
- You'll see the model invoke this tool inside a reasoning loop
- Next hands-on: building a resource provider that exposes documents and files through MCP → foundation for RAG systems

## 💡 Big Takeaway

A well-designed MCP tool has typed inputs, deterministic logic, and structured output — giving AI agents a reliable, schema-driven capability they can reason about and call with confidence.
