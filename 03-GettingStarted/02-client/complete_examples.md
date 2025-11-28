# Complete MCP Client Examples

## Available Clients

### Python Client (`client_example_python.py`)

- **Transport**: Stdio (Standard Input/Output)
- **Target Server**: Local Python MCP server
- **Features**:
  - Async/await pattern for operations
  - Tool and resource discovery
  - Calculator operations testing
  - Resource content reading
  - Class-based organization

**To run:**

```bash
python client_example_python.py
```

## Common Features Across All Clients

Each client implementation demonstrates:

1. **Connection Management**
   - Establishing connection to MCP server
   - Handling connection errors
   - Proper cleanup and resource management

2. **Server Discovery**
   - Listing available tools
   - Listing available resources (where supported)
   - Listing available prompts (where supported)

3. **Tool Invocation**
   - Basic calculator operations (add, subtract, multiply, divide)
   - Help command for server information
   - Proper argument passing and result handling

4. **Error Handling**
   - Connection errors
   - Tool execution errors
   - Graceful failure and user feedback

5. **Result Processing**
   - Extracting text content from responses
   - Formatting output for readability
   - Handling different response formats

## Prerequisites

Before running these clients, ensure you have:

1. **The corresponding MCP server running** (from `../01-first-server/`)
2. **Required dependencies installed** for your chosen language
3. **Proper network connectivity** (for HTTP-based transports)

## Next Steps

After exploring these client examples:

1. **Modify the clients** to add new features or operations
2. **Create your own server** and test it with these clients
3. **Experiment with different transports** (SSE vs. Stdio)
4. **Build a more complex application** that integrates MCP functionality

## Troubleshooting

### Common Issues

1. **Connection refused**: Ensure the MCP server is running on the expected port/path
2. **Module not found**: Install the required MCP SDK for your language
3. **Permission denied**: Check file permissions for stdio transport
4. **Tool not found**: Verify the server implements the expected tools

### Debug Tips

1. **Enable verbose logging** in your MCP SDK
2. **Check server logs** for error messages
3. **Verify tool names and signatures** match between client and server
4. **Test with MCP Inspector** first to validate server functionality

## Related Documentation

- [Main Client Tutorial](./README.md)
- [MCP Server Examples](../01-first-server/)
- [MCP with LLM Integration](../03-llm-client/)
- [Official MCP Documentation](https://modelcontextprotocol.io/)
