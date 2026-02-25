import os
from dotenv import load_dotenv

load_dotenv()


class CalculatorConfig:
    
    def __init__(self):
        self.history_file = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
        self.auto_save = self._parse_bool(os.getenv("CALCULATOR_AUTO_SAVE", "true"))
        self.max_history = int(os.getenv("CALCULATOR_MAX_HISTORY", "100"))
        self.log_level = os.getenv("CALCULATOR_LOG_LEVEL", "INFO")

    def _parse_bool(self, value: str) -> bool:
        
        return value.strip().lower() == "true"