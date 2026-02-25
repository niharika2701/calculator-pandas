import pandas as pd

class Memento:
    def __init__(self, state: pd.DataFrame):
        self.state = state.copy()


class MementoManager:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save(self, current_state: pd.DataFrame) -> None:
        self._undo_stack.append(Memento(current_state))
        self._redo_stack.clear()

    def undo(self, current_state: pd.DataFrame) -> pd.DataFrame:
        if not self.can_undo():
            return current_state
        self._redo_stack.append(Memento(current_state))
        previous = self._undo_stack.pop()
        if previous.state.equals(current_state) and self.can_undo():
            self._redo_stack.append(previous)
            previous = self._undo_stack.pop()
        return previous.state

    def redo(self, current_state: pd.DataFrame) -> pd.DataFrame:
        if not self.can_redo():
            return current_state
        self._undo_stack.append(Memento(current_state))
        return self._redo_stack.pop().state

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0