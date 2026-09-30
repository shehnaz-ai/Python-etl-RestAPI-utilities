
import pandas as pd
import pytest

from etl_utils.data_loader import DataLoader
from etl_utils.exceptions import DataIngestionError


def test_read_csv(tmp_path):
    path = tmp_path / "input.csv"
    pd.DataFrame({"id": [1, 2]}).to_csv(path, index=False)

    df = DataLoader.read({
        "type": "csv",
        "path": str(path)
    })

    assert df["id"].tolist() == [1, 2]


def test_read_json(tmp_path):
    path = tmp_path / "input.json"
    path.write_text('[{"id": 1}, {"id": 2}]', encoding="utf-8")

    df = DataLoader.read({
        "type": "json",
        "path": str(path)
    })

    assert df["id"].tolist() == [1, 2]


def test_missing_source():
    with pytest.raises(DataIngestionError):
        DataLoader.read({
            "type": "csv",
            "path": "missing.csv"
        })


def test_write_csv(tmp_path):
    df = pd.DataFrame({"id": [1, 2]})
    path = tmp_path / "output" / "result.csv"

    DataLoader.write(
        df,
        {"type": "csv", "path": str(path)}
    )

    assert pd.read_csv(path)["id"].tolist() == [1, 2]