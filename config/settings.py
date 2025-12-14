"""
Centralized configuration management using environment variables.

Usage:
    from config import settings

    model_path = settings.CHATGLM_MODEL_PATH
    data_dir = settings.DATA_DIR
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


def _get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent


def _get_env(key: str, default: str = "") -> str:
    """Get environment variable with fallback to default."""
    return os.environ.get(key, default)


def _get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean environment variable."""
    return os.environ.get(key, str(default)).lower() in ("true", "1", "yes")


def _get_env_int(key: str, default: int = 0) -> int:
    """Get integer environment variable."""
    try:
        return int(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


def _get_env_float(key: str, default: float = 0.0) -> float:
    """Get float environment variable."""
    try:
        return float(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


@dataclass
class Settings:
    """
    Application settings loaded from environment variables.

    All hardcoded paths and configurations are centralized here.
    Use .env file or export environment variables to configure.
    """

    # ============== Path Configuration ==============
    PROJECT_ROOT: Path = field(default_factory=_get_project_root)

    @property
    def DATA_DIR(self) -> Path:
        """Data directory for storing generated data."""
        custom = _get_env("DATA_DIR")
        return Path(custom) if custom else self.PROJECT_ROOT / "data"

    @property
    def RAW_DATA_PATH(self) -> Path:
        """Raw text data file path."""
        custom = _get_env("RAW_DATA_PATH")
        return Path(custom) if custom else self.DATA_DIR / "raw_data" / "raw_data.txt"

    # ============== Model Configuration ==============
    @property
    def CHATGLM_MODEL_PATH(self) -> str:
        """ChatGLM model weights path."""
        return _get_env("CHATGLM_MODEL_PATH", "THUDM/chatglm-6b")

    @property
    def BERT_MODEL_NAME(self) -> str:
        """BERT model name or path for tokenization and SPN4RE."""
        return _get_env("BERT_MODEL_NAME", "bert-base-chinese")

    @property
    def UIE_MODEL_NAME(self) -> str:
        """PaddleNLP UIE model name."""
        return _get_env("UIE_MODEL_NAME", "uie-base")

    # ============== Training Configuration ==============
    @property
    def TRAIN_RATIO(self) -> float:
        """Training data ratio."""
        return _get_env_float("TRAIN_RATIO", 0.5)

    @property
    def VALID_RATIO(self) -> float:
        """Validation data ratio."""
        return _get_env_float("VALID_RATIO", 0.2)

    @property
    def TEST_RATIO(self) -> float:
        """Test data ratio (computed from train and valid)."""
        return 1.0 - self.TRAIN_RATIO - self.VALID_RATIO

    @property
    def MAX_EPOCH(self) -> int:
        """Maximum training epochs for SPN4RE."""
        return _get_env_int("MAX_EPOCH", 10)

    @property
    def MAX_ITERATION(self) -> int:
        """Maximum knowledge graph expansion iterations."""
        return _get_env_int("MAX_ITERATION", 10)

    @property
    def BATCH_SIZE(self) -> int:
        """Training batch size."""
        return _get_env_int("BATCH_SIZE", 8)

    @property
    def MAX_SPAN_LENGTH(self) -> int:
        """Maximum span length for entity extraction."""
        return _get_env_int("MAX_SPAN_LENGTH", 10)

    @property
    def NUM_GENERATED_TRIPLES(self) -> int:
        """Number of generated triples per sentence."""
        return _get_env_int("NUM_GENERATED_TRIPLES", 15)

    # ============== GPU Configuration ==============
    @property
    def CUDA_VISIBLE_DEVICES(self) -> str:
        """CUDA visible devices."""
        return _get_env("CUDA_VISIBLE_DEVICES", "0")

    @property
    def DEFAULT_GPU(self) -> str:
        """Default GPU ID for training."""
        return _get_env("DEFAULT_GPU", "0")

    # ============== Server Configuration ==============
    @property
    def SERVER_HOST(self) -> str:
        """Flask server host."""
        return _get_env("SERVER_HOST", "0.0.0.0")

    @property
    def SERVER_PORT(self) -> int:
        """Flask server port."""
        return _get_env_int("SERVER_PORT", 8000)

    @property
    def SECRET_KEY(self) -> str:
        """Flask secret key. MUST be set in production."""
        key = _get_env("SECRET_KEY")
        if not key:
            import warnings
            warnings.warn(
                "SECRET_KEY not set! Using random key. "
                "Set SECRET_KEY environment variable in production.",
                UserWarning
            )
            import secrets
            return secrets.token_hex(32)
        return key

    @property
    def DEBUG(self) -> bool:
        """Debug mode flag."""
        return _get_env_bool("DEBUG", False)

    # ============== Schema Configuration ==============
    @property
    def SCHEMA_VERSION(self) -> str:
        """Schema version to use (v1, v2, v3, v4)."""
        return _get_env("SCHEMA_VERSION", "v4")

    def get_schema(self) -> dict:
        """Load schema based on version configuration."""
        version = self.SCHEMA_VERSION
        if version == "v1":
            from data.schema.schema_v1 import schema
        elif version == "v2":
            from data.schema.schema_v2 import schema
        elif version == "v3":
            from data.schema.schema_v3 import schema
        else:
            from data.schema.schema_v4 import schema
        return schema

    # ============== Extend Ratio Threshold ==============
    @property
    def EXTEND_RATIO_THRESHOLD(self) -> float:
        """Minimum extend ratio to continue iteration."""
        return _get_env_float("EXTEND_RATIO_THRESHOLD", 0.01)

    def setup_cuda(self) -> None:
        """Setup CUDA environment variables."""
        os.environ["CUDA_VISIBLE_DEVICES"] = self.CUDA_VISIBLE_DEVICES
        os.environ["MKL_SERVICE_FORCE_INTEL"] = "1"
        os.environ["MKL_THREADING_LAYER"] = "GNU"


# Global settings instance
settings = Settings()


def load_dotenv() -> None:
    """
    Load environment variables from .env file if exists.

    Call this at the start of your application if using .env file.
    """
    env_path = _get_project_root() / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
