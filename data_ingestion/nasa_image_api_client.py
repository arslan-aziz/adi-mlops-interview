import requests
from data_ingestion.api_client import BaseApiClient, ApiException

class SearchResultsExhaustedException(ApiException):
    pass

class NasaImageApiClient(BaseApiClient):
    NASA_IMAGE_API_SEARCH_ENDPOINT = "search"
    DEFAULT_PAGE_SIZE = 100

    def __init__(self, base_url: str, api_key: str = None):
        super().__init__(base_url, api_key)

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code != 200:
            error_message = response.content.decode()
            error_string = f"""
            Invalid request with status code {response.status_code}
            and message {error_message}
            """
            if (
                "Maximum number of search results have been displayed"
                in error_message
            ):
                raise SearchResultsExhaustedException(error_string)
            else:
                raise ApiException(error_string)

    def estimate_number_pages_in_paginated_result(
        self, response: requests.Response, page_size: int = DEFAULT_PAGE_SIZE
    ) -> int:
        total_hits = response.json()["collection"]["metadata"]["total_hits"]
        return total_hits // page_size + 1
