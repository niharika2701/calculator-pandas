from app.operations import Operation


class Calculation:
    def __init__(self, operand_a: float, operand_b: float, operation: Operation):
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operation = operation
        self.result = None

    def compute(self) -> float:
        self.result = self.operation.execute(self.operand_a, self.operand_b)
        return self.result

    def __str__(self):
        op_name = type(self.operation).__name__
        return f"{op_name}({self.operand_a}, {self.operand_b}) = {self.result}"