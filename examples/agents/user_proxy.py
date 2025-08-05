import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from src.models import LLAMA_3_1_8B_CONCISE

async def main():
    """Human input example - party planning consultation using UserProxyAgent"""
    print("🎉 Party Planning Consultation")
    print("=" * 40)
    
    # Create model client
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    
    # Create party planner agent
    party_planner = AssistantAgent(
        name="party_planner",
        model_client=model_client,
        system_message="""You are an experienced party planner. Help the user plan their event by:
        
        - Asking clarifying questions about their needs
        - Providing specific suggestions and recommendations
        - Offering creative ideas and practical solutions
        - Being enthusiastic and helpful
        
        Keep responses concise (2-3 sentences) and always ask a follow-up question to keep the conversation going."""
    )
    
    # Create user proxy agent that handles human input
    user_proxy = UserProxyAgent(
        name="user_proxy",
        input_func=input  # Use input() to get user input from console
    )
    
    # Create termination condition - conversation ends when user says "DONE"
    termination = TextMentionTermination("DONE")
    
    # Create the consultation team
    consultation = RoundRobinGroupChat(
        [party_planner, user_proxy], 
        termination_condition=termination
    )
    
    print("Welcome to your party planning consultation!")
    print("The party planner will ask questions and you can respond naturally.")
    print("Type 'DONE' when you want to end the consultation.\n")
    
    # Run the conversation and stream to console
    stream = consultation.run_stream(
        task="Hello! I'd like help planning a party. What information do you need to get started?"
    )
    
    result = await Console(stream)
    
    await model_client.close()
    print("\n✅ Party planning consultation completed!")
    
if __name__ == "__main__":
    asyncio.run(main())
