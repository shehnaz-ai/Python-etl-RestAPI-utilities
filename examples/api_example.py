import logging
from pathlib import Path

from etl_utils.api_client import APIClient


def main():

    with APIClient(
            base_url="https://dummyjson.com",
            timeout=30,
            max_retries=3
    ) as client:

        response = client.get("/users")

        users = response["users"]

        print(f"Total users received: {len(users)}")

        for user in users[:5]:

            print(
                user["id"],
                user["firstName"],
                user["email"]
            )


if __name__ == "__main__":
    main()