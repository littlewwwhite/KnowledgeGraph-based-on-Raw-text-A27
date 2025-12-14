"""
Unified logging module for the KnowledgeGraph project.

Provides structured logging with colored console output.
Replaces scattered print statements throughout the codebase.

Usage:
    from modules.utils.logger import logger

    logger.info("Processing started")
    logger.success("Task completed")
    logger.warning("Low memory")
    logger.error("Failed to load model")
    logger.debug("Variable value: %s", value)
"""
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"

    # Light variants
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_PURPLE = "\033[95m"
    LIGHT_CYAN = "\033[96m"


def colorize(text: str, color: str) -> str:
    """Apply ANSI color to text."""
    return f"{color}{text}{Colors.RESET}"


# Shortcut functions for colored text (compatible with cprint module)
def red(text: str) -> str:
    return colorize(str(text), Colors.RED)

def green(text: str) -> str:
    return colorize(str(text), Colors.GREEN)

def yellow(text: str) -> str:
    return colorize(str(text), Colors.YELLOW)

def blue(text: str) -> str:
    return colorize(str(text), Colors.BLUE)

def purple(text: str) -> str:
    return colorize(str(text), Colors.PURPLE)

def cyan(text: str) -> str:
    return colorize(str(text), Colors.CYAN)

def gray(text: str) -> str:
    return colorize(str(text), Colors.GRAY)

def bold(text: str) -> str:
    return colorize(str(text), Colors.BOLD)


# Custom log level for SUCCESS
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for different log levels."""

    LEVEL_COLORS = {
        logging.DEBUG: Colors.GRAY,
        logging.INFO: Colors.BLUE,
        SUCCESS_LEVEL: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.LIGHT_RED,
    }

    LEVEL_ICONS = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️ ",
        SUCCESS_LEVEL: "✅",
        logging.WARNING: "⚠️ ",
        logging.ERROR: "❌",
        logging.CRITICAL: "💀",
    }

    def __init__(self, use_icons: bool = False):
        super().__init__()
        self.use_icons = use_icons

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
        icon = self.LEVEL_ICONS.get(record.levelno, "") if self.use_icons else ""

        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        level_name = record.levelname

        # Color the level name
        colored_level = f"{color}{level_name:8}{Colors.RESET}"

        # Format the message
        message = record.getMessage()

        # Add location info for debug level
        if record.levelno == logging.DEBUG:
            location = f"{Colors.GRAY}({record.filename}:{record.lineno}){Colors.RESET}"
            return f"{Colors.GRAY}{timestamp}{Colors.RESET} {colored_level} {icon}{message} {location}"

        return f"{Colors.GRAY}{timestamp}{Colors.RESET} {colored_level} {icon}{message}"


class KGLogger:
    """
    Custom logger for the KnowledgeGraph project.

    Provides:
    - Colored console output
    - Optional file logging
    - Success level logging
    - Structured logging methods
    """

    def __init__(
        self,
        name: str = "kg",
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
        use_icons: bool = False
    ):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._logger.handlers.clear()

        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter(use_icons=use_icons))
        self._logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)

    def debug(self, msg: str, *args, **kwargs):
        """Log debug message."""
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """Log info message."""
        self._logger.info(msg, *args, **kwargs)

    def success(self, msg: str, *args, **kwargs):
        """Log success message (custom level)."""
        self._logger.log(SUCCESS_LEVEL, msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """Log warning message."""
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """Log error message."""
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """Log critical message."""
        self._logger.critical(msg, *args, **kwargs)

    def set_level(self, level: int):
        """Change log level."""
        self._logger.setLevel(level)

    def add_file_handler(self, log_file: Path):
        """Add file handler for logging to file."""
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)

    # Progress logging helpers
    def progress(self, current: int, total: int, prefix: str = "Progress"):
        """Log progress information."""
        percentage = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        self.info(f"{prefix}: [{bar}] {current}/{total} ({percentage:.1f}%)")

    def step(self, step_num: int, total_steps: int, description: str):
        """Log a step in a multi-step process."""
        self.info(f"[{step_num}/{total_steps}] {description}")

    def section(self, title: str):
        """Log a section header."""
        separator = "=" * 50
        self.info(f"\n{separator}")
        self.info(f"  {title}")
        self.info(f"{separator}")


# Default logger instance
logger = KGLogger(name="kg", level=logging.INFO)


# Convenience function to get logger with custom settings
def get_logger(
    name: str = "kg",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    use_icons: bool = False
) -> KGLogger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name.
        level: Log level (default: INFO).
        log_file: Optional path to log file.
        use_icons: Whether to use emoji icons.

    Returns:
        Configured KGLogger instance.
    """
    return KGLogger(name=name, level=level, log_file=log_file, use_icons=use_icons)
