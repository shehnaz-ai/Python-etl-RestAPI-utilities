from etl_utils.file_utils import (read_csv,validate_dataframe_not_empty, write_csv,read_json,write_json,validate_columns)

def main():
    # Define file paths
    input_file = "data/raw/customers.csv"
    output_file = (
        "data/processed/"
        "customers_processed.csv"
    )


    # Read the CSV file
    df = read_csv(input_file)
    print("Input Data:")
    print(df)
    #validate that the DataFrame is not empty
    validate_dataframe_not_empty(df)
    # Validate required columns
    required_columns = [
        "customer_id",
        "name",
        "email",
        "city",
        "country",
        "status",
        "created_date",
        "updated_date"
    ]
    validate_columns(df, required_columns)
    write_csv(
        df,
        output_file
    )

    print(
        f"\nSuccessfully wrote "
        f"{len(df)} records."
    )
    transactions = read_json(
        "data/raw/transactions.json"
    )

    write_json(
        transactions,
        "data/processed/transactions_processed.json"
    )

if __name__ == "__main__":
    main()
