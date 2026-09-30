
from pathlib import Path
from typing import Any

import yaml

from etl_utils.exceptions import ConfigurationError


class ConfigLoader:
    """Load and validate metadata-driven ETL configuration."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load(self) -> dict[str, Any]:
        if not self.config_path.is_file():
            raise ConfigurationError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with self.config_path.open(
                    "r", encoding="utf-8"
            ) as file:
                config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise ConfigurationError(
                f"Invalid YAML: {exc}"
            ) from exc

        if not isinstance(config, dict):
            raise ConfigurationError(
                "Configuration must be a YAML mapping"
            )

        self.validate(config)
        return config

    @staticmethod
    def validate(config: dict[str, Any]) -> None:
        if not isinstance(config.get("pipelines"), list):
            raise ConfigurationError(
                "'pipelines' must be a list"
            )

        names = set()

        for index, pipeline in enumerate(config["pipelines"]):
            prefix = f"pipelines[{index}]"

            if not isinstance(pipeline, dict):
                raise ConfigurationError(
                    f"{prefix} must be a mapping"
                )

            name = pipeline.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ConfigurationError(
                    f"{prefix}.name must be a non-empty string"
                )

            if name in names:
                raise ConfigurationError(
                    f"Duplicate pipeline name: {name}"
                )
            names.add(name)

            if not isinstance(pipeline.get("enabled", True), bool):
                raise ConfigurationError(
                    f"{prefix}.enabled must be Boolean"
                )

            source = pipeline.get("source")
            target = pipeline.get("target")

            if not isinstance(source, dict):
                raise ConfigurationError(
                    f"{prefix}.source must be a mapping"
                )

            if not isinstance(target, dict):
                raise ConfigurationError(
                    f"{prefix}.target must be a mapping"
                )

            for section_name, section in (
                    ("source", source),
                    ("target", target)
            ):
                kind = section.get("type")
                path = section.get("path")

                if kind not in (
                        {"csv", "json"}
                        if section_name == "source"
                        else {"csv", "json", "parquet"}
                ):
                    raise ConfigurationError(
                        f"Unsupported {section_name} type "
                        f"'{kind}' in pipeline '{name}'"
                    )

                if not isinstance(path, str) or not path.strip():
                    raise ConfigurationError(
                        f"{prefix}.{section_name}.path "
                        "must be a non-empty string"
                    )

            for key in ("quality_rules", "transformations"):
                value = pipeline.get(key, [])
                if not isinstance(value, list):
                    raise ConfigurationError(
                        f"{prefix}.{key} must be a list"
                    )

                if not all(isinstance(item, dict) for item in value):
                    raise ConfigurationError(
                        f"Every item in {prefix}.{key} "
                        "must be a mapping"
                    )