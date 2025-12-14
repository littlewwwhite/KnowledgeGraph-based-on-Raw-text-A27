"""
Tests for config/settings.py - Configuration management.
"""
import os
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from config.settings import Settings, settings


class TestSettingsDefaults:
    """Tests for default settings values."""

    def test_project_root_exists(self) -> None:
        """Test that PROJECT_ROOT points to valid directory."""
        assert settings.PROJECT_ROOT.exists()
        assert settings.PROJECT_ROOT.is_dir()

    def test_data_dir_path(self) -> None:
        """Test DATA_DIR is under PROJECT_ROOT."""
        assert str(settings.DATA_DIR).startswith(str(settings.PROJECT_ROOT))

    def test_default_bert_model(self) -> None:
        """Test default BERT model name."""
        # Should have a default even without env var
        assert settings.BERT_MODEL_NAME is not None
        assert len(settings.BERT_MODEL_NAME) > 0

    def test_default_chatglm_model(self) -> None:
        """Test default ChatGLM model path."""
        assert settings.CHATGLM_MODEL_PATH is not None

    def test_train_ratio_valid(self) -> None:
        """Test TRAIN_RATIO is a valid proportion."""
        assert 0.0 < settings.TRAIN_RATIO < 1.0

    def test_valid_ratio_valid(self) -> None:
        """Test VALID_RATIO is a valid proportion."""
        assert 0.0 < settings.VALID_RATIO < 1.0

    def test_train_valid_sum_less_than_one(self) -> None:
        """Test train + valid ratio leaves room for test set."""
        assert settings.TRAIN_RATIO + settings.VALID_RATIO < 1.0


class TestSettingsWithEnvVars:
    """Tests for settings with environment variables."""

    def test_bert_model_from_env(self) -> None:
        """Test BERT_MODEL_NAME can be set via env var."""
        with patch.dict(os.environ, {"BERT_MODEL_NAME": "custom-bert-model"}):
            new_settings = Settings()
            assert new_settings.BERT_MODEL_NAME == "custom-bert-model"

    def test_chatglm_model_from_env(self) -> None:
        """Test CHATGLM_MODEL_PATH can be set via env var."""
        with patch.dict(os.environ, {"CHATGLM_MODEL_PATH": "/custom/model/path"}):
            new_settings = Settings()
            assert new_settings.CHATGLM_MODEL_PATH == "/custom/model/path"

    def test_max_epoch_from_env(self) -> None:
        """Test MAX_EPOCH can be set via env var."""
        with patch.dict(os.environ, {"MAX_EPOCH": "50"}):
            new_settings = Settings()
            assert new_settings.MAX_EPOCH == 50

    def test_train_ratio_from_env(self) -> None:
        """Test TRAIN_RATIO can be set via env var."""
        with patch.dict(os.environ, {"TRAIN_RATIO": "0.7"}):
            new_settings = Settings()
            assert new_settings.TRAIN_RATIO == 0.7


class TestSettingsTrainingParams:
    """Tests for training-related settings."""

    def test_max_epoch_positive(self) -> None:
        """Test MAX_EPOCH is positive."""
        assert settings.MAX_EPOCH > 0

    def test_max_span_length_positive(self) -> None:
        """Test MAX_SPAN_LENGTH is positive."""
        assert settings.MAX_SPAN_LENGTH > 0

    def test_num_generated_triples_positive(self) -> None:
        """Test NUM_GENERATED_TRIPLES is positive."""
        assert settings.NUM_GENERATED_TRIPLES > 0


class TestSettingsPathProperties:
    """Tests for path-related properties."""

    def test_raw_data_path_type(self) -> None:
        """Test RAW_DATA_PATH returns Path or str."""
        path = settings.RAW_DATA_PATH
        assert isinstance(path, (str, Path))

    def test_data_dir_type(self) -> None:
        """Test DATA_DIR returns Path."""
        assert isinstance(settings.DATA_DIR, Path)


class TestSettingsSingleton:
    """Tests for settings singleton behavior."""

    def test_global_settings_instance(self) -> None:
        """Test that global settings instance is accessible."""
        from config.settings import settings as imported_settings
        assert imported_settings is not None

    def test_settings_attributes_accessible(self) -> None:
        """Test all expected attributes are accessible."""
        attrs = [
            "PROJECT_ROOT",
            "DATA_DIR",
            "BERT_MODEL_NAME",
            "CHATGLM_MODEL_PATH",
            "MAX_EPOCH",
            "MAX_SPAN_LENGTH",
            "NUM_GENERATED_TRIPLES",
            "TRAIN_RATIO",
            "VALID_RATIO",
        ]
        for attr in attrs:
            assert hasattr(settings, attr), f"Missing attribute: {attr}"
