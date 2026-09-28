import json
import pandas as pd
from pathlib import Path


def validate_file_exists(file_path: str) -> Path:
    """Validate that the file exists."""
    path=Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    return path

def validate_dataframe_not_empty(
        df: pd.DataFrame
) -> None:
    """
    Validate that a DataFrame contains records.
    """

    if df.empty:
        raise ValueError(
            "DataFrame contains no records."
        )


def read_csv(file_path: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame."""
    path = validate_file_exists(file_path)
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError(f"CSV file is empty: {path}")
    return df

def write_csv(df: pd.DataFrame, file_path: str):
    """Write a DataFrame to a CSV file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def read_json(file_path: str):
    """Read a JSON file."""
    path = validate_file_exists(file_path)
    with path.open("r",encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json(data, file_path: str):
    """ Write Python data to JSON."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open( "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4,ensure_ascii=False)

def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Validate that the DataFrame contains the required columns.
        Validate that required columns exist."""

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
        ]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )
