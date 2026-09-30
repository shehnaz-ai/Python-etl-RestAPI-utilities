
import pandas as pd

from etl_utils.etl_runner import ETLRunner


def test_run_pipeline(tmp_path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"

    pd.DataFrame({
        "customer_id": [1, 2],
        "name": [" John ", "Sarah"],
        "email": ["john@example.com", "sarah@example.com"],
        "status": ["active", "inactive"]
    }).to_csv(source, index=False)

    pipeline = {
        "name": "customers",
        "source": {
            "type": "csv",
            "path": str(source)
        },
        "primary_key": ["customer_id"],
        "quality_rules": [
            {"type": "not_null", "columns": ["customer_id", "email"]},
            {"type": "unique", "columns": ["customer_id"]},
            {"type": "email", "column": "email"}
        ],
        "transformations": [
            {"type": "trim", "columns": ["name"]},
            {"type": "uppercase", "columns": ["status"]}
        ],
        "target": {
            "type": "csv",
            "path": str(target)
        }
    }

    runner = ETLRunner(
        logger=__import__("logging").getLogger("test.etl")
    )
    runner.logger.handlers.clear()
    runner.logger.addHandler(
        __import__("logging").NullHandler()
    )

    # Isolate the audit output from the real project.
    # The monitor's audit path is configured by the runner,
    # so this test can replace its factory.
    from etl_utils import etl_runner

    original_monitor = etl_runner.PipelineMonitor

    class TestMonitor(original_monitor):
        def __init__(self, *args, **kwargs):
            kwargs["audit_file"] = str(tmp_path / "audit.jsonl")
            super().__init__(*args, **kwargs)

    etl_runner.PipelineMonitor = TestMonitor
    try:
        result = runner.run_pipeline(pipeline)
    finally:
        etl_runner.PipelineMonitor = original_monitor

    assert result["status"] == "SUCCESS"
    assert result["records_read"] == 2
    assert result["records_processed"] == 2

    output = pd.read_csv(target)
    assert output["status"].tolist() == ["ACTIVE", "INACTIVE"]
    assert output["name"].tolist() == ["John", "Sarah"]