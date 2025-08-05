import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.models.ollama_llama import LLAMA_3_1_8B

async def main() -> None:
    # Create model client for Ollama
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B)
    
    # Create assistant agent
    agent = AssistantAgent(
        name="assistant", 
        model_client=model_client,
        system_message="You are a helpful assistant. Be conversational and friendly. Keep responses concise."
    )
    
    print("🤖 Chat started! Type 'exit' to end the conversation.")
    print("=" * 50)
    
    # Simple chat loop
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
            
        # Send to agent and get response
        result = await agent.run(task=user_input)
        
        # Extract assistant's response
        for message in result.messages:
            if message.source == "assistant":
                print(f"Assistant: {message.content}")
                break
    
    # Close the model client
    await model_client.close()
    print("\n👋 Chat ended!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
