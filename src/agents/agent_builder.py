"""
Object-oriented agent system for AutoGen
Provides flexible agent creation with configurable goals, models, and tools
"""

from typing import List, Callable
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


class AgentBuilder:
    # Builder class for creating specialized AssistantAgents

    def __init__(self, name: str, purpose: str, model_client: OpenAIChatCompletionClient):
        self.name = name
        self.system_message_template = """You are a specialized agent named {name}. 
        Your purpose is: {purpose}"""
        self.model_client = model_client
        self.tools: List[Callable] = []
        self.system_message_template = self._default_system_message()
    
    def set_tools(self, tools: List[Callable]) -> 'AgentBuilder':
        self.tools = tools
        return self
    
    def set_system_message(self, message: str) -> 'AgentBuilder':
        self.system_message_template = message
        return self
    
    def build(self) -> AssistantAgent:
        system_message = self.system_message_template
        # Add tool information to system message if tools are present
        if self.tools:
            tool_names = [tool.__name__ for tool in self.tools]
            tool_info = f"\n\nAvailable tools: {', '.join(tool_names)}"
            system_message += tool_info

        return AssistantAgent(
            name=self.name,
            model_client=self.model_client,
            system_message=system_message,
            tools=self.tools if self.tools else None
        )


class UserAgentBuilder:
    def __init__(self, name: str = "user_proxy"):
        self.name = name
        self.input_prompt = "💬 Your response: "
        def input_func(prompt=None):
                return input(self.input_prompt)
        self.custom_input_func = input_func
        
    def set_prompt(self, prompt: str) -> 'UserAgentBuilder':
        self.input_prompt = prompt
        return self
    
    def set_input_function(self, func: Callable) -> 'UserAgentBuilder':
        self.custom_input_func = func
        return self
    
    def build(self) -> UserProxyAgent:
        return UserProxyAgent(
            name=self.name,
            input_func=self.custom_input_func
        )


# class AgentTeam:
#     def __init__(self):
#         """Initialize an empty agent team."""
#         self.agents: Dict[str, AssistantAgent] = {}
#         self.user_agent: Optional[UserProxyAgent] = None
        
#     def add_agent(self, agent: AssistantAgent) -> 'AgentTeam':
#         """
#         Add an agent to the team.
        
#         Args:
#             agent: The agent to add
            
#         Returns:
#             Self for method chaining
#         """
#         self.agents[agent.name] = agent
#         return self
    
#     def set_user_agent(self, user_agent: UserProxyAgent) -> 'AgentTeam':
#         """
#         Set the user proxy agent for the team.
        
#         Args:
#             user_agent: The user proxy agent
            
#         Returns:
#             Self for method chaining
#         """
#         self.user_agent = user_agent
#         return self
    
#     def get_agent(self, name: str) -> Optional[AssistantAgent]:
#         """
#         Get an agent by name.
        
#         Args:
#             name: The agent's name
            
#         Returns:
#             The agent if found, None otherwise
#         """
#         return self.agents.get(name)
    
#     def get_all_agents(self) -> List[AssistantAgent]:
#         """
#         Get all agents in the team.
        
#         Returns:
#             List of all agents
#         """
#         return list(self.agents.values())
    
#     def get_participants(self) -> List[Any]:
#         """
#         Get all participants (agents + user agent) for use in group chats.
        
#         Returns:
#             List of all participants
#         """
#         participants = list(self.agents.values())
#         if self.user_agent:
#             participants.append(self.user_agent)
#         return participants
    
#     def __len__(self) -> int:
#         """Return the number of agents in the team."""
#         return len(self.agents)
    
#     def __contains__(self, name: str) -> bool:
#         """Check if an agent with the given name exists."""
        return name in self.agents


# # Example usage and factory functions
# def create_research_agent(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
#     """Factory function to create a research specialist agent."""
#     return (AgentBuilder("researcher", 
#                         "Research topics thoroughly and provide detailed, factual information", 
#                         model_client)
#             .build())


# def create_planning_agent(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
#     """Factory function to create a planning specialist agent."""
#     return (AgentBuilder("planner",
#                         "Create detailed project plans and break down complex tasks into manageable steps",
#                         model_client)
#             .build())


# def create_creative_agent(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
#     """Factory function to create a creative problem-solving agent."""
#     return (AgentBuilder("creative_thinker",
#                         "Generate innovative solutions and think outside the box for any challenge",
#                         model_client)
#             .build())


# def create_default_user_agent() -> UserProxyAgent:
#     """Factory function to create a default user proxy agent."""
#     return UserAgentBuilder().build()
