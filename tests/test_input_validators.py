import pytest
from app.input_validators import InputValidator
from app.exceptions import InvalidInputError


class TestInputValidator:
    def test_valid_integer_input(self):
        result = InputValidator.parse_number("5")
        assert result == 5.0

    def test_valid_float_input(self):
        result = InputValidator.parse_number("3.14")
        assert result == pytest.approx(3.14)

    def test_negative_number_input(self):
        result = InputValidator.parse_number("-7")
        assert result == -7.0

    def test_invalid_string_raises_error(self):
        with pytest.raises(InvalidInputError):
            InputValidator.parse_number("abc")

    def test_empty_string_raises_error(self):
        with pytest.raises(InvalidInputError):
            InputValidator.parse_number("")

    def test_valid_operation_name(self):
        result = InputValidator.parse_operation("add")
        assert result == "add"

    def test_operation_name_case_insensitive(self):
        result = InputValidator.parse_operation("ADD")
        assert result == "add"

    def test_invalid_operation_raises_error(self):
        with pytest.raises(InvalidInputError):
            InputValidator.parse_operation("modulo")

    def test_whitespace_stripped_from_number(self):
        result = InputValidator.parse_number("  5  ")
        assert result == 5.0

    def test_whitespace_stripped_from_operation(self):
        result = InputValidator.parse_operation("  add  ")
        assert result == "add"

    @pytest.mark.parametrize("valid_op", [
        "add", "subtract", "multiply", "divide", "power", "root"
    ])
    def test_all_valid_operations_accepted(self, valid_op):
        result = InputValidator.parse_operation(valid_op)
        assert result == valid_op