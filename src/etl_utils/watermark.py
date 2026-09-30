from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class WatermarkStore:

    def __init__(self, path: str = "metadata/watermarks.json"):
        self.path = Path(path)

    def _load(self) -> dict[str, Any]:

        if not self.path.exists():
            return {}

        with self.path.open(
                "r",
                encoding="utf-8",
        ) as file:
            return json.load(file)

    def get(self, pipeline_name: str) -> str | None:

        data = self._load()

        return data.get(pipeline_name)

    def set(
            self,
            pipeline_name: str,
            watermark: str,
    ) -> None:

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self._load()

        data[pipeline_name] = watermark

        temp_path = self.path.with_suffix(".tmp")

        with temp_path.open(
                "w",
                encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
            )

        temp_path.replace(self.path)