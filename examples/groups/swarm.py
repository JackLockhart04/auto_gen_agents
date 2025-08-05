import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import MaxMessageTermination
from src.models import LLAMA_3_1_8B_CONCISE

async def main():
    """Creative Idea Swarm - party theme brainstorming"""
    print("🎉 Party Theme Idea Swarm")
    print("=" * 40)
    
    # Create model client
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    
    # Creative Agent 1 - Wild Ideas
    wild_creative = AssistantAgent(
        name="wild_creative",
        model_client=model_client,
        system_message="""You're the wild creative agent! Come up with bold, unusual party themes.
        
        Build on others' ideas by making them MORE creative and unexpected. 
        Suggest 1-2 wild theme ideas per response. Be brief but exciting!"""
    )
    
    # Creative Agent 2 - Practical Fun
    practical_creative = AssistantAgent(
        name="practical_creative",
        model_client=model_client,
        system_message="""You're the practical creative agent! Take wild ideas and make them doable.
        
        When you see others' ideas, suggest how to actually make them happen or blend concepts.
        Suggest 1-2 practical but fun theme variations per response."""
    )
    
    # Creative Agent 3 - Theme Mixer
    theme_mixer = AssistantAgent(
        name="theme_mixer",
        model_client=model_client,
        system_message="""You're the theme mixer agent! Combine different ideas into hybrid themes.
        
        Take elements from multiple suggestions and create mashup themes.
        Suggest 1-2 creative combinations per response. Mix and match concepts!"""
    )
    
    # Create the creative swarm
    termination = MaxMessageTermination(max_messages=6)  # Fewer messages for more focused interaction
    idea_swarm = Swarm(
        participants=[wild_creative, practical_creative, theme_mixer],
        termination_condition=termination
    )
    
    # Party scenarios to brainstorm for
    party_scenarios = [
        "Birthday party for a 25-year-old who loves video games and pizza",
        "Company holiday party for a tech startup with 50 employees"
    ]
    
    for i, scenario in enumerate(party_scenarios, 1):
        print(f"\n🎈 Party Scenario #{i}")
        print("-" * 60)
        print(f"Scenario: {scenario}")
        print("-" * 60)
        
        result = await idea_swarm.run(
            task=f"Brainstorm creative party themes for this scenario: {scenario}\n\nBuild on each other's ideas and create something amazing together!"
        )
        
        # Show the creative collaboration
        for message in result.messages:
            if message.source != "user":
                # Add emojis for different creative styles
                agent_emoji = {
                    "wild_creative": "🚀",
                    "practical_creative": "🎯", 
                    "theme_mixer": "🌈"
                }
                emoji = agent_emoji.get(message.source, "💡")
                print(f"{emoji} {message.source}: {message.content}\n")
    
    await model_client.close()
    print("✅ Creative idea swarm session completed!")

if __name__ == "__main__":
    asyncio.run(main())
