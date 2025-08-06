import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.models import LLAMA_3_1_8B_CONCISE

# Import our organized modules
from agents import create_all_agents
from utils import process_conversation_stream, print_conversation_summary


async def main():
    print("Tool build start")
    print("=" * 40)

    # Get initial tool description from user
    tool_description = input("\nPlease describe the tool you would like to build: ")
    print("Type 'DONE' when you want to end the consultation.\n")
    
    # Create model client
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    

if __name__ == "__main__":
    asyncio.run(main())
