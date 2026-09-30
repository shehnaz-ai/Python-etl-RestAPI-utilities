
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import time
import uuid


@dataclass
class ETLMetrics:
    pipeline_name: str
    execution_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    status: str = "PENDING"
    start_time: str | None = None
    end_time: str | None = None
    duration_seconds: float = 0.0
    records_read: int = 0
    records_processed: int = 0
    records_rejected: int = 0
    error_message: str | None = None

    _start_clock: float | None = field(
        default=None, repr=False, compare=False
    )

    def start(self) -> None:
        if self.status == "RUNNING":
            raise RuntimeError("Metrics are already running")

        if self.status in {"SUCCESS", "FAILED"}:
            raise RuntimeError("Metrics have already finished")

        self.status = "RUNNING"
        self.start_time = datetime.now(
            timezone.utc
        ).isoformat()
        self._start_clock = time.perf_counter()

    def finish(self, status: str = "SUCCESS") -> None:
        if self.status != "RUNNING":
            raise RuntimeError(
                "Metrics must be running before finishing"
            )

        if status not in {"SUCCESS", "FAILED"}:
            raise ValueError(
                "status must be SUCCESS or FAILED"
            )

        self.end_time = datetime.now(
            timezone.utc
        ).isoformat()

        self.duration_seconds = round(
            time.perf_counter() - self._start_clock,
            6
        )
        self.status = status

    def record_read(self, count: int) -> None:
        self._validate_count(count)
        self.records_read += count

    def record_processed(self, count: int) -> None:
        self._validate_count(count)
        self.records_processed += count

    def record_rejected(self, count: int) -> None:
        self._validate_count(count)
        self.records_rejected += count

    def record_error(self, error: Exception) -> None:
        self.error_message = str(error)

    @staticmethod
    def _validate_count(count: int) -> None:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("Record count must be an integer")
        if count < 0:
            raise ValueError("Record count cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.pop("_start_clock", None)
        return result