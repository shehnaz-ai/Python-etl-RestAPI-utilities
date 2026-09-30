
import json
import logging

import pytest

from etl_utils.exceptions import PipelineExecutionError
from etl_utils.pipeline_monitor import PipelineMonitor


def test_pipeline_success(tmp_path):
    audit_file = tmp_path / "audit.jsonl"

    with PipelineMonitor(
            "test_pipeline",
            audit_file=str(audit_file),
            logger=logging.getLogger("test.pipeline.success")
    ) as monitor:
        monitor.record_read(10)
        monitor.record_processed(8)
        monitor.record_rejected(2)

    records = [
        json.loads(line)
        for line in audit_file.read_text(
            encoding="utf-8"
        ).splitlines()
    ]

    assert len(records) == 1
    assert records[0]["status"] == "SUCCESS"
    assert records[0]["records_read"] == 10
    assert records[0]["records_processed"] == 8
    assert records[0]["records_rejected"] == 2


def test_pipeline_failure(tmp_path):
    audit_file = tmp_path / "audit.jsonl"

    with pytest.raises(PipelineExecutionError):
        with PipelineMonitor(
                "failing_pipeline",
                audit_file=str(audit_file),
                logger=logging.getLogger("test.pipeline.failure")
        ):
            raise ValueError("Simulated failure")

    record = json.loads(
        audit_file.read_text(encoding="utf-8").strip()
    )

    assert record["status"] == "FAILED"
    assert "Simulated failure" in record["error_message"]


def test_pipeline_preserves_original_error(tmp_path):
    with pytest.raises(PipelineExecutionError) as exc_info:
        with PipelineMonitor(
                "failing_pipeline",
                audit_file=str(tmp_path / "audit.jsonl"),
                logger=logging.getLogger("test.pipeline.cause")
        ):
            raise ValueError("Original error")

    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Original error"