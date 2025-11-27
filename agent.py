from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

class Agent (AssistantAgent):
    pass


async def main():
    model = OpenAIChatCompletionClient(
        model='gpt-4o',
        api_key=open('./api_openai.txt').read().strip()
    )

    agent = AssistantAgent(
        name='agent',
        system_message=open('./agent.txt').read().strip(),
        model_client=model,
    )