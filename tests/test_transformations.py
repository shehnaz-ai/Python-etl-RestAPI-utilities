
import pandas as pd
import pytest

from etl_utils.transformations import DataTransformer


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Customer ID": [1, 2, 3],
        "Name": [" John ", "SARAH", " David "],
        "Amount": ["100.50", "200.00", "invalid"],
        "Status": ["active", "inactive", "active"],
        "Created Date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-03"
        ]
    })


def test_standardize_column_names(sample_df):
    result = (
        DataTransformer(sample_df)
        .standardize_column_names()
        .result()
    )
    assert "customer_id" in result.columns
    assert "created_date" in result.columns


def test_trim_strings(sample_df):
    result = (
        DataTransformer(sample_df)
        .trim_strings(["Name"])
        .result()
    )
    assert result["Name"].tolist() == [
        "John", "SARAH", "David"
    ]


def test_rename_columns(sample_df):
    result = (
        DataTransformer(sample_df)
        .rename_columns({"Customer ID": "customer_id"})
        .result()
    )
    assert "customer_id" in result.columns


def test_standardize_strings(sample_df):
    result = (
        DataTransformer(sample_df)
        .standardize_strings(["Status"], case="upper")
        .result()
    )
    assert result["Status"].tolist() == [
        "ACTIVE", "INACTIVE", "ACTIVE"
    ]


def test_convert_types(sample_df):
    result = (
        DataTransformer(sample_df)
        .convert_types(
            {"Amount": "float64"},
            errors="coerce"
        )
        .result()
    )
    assert result["Amount"].dtype == "float64"
    assert pd.isna(result["Amount"].iloc[2])


def test_standardize_dates(sample_df):
    result = (
        DataTransformer(sample_df)
        .standardize_dates(
            ["Created Date"],
            date_format="%Y-%m-%d"
        )
        .result()
    )
    assert pd.api.types.is_datetime64_any_dtype(
        result["Created Date"]
    )


def test_fill_nulls():
    df = pd.DataFrame({"city": ["London", None]})
    result = (
        DataTransformer(df)
        .fill_nulls({"city": "UNKNOWN"})
        .result()
    )
    assert result["city"].tolist() == [
        "London", "UNKNOWN"
    ]


def test_add_column(sample_df):
    result = (
        DataTransformer(sample_df)
        .convert_types({"Amount": "float64"}, errors="coerce")
        .add_column(
            "double_amount",
            lambda data: data["Amount"] * 2
        )
        .result()
    )
    assert result["double_amount"].iloc[0] == 201.0


def test_filter_rows(sample_df):
    result = (
        DataTransformer(sample_df)
        .filter_rows(
            lambda data: data["Status"].eq("active")
        )
        .result()
    )
    assert len(result) == 2


def test_sort_by(sample_df):
    result = (
        DataTransformer(sample_df)
        .sort_by(["Customer ID"], ascending=False)
        .result()
    )
    assert result["Customer ID"].tolist() == [3, 2, 1]


def test_missing_column(sample_df):
    with pytest.raises(ValueError, match="Missing columns"):
        DataTransformer(sample_df).trim_strings(["unknown"])


def test_invalid_case(sample_df):
    with pytest.raises(ValueError):
        DataTransformer(sample_df).standardize_strings(
            ["Name"], case="invalid"
        )


def test_original_dataframe_is_unchanged(sample_df):
    original = sample_df.copy(deep=True)

    DataTransformer(sample_df).trim_strings(["Name"])

    pd.testing.assert_frame_equal(sample_df, original)