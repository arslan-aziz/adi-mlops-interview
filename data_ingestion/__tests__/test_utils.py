import pytest

from data_ingestion.utils import get_bucket_and_key_from_s3_url, S3UrlParsingException


def test_get_bucket_and_key_from_s3_url():
    # happy path
    test_s3_url = "s3://abucket/dir1/dir2/data1.svg"

    bucket, key = get_bucket_and_key_from_s3_url(test_s3_url)
    assert bucket == "abucket"
    assert key == "dir1/dir2/data1.svg"

    # error path
    error_s3_url_1 = "abucket/dir1/data1.png"
    with pytest.raises(S3UrlParsingException):
        bucket, key = get_bucket_and_key_from_s3_url(error_s3_url_1)

    error_s3_url_2 = ""
    with pytest.raises(S3UrlParsingException):
        bucket, key = get_bucket_and_key_from_s3_url(error_s3_url_2)
