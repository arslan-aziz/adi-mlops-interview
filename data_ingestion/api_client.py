import requests
from urllib.parse import urljoin

class ApiException(Exception):
    pass

class BaseApiClient:

    def __init__(self, base_url: str, api_key:str=None):
        self.base_url = base_url
        self.api_key = api_key
    
    def make_get_request(self, endpoint: str, query_params: dict=None, headers: dict=None) -> requests.Response:
        full_url = urljoin(self.base_url, endpoint)
        response = requests.get(full_url, params=query_params, headers=headers)
        self.validate_response(response)
        return response

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code != 200:
            error_string = f"""
            Invalid request with status code {response.status_code}
            and message {response.content.decode()}
            """
            raise ApiException(error_string)
