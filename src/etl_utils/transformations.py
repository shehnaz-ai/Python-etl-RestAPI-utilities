
from collections.abc import Callable
from typing import Any

import pandas as pd


class DataTransformer:
    """Reusable, chainable Pandas transformation utilities."""

    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        self.df = df.copy()

    def _require_columns(self, columns: list[str]) -> None:
        missing = [col for col in columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    # 1. Rename columns
    def rename_columns(
            self, mapping: dict[str, str]
    ) -> "DataTransformer":
        self._require_columns(list(mapping.keys()))

        if len(set(mapping.values())) != len(mapping.values()):
            raise ValueError("Renaming would create duplicate column names")

        renamed = self.df.rename(columns=mapping)
        if not renamed.columns.is_unique:
            raise ValueError("Renaming creates duplicate column names")

        self.df = renamed
        return self

    # 2. Standardize column names
    def standardize_column_names(self) -> "DataTransformer":
        names = (
            self.df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[^a-z0-9]+", "_", regex=True)
            .str.strip("_")
        )

        if not names.is_unique:
            raise ValueError(
                "Column standardization creates duplicate names"
            )

        self.df.columns = names
        return self

    # 3. Trim whitespace from string columns
    def trim_strings(
            self, columns: list[str] | None = None
    ) -> "DataTransformer":
        if columns is None:
            columns = self.df.select_dtypes(
                include=["object", "string"]
            ).columns.tolist()

        self._require_columns(columns)

        for col in columns:
            if (
                    pd.api.types.is_object_dtype(self.df[col])
                    or pd.api.types.is_string_dtype(self.df[col])
            ):
                self.df[col] = self.df[col].map(
                    lambda value: value.strip()
                    if isinstance(value, str)
                    else value
                )

        return self

    # 4. Standardize string values
    def standardize_strings(
            self,
            columns: list[str],
            case: str = "lower"
    ) -> "DataTransformer":
        self._require_columns(columns)

        if case not in {"lower", "upper", "title"}:
            raise ValueError(
                "case must be lower, upper, or title"
            )

        for col in columns:
            def normalize(value: Any) -> Any:
                if not isinstance(value, str):
                    return value
                if case == "lower":
                    return value.lower()
                if case == "upper":
                    return value.upper()
                return value.title()

            self.df[col] = self.df[col].map(normalize)

        return self

    # 5. Convert data types
    def convert_types(
            self,
            type_mapping: dict[str, str],
            errors: str = "raise"
    ) -> "DataTransformer":
        self._require_columns(list(type_mapping.keys()))

        if errors not in {"raise", "coerce"}:
            raise ValueError("errors must be 'raise' or 'coerce'")

        supported = {
            "int64", "Int64", "float64", "string",
            "str", "bool", "boolean"
        }

        for col, dtype in type_mapping.items():
            if dtype not in supported:
                raise ValueError(
                    f"Unsupported dtype '{dtype}' for column '{col}'"
                )

            try:
                if dtype in {"int64", "Int64", "float64"}:
                    values = pd.to_numeric(
                        self.df[col], errors=errors
                    )
                    self.df[col] = values.astype(dtype)
                elif dtype == "str":
                    self.df[col] = self.df[col].astype(str)
                elif dtype in {"bool", "boolean"}:
                    self.df[col] = self.df[col].astype(dtype)
                else:
                    self.df[col] = self.df[col].astype(dtype)
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Cannot convert '{col}' to {dtype}: {exc}"
                ) from exc

        return self

    # 6. Standardize dates
    def standardize_dates(
            self,
            columns: list[str],
            date_format: str | None = None,
            errors: str = "raise"
    ) -> "DataTransformer":
        self._require_columns(columns)

        if errors not in {"raise", "coerce"}:
            raise ValueError("errors must be 'raise' or 'coerce'")

        for col in columns:
            try:
                self.df[col] = pd.to_datetime(
                    self.df[col],
                    format=date_format,
                    errors=errors
                )
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Cannot parse dates in '{col}': {exc}"
                ) from exc

        return self

    # 7. Fill null values
    def fill_nulls(
            self,
            fill_mapping: dict[str, Any]
    ) -> "DataTransformer":
        self._require_columns(list(fill_mapping.keys()))

        for col, value in fill_mapping.items():
            self.df[col] = self.df[col].fillna(value)

        return self

    # 8. Add a derived column
    def add_column(
            self,
            column: str,
            expression: Callable[[pd.DataFrame], Any]
    ) -> "DataTransformer":
        if not callable(expression):
            raise TypeError("expression must be callable")

        if column in self.df.columns:
            raise ValueError(
                f"Column '{column}' already exists"
            )

        result = expression(self.df.copy())

        if isinstance(result, pd.Series):
            if not result.index.equals(self.df.index):
                raise ValueError(
                    "Derived Series must have the same index as the DataFrame"
                )
            self.df[column] = result
        elif isinstance(result, (list, tuple)):
            if len(result) != len(self.df):
                raise ValueError(
                    "Derived values must match DataFrame length"
                )
            self.df[column] = result
        else:
            self.df[column] = result

        return self

    # 9. Filter records
    def filter_rows(
            self,
            condition: Callable[[pd.DataFrame], pd.Series]
    ) -> "DataTransformer":
        if not callable(condition):
            raise TypeError("condition must be callable")

        mask = condition(self.df.copy())

        if not isinstance(mask, pd.Series):
            raise TypeError("Filter must return a pandas Series")

        if not mask.index.equals(self.df.index):
            raise ValueError(
                "Filter mask index must match the DataFrame index"
            )

        if not pd.api.types.is_bool_dtype(mask.dtype):
            raise TypeError("Filter must return a Boolean Series")

        if mask.isna().any():
            raise ValueError("Filter mask cannot contain null values")

        self.df = self.df.loc[mask].copy()
        return self

    # 10. Sort records
    def sort_by(
            self,
            columns: list[str],
            ascending: bool = True
    ) -> "DataTransformer":
        self._require_columns(columns)
        self.df = self.df.sort_values(
            by=columns,
            ascending=ascending
        ).reset_index(drop=True)
        return self

    # Return transformed data
    def result(self) -> pd.DataFrame:
        return self.df.copy()