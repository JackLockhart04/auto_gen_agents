# Two agent communication

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

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
    
    # Create writer agent
    writer = AssistantAgent(
        name="writer",
        model_client=model_client,
        system_message="""You are a creative writer. Your job is to write engaging content based on the topic given. 
        Be creative, descriptive, and engaging. After receiving feedback from the editor, incorporate their suggestions 
        to improve your writing. Keep your writing concise but compelling."""
    )
    
    # Create editor agent  
    editor = AssistantAgent(
        name="editor",
        model_client=model_client,
        system_message="""You are a professional editor. Your job is to review the writer's work and provide 
        constructive feedback. Focus on clarity, flow, engagement, and overall quality. Suggest specific improvements 
        and be encouraging while being honest about areas that need work. If the writing is good, acknowledge it!"""
    )
    
    # Set up termination after a few rounds of back-and-forth
    termination = MaxMessageTermination(max_messages=8)
    
    # Create the team (writer goes first, then editor)
    team = RoundRobinGroupChat([writer, editor], termination_condition=termination)
    
    print("📝 Writer & Editor Collaboration")
    print("=" * 40)
    print("Topic: Write a short story opening about a mysterious library")
    print("\n")
    
    # Start the collaboration
    result = await team.run(
        task="Write the opening paragraph for a short story about someone who discovers a mysterious library that appears only at midnight. Make it atmospheric and intriguing."
    )
    
    print("\n" + "=" * 40)
    print("📋 Collaboration Summary:")
    print("=" * 40)
    
    # Display the conversation
    for i, message in enumerate(result.messages, 1):
        agent_name = "✍️  Writer" if message.source == "writer" else "✏️  Editor"
        print(f"\n{i}. {agent_name}:")
        print(f"{message.content}\n")
        print("-" * 30)
    
    # Close the model client
    await model_client.close()
    print("\n🎯 Collaboration completed!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
