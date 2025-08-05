from typing import Annotated

async def calculate(
    expression: Annotated[str, "A mathematical expression to calculate (e.g., '2 + 3 * 4', '(10 + 5) / 3')"]
) -> str:
    """
    Calculate a mathematical expression safely.
    
    Supports basic arithmetic operations: +, -, *, /, parentheses, and decimal numbers.
    
    Args:
        expression: A mathematical expression as a string
        
    Returns:
        The result of the calculation or an error message
        
    Examples:
        calculate("2 + 3") -> "Result: 5"
        calculate("10 * (3 + 2)") -> "Result: 50"
        calculate("15 / 3") -> "Result: 5.0"
    """
    try:
        # Validate expression contains only allowed characters
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations (+, -, *, /, parentheses) and numbers are allowed"
        
        # Check for empty expression
        if not expression.strip():
            return "Error: Empty expression provided"
            
        # Evaluate the expression
        result = eval(expression)
        
        # Format result (remove unnecessary decimals for whole numbers)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        return f"Result: {result}"
        
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except SyntaxError:
        return "Error: Invalid mathematical expression"
    except Exception as e:
        return f"Error: {str(e)}"
