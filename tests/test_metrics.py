
import pytest

from etl_utils.metrics import ETLMetrics


def test_metrics_success():
    metrics = ETLMetrics("customer_etl")
    metrics.start()
    metrics.record_read(100)
    metrics.record_processed(90)
    metrics.record_rejected(10)
    metrics.finish("SUCCESS")

    assert metrics.status == "SUCCESS"
    assert metrics.records_read == 100
    assert metrics.records_processed == 90
    assert metrics.records_rejected == 10
    assert metrics.duration_seconds >= 0
    assert metrics.start_time is not None
    assert metrics.end_time is not None


def test_metrics_failure():
    metrics = ETLMetrics("customer_etl")
    metrics.start()
    metrics.record_error(ValueError("Invalid data"))
    metrics.finish("FAILED")

    assert metrics.status == "FAILED"
    assert metrics.error_message == "Invalid data"


def test_negative_record_count():
    metrics = ETLMetrics("customer_etl")

    with pytest.raises(ValueError):
        metrics.record_read(-1)


def test_invalid_status():
    metrics = ETLMetrics("customer_etl")
    metrics.start()

    with pytest.raises(ValueError):
        metrics.finish("UNKNOWN")


def test_metrics_to_dict():
    metrics = ETLMetrics("customer_etl")
    result = metrics.to_dict()

    assert result["pipeline_name"] == "customer_etl"
    assert "_start_clock" not in result
    assert "execution_id" in result