from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools, StdioServerParams
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import FunctionCallTermination
import asyncio

def terminate():
    """Terminate the conversation"""
    pass


async def main():
    params = StdioServerParams(
        command="npx",
        args=["-y", "mcp-remote", f"https://mcp.tavily.com/mcp/?tavilyApiKey={open('api_tavily.txt').read().strip()}"]
    )

    mcp_tools = await mcp_server_tools(server_params=params)

    model = OpenAIChatCompletionClient(
        model='gpt-4o',
        api_key=open('api_openai.txt').read().strip()
    )

    agent = AssistantAgent(
        name='agent',
        system_message=open('agent.txt').read().strip(),
        model_client=model,
        tools=(mcp_tools + [terminate]),
        reflect_on_tool_use=True
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        max_turns=10,
        termination_condition=FunctionCallTermination(function_name='terminate')
    )

    task = "Is Lionel Messi 25 years old?"

    async for msg in team.run_stream(task=task):
        print("---" * 20)
        print(msg)

if __name__ == '__main__':
    asyncio.run(main())