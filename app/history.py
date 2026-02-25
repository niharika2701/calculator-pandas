import os
import pandas as pd
from typing import Optional


class HistoryManager:
    def __init__(self):
        self._df = pd.DataFrame(
            columns=["operand_a", "operand_b", "operation", "result"]
        )
        self._observers = []

    def add_observer(self, observer):
        
        self._observers.append(observer)

    def _notify_observers(self, event: str):
        
        for observer in self._observers:
            observer.update(event)

    def add(self, calculation) -> None:
        new_row = {
        "operand_a": calculation.operand_a,
        "operand_b": calculation.operand_b,
        "operation": type(calculation.operation).__name__,
        "result": calculation.result
    }
        self._df = pd.concat(
        [self._df, pd.DataFrame([new_row])],
        ignore_index=True
    )
        self._df = self._df.infer_objects()
        self._notify_observers("add")

    def get_all(self) -> pd.DataFrame:
        
        return self._df

    def get_last(self) -> Optional[dict]:
        
        if self._df.empty:
            return None
        return self._df.iloc[-1].to_dict()

    def clear(self) -> None:
        
        self._df = pd.DataFrame(
            columns=["operand_a", "operand_b", "operation", "result"]
        )
        self._notify_observers("clear")

    def save(self, filepath: str) -> None:
        
        self._df.to_csv(filepath, index=False)
        self._notify_observers("save")

    def load(self, filepath: str) -> None:
        
        try:
            self._df = pd.read_csv(filepath)
        except FileNotFoundError:
            pass  