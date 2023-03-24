from unittest.mock import patch, MagicMock
import datetime

from data_ingestion.api_client import ApiException
from data_ingestion.main import (
    make_nasa_api_search_request_and_get_json,
    parse_nasa_image_api_search_hit,
)


@patch("data_ingestion.main.NasaImageApiClient")
def test_make_nasa_api_search_request_and_get_json(mock_nasa_image_api_client):
    # Test the happy path
    TEST_DATA = {"collection": {"items": [1, 2, 3]}}
    mock_nasa_image_api_client.return_value.make_get_request.return_value.json.return_value = (
        TEST_DATA
    )
    assert (
        make_nasa_api_search_request_and_get_json(1) == TEST_DATA["collection"]["items"]
    )

    # Test the error path
    mock_nasa_image_api_client.return_value.make_get_request.side_effect = (
        ApiException()
    )
    assert make_nasa_api_search_request_and_get_json(1) == []

def test_parse_nasa_image_api_search_hit():
    TEST_DATA = {
        "data": [
            {
                "center": "JSC",
                "date_created": "1969-07-21T00:00:00Z",
                "description": "a description",
                "media_type": "image",
                "nasa_id": "as11-40-5874",
                "title": "An Image from Space about the Moon",
            }
        ],
        "href": "https://images-assets.nasa.gov/image/as11-40-5874/collection.json",
        "links": [
            {
                "href": "https//images-assets.nasa.gov/animage.jpg",
                "rel": "preview",
                "render": "image",
            },
            {"href": "https//images-assets.nasa.gov/notanimage.txt", "render": "text"},
        ],
    }

    CORRECT_RESULT = {
        "nasa_id": "as11-40-5874",
        "title": "An Image from Space about the Moon",
        "date_created": datetime.datetime(
            1969, 7, 21, 0, 0, tzinfo=datetime.timezone.utc
        ),
        "description": "a description",
        "image_href": "https//images-assets.nasa.gov/animage.jpg",
        "original_image_file_name": "animage.jpg",
        "image_file_extension": ".jpg",
    }

    assert parse_nasa_image_api_search_hit(TEST_DATA) == CORRECT_RESULT
