import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.calculator_repl import Calculator


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_calculator_initializes(self):
        assert self.calc is not None
        assert self.calc.history is not None
        assert self.calc.config is not None

    def test_calculate_add(self):
        result = self.calc.calculate("add", 3, 5)
        assert result == 8

    def test_calculate_subtract(self):
        result = self.calc.calculate("subtract", 10, 4)
        assert result == 6

    def test_calculate_multiply(self):
        result = self.calc.calculate("multiply", 3, 4)
        assert result == 12

    def test_calculate_divide(self):
        result = self.calc.calculate("divide", 10, 2)
        assert result == 5

    def test_calculate_power(self):
        result = self.calc.calculate("power", 2, 10)
        assert result == 1024

    def test_calculate_root(self):
        result = self.calc.calculate("root", 9, 2)
        assert result == pytest.approx(3.0)

    def test_calculate_adds_to_history(self):
        self.calc.calculate("add", 3, 5)
        assert len(self.calc.history.get_all()) == 1

    def test_calculate_division_by_zero(self):
        from app.exceptions import DivisionByZeroError
        with pytest.raises(DivisionByZeroError):
            self.calc.calculate("divide", 10, 0)

    def test_undo_after_calculation(self):
        self.calc.calculate("add", 3, 5)
        self.calc.calculate("multiply", 4, 5)
        self.calc.undo()
        assert len(self.calc.history.get_all()) == 1

    def test_redo_after_undo(self):
        self.calc.calculate("add", 3, 5)
        self.calc.calculate("multiply", 4, 5)
        self.calc.undo()
        self.calc.redo()
        assert len(self.calc.history.get_all()) == 2

    def test_clear_history(self):
        self.calc.calculate("add", 3, 5)
        self.calc.clear_history()
        assert self.calc.history.get_all().empty

    def test_observer_notified_on_calculate(self):
        mock_observer = MagicMock()
        mock_observer.update = MagicMock()
        self.calc.history.add_observer(mock_observer)
        self.calc.calculate("add", 3, 5)
        mock_observer.update.assert_called()

    @pytest.mark.parametrize("operation, a, b, expected", [
        ("add", 1, 2, 3),
        ("subtract", 5, 3, 2),
        ("multiply", 3, 3, 9),
        ("divide", 9, 3, 3),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4.0),
    ])
    def test_calculate_parametrized(self, operation, a, b, expected):
        result = self.calc.calculate(operation, a, b)
        assert result == pytest.approx(expected)


class TestREPL:
    def test_exit_command(self):
        with patch("builtins.input", return_value="exit"):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                mock_print.assert_any_call("Goodbye!")

    def test_help_command(self):
        with patch("builtins.input", side_effect=["help", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "add" in printed.lower()

    def test_history_command_empty(self):
        with patch("builtins.input", side_effect=["history", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "empty" in printed.lower() or "history" in printed.lower()

    def test_valid_calculation_via_repl(self):
        with patch("builtins.input", side_effect=["add 3 5", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "8" in printed

    def test_invalid_input_handled_gracefully(self):
        with patch("builtins.input", side_effect=["add abc 5", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "error" in printed.lower() or "invalid" in printed.lower()

    def test_clear_command(self):
        with patch("builtins.input", side_effect=["add 3 5", "clear", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "clear" in printed.lower() or "cleared" in printed.lower()

    def test_undo_command(self):
        with patch("builtins.input", side_effect=["add 3 5", "undo", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "undo" in printed.lower()

    def test_redo_command(self):
        with patch("builtins.input", side_effect=["add 3 5", "undo", "redo", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "redo" in printed.lower()

    def test_unknown_command_handled(self):
        with patch("builtins.input", side_effect=["foobar", "exit"]):
            with patch("builtins.print") as mock_print:
                from app.calculator_repl import run_repl
                run_repl()
                printed = " ".join(str(c) for c in mock_print.call_args_list)
                assert "unknown" in printed.lower() or "error" in printed.lower()