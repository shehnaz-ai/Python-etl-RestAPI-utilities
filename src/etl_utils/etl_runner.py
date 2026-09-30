import logging
from typing import Any

import pandas as pd

from etl_utils.config_loader import ConfigLoader
from etl_utils.data_loader import DataLoader
from etl_utils.data_validator import DataQualityValidator
from etl_utils.exceptions import (
    ConfigurationError,
    DataValidationError
)
from etl_utils.logger import setup_logger
from etl_utils.pipeline_monitor import PipelineMonitor
from etl_utils.transformations import DataTransformer


class ETLRunner:
    """Execute pipelines defined in YAML metadata."""


    def __init__(
            self,
            config_path: str = "config/config.yaml",
            logger: logging.Logger | None = None
    ):
        self.config_path = config_path
        self.logger = logger or setup_logger("etl_utils")


    def run(self) -> list[dict[str, Any]]:
        config = ConfigLoader(self.config_path).load()
        results = []

        for pipeline in config["pipelines"]:
            if not pipeline.get("enabled", True):
                self.logger.info(
                    "Skipping disabled pipeline: %s",
                    pipeline["name"]
                )
                continue

            results.append(self.run_pipeline(pipeline))

        return results

    def run_pipeline(
            self,
            pipeline: dict[str, Any]
    ) -> dict[str, Any]:
        name = pipeline["name"]

        monitor = PipelineMonitor(
            pipeline_name=name,
            audit_file="logs/etl_audit.jsonl",
            logger=self.logger
        )

        try:
            with monitor:
                self.logger.info(
                    "Starting pipeline: %s", name
                )

                # 1. Ingestion
                df = DataLoader.read(pipeline["source"])
                monitor.record_read(len(df))

                # 2. Validation
                self._validate(df, pipeline)

                # 3. Transformation
                result = self._transform(
                    df,
                    pipeline.get("transformations", [])
                )

                monitor.record_processed(len(result))

                # 4. Loading
                DataLoader.write(
                    result,
                    pipeline["target"]
                )

                self.logger.info(
                    "Completed pipeline '%s' with %d rows",
                    name,
                    len(result)
                )

        except Exception:
            self.logger.exception(
                "Pipeline '%s' failed", name
            )
            raise

        return monitor.metrics.to_dict()

    @staticmethod
    def _validate(
            df: pd.DataFrame,
            pipeline: dict[str, Any]
    ) -> None:
        validator = DataQualityValidator(df)

        # Validate primary key definitions.
        primary_key = pipeline.get("primary_key", [])

        if primary_key:
            missing = validator.validate_required_columns(primary_key)

            if missing:
                raise DataValidationError(
                    f"Missing primary key columns: {missing}"
                )

        # Apply quality rules.
        for rule in pipeline.get("quality_rules", []):
            rule_type = rule.get("type")

            if rule_type == "not_null":
                validator.validate_not_null(rule["columns"])

            elif rule_type == "unique":
                validator.validate_unique(rule["columns"])

            elif rule_type == "email":
                validator.validate_email(rule["column"])

            else:
                raise DataValidationError(
                    f"Unsupported quality rule: {rule_type}"
                )

        # Retrieve the accumulated validation results.
        valid, rejected, summary = validator.get_results()

        # Fail the pipeline if any records were rejected.
        if not rejected.empty:
            raise DataValidationError(
                f"Data quality validation failed. "
                f"Rejected rows: {len(rejected)}. "
                f"Summary: {summary}"
            )


    @staticmethod
    def _transform(
            df: pd.DataFrame,
            steps: list[dict[str, Any]]
    ) -> pd.DataFrame:
        transformer = DataTransformer(df)

        for step in steps:
            operation = step.get("type")

            if operation == "trim":
                transformer.trim_strings(step["columns"])

            elif operation == "uppercase":
                transformer.standardize_strings(
                    step["columns"],
                    case="upper"
                )

            elif operation == "lowercase":
                transformer.standardize_strings(
                    step["columns"],
                    case="lower"
                )

            elif operation == "rename":
                transformer.rename_columns(step["mapping"])

            elif operation == "numeric":
                transformer.convert_types(
                    step["columns"],
                    errors="raise"
                )

            elif operation == "dates":
                transformer.standardize_dates(
                    step["columns"],
                    date_format=step.get("format"),
                    errors="raise"
                )

            elif operation == "fill_nulls":
                transformer.fill_nulls(step["mapping"])

            else:
                raise ConfigurationError(
                    f"Unsupported transformation: {operation}"
                )

        return transformer.result()