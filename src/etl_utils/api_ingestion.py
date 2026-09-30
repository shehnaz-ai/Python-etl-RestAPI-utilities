from __future__ import annotations

import logging
from typing import Any, Dict, Optional
import pandas as pd
import requests

from etl_utils.api_client import APIClient
from etl_utils.exceptions import DataIngestionError

class APIIngestor:
    """Ingest records from REST APIs."""

    def __init__(
            self,
            client: APIClient,
            logger=None,
    ):
        self.client = client
        self.logger = logger

    def _extract_records(
            self,
            response: Any,
            records_path: str | None = None,
    ) -> list[dict[str, Any]]:

        data = response

        if records_path:
            for part in records_path.split("."):
                if not isinstance(data, dict):
                    raise DataIngestionError(
                        f"Cannot navigate records_path '{records_path}'"
                    )

                data = data.get(part)

        if isinstance(data, list):
            records = data

        elif isinstance(data, dict):
            records = [data]

        else:
            raise DataIngestionError(
                "API response must contain a list or object"
            )

        if not all(isinstance(record, dict) for record in records):
            raise DataIngestionError(
                "API records must be dictionaries"
            )

        return records

    def fetch(
            self,
            url: str,
            records_path: str | None = None,
            params: dict[str, Any] | None = None,
    ) -> pd.DataFrame:

        try:
            if self.logger:
                self.logger.info(
                    "Fetching API data from %s",
                    url,
                )

            response = self.client.get(
                url,
                params=params,
            )

            records = self._extract_records(
                response,
                records_path,
            )

            df = pd.DataFrame(records)

            if self.logger:
                self.logger.info(
                    "API ingestion completed: %s records",
                    len(df),
                )

            return df

        except Exception as exc:
            if isinstance(exc, DataIngestionError):
                raise

            raise DataIngestionError(
                f"API ingestion failed: {exc}"
            ) from exc


    def fetch_limit_offset(
                self,
                url: str,
                records_path: str,
                page_size: int = 100,
                max_pages: int | None = None,
        ) -> pd.DataFrame:

        all_records: list[dict[str, Any]] = []

        skip = 0
        page_number = 0

        while True:

            if max_pages is not None and page_number >= max_pages:
                break

            page_number += 1

            params = {
                "limit": page_size,
                "skip": skip,
            }

            if self.logger:
                self.logger.info(
                    "Fetching API page=%s skip=%s limit=%s",
                    page_number,
                    skip,
                    page_size,
                )

            response = self.client.get(
                url,
                params=params,
            )

            records = self._extract_records(
                response,
                records_path,
            )

            if not records:
                break

            all_records.extend(records)

            if len(records) < page_size:
                break

            skip += page_size

        return pd.DataFrame(all_records)