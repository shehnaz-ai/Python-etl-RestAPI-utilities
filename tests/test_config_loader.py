
import pytest
import yaml

from etl_utils.config_loader import ConfigLoader
from etl_utils.exceptions import ConfigurationError


def test_load_valid_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        yaml.safe_dump({
            "pipelines": [{
                "name": "customers",
                "source": {
                    "type": "csv",
                    "path": "customers.csv"
                },
                "target": {
                    "type": "csv",
                    "path": "output.csv"
                }
            }]
        }),
        encoding="utf-8"
    )

    config = ConfigLoader(str(config_file)).load()

    assert config["pipelines"][0]["name"] == "customers"


def test_missing_config():
    with pytest.raises(ConfigurationError):
        ConfigLoader("missing.yaml").load()


def test_duplicate_pipeline_names():
    config = {
        "pipelines": [
            {
                "name": "customers",
                "source": {"type": "csv", "path": "in.csv"},
                "target": {"type": "csv", "path": "out.csv"}
            },
            {
                "name": "customers",
                "source": {"type": "csv", "path": "in2.csv"},
                "target": {"type": "csv", "path": "out2.csv"}
            }
        ]
    }

    with pytest.raises(
            ConfigurationError,
            match="Duplicate pipeline name"
    ):
        ConfigLoader.validate(config)


def test_unsupported_source():
    config = {
        "pipelines": [{
            "name": "customers",
            "source": {"type": "database", "path": "db"},
            "target": {"type": "csv", "path": "out.csv"}
        }]
    }

    with pytest.raises(ConfigurationError):
        ConfigLoader.validate(config)