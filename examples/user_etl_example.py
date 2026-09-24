import sys
from pathlib import Path
import logging

from src.etl_utils.data_validator import validate_not_nulls, find_duplicates
from src.etl_utils.api_client import APIClient
from src.etl_utils.data_validator import validate_columns
from src.etl_utils.transformations import (
    standardize_column_names,
    trim_string_columns
)
from src.etl_utils.file_utils import  write_json
from src.etl_utils.logger import configure_logging
import pandas as  pd

def main():
    # Configure logging
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("ETL pipeline started")
    logger.warning("Missing email records detected")
    logger.error("Pipeline failed")

    """How You Can want to read data from API and then clean it and save it to json file"""

    client = APIClient("https://dummyjson.com")
    users = client.get("/users")
    print(users)
    df=pd.DataFrame(users)
    df=standardize_column_names(df)
    df=trim_string_columns(df)
    # Define file paths
    #input_file = "data/input_data.csv"
    #output_file = "data/cleaned_data.csv"

    # Read the CSV file
    #df = read_csv(input_file)

    # Validate required columns
    required_columns = ["id", "firstName", "lastName","maidenName","age","gender","email","phone","username","password","birthDate","image","bloodGroup","height","weight","eyeColor","hair","domain","ip","address_address","address_city","address_coordinates_latitude","address_coordinates_longitude","address_postalCode","address_state"]
    validate_columns(df, required_columns)

    # Validate that there are no null values in required columns
    validate_not_nulls(df, required_columns)

    # Find duplicates based on 'id' column
    duplicates = find_duplicates(df, ["id"])
    if not duplicates.empty:
        print(f"Found duplicates:\n{duplicates}")

    # Remove duplicates and save cleaned data
    df_cleaned = df.drop_duplicates(subset=["id"])
    output_file = "data/processed/cleaned_data.json"
    write_json(df_cleaned, output_file)
    print(f"Successfully processed {len(df_cleaned)} records")


if __name__ == "__main__":
    main()