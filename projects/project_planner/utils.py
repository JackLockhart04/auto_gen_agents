"""
Utilities for message processing and formatting.
This module handles custom message formatting and stream processing.
"""


def format_message(message) -> bool:
    """
    Format and print a message based on its source agent.
    
    Args:
        message: Message object with source and content attributes
        
    Returns:
        True if message was processed and displayed, False if skipped
    """
    # Handle different message types
    if not (hasattr(message, 'source') and hasattr(message, 'content')):
        return False
        
    # Skip empty messages from user_proxy
    if message.source == "user_proxy" and not message.content.strip():
        return False
        
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
        # Handle unknown message sources
        print(f"🔸 {message.source}: {message.content}\n")
        
    return True


async def process_conversation_stream(stream):
    """
    Process the conversation stream with custom formatting.
    
    Args:
        stream: Async stream from the group chat
        
    Returns:
        Final result object from the conversation
    """
    final_result = None
    
    async for message in stream:
        # Try to format the message
        if not format_message(message):
            # This might be the final result
            final_result = message
    
    return final_result


def print_conversation_summary(final_result):
    """
    Print a summary of the completed conversation.
    
    Args:
        final_result: Final result object from the conversation
    """
    if final_result:
        message_count = len(getattr(final_result, 'messages', []))
        print(f"📊 Conversation completed with {message_count} total messages")
    
    print("\n✅ Project planning consultation completed!")
