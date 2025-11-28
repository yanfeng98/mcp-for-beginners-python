# Creating a client with LLM

So far, you've seen how to create a server and a client. The client have been able to call the server explicitly to list its tools, resources and prompts. However, it's not very practical approach. Your user lives in the agentic era and expects to use prompts and communicate with an LLM to do so. For your user, it doesn't care if you use MCP or not to store your capabilities but they do expect to use natural language to interact. So how do we solve this? The solution is about adding an LLM to the client.

## Overview

In this lesson we focus on adding an LLM to do your client and show how this provides a much better experience for your user.

## Approach

Let's try to understand the approach we need to take. Adding an LLM sounds simple, but will we actually do this?

Here's how the client will interact with the server:

1. Establish connection with server.

1. List capabilities, prompts, resources and tools, and save down their schema.

1. Add an LLM and pass the saved capabilities and their schema in a format the LLM understands.

1. Handle a user prompt by passing it to the LLM together with the tools listed by the client.

Great, now we understand how we can do this at high level, let's try this out in below exercise.

## Exercise: Creating a client with an LLM

In this exercise, we will learn to add an LLM to our client.

### Authentication using GitHub Personal Access Token

Creating a GitHub token is a straightforward process. Here’s how you can do it:

- Go to GitHub Settings – Click on your profile picture in the top right corner and select Settings.
- Navigate to Developer Settings – Scroll down and click on Developer Settings.
- Select Personal Access Tokens – Click on Fine-grained tokens and then Generate new token.
- Configure Your Token – Add a note for reference, set an expiration date, and select the necessary scopes (permissions). In this case be sure to add the Models permission.
- Generate and Copy the Token – Click Generate token, and make sure to copy it immediately, as you won’t be able to see it again.

### -1- Connect to server

Let's create our client first:

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

- Imported the needed libraries for MCP
- Created a client

### -2- List server capabilities

Now we will connect to the server and ask for its capabilities:

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
    print("Tool", tool.inputSchema["properties"])
```

Here's what we added:

- Listing resources and tools and printed them. For tools we also list `inputSchema` which we use later.

### -3- Convert server capabilities to LLM tools

Next step after listing server capabilities is to convert them into a format that the LLM understands. Once we do that, we can provide these capabilities as tools to our LLM.

#### Python

1. First, let's create the following converter function

    ```python
    def convert_to_llm_tool(tool):
        tool_schema = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "type": "function",
                "parameters": {
                    "type": "object",
                    "properties": tool.inputSchema["properties"]
                }
            }
        }

        return tool_schema
    ```

    In the function above `convert_to_llm_tools` we take an MCP tool response and convert it to a format that the LLM can understand.

1. Next, let's update our client code to leverage this function like so:

    ```python
    for tool in tools.tools:
        print("Tool: ", tool.name)
        print("Tool", tool.inputSchema["properties"])
        functions.append(convert_to_llm_tool(tool))
    ```

    Here, we're adding a call to `convert_to_llm_tool` to convert the MCP tool response to something we can feed the LLM later.

### -4- Handle user prompt request

In this part of the code, we will handle user requests.

#### Python

1. Let's add some imports needed to call an LLM

    ```python
    # llm
    import os
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    import json
    ```

1. Next, let's add the function that will call the LLM:

    ```python
    # llm

    def call_llm(prompt, functions):
        token = os.environ["GITHUB_TOKEN"]
        endpoint = "https://models.inference.ai.azure.com"

        model_name = "gpt-4o"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        print("CALLING LLM")
        response = client.complete(
            messages=[
                {
                "role": "system",
                "content": "You are a helpful assistant.",
                },
                {
                "role": "user",
                "content": prompt,
                },
            ],
            model=model_name,
            tools = functions,
            # Optional parameters
            temperature=1.,
            max_tokens=1000,
            top_p=1.
        )

        response_message = response.choices[0].message

        functions_to_call = []

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                print("TOOL: ", tool_call)
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                functions_to_call.append({ "name": name, "args": args })

        return functions_to_call
    ```

    In the preceding code we've:

    - Passed our functions, that we found on the MCP server and converted, to the LLM.
    - Then we called the LLM with said functions.
    - Then, we're inspecting the result to see what functions we should call, if any.
    - Finally, we pass an array of functions to call.

1. Final step, let's update our main code:

    ```python
    prompt = "Add 2 to 20"

    # ask LLM what tools to all, if any
    functions_to_call = call_llm(prompt, functions)

    # call suggested functions
    for f in functions_to_call:
        result = await session.call_tool(f["name"], arguments=f["args"])
        print("TOOLS result: ", result.content)
    ```

    There, that was the final step, in the code above we're:

    - Calling an MCP tool via `call_tool` using a function that the LLM thought we should call based on our prompt.
    - Printing the result of the tool call to the MCP Server.

## Assignment

Take the code from the exercise and build out the server with some more tools. Then create a client with an LLM, like in the exercise, and test it out with different prompts to make sure all your server tools gets called dynamically. This way of building a client means the end user will have a great user experience as they're able to use prompts, instead of exact client commands, and be oblivious to any MCP server being called.

## Solution

[Solution](/03-GettingStarted/03-llm-client/solution/README.md)

## Samples

- [Python Calculator](../samples/python/)

## Additional Resources

## What's Next

- Next: [Consuming a server using Visual Studio Code](../04-vscode/README.md)
