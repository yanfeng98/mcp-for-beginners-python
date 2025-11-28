# Creating a client

## Exercise: Writing a client

### -1- Import the libraries

Let's import the libraries we need, we will need references to a client and to our chosen transport protocol, stdio. stdio is a protocol for things meant to run on your local machine. SSE is another transport protocol we will show in future chapters but that's your other option. For now though, let's continue with stdio.

#### Python

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
```

### -2- Instantiating client and transport

We will need to create an instance of the transport and that of our client:

#### Python

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()



if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

In the preceding code we've:

- Imported the needed libraries
- Instantiated a server parameters object as we will use this to run the server so we can connect to it with our client.
- Defined a method `run` that in turn calls `stdio_client` which starts a client session.
- Created an entry point where we provide the `run` method to `asyncio.run`.

### -3- Listing the server features

Now, we have a client that can connect to should the program be run. However, it doesn't actually list its features so let's do that next:

#### Python

```python
# List available resources
resources = await session.list_resources()
print("LISTING RESOURCES")
for resource in resources:
    print("Resource: ", resource)

# List available tools
tools = await session.list_tools()
print("LISTING TOOLS")
for tool in tools.tools:
    print("Tool: ", tool.name)
```

Here we list the available resources, `list_resources()` and tools, `list_tools` and print them out.

### -4- Invoke features

To invoke the features we need to ensure we specify the correct arguments and in some cases the name of what we're trying to invoke.

#### Python

```python
# Read a resource
print("READING RESOURCE")
content, mime_type = await session.read_resource("greeting://hello")

# Call a tool
print("CALL TOOL")
result = await session.call_tool("add", arguments={"a": 1, "b": 7})
print(result.content)
```

In the preceding code, we've:

- Called a resource called `greeting` using `read_resource`.
- Invoked a tool called `add` using `call_tool`.

### -5- Run the client

To run the client, type the following command in the terminal:

#### Python

Call the client with the following command:

```sh
python client.py
```

## Assignment

In this assignment, you'll use what you've learned in creating a client but create a client of your own.

Here's a server you can use that you need to call via your client code, see if you can add more features to the server to make it more interesting.

### Python

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

```

## Solution

The **solution folder** contains complete, ready-to-run client implementations that demonstrate all the concepts covered in this tutorial. Each solution includes both client and server code organized in separate, self-contained projects.

### 📁 Solution Structure

The solution directory is organized by programming language:

```text
solution/
└── python/              # Python client implementation
    ├── client.py        # Main client code
    ├── server.py        # Compatible server
    └── README.md        # Python-specific instructions
```

### 📖 Using the Solutions

1. **Navigate to your preferred language folder**:

   ```bash
   cd solution/python/        # For Python
   ```

2. **Follow the README instructions** in each folder for:
   - Installing dependencies
   - Building the project
   - Running the client

3. **Example output** you should see:

   ```text
   Prompt: Please review this code: console.log("hello");
   Resource template: file
   Tool result: { content: [ { type: 'text', text: '9' } ] }
   ```

For complete documentation and step-by-step instructions, see: **[📖 Solution Documentation](./solution/README.md)**

## 🎯 Complete Examples

### Available Complete Examples

| Language | File | Description |
|----------|------|-------------|
| **Python** | [`client_example_python.py`](./client_example_python.py) | Complete Python client using async/await patterns |

Each complete example includes:

- ✅ **Connection establishment** and error handling
- ✅ **Server discovery** (tools, resources, prompts where applicable)
- ✅ **Calculator operations** (add, subtract, multiply, divide, help)
- ✅ **Result processing** and formatted output
- ✅ **Comprehensive error handling**
- ✅ **Clean, documented code** with step-by-step comments

### Getting Started with Complete Examples

1. **Choose your preferred language** from the table above
2. **Review the complete example file** to understand the full implementation
3. **Run the example** following the instructions in [`complete_examples.md`](./complete_examples.md)
4. **Modify and extend** the example for your specific use case

For detailed documentation about running and customizing these examples, see: **[📖 Complete Examples Documentation](./complete_examples.md)**

### 💡 Solution vs. Complete Examples

| **Solution Folder** | **Complete Examples** |
|--------------------|--------------------- |
| Full project structure with build files | Single-file implementations |
| Ready-to-run with dependencies | Focused code examples |
| Production-like setup | Educational reference |
| Language-specific tooling | Cross-language comparison |

Both approaches are valuable - use the **solution folder** for complete projects and the **complete examples** for learning and reference.

## Additional Resources

- [Building clients in MCP](https://modelcontextprotocol.io/quickstart/client)

## Samples

- [Python Calculator](../samples/python/)

## What's Next

- Next: [Creating a client with an LLM](../03-llm-client/README.md)
