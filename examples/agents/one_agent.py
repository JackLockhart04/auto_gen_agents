# Single agent example

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    # Create model client for Ollama
    model_client = OpenAIChatCompletionClient(
        model="llama3.1:8b",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "Llama",
            "structured_output": True
        }
    )
    
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