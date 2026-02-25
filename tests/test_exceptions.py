import pytest
from app.exceptions import (
    CalculatorException,
    DivisionByZeroError,
    InvalidOperationError,
    InvalidInputError
)


class TestExceptions:
    def test_calculator_exception_is_base(self):
        exc = CalculatorException("base error")
        assert isinstance(exc, Exception)
        assert str(exc) == "base error"

    def test_division_by_zero_is_calculator_exception(self):
        exc = DivisionByZeroError()
        assert isinstance(exc, CalculatorException)

    def test_division_by_zero_default_message(self):
        exc = DivisionByZeroError()
        assert "zero" in str(exc).lower()

    def test_invalid_operation_error(self):
        exc = InvalidOperationError("modulo")
        assert isinstance(exc, CalculatorException)
        assert "modulo" in str(exc)

    def test_invalid_input_error(self):
        exc = InvalidInputError("abc")
        assert isinstance(exc, CalculatorException)
        assert "abc" in str(exc)

    @pytest.mark.parametrize("exc_class, args, expected_text", [
        (DivisionByZeroError, [], "zero"),
        (InvalidOperationError, ["modulo"], "modulo"),
        (InvalidInputError, ["abc"], "abc"),
    ])
    def test_exception_messages(self, exc_class, args, expected_text):
        exc = exc_class(*args)
        assert expected_text in str(exc).lower()