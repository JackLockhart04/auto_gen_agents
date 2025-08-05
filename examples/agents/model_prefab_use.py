# Prefab model configuration to create a model client


import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.models import LLAMA_3_1_8B

async def main() -> None:
    # Create model client using the prefab configuration
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B)
    
    # Create assistant agent
    agent = AssistantAgent("assistant", model_client=model_client)
    
    # Run the task
    result = await agent.run(task="What is the capital of France?")
    
    # Extract and print just the question and response
    messages = result.messages
    for message in messages:
        if message.source == "user":
            print(f"Question: {message.content}")
        elif message.source == "assistant":
            print(f"Response: {message.content}")
    
    # Close the model client
    await model_client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
