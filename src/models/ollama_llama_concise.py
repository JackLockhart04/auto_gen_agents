"""
Concise version of Ollama Llama model configuration with token limits
"""

# Concise model configuration with token limits
LLAMA_3_1_8B_CONCISE = {
    "model": "llama3.1:8b",
    "api_key": "ollama",  # Required but not used by Ollama
    "base_url": "http://127.0.0.1:11434/v1",
    "model_info": {
        "family": "Llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "function_call_strict_mode": False,
        "structured_output": False
    },
    # Limit response length
    "create_config": {
        "max_tokens": 200,  # Limit to ~200 tokens (roughly 2-3 paragraphs)
        "temperature": 0.1,
        "stop": None
    }
}
