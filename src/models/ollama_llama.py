from autogen_ext.models.openai import OpenAIChatCompletionClient

# Llama 3.1 8B configuration
LLAMA_3_1_8B = {
    "model": "llama3.1:8b",
    "api_key": "ollama",
    "base_url": "http://localhost:11434/v1",
    "model_info": {
        "family": "Llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "function_call_strict_mode": False
    },
    "create_config": {
        "max_tokens": 1000,  # Limit to ~500 tokens
        "temperature": 0.1,  # Very low for maximum accuracy and consistency
        "stop": None
    }
}