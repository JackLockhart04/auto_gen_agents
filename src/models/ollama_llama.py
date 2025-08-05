# Llama 3.1 8B configuration
LLAMA_3_1_8B = {
    "model": "llama3.1:8b", # Ollama Llama 3.1 8B model
    "api_key": "ollama", # Required but not used by Ollama
    "base_url": "http://localhost:11434/v1", # Local Ollama server
    "model_info": {
        "family": "Llama", # Llama family of models
        "vision": False, # No image capabilities
        "function_calling": True, # Enable function calling
        "json_output": True, # Enable JSON output
        "structured_output": True, # Enable structured output
        "function_call_strict_mode": False # Allow flexible function calling
    },
    "create_config": {
        "max_tokens": 1000,  # Limit to ~500 tokens
        "temperature": 0.1,  # Very low for maximum accuracy and consistency
        "stop": None # No specific stop sequences
    }
}