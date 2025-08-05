"""
Agent definitions for the project planner application.
This module contains all agent creation and configuration logic.
"""

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_project_planner(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
    """Create and configure the project planner agent."""
    return AssistantAgent(
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


def create_idea_generator(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
    """Create and configure the idea generator agent."""
    return AssistantAgent(
        name="idea_generator",
        model_client=model_client,
        system_message="""You are a creative idea generator. 
        Help the user brainstorm innovative solutions and approaches for their project.
        - Focus on generating unique, out-of-the-box ideas
        - Keep responses concise (2-3 sentences max)
        - Always ask a follow-up question to another agent to keep the conversation going"""
    )


def create_user_proxy() -> UserProxyAgent:
    """Create and configure the user proxy agent with custom input prompt."""
    
    def custom_input(prompt=None):
        """Custom input function that always uses our custom prompt."""
        return input("💬 Your response: ")
    
    return UserProxyAgent(
        name="user_proxy",
        input_func=custom_input
    )


def create_all_agents(model_client: OpenAIChatCompletionClient) -> dict:
    """
    Create all agents for the project planner application.
    
    Args:
        model_client: The OpenAI chat completion client
        
    Returns:
        Dictionary with agent names as keys and agent instances as values
    """
    return {
        "project_planner": create_project_planner(model_client),
        "idea_generator": create_idea_generator(model_client),
        "user_proxy": create_user_proxy()
    }
