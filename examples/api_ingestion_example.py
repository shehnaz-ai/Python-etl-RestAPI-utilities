from etl_utils.api_client import APIClient
from etl_utils.api_ingestion import APIIngestor


def main():

    with APIClient() as client:

        ingestor = APIIngestor(client)
        df = ingestor.fetch_limit_offset(
            url="https://dummyjson.com/users",
            records_path="users",
            page_size=30,
        )
        #df = ingestor.fetch(
            #url="https://dummyjson.com/users",
           # records_path="users",
        #)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nFirst 5 records:")
        print(df.head())

        print("\nRecord count:")
        print(len(df))


if __name__ == "__main__":
    main()