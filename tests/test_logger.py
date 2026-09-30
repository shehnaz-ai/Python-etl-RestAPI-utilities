
import logging

from etl_utils.logger import setup_logger, get_logger


def test_setup_logger(tmp_path):
    logger = setup_logger(
        name="test_logger_basic",
        log_dir=str(tmp_path)
    )

    logger.info("Test log message")

    assert len(logger.handlers) == 2
    assert (tmp_path / "test_logger_basic.log").exists()


def test_logger_does_not_duplicate_handlers(tmp_path):
    logger = setup_logger(
        name="test_logger_duplicate",
        log_dir=str(tmp_path)
    )
    handler_count = len(logger.handlers)

    setup_logger(
        name="test_logger_duplicate",
        log_dir=str(tmp_path)
    )

    assert len(logger.handlers) == handler_count


def test_get_logger():
    logger = get_logger("etl_utils.test")
    assert isinstance(logger, logging.Logger)


def test_invalid_rotation_size(tmp_path):
    import pytest

    with pytest.raises(ValueError):
        setup_logger(
            name="test_invalid_rotation",
            log_dir=str(tmp_path),
            max_bytes=0
        )