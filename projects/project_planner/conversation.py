"""
Conversation configuration for the project planner application.
This module contains team setup and conversation flow logic.
"""

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_selector_group_chat(agents: dict, model_client: OpenAIChatCompletionClient) -> SelectorGroupChat:
    """
    Create and configure the SelectorGroupChat for intelligent agent routing.
    
    Args:
        agents: Dictionary of agent instances
        model_client: The OpenAI chat completion client
        
    Returns:
        Configured SelectorGroupChat instance
    """
    # Create termination condition - conversation ends when user says "DONE"
    text_termination = TextMentionTermination("DONE")
    
    # Define the selector prompt for intelligent routing
    selector_prompt = """Select the next speaker:
    - project_planner: if the user just provided information and you need to respond with planning advice
    - idea_generator: if the user is looking for creative solutions or brainstorming
    - user_proxy: if the project_planner asked a question that needs user input
    
    Return only the agent name."""
    
    return SelectorGroupChat(
        participants=[agents["project_planner"], agents["idea_generator"], agents["user_proxy"]],
        model_client=model_client,
        termination_condition=text_termination,
        selector_prompt=selector_prompt
    )


def create_initial_task(project_description: str) -> str:
    """
    Create the initial task message for the conversation.
    
    Args:
        project_description: User's project description
        
    Returns:
        Formatted initial task string
    """
    return f"""I need to plan a project. The basic requirements are: "{project_description}"
    Do not make assumptions. Start by asking about key requirements and ask about any 
    information necessary to create a detailed project plan."""
