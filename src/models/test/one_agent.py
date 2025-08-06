# Single agent example

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from ollama_qwen import QWEN_2_5VL_7B

async def main() -> None:
    # Create model client for Ollama
    model_client = OpenAIChatCompletionClient(**QWEN_2_5VL_7B)
    
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