import pytest
from app.calculation import Calculation
from app.operations import Add, Subtract, Multiply, Divide, Power, Root

class TestCalculation:
    def test_calculation_stores_values(self):
        op = Add()
        calc = Calculation(3, 5, op)
        assert calc.operand_a == 3
        assert calc.operand_b == 5
        assert calc.operation == op

    def test_calculation_computes_result(self):
        op = Add()
        calc = Calculation(3, 5, op)
        result = calc.compute()
        assert result == 8

    def test_calculation_stores_result_after_compute(self):
        op = Multiply()
        calc = Calculation(4, 5, op)
        calc.compute()
        assert calc.result == 20

    def test_calculation_result_is_none_before_compute(self):
        op = Add()
        calc = Calculation(3, 5, op)
        assert calc.result is None

    def test_calculation_string_representation(self):
        op = Add()
        calc = Calculation(3, 5, op)
        calc.compute()
        assert "Add" in str(calc)
        assert "3" in str(calc)
        assert "5" in str(calc)
        assert "8" in str(calc)

    @pytest.mark.parametrize("a, b, op_class, expected", [
        (3, 5, Add, 8),
        (10, 4, Subtract, 6),
        (3, 4, Multiply, 12),
        (10, 2, Divide, 5),
        (2, 10, Power, 1024),
        (9, 2, Root, 3.0),
    ])
    def test_calculation_with_all_operations(self, a, b, op_class, expected):
        op = op_class()
        calc = Calculation(a, b, op)
        result = calc.compute()
        assert result == pytest.approx(expected)