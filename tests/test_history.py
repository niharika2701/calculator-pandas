import pytest
import os
import pandas as pd
from app.history import HistoryManager
from app.calculation import Calculation
from app.operations import Add, Subtract, Multiply


class TestHistoryManager:
    def setup_method(self):
        self.history = HistoryManager()
        self.history.clear()

    def test_history_starts_empty(self):
        assert self.history.get_all().empty

    def test_add_calculation_to_history(self):
        calc = Calculation(3, 5, Add())
        calc.compute()
        self.history.add(calc)
        assert len(self.history.get_all()) == 1

    def test_history_stores_correct_values(self):
        calc = Calculation(3, 5, Add())
        calc.compute()
        self.history.add(calc)
        df = self.history.get_all()
        assert df.iloc[0]["operand_a"] == 3
        assert df.iloc[0]["operand_b"] == 5
        assert df.iloc[0]["operation"] == "Add"
        assert df.iloc[0]["result"] == 8

    def test_clear_history(self):
        calc = Calculation(3, 5, Add())
        calc.compute()
        self.history.add(calc)
        self.history.clear()
        assert self.history.get_all().empty

    def test_add_multiple_calculations(self):
        for i in range(5):
            calc = Calculation(i, i, Add())
            calc.compute()
            self.history.add(calc)
        assert len(self.history.get_all()) == 5

    def test_save_and_load_history(self, tmp_path):
        filepath = str(tmp_path / "test_history.csv")
        calc = Calculation(3, 5, Add())
        calc.compute()
        self.history.add(calc)
        self.history.save(filepath)
        new_history = HistoryManager()
        new_history.load(filepath)
        assert len(new_history.get_all()) == 1

    def test_load_nonexistent_file_stays_empty(self):
        self.history.load("nonexistent_file.csv")
        assert self.history.get_all().empty

    def test_get_last_calculation(self):
        calc1 = Calculation(1, 2, Add())
        calc1.compute()
        calc2 = Calculation(3, 4, Multiply())
        calc2.compute()
        self.history.add(calc1)
        self.history.add(calc2)
        last = self.history.get_last()
        assert last["operation"] == "Multiply"

    def test_get_last_empty_history_returns_none(self):
        assert self.history.get_last() is None