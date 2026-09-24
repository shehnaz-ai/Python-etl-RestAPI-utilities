import sys
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from src.etl_utils.api_client import APIClient


def test_api_client_success():

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "users": [
            {
                "id": 1,
                "firstName": "John"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
            "etl_utils.api_client.requests.Session.get",
            return_value=mock_response
    ) as mock_get:

        client = APIClient(
            "https://dummyjson.com"
        )

        result = client.get("/users")

        assert "users" in result

        mock_get.assert_called_once()


def test_api_client_http_error():

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        Exception("HTTP error")
    )

    with patch(
            "etl_utils.api_client.requests.Session.get",
            return_value=mock_response
    ):

        client = APIClient(
            "https://dummyjson.com"
        )

        with pytest.raises(Exception):
            client.get("/users")