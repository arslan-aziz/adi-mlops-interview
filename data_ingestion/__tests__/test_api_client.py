import pytest
from unittest.mock import MagicMock
from requests import Response

from data_ingestion.api_client import ApiException, BaseApiClient

def test_validate_response():
    api_client = BaseApiClient('aurl')
    
    # happy path
    mock_response = MagicMock(status_code=200, spec=Response)
    api_client.validate_response(mock_response)

    # error path
    with pytest.raises(ApiException):
        mock_response = MagicMock(status_code=400, spec=Response)
        api_client.validate_response(mock_response)
