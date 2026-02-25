from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Add(Operation):
    def execute(self, a: float, b: float) -> float:
        return a+b

class Subtract(Operation):
    def execute(self, a: float, b: float) -> float:
        return a-b

class Multiply(Operation):
    def execute(self, a: float, b: float) -> float:
        return a*b

class Divide(Operation):
    def execute(self, a: float, b: float) -> float:
        if b==0:
            raise ValueError("Cannot divide by zero")
        return a/b
    
class Power(Operation):
    def execute(self, a: float, b: float) -> float:
        return a**b

class Root(Operation):
    def execute(self, a: float, b: float) -> float:
        if b==0:
            raise ValueError("Root degree cannot be zero")
        if a<0:
            raise ValueError("Cannot take root of negative number")
        return a **(1/b)

class OperationFactory:
    _operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
    }
    @classmethod
    def create(cls, operation_name: str) -> Operation:
        key = operation_name.lower()
        if key not in cls._operations:
            raise ValueError(f"Unknown operation: '{operation_name}'")
        return cls._operations[key]()

