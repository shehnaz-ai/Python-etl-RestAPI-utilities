import pandas as pd

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase and replace spaces with underscores."""
    result=df.copy()
    result.columns = result.columns.str.strip().str.lower().str.replace(' ', '_')
    return result

def trim_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace from string columns."""
    result=df.copy()
    str_cols = result.select_dtypes(include=["object","string"]).columns
    result[str_cols] = result[str_cols].apply(lambda x: x.str.strip())
    return result

