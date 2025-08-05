# Tool use for one agent

import asyncio
from typing import Annotated
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from src.models import LLAMA_3_1_8B

# Define calculator tool function with proper annotation
async def calculate(
    expression: Annotated[str, "A mathematical expression to calculate (e.g., '2 + 3 * 4')"]
) -> str:
    """Calculate a mathematical expression safely."""
    try:
        # Simple eval for basic math - in production, use a safer math parser
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations (+, -, *, /, parentheses) and numbers are allowed"
        
        result = eval(expression)
        return f"The calculation result is: {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: Invalid expression - {str(e)}"

async def main() -> None:
    # Create model client for Ollama
    model_client = OpenAIChatCompletionClient(**LLAMA_3_1_8B)
    
    # Create math agent with calculator tool
    math_agent = AssistantAgent(
        name="math_agent",
        model_client=model_client,
        tools=[calculate],
        system_message="""You are a helpful math assistant. When given a mathematical expression to calculate, 
        ALWAYS use the calculate tool to get the accurate result. Don't try to do math in your head."""
    )
    
    print("🔢 Math Agent with Calculator Tool")
    print("=" * 40)
    
    # Test expression
    test_expression = "10+(17*19)"
    print(f"Testing expression: {test_expression}")
    print()
    
    # Send task to agent
    task = f"Please calculate: {test_expression}"
    result = await math_agent.run(task=task)
    
    print("Full Conversation:")
    print("=" * 20)
    
    # Display all messages in the conversation
    for i, message in enumerate(result.messages, 1):
        print(f"{i}. {message.source}: {message.content}")
        print("-" * 30)
    
    # Close the model client
    await model_client.close()
    print(f"\n✅ Tool integration test completed!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
