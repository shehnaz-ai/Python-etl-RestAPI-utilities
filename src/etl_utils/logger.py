import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(
        name: str = "etl_utils",
        log_dir: str = "logs",
        level: int = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5
)-> logging.Logger:
    """
    Configure a reusable logger with console and rotating
    file handlers.
    """
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    if backup_count < 0:
        raise ValueError("backup_count cannot be negative")

    log_directory = Path(log_dir)
    log_directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    # Avoid adding duplicate handlers on repeated calls.
    if getattr(logger, "_etl_configured", False):
        for handler in logger.handlers:
            handler.setLevel(level)
        return logger

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_directory / f"{name.replace('.', '_')}.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger._etl_configured = True

    return logger


def get_logger(name: str = "etl_utils") -> logging.Logger:
    """Return a named child logger."""
    return logging.getLogger(name)
