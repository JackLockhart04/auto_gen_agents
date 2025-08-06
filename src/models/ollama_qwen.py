# QWEN 2.5vl:7B configuration
QWEN_2_5VL_7B = {
    "model": "qwen2.5vl:7b", # Ollama QWEN 2.5vl:7B model (exact name from ollama list)
    "api_key": "ollama", # Required but not used by Ollama
    "base_url": "http://localhost:11434/v1", # Local Ollama server
    "model_info": {
        "family": "Qwen", # Qwen family of models
        "vision": True, # image capabilities
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