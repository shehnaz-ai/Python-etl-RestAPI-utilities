import pandas as pd

def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Validate that the DataFrame contains the required columns."""
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")


def validate_not_nulls(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Validate that the specified columns do not contain null values."""
    null_columns = df[df[columns].isnull().any(axis=1)]

    if null_columns:
        raise ValueError(f"Columns contain null values: {sorted(null_columns)}")
    return null_columns

def find_duplicates(df: pd.DataFrame, key_columns: list[str]) -> pd.DataFrame:
    """Find duplicate rows based on the specified key_columns."""
    duplicates = df[df.duplicated(subset=key_columns, keep=False)]
    return duplicates

