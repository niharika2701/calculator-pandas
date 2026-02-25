import pytest
from unittest.mock import patch
from app.calculator_config import CalculatorConfig


class TestCalculatorConfig:
    def test_config_loads_history_file(self):
        config = CalculatorConfig()
        assert config.history_file is not None
        assert isinstance(config.history_file, str)

    def test_config_loads_auto_save(self):
        config = CalculatorConfig()
        assert isinstance(config.auto_save, bool)

    def test_config_loads_max_history(self):
        config = CalculatorConfig()
        assert isinstance(config.max_history, int)
        assert config.max_history > 0

    def test_config_default_history_file(self):
        with patch.dict("os.environ", {}, clear=True):
            config = CalculatorConfig()
            assert config.history_file == "history.csv"

    def test_config_default_auto_save(self):
        with patch.dict("os.environ", {}, clear=True):
            config = CalculatorConfig()
            assert config.auto_save is True

    def test_config_default_max_history(self):
        with patch.dict("os.environ", {}, clear=True):
            config = CalculatorConfig()
            assert config.max_history == 100

    def test_config_custom_values(self):
        with patch.dict("os.environ", {
            "CALCULATOR_HISTORY_FILE": "custom.csv",
            "CALCULATOR_AUTO_SAVE": "false",
            "CALCULATOR_MAX_HISTORY": "50"
        }):
            config = CalculatorConfig()
            assert config.history_file == "custom.csv"
            assert config.auto_save is False
            assert config.max_history == 50

    @pytest.mark.parametrize("auto_save_val, expected", [
        ("true", True),
        ("True", True),
        ("false", False),
        ("False", False),
    ])
    def test_config_auto_save_parsing(self, auto_save_val, expected):
        with patch.dict("os.environ", {"CALCULATOR_AUTO_SAVE": auto_save_val}):
            config = CalculatorConfig()
            assert config.auto_save is expected