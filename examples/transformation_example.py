
import pandas as pd

from etl_utils.transformations import DataTransformer


def main():
    df = pd.DataFrame({
        "Customer ID": [1, 2, 3, 4, 5],
        "Customer Name": [
            " John Smith ",
            "SARAH KHAN",
            " David Lee ",
            "Alice Brown",
            "Mike Wilson"
        ],
        "Email Address": [
            "JOHN@EXAMPLE.COM",
            "sarah@example.com",
            "david@example.com",
            "alice@example.com",
            "mike@example.com"
        ],
        "City": [
            " New York ",
            " London ",
            " Toronto ",
            " Sydney ",
            " Berlin "
        ],
        "Status": [
            "active", "ACTIVE", "inactive",
            "active", "inactive"
        ],
        "Created Date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-03",
            "2025-01-04",
            "2025-01-05"
        ],
        "Amount": ["1200.50", "800.00", "150.75", "300", "500"]
    })

    transformer = (
        DataTransformer(df)
        .standardize_column_names()
        .trim_strings()
        .rename_columns({
            "customer_name": "name",
            "email_address": "email",
            "created_date": "created_at"
        })
        .standardize_strings(
            ["name", "email"],
            case="lower"
        )
        .standardize_strings(
            ["status"],
            case="upper"
        )
        .convert_types({
            "customer_id": "int64",
            "amount": "float64"
        })
        .standardize_dates(
            ["created_at"],
            date_format="%Y-%m-%d"
        )
        .add_column(
            "amount_with_tax",
            lambda data: (data["amount"] * 1.18).round(2)
        )
        .filter_rows(
            lambda data: data["status"].eq("ACTIVE")
        )
        .sort_by(["customer_id"])
    )

    result = transformer.result()

    print("Transformed customers:")
    print(result)

    result.to_csv(
        "data/processed/customers_transformed.csv",
        index=False
    )

    print(f"\nProcessed {len(result)} active customers.")


if __name__ == "__main__":
    main()