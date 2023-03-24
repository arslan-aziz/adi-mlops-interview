import pytest
from unittest.mock import MagicMock
from requests import Response

from data_ingestion.api_client import ApiException
from data_ingestion.nasa_image_api_client import (
    NasaImageApiClient,
    SearchResultsExhaustedException,
)


def test_validate_response():
    api_client = NasaImageApiClient("aurl")

    # happy path
    mock_response = MagicMock(status_code=200, spec=Response)
    api_client.validate_response(mock_response)

    # error path
    mock_response = MagicMock(
        status_code=400,
        content=b"Maximum number of search results have been displayed",
        spec=Response,
    )
    with pytest.raises(SearchResultsExhaustedException):
        api_client.validate_response(mock_response)

    mock_response = MagicMock(status_code=400, spec=Response)
    with pytest.raises(ApiException):
        api_client.validate_response(mock_response)
