import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from src.models import LLAMA_3_1_8B_CONCISE

async def main():
    print("Project planning consultation")
    print("=" * 40)
    
    # Get initial project description from user
    project_description = input("\nPlease describe your project (what you want to accomplish): ")
    print("Type 'DONE' when you want to end the consultation.\n")
    # print("The project planner will ask questions and you can respond naturally.")
  
    
    # Create model client
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    
    # Create project planner agent
    project_planner = AssistantAgent(
        name="project_planner",
        model_client=model_client,
        system_message="""You are an experienced project planner. Help the user plan their project by:

        - Asking clarifying questions about their needs
        - Providing specific suggestions and recommendations
        - Offering creative ideas and practical solutions
        - Being enthusiastic and helpful
        - Keep responses concise (2-3 sentences max)
        - Always ask a follow-up question to another agent to keep the conversation going."""
    )
    
    idea_generator = AssistantAgent(
        name="idea_generator",
        model_client=model_client,
        system_message="""You are a creative idea generator. 
        Help the user brainstorm innovative solutions and approaches for their project.
        - Focus on generating unique, out-of-the-box ideas
        - Keep responses concise (2-3 sentences max)
        - Always ask a follow-up question to another agent to keep the conversation going"""
    )
    
    # # Create a coordinator agent to help with flow
    # coordinator = AssistantAgent(
    #     name="coordinator",
    #     model_client=model_client,
    #     system_message="""You are a conversation coordinator. Your job is to:
        
    #     - Summarize what has been discussed so far
    #     - Identify if more user input is needed
    #     - Redirect to the project planner when you have enough info
        
    #     Keep responses very brief (1 sentence max)."""
    # )
    
    # Create custom input function that always uses our custom prompt
    def custom_input(prompt=None):
        # Always use our custom prompt, ignoring the passed prompt
        return input("💬 Your response: ")
    
    # Create user proxy agent that handles human input
    user_proxy = UserProxyAgent(
        name="user_proxy",
        input_func=custom_input  # Use custom input function with our prompt
    )
    
    # Create termination condition - conversation ends when user says "DONE"
    text_termination = TextMentionTermination("DONE")
    
    # Create the consultation team
    max_message_termination = MaxMessageTermination(max_messages=10)  # Increased for 3 agents
    expert_panel = SelectorGroupChat(
        participants=[project_planner, user_proxy],
        model_client=model_client,
        termination_condition=text_termination,
        selector_prompt="""Select the next speaker:
        - project_planner: if the user just provided information and you need to respond with planning advice
        - idea_generator: if the user is looking for creative solutions or brainstorming
        - user_proxy: if the project_planner asked a question that needs user input
        
        Return only the agent name."""
    )
    
    # Run the conversation and process stream manually
    initial_task = f"""I need to plan a project. The basic requirements are: "{project_description}"
    Do not make assumptions. Start by asking about key requirements and ask about any 
    information necessary to create a detailed project plan."""
    
    stream = expert_panel.run_stream(task=initial_task)
    
    # Process the stream manually for custom formatting
    final_result = None
    async for message in stream:
        # Handle different message types
        if hasattr(message, 'source') and hasattr(message, 'content'):
            # Skip empty messages from user_proxy
            if message.source == "user_proxy" and not message.content.strip():
                continue
                
            # Format based on the agent source
            if message.source == "project_planner":
                print(f"🎯 Planner: {message.content}\n")
            elif message.source == "idea_generator":
                print(f"💡 Ideas: {message.content}\n")
            elif message.source == "user_proxy":
                print(f"👤 You: {message.content}\n")
            elif message.source == "user":
                print(f"👤 You: {message.content}\n")
        else:
            # This might be the final result
            final_result = message
    
    # Store the final result for potential future use
    if final_result:
        print(f"📊 Conversation completed with {len(getattr(final_result, 'messages', []))} total messages")
    
    await model_client.close()
    print("\n✅ Project planning consultation completed!")

if __name__ == "__main__":
    asyncio.run(main())
