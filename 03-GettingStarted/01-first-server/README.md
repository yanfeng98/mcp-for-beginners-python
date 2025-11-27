# Getting Started with MCP

## Overview

## Setting Up Your MCP Environment

Before you begin working with MCP, it's important to prepare your development environment and understand the basic workflow. This section will guide you through the initial setup steps to ensure a smooth start with MCP.

### Prerequisites

Before diving into MCP development, ensure you have:

- **Development Environment**: For your chosen language (C#, Java, Python, TypeScript, or Rust)
- **IDE/Editor**: Visual Studio, Visual Studio Code, IntelliJ, Eclipse, PyCharm, or any modern code editor
- **Package Managers**: NuGet, Maven/Gradle, pip, npm/yarn, or Cargo
- **API Keys**: For any AI services you plan to use in your host applications

## Basic MCP Server Structure

An MCP server typically includes:

- **Server Configuration**: Setup port, authentication, and other settings
- **Resources**: Data and context made available to LLMs
- **Tools**: Functionality that models can invoke
- **Prompts**: Templates for generating or structuring text

Here's a simplified example in TypeScript:

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});

// Add an addition tool
server.tool("add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

// Add a dynamic greeting resource
server.resource(
  "file",
  // The 'list' parameter controls how the resource lists available files. Setting it to undefined disables listing for this resource.
  new ResourceTemplate("file://{path}", { list: undefined }),
  async (uri, { path }) => ({
    contents: [{
      uri: uri.href,
      text: `File, ${path}!`
    }]
  })
);

// Add a file resource that reads the file contents
server.resource(
  "file",
  new ResourceTemplate("file://{path}", { list: undefined }),
  async (uri, { path }) => {
    let text;
    try {
      text = await fs.readFile(path, "utf8");
    } catch (err) {
      text = `Error reading file: ${err.message}`;
    }
    return {
      contents: [{
        uri: uri.href,
        text
      }]
    };
  }
);

server.prompt(
  "review-code",
  { code: z.string() },
  ({ code }) => ({
    messages: [{
      role: "user",
      content: {
        type: "text",
        text: `Please review this code:\n\n${code}`
      }
    }]
  })
);

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
```

In the preceding code we:

- Import the necessary classes from the MCP TypeScript SDK.
- Create and configure a new MCP server instance.
- Register a custom tool (`calculator`) with a handler function.
- Start the server to listen for incoming MCP requests.

## Testing and Debugging

Before you begin testing your MCP server, it's important to understand the available tools and best practices for debugging. Effective testing ensures your server behaves as expected and helps you quickly identify and resolve issues. The following section outlines recommended approaches for validating your MCP implementation.

MCP provides tools to help you test and debug your servers:

- **Inspector tool**, this graphical interface allows you to connect to your server and test your tools, prompts and resources.
- **curl**, you can also connect to your server using a command line tool like curl or other clients than can create and run HTTP commands.

### Using MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a visual testing tool that helps you:

1. **Discover Server Capabilities**: Automatically detect available resources, tools, and prompts
2. **Test Tool Execution**: Try different parameters and see responses in real-time
3. **View Server Metadata**: Examine server info, schemas, and configurations

```bash
# ex TypeScript, installing and running MCP Inspector
npx @modelcontextprotocol/inspector node build/index.js
```

When you run the above commands, the MCP Inspector will launch a local web interface in your browser. You can expect to see a dashboard displaying your registered MCP servers, their available tools, resources, and prompts. The interface allows you to interactively test tool execution, inspect server metadata, and view real-time responses, making it easier to validate and debug your MCP server implementations.

Here's a screenshot of what it can look like:

![MCP Inspector server connection](/03-GettingStarted/01-first-server/assets/connected.png)

## Common Setup Issues and Solutions

| Issue | Possible Solution |
|-------|-------------------|
| Connection refused | Check if server is running and port is correct |
| Tool execution errors | Review parameter validation and error handling |
| Authentication failures | Verify API keys and permissions |
| Schema validation errors | Ensure parameters match the defined schema |
| Server not starting | Check for port conflicts or missing dependencies |
| CORS errors | Configure proper CORS headers for cross-origin requests |
| Authentication issues | Verify token validity and permissions |

## Local Development

For local development and testing, you can run MCP servers directly on your machine:

1. **Start the server process**: Run your MCP server application
2. **Configure networking**: Ensure the server is accessible on the expected port
3. **Connect clients**: Use local connection URLs like `http://localhost:3000`

```bash
# Example: Running a TypeScript MCP server locally
npm run start
# Server running at http://localhost:3000
```

## Building your first MCP Server

We've covered [Core concepts](/01-CoreConcepts/README.md) in a previous lesson, now it's time to put that knowledge to work.

### What a server can do

Before we start writing code, let's just remind ourselves what a server can do:

An MCP server can for example:

- Access local files and databases
- Connect to remote APIs
- Perform computations
- Integrate with other tools and services
- Provide a user interface for interaction

## Exercise: Creating a server

To create a server, you need to follow these steps:

- Install the MCP SDK.
- Create a a project and set up the project structure.
- Write the server code.
- Test the server.

### -1- Create project

#### Python

```sh
# Create project dir
mkdir calculator-server
cd calculator-server
# Open the folder in Visual Studio Code - Skip this if you are using a different IDE
code .
```

### -2- Add dependencies

#### Python

```sh
# Create a virtual env and install dependencies
python -m venv venv
source venv/bin/activate
pip install "mcp[cli]"
```

### -3- Create project files

#### Python

Create a file *server.py*

```sh
touch server.py
```

### -4- Create server code

#### Python

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")
```

### -5- Adding a tool and a resource

#### Python

```python
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

In the preceding code we've:

- Defined a tool `add` that takes parameters `a` and `p`, both integers.
- Created a resource called `greeting` that takes parameter `name`.

### -6- Final code

#### Python

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

# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()
```

### -7- Test the server

Start the server with the following command:

#### Python

```sh
mcp run server.py
```

> To use MCP Inspector, use `mcp dev server.py` which automatically launches the Inspector and provides the required proxy session token. If using `mcp run server.py`, you’ll need to manually start the Inspector and configure the connection.

### -8- Run using the inspector

The inspector is a great tool that can start up your server and lets you interact with it so you can test that it works. Let's start it up:

#### Python

Python wraps a Node.js tool called inspector. It's possible to call said tool like so:

```sh
mcp dev server.py
```

However, it doesn't implement all the methods available on the tool so you're recommended to run the Node.js tool directly like below:

```sh
npx @modelcontextprotocol/inspector mcp run server.py
```

If you're using a tool or IDE that allows you to configure commands and arguments for running scripts,
make sure to set `python` in the `Command` field and `server.py` as `Arguments`. This ensures the script runs correctly.

### Official SDKs

- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) - The official Python implementation

## Samples

- [Python Calculator](../samples/python/)

## Solution

[Solution](./solution/README.md)

## What's next

Next: [Getting Started with MCP Clients](../02-client/README.md)
