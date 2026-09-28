from pathlib import Path

import pandas as pd
import pytest

from etl_utils.file_utils import (
    read_csv,
    write_csv,
    read_json,
    write_json,
    validate_file_exists,
    validate_columns
)


def test_read_csv(tmp_path):

    file_path = tmp_path / "customers.csv"

    file_path.write_text(
        "customer_id,name\n"
        "1,John\n"
        "2,Sarah\n",
        encoding="utf-8"
    )

    df = read_csv(file_path)

    assert len(df) == 2
    assert list(df.columns) == [
        "customer_id",
        "name"
    ]


def test_write_csv(tmp_path):

    df = pd.DataFrame({
        "customer_id": [1, 2],
        "name": ["John", "Sarah"]
    })

    output_file = (
            tmp_path / "output" / "customers.csv"
    )

    write_csv(
        df,
        output_file
    )

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert len(result) == 2


def test_read_json(tmp_path):

    file_path = tmp_path / "data.json"

    file_path.write_text(
        '{"customer_id": 1, "name": "John"}',
        encoding="utf-8"
    )

    data = read_json(file_path)

    assert data["customer_id"] == 1
    assert data["name"] == "John"


def test_write_json(tmp_path):

    data = {
        "customer_id": 1,
        "name": "John"
    }

    output_file = (
            tmp_path / "output" / "customer.json"
    )

    write_json(
        data,
        output_file
    )

    assert output_file.exists()

    result = read_json(output_file)

    assert result == data


def test_missing_file():

    with pytest.raises(FileNotFoundError):

        validate_file_exists(
            "does_not_exist.csv"
        )


def test_validate_columns_success():

    df = pd.DataFrame({
        "customer_id": [1, 2],
        "name": ["John", "Sarah"]
    })

    validate_columns(
        df,
        ["customer_id", "name"]
    )


def test_validate_columns_failure():

    df = pd.DataFrame({
        "customer_id": [1, 2]
    })

    with pytest.raises(ValueError):

        validate_columns(
            df,
            ["customer_id", "name"]
        )