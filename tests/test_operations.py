import pytest
from app.operations import (Add, Subtract, Multiply, Divide, Power, Root, OperationFactory)

class TestAdd:
    def test_add_postive_numbers(self):
        op=Add()
        result=op.execute(3, 5)
        assert result == 8

    def test_add_negative_numbers(self):
        op=Add()
        result=op.execute(-3, -5)
        assert result == -8

    def test_add_zero(self):
        op=Add()
        result=op.execute(0, 5)
        assert result == 5

class TestSubtract:
    def test_subtract_positive_numbers(self):
        op = Subtract()
        result = op.execute(10, 4)
        assert result == 6

    def test_subtract_resulting_in_negative(self):
        op = Subtract()
        result = op.execute(3, 10)
        assert result == -7

    def test_subtract_zero(self):
        op = Subtract()
        result = op.execute(5, 0)
        assert result == 5

class TestMultiply:
    def test_multiply_positive_numbers(self):
        op = Multiply()
        result = op.execute(3, 4)
        assert result == 12

    def test_multiply_by_zero(self):
        op = Multiply()
        result = op.execute(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        op = Multiply()
        result = op.execute(-3, -4)
        assert result == 12

class TestDivide:
    def test_divide_positive_numbers(self):
        op = Divide()
        result = op.execute(10, 2)
        assert result == 5

    def test_divide_resulting_in_float(self):
        op = Divide()
        result = op.execute(7, 2)
        assert result == 3.5

    def test_divide_by_zero_raises_error(self):
        # EAFP: we expect this exception to be raised
        op = Divide()
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            op.execute(10, 0)

class TestPower:
    def test_power_positive_exponent(self):
        op = Power()
        result = op.execute(2, 10)
        assert result == 1024

    def test_power_zero_exponent(self):
        op = Power()
        result = op.execute(5, 0)
        assert result == 1

    def test_power_negative_exponent(self):
        op = Power()
        result = op.execute(2, -1)
        assert result == 0.5

class TestRoot:
    def test_square_root(self):
        op = Root()
        result = op.execute(9, 2)
        assert result == 3.0

    def test_cube_root(self):
        op = Root()
        result = op.execute(27, 3)
        assert result == pytest.approx(3.0)

    def test_root_of_negative_raises_error(self):
        op = Root()
        with pytest.raises(ValueError, match="Cannot take root of negative number"):
            op.execute(-9, 2)

    def test_zero_root_raises_error(self):
        op = Root()
        with pytest.raises(ValueError, match="Root degree cannot be zero"):
            op.execute(9, 0)

class TestOperationFactory:
    @pytest.mark.parametrize("operation_name, expected_class", [
        ("add", Add),
        ("subtract", Subtract),
        ("multiply", Multiply),
        ("divide", Divide),
        ("power", Power),
        ("root", Root),
    ])
    def test_factory_creates_correct_operation(self, operation_name, expected_class):
        op = OperationFactory.create(operation_name)
        assert isinstance(op, expected_class)
        
    def test_factory_invalid_operation_raises_error(self):
        with pytest.raises(ValueError, match="Unknown operation"):
            OperationFactory.create("modulo")

    def test_factory_case_insensitive(self):
        op = OperationFactory.create("ADD")
        assert isinstance(op, Add)

