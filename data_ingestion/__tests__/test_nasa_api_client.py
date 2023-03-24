import pytest
from unittest.mock import MagicMock
from requests import Response

from data_ingestion.api_client import ApiException
from data_ingestion.nasa_image_api_client import NasaImageApiClient


def test_validate_response():
    api_client = NasaImageApiClient("aurl")

    # happy path
    mock_response = MagicMock(status_code=200, spec=Response)
    api_client.validate_response(mock_response)

    mock_response = MagicMock(
        status_code=200,
        content=b"Maximum number of search results have been displayed",
        spec=Response,
    )
    api_client.validate_response(mock_response)

    # error path
    with pytest.raises(ApiException):
        mock_response = MagicMock(status_code=400, spec=Response)
        api_client.validate_response(mock_response)
