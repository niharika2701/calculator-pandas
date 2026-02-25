from app.exceptions import InvalidInputError

VALID_OPERATIONS = {"add", "subtract", "multiply", "divide", "power", "root"}

class InputValidator:
    @staticmethod
    def parse_number(value: str) -> float:
        try:
            return float(value.strip())
        except (ValueError, AttributeError):
            raise InvalidInputError(value)

    @staticmethod
    def parse_operation(value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in VALID_OPERATIONS:
            raise InvalidInputError(value)
        return cleaned