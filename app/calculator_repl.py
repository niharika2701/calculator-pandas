import logging
from app.calculator_config import CalculatorConfig
from app.history import HistoryManager
from app.calculator_memento import MementoManager
from app.operations import OperationFactory
from app.calculation import Calculation
from app.input_validators import InputValidator
from app.exceptions import (
    CalculatorException, DivisionByZeroError, InvalidInputError
)

class LoggingObserver:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("CalculatorLogger")

    def update(self, event: str):
        self.logger.info(f"History event: {event}")


class AutoSaveObserver:
    def __init__(self, history: HistoryManager, filepath: str):
        self._history = history
        self._filepath = filepath

    def update(self, event: str):
        if event in ("add", "clear"):
            self._history.save(self._filepath)

class Calculator:
    def __init__(self):
        self.config = CalculatorConfig()
        self.history = HistoryManager()
        self.memento = MementoManager()

        self.history.add_observer(LoggingObserver())
        if self.config.auto_save:
            self.history.add_observer(
                AutoSaveObserver(self.history, self.config.history_file)
            )

        self.history.load(self.config.history_file)

    def calculate(self, operation: str, a: float, b: float) -> float:
        self.memento.save(self.history.get_all())

        try:
            op = OperationFactory.create(operation)
            calc = Calculation(a, b, op)
            result = calc.compute()
        except ValueError as e:
            if "zero" in str(e).lower():
                raise DivisionByZeroError()
            raise

        self.history.add(calc)
        return result

    def undo(self) -> None:
        restored = self.memento.undo(self.history.get_all())
        self.history._df = restored

    def redo(self) -> None:
        restored = self.memento.redo(self.history.get_all())
        self.history._df = restored

    def clear_history(self) -> None:
        self.memento.save(self.history.get_all())
        self.history.clear()

def run_repl():
    calculator = Calculator()
    print("Calculator Ready! Type 'help' for commands.")

    while True:
        try:
            user_input = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):  
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        elif user_input.lower() == "help":
            print("""
Commands:
  add <a> <b>       - Add two numbers
  subtract <a> <b>  - Subtract b from a
  multiply <a> <b>  - Multiply two numbers
  divide <a> <b>    - Divide a by b
  power <a> <b>     - Raise a to the power of b
  root <a> <b>      - Take the bth root of a
  history           - Show calculation history
  clear             - Clear history
  undo              - Undo last calculation
  redo              - Redo last undone calculation
  save              - Save history to file
  load              - Load history from file
  exit              - Exit the calculator
            """)

        elif user_input.lower() == "history":
            df = calculator.history.get_all()
            if df.empty:
                print("History is empty.")
            else:
                print(df.to_string(index=False))

        elif user_input.lower() == "clear":
            calculator.clear_history()
            print("History cleared.")

        elif user_input.lower() == "undo":
            calculator.undo()
            print("Undo successful.")

        elif user_input.lower() == "redo":
            calculator.redo()
            print("Redo successful.")

        elif user_input.lower() == "save":
            calculator.history.save(calculator.config.history_file)
            print(f"History saved to {calculator.config.history_file}.")

        elif user_input.lower() == "load":
            calculator.history.load(calculator.config.history_file)
            print(f"History loaded from {calculator.config.history_file}.")

        else:
            parts = user_input.split()
            if len(parts) != 3:
                print("Error: use format: <operation> <a> <b>")
                continue
            try:
                operation = InputValidator.parse_operation(parts[0])
                a = InputValidator.parse_number(parts[1])
                b = InputValidator.parse_number(parts[2])
                result = calculator.calculate(operation, a, b)
                print(f"Result: {result}")
            except DivisionByZeroError as e:
                print(f"Error: {e}")
            except InvalidInputError as e:
                print(f"Error: {e}")
            except CalculatorException as e:
                print(f"Error: {e}")


if __name__ == "__main__":  
    run_repl()