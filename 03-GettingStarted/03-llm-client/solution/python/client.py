import os
import json
import openai
from typing import Any
from openai import OpenAI
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

server_params = StdioServerParameters(
    command="mcp",
    args=["run", "server.py"],
    env=None,
)

def call_llm(prompt: str, functions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    model_name: str = "deepseek-v3-1-terminus"
    base_url: str = os.environ["DEEPSEEK_API_BASE"]
    api_key: str = os.environ["DEEPSEEK_API_KEY"]

    client: OpenAI = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=openai.Timeout(600, connect=600)
    )

    print("CALLING LLM")
    response = client.chat.completions.create(
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
        tools=functions,
        temperature=1.,
        max_tokens=1000,
        top_p=1.
    )

    response_message = response.choices[0].message

    functions_to_call: list[dict[str, Any]] = []

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print("TOOL: ", tool_call)
            name: str = tool_call.function.name
            args: dict[str, Any] = json.loads(tool_call.function.arguments)
            functions_to_call.append({ "name": name, "args": args })

    return functions_to_call

def convert_to_llm_tool(tool) -> dict[str, Any]:
    tool_schema: dict[str, Any] = {
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

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            await session.initialize()

            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)

            tools = await session.list_tools()
            print("LISTING TOOLS")

            functions: list[dict[str, Any]] = []

            for tool in tools.tools:
                print("Tool: ", tool.name)
                print("Tool", tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))

            prompt: str = "Add 2 to 20"

            functions_to_call: list[dict[str, Any]] = call_llm(prompt, functions)

            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments=f["args"])
                print("TOOLS result: ", result.content)

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())