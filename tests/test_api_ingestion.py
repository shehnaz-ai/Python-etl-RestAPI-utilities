import pandas as pd

from etl_utils.api_ingestion import APIIngestor


class FakeAPIClient:

    def get(self, endpoint, params=None):

        return {
            "users": [
                {
                    "id": 1,
                    "email": "a@example.com",
                },
                {
                    "id": 2,
                    "email": "b@example.com",
                },
            ]
        }


def test_api_ingestion():

    client = FakeAPIClient()

    ingestor = APIIngestor(client)

    df = ingestor.fetch(
        url="https://example.com/users",
        records_path="users",
    )

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 2

    assert "id" in df.columns

    assert "email" in df.columns


class FakePaginationClient:

    def get(self, endpoint, params=None):

        skip = params["skip"]

        if skip == 0:
            return {
                "users": [
                    {"id": 1},
                    {"id": 2},
                ]
            }

        if skip == 2:
            return {
                "users": [
                    {"id": 3},
                    {"id": 4},
                ]
            }

        return {
            "users": []
        }


def test_limit_offset_pagination():

    client = FakePaginationClient()

    ingestor = APIIngestor(client)

    df = ingestor.fetch_limit_offset(
        url="https://example.com/users",
        records_path="users",
        page_size=2,
    )

    assert len(df) == 4

    assert df["id"].tolist() == [
        1,
        2,
        3,
        4,
    ]