# MCP Protocol Chi tiết

[[Agentic AI Architecture Với Pattern, Framework & MCP]]

---

## Overview

**Model Context Protocol (MCP)** là một open standard protocol do Anthropic phát triển để kết nối AI models với external data sources và tools một cách standardized.

---

## MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      MCP Host                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │Client 1 │  │Client 2 │  │Client 3 │                 │
│  │ (Claude)│  │ (App)   │  │ (Agent) │                 │
│  └────┬────┘  └────┬────┘  └────┬────┘                 │
│       └─────────────┴─────────────┘                    │
│                    │                                     │
│              MCP Protocol Layer                          │
│                    │                                     │
│       ┌─────────────┼─────────────┐                     │
│       ▼             ▼             ▼                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │Server 1 │  │Server 2 │  │Server 3 │                │
│  │ (Files) │  │ (DB)    │  │ (APIs)  │                │
│  └─────────┘  └─────────┘  └─────────┘                │
└─────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. MCP Host
- Application hosting the protocol (Claude Desktop, IDE, Agent system)
- Manages client connections
- Coordinates tool execution

### 2. MCP Client
- Connector within the host
- Establishes connection to servers
- Handles protocol messages

### 3. MCP Server
- Provides capabilities to clients
- Implements standardized interfaces
- Wraps existing data sources/tools

---

## Protocol Primitives

### Resources
```typescript
// Read-only data from server
interface Resource {
  uri: string;
  mimeType?: string;
  name: string;
  description?: string;
}

// Example: File resource
{
  "uri": "file:///home/user/documents/report.pdf",
  "mimeType": "application/pdf",
  "name": "Q4 Report",
  "description": "Quarterly financial report"
}
```

### Tools
```typescript
// Executable functions
interface Tool {
  name: string;
  description: string;
  inputSchema: JSONSchema;
}

// Example: Database query tool
{
  "name": "query_database",
  "description": "Execute SQL query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  }
}
```

### Prompts
```typescript
// Reusable prompt templates
interface Prompt {
  name: string;
  description?: string;
  arguments?: PromptArgument[];
}
```

---

## Communication Flow

```
Client                        Server
  │                              │
  │─── initialize ───────────────►│
  │◄─── initialize result ───────│
  │                              │
  │─── tools/list ──────────────►│
  │◄─── list result ─────────────│
  │                              │
  │─── tools/call ──────────────►│
  │◄─── call result ─────────────│
  │                              │
  │─── resources/list ──────────►│
  │◄─── list result ─────────────│
  │                              │
  │─── resources/read ──────────►│
  │◄─── read result ─────────────│
```

---

## Transport Methods

| Transport | Use Case | Implementation |
|-----------|----------|----------------|
| **stdio** | Local processes | `stdio_client`, `stdio_server` |
| **SSE** | Remote servers | HTTP Server-Sent Events |
| **HTTP** | Web APIs | RESTful endpoints |

---

## Python SDK Implementation

### Server Implementation
```python
from mcp.server import Server
from mcp.types import TextContent, Tool
import mcp.server.stdio

server = Server("my-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculate",
            description="Perform calculation",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "calculate":
        result = eval(arguments["expression"])
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

# Run server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### Client Implementation
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Server configuration
server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None
)

async def use_mcp():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call tool
            result = await session.call_tool(
                "calculate",
                {"expression": "2 + 2"}
            )
            print(f"Result: {result}")
```

---

## Server Types Reference

### FileSystem Server
```python
# Provides: file:// URIs
# Capabilities: read, write, list, search
resources = [
    "file:///home/user/documents",
    "file:///home/user/projects"
]
```

### Database Server
```python
# Provides: SQL/NoSQL access
# Capabilities: query, insert, update, delete
tools = [
    "query_sql",
    "query_nosql",
    "execute_transaction"
]
```

### API Gateway Server
```python
# Provides: REST/GraphQL access
# Capabilities: GET, POST, PUT, DELETE
resources = [
    "api://weather/current",
    "api://stocks/quote/{symbol}"
]
```

---

## Security Considerations

```
┌─────────────────────────────────────────┐
│         Security Layers                  │
├─────────────────────────────────────────┤
│ 1. Transport Security                   │
│    - TLS for remote connections         │
│    - stdio for local trusted processes  │
├─────────────────────────────────────────┤
│ 2. Capability Negotiation               │
│    - Explicit permission requests       │
│    - User confirmation for actions      │
├─────────────────────────────────────────┤
│ 3. Sandboxing                             │
│    - Process isolation                  │
│    - Resource limits                    │
├─────────────────────────────────────────┤
│ 4. Audit Logging                          │
│    - All tool calls logged              │
│    - Resource access tracking             │
└─────────────────────────────────────────┘
```

---

## MCP vs A2A vs ACP

| Protocol | Focus | Best For | Maturity |
|----------|-------|----------|----------|
| **MCP** | Tool/Resource access | Universal tool integration | Stable |
| **A2A** | Agent-to-agent | Direct agent collaboration | Beta |
| **ACP** | Enterprise coordination | Secure B2B communication | Emerging |

---

## Best Practices

1. **Idempotent Tools**: Design tools to be safely retried
2. **Clear Descriptions**: Help LLM understand when to use tools
3. **Schema Validation**: Strict input/output schemas
4. **Error Handling**: Graceful degradation
5. **Resource Discovery**: Dynamic capability advertisement

---

## Resources

- [MCP Official Docs](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
