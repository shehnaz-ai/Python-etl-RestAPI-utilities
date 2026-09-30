
import json
import logging
from pathlib import Path
from typing import Any

from etl_utils.metrics import ETLMetrics
from etl_utils.logger import get_logger
from etl_utils.exceptions import PipelineExecutionError


class PipelineMonitor:
    """Monitor and audit a single ETL pipeline execution."""

    def __init__(
            self,
            pipeline_name: str,
            audit_file: str = "logs/etl_audit.jsonl",
            logger: logging.Logger | None = None
    ):
        self.metrics = ETLMetrics(pipeline_name)
        self.audit_file = Path(audit_file)
        self.logger = logger or get_logger("etl_utils.pipeline")
        self._finished = False

    def start(self) -> None:
        self.metrics.start()
        self.logger.info(
            "Pipeline started: name=%s execution_id=%s",
            self.metrics.pipeline_name,
            self.metrics.execution_id
        )

    def record_read(self, count: int) -> None:
        self.metrics.record_read(count)

    def record_processed(self, count: int) -> None:
        self.metrics.record_processed(count)

    def record_rejected(self, count: int) -> None:
        self.metrics.record_rejected(count)

    def _write_audit(self) -> None:
        self.audit_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        record: dict[str, Any] = self.metrics.to_dict()

        with self.audit_file.open(
                "a", encoding="utf-8"
        ) as file:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    def _finish(self, status: str) -> None:
        self.metrics.finish(status)
        self._finished = True

        self.logger.info(
            "Pipeline %s: name=%s execution_id=%s "
            "duration=%.6fs read=%d processed=%d rejected=%d",
            status,
            self.metrics.pipeline_name,
            self.metrics.execution_id,
            self.metrics.duration_seconds,
            self.metrics.records_read,
            self.metrics.records_processed,
            self.metrics.records_rejected
        )

        self._write_audit()

    def complete(self) -> None:
        self._finish("SUCCESS")

    def fail(self, error: Exception) -> None:
        self.metrics.record_error(error)
        self.logger.exception(
            "Pipeline failed: name=%s execution_id=%s",
            self.metrics.pipeline_name,
            self.metrics.execution_id,
            exc_info=(
                type(error),
                error,
                error.__traceback__
            )
        )
        self._finish("FAILED")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is None:
            self.complete()
            return False

        self.fail(exc_value)

        if isinstance(exc_value, PipelineExecutionError):
            return False

        raise PipelineExecutionError(
            f"Pipeline '{self.metrics.pipeline_name}' "
            f"failed: {exc_value}"
        ) from exc_value