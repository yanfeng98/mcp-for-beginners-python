# Getting Started with MCP

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
