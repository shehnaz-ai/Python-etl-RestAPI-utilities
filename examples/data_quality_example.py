from etl_utils.file_utils import read_csv, write_csv
from etl_utils.data_validator import DataQualityValidator


def main():
    df = read_csv("data/raw/customers.csv")

    validator = DataQualityValidator(df)

    validator.validate_columns([
        "customer_id",
        "name",
        "email",
        "city",
        "country",
        "status",
        "created_date",
        "updated_date"
    ])

    valid, rejected, summary = (
        validator
        .validate_not_null([
            "customer_id",
            "name",
            "email"
        ])
        .validate_duplicates(["customer_id"])
        .validate_email("email")
        .get_results()
    )

    write_csv(
        valid,
        "data/processed/customers_valid.csv"
    )

    if not rejected.empty:
        write_csv(
            rejected,
            "data/rejected/customers_rejected.csv"
        )

    print("Data Quality Report")
    print("-" * 30)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()