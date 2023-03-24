from typing import Tuple

class S3UrlParsingException(Exception):
    pass

def get_bucket_and_key_from_s3_url(s3_url: str) -> Tuple[str, str]:
    if len(s3_url.split('/')) < 4 or s3_url.split('/')[0] != 's3:':
        raise S3UrlParsingException(f"Error parsing {s3_url}. Is this a valid url?")

    try:
        bucket = s3_url.split('/')[2]
        key = '/'.join(s3_url.split('/')[3:])
    except:
        raise S3UrlParsingException(f"Error parsing {s3_url}. Is this a valid url?")
    return bucket, key