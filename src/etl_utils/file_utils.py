import json
import pandas as pd
from pathlib import Path

def read_csv(file_path: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV file {file_path}: {e}")

def read_json(file_path: str):
    """Read a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to read JSON file {file_path}: {e}")

def write_csv(df: pd.DataFrame, file_path: str):
    """Write a DataFrame to a CSV file."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
    except Exception as e:
        raise RuntimeError(f"Failed to write CSV file {file_path}: {e}")

def write_json(data, file_path: str):
    """Write data to a JSON file."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to write JSON file {file_path}: {e}")

