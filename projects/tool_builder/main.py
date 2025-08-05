import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.models import LLAMA_3_1_8B_CONCISE

# Import our organized modules
from agents import create_all_agents
from conversation import create_selector_group_chat, create_initial_task
from utils import process_conversation_stream, print_conversation_summary


async def main():
    print("Project planning consultation")
    print("=" * 40)
    
    # Get initial project description from user
    project_description = input("\nPlease describe your project (what you want to accomplish): ")
    print("Type 'DONE' when you want to end the consultation.\n")
    
    # Create model client
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    
    try:
        # Create all agents
        agents = create_all_agents(model_client)
        
        # Create the conversation group chat
        expert_panel = create_selector_group_chat(agents, model_client)
        
        # Create initial task and start conversation
        initial_task = create_initial_task(project_description)
        stream = expert_panel.run_stream(task=initial_task)
        
        # Process the conversation stream with custom formatting
        final_result = await process_conversation_stream(stream)
        
        # Print conversation summary
        print_conversation_summary(final_result)
        
    finally:
        # Always close the model client
        await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
