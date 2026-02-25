import pytest
import pandas as pd
from app.calculator_memento import Memento, MementoManager


class TestMemento:
    def test_memento_stores_state(self):
        df = pd.DataFrame([{"operand_a": 3, "operand_b": 5,
                            "operation": "Add", "result": 8}])
        memento = Memento(df)
        assert memento.state.equals(df)

    def test_memento_state_is_copy(self):
        df = pd.DataFrame([{"operand_a": 3, "operand_b": 5,
                            "operation": "Add", "result": 8}])
        memento = Memento(df)
        df["result"] = 999
        assert memento.state.iloc[0]["result"] == 8

class TestMementoManager:
    def setup_method(self):
        self.manager = MementoManager()

    def test_starts_with_empty_stacks(self):
        assert not self.manager.can_undo()
        assert not self.manager.can_redo()

    def test_save_enables_undo(self):
        df = pd.DataFrame(columns=["operand_a", "operand_b",
                                   "operation", "result"])
        self.manager.save(df)
        assert self.manager.can_undo()

    def test_undo_returns_previous_state(self):
        df1 = pd.DataFrame([{"operand_a": 1, "operand_b": 2,
                             "operation": "Add", "result": 3}])
        df2 = pd.DataFrame([{"operand_a": 1, "operand_b": 2,
                             "operation": "Add", "result": 3},
                            {"operand_a": 4, "operand_b": 5,
                             "operation": "Multiply", "result": 20}])
        self.manager.save(df1)
        self.manager.save(df2)
        restored = self.manager.undo(df2)
        assert restored.equals(df1)

    def test_undo_enables_redo(self):
        df1 = pd.DataFrame(columns=["operand_a", "operand_b",
                                    "operation", "result"])
        df2 = pd.DataFrame([{"operand_a": 1, "operand_b": 2,
                             "operation": "Add", "result": 3}])
        self.manager.save(df1)
        self.manager.save(df2)
        self.manager.undo(df2)
        assert self.manager.can_redo()

    def test_redo_returns_next_state(self):
        df1 = pd.DataFrame(columns=["operand_a", "operand_b",
                                    "operation", "result"])
        df2 = pd.DataFrame([{"operand_a": 1, "operand_b": 2,
                             "operation": "Add", "result": 3}])
        self.manager.save(df1)
        self.manager.save(df2)
        self.manager.undo(df2)
        restored = self.manager.redo(df1)
        assert restored.equals(df2)

    def test_new_save_clears_redo_stack(self):
        df1 = pd.DataFrame(columns=["operand_a", "operand_b",
                                    "operation", "result"])
        df2 = pd.DataFrame([{"operand_a": 1, "operand_b": 2,
                             "operation": "Add", "result": 3}])
        df3 = pd.DataFrame([{"operand_a": 9, "operand_b": 3,
                             "operation": "Divide", "result": 3}])
        self.manager.save(df1)
        self.manager.save(df2)
        self.manager.undo(df2)
        self.manager.save(df3)
        assert not self.manager.can_redo()

    def test_undo_when_empty_returns_current(self):
        df = pd.DataFrame(columns=["operand_a", "operand_b",
                                   "operation", "result"])
        result = self.manager.undo(df)
        assert result.equals(df)

    def test_redo_when_empty_returns_current(self):
        df = pd.DataFrame(columns=["operand_a", "operand_b",
                                   "operation", "result"])
        result = self.manager.redo(df)
        assert result.equals(df)