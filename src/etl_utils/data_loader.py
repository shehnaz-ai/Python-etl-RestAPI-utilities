
import json
from pathlib import Path
from typing import Any
from logging import Logger
import pandas as pd

from etl_utils.exceptions import (
    DataIngestionError,
    DataLoadingError
)

from etl_utils.api_client import APIClient
from etl_utils.api_ingestion import APIIngestor


class DataLoader:
    """Generic local file reader and writer."""

    @staticmethod
    def read(source: dict[str, Any]) -> pd.DataFrame:
        source_type = source["type"]
        path = Path(source["path"])

        try:
            if not path.is_file():
                raise FileNotFoundError(
                    f"Source file not found: {path}"
                )

            if source_type == "csv":
                return pd.read_csv(path)

            if source_type == "json":
                with path.open("r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    raise ValueError(
                        "JSON source must contain a list of records"
                    )

                if not isinstance(data, list):
                    raise ValueError(
                        "JSON source must contain a list"
                    )

                return pd.DataFrame(data)

            if source_type == "api":

                url = source["url"]

                records_path = source.get("records_path")

                pagination = source.get("pagination", {})

                with APIClient() as client:

                    ingestor = APIIngestor(
                        client=client,
                        logger=self.logger,
                    )

                    if pagination.get("enabled"):

                        pagination_type = pagination.get("type")

                        if pagination_type == "limit_offset":

                            return ingestor.fetch_limit_offset(
                                url=url,
                                records_path=records_path,
                                page_size=pagination.get(
                                    "page_size",
                                    100,
                                ),
                            )

                        raise DataIngestionError(
                            f"Unsupported pagination type: "
                            f"{pagination_type}"
                        )

                    return ingestor.fetch(
                        url=url,
                        records_path=records_path,
                    )
            raise ValueError(
                f"Unsupported source type: {source_type}"
            )

        except Exception as exc:
            raise DataIngestionError(
                f"Failed to read {path}: {exc}"
            ) from exc

    @staticmethod
    def write(
            df: pd.DataFrame,
            target: dict[str, Any]
    ) -> None:
        target_type = target["type"]
        path = Path(target["path"])

        try:
            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if target_type == "csv":
                df.to_csv(path, index=False)

            elif target_type == "json":
                df.to_json(
                    path,
                    orient="records",
                    indent=4,
                    date_format="iso"
                )

            elif target_type == "parquet":
                df.to_parquet(path, index=False)

            else:
                raise ValueError(
                    f"Unsupported target type: {target_type}"
                )

        except Exception as exc:
            raise DataLoadingError(
                f"Failed to write {path}: {exc}"
            ) from exc

