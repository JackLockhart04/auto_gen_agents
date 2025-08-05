import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from src.models import LLAMA_3_1_8B_CONCISE

async def main():
    """Expert panel with concise responses"""
    print("🎯 Expert Panel with Concise Responses")
    print("=" * 40)
    
    # Create model client using concise prefab
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B_CONCISE)
    
    # Create specialist agents with concise instructions
    math_expert = AssistantAgent(
        name="math_expert",
        model_client=model_client,
        system_message="""You are a mathematics expert. Provide clear, concise mathematical explanations.
        
        Rules:
        - Maximum 3 sentences per response
        - Focus on the core concept only
        - Include one brief example if helpful"""
    )
    
    tech_expert = AssistantAgent(
        name="tech_expert", 
        model_client=model_client,
        system_message="""You are a technology expert. Provide practical, concise technical guidance.
        
        Rules:
        - Maximum 3 sentences per response  
        - Focus on the essential concept only
        - Include one brief code example if helpful"""
    )
    
    history_expert = AssistantAgent(
        name="history_expert",
        model_client=model_client,
        system_message="""You are a history expert. Share concise historical insights.
        
        Rules:
        - Maximum 3 sentences per response
        - Focus on key facts and dates only
        - Avoid lengthy background context"""
    )
    
    # Create the expert panel with fewer max messages
    termination = MaxMessageTermination(max_messages=3)  # Reduced from 6
    expert_panel = SelectorGroupChat(
        participants=[math_expert, tech_expert, history_expert],
        model_client=model_client,
        termination_condition=termination
    )
    
    # Test questions for different experts
    questions = [
        "What is the quadratic formula?",
        "How does recursion work?", 
        "What caused World War I?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 60)
        
        result = await expert_panel.run(task=question)
        
        # Show the conversation
        for message in result.messages:
            if message.source != "user":
                # Add emojis for different experts
                agent_emoji = {
                    "math_expert": "🔢", 
                    "tech_expert": "💻",
                    "history_expert": "📚"
                }
                emoji = agent_emoji.get(message.source, "🤖")
                print(f"{emoji} {message.source}: {message.content}\n")
    
    await model_client.close()
    print("✅ Concise expert panel session completed!")

if __name__ == "__main__":
    asyncio.run(main())
