
import pandas as pd
import pytest

from etl_utils.data_validator import DataQualityValidator
from etl_utils.exceptions import SchemaValidationError


def test_validate_not_null():
    df = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "name": ["John", None, "Alice"]
    })

    valid, rejected, summary = (
        DataQualityValidator(df)
        .validate_not_null(["name"])
        .get_results()
    )

    assert len(valid) == 2
    assert len(rejected) == 1
    assert "NULL_VALUE" in rejected.iloc[0]["rejection_reasons"]


def test_validate_duplicates():
    df = pd.DataFrame({
        "customer_id": [1, 2, 2, 3]
    })

    valid, rejected, summary = (
        DataQualityValidator(df)
        .validate_duplicates(["customer_id"])
        .get_results()
    )

    assert len(valid) == 3
    assert len(rejected) == 1
    assert summary["rejected_records"] == 1


def test_validate_email():
    df = pd.DataFrame({
        "email": [
            "john@example.com",
            "invalid-email",
            "alice@example.com"
        ]
    })

    valid, rejected, summary = (
        DataQualityValidator(df)
        .validate_email("email")
        .get_results()
    )

    assert len(valid) == 2
    assert len(rejected) == 1


def test_validate_numeric_range():
    df = pd.DataFrame({
        "amount": [100, -10, 500, 0]
    })

    valid, rejected, summary = (
        DataQualityValidator(df)
        .validate_numeric_range("amount", minimum=0)
        .get_results()
    )

    assert len(valid) == 3
    assert len(rejected) == 1


def test_missing_column():
    df = pd.DataFrame({"customer_id": [1, 2]})

    with pytest.raises(SchemaValidationError):
        DataQualityValidator(df).validate_columns(
            ["customer_id", "email"]
        )


def test_multiple_validation_errors():
    df = pd.DataFrame({
        "customer_id": [1, 2, 2],
        "email": ["good@example.com", "bad", None]
    })

    valid, rejected, summary = (
        DataQualityValidator(df)
        .validate_not_null(["email"])
        .validate_duplicates(["customer_id"])
        .validate_email("email")
        .get_results()
    )

    assert len(valid) == 1
    assert len(rejected) == 2
    assert summary["total_records"] == 3