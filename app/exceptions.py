class CalculatorException(Exception):
    pass

class DivisionByZeroError(CalculatorException):
    def __init__(self):
        super().__init__("Cannot divide by zero")

class InvalidOperationError(CalculatorException):
    def __init__(self, operation: str):
        super().__init__(f"Unknown operation: '{operation}'")

class InvalidInputError(CalculatorException):
    def __init__(self, value: str):
        super().__init__(f"Invalid input: '{value}'")