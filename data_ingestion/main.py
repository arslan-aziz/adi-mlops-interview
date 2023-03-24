import os
import datetime
from typing import Iterator
import boto3
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lit, concat
from pyspark.sql.types import (
    StringType,
    TimestampType,
    StructType,
    StructField,
    BinaryType,
    Row
)

from data_ingestion.api_client import BaseApiClient, ApiException
from data_ingestion.nasa_image_api_client import NasaImageApiClient
from data_ingestion.config import (
    NASA_API_KEY,
    NASA_IMAGE_API_BASE_URL,
    S3_BUCKET_NAME,
    S3_KEY_PREFIX,
    PY_LOG_LEVEL,
    PY_SPARK_LOG_LEVEL_MAP,
)
from data_ingestion.utils import get_bucket_and_key_from_s3_url

logger = logging.getLogger(__name__)
logger.setLevel(PY_LOG_LEVEL)

MOON_SEARCH_QUERY = 'moon'
IMAGE_MEDIA_TYPE = 'image'
S3_IMAGES_OUTPUT_LOCATION = 'images'
S3_RECORDS_OUTPUT_LOCATION = 'records'

def make_nasa_api_search_request_and_get_json(page_id: int) -> dict:
    EMPTY_RESULT = []

    nasa_api_client = NasaImageApiClient(base_url=NASA_IMAGE_API_BASE_URL, api_key=NASA_API_KEY)
    try:
        response = nasa_api_client.make_get_request(
            NasaImageApiClient.NASA_IMAGE_API_SEARCH_ENDPOINT,
            query_params={
                'q': MOON_SEARCH_QUERY,
                'media_type': IMAGE_MEDIA_TYPE,
                'page': page_id,
                'page_size': NasaImageApiClient.DEFAULT_PAGE_SIZE
            }
        )
    except ApiException as e:
        return EMPTY_RESULT
    return response.json()['collection']['items']

def parse_nasa_image_api_search_hit(response_data: dict) -> dict:
    # get the image url
    image_href = [link['href'] for link in response_data['links'] if 'render' in link and link['render'] == 'image'][0]
    dt_format = '%Y-%m-%dT%H:%M:%SZ'
    date_created_dt = datetime.datetime.strptime(response_data['data'][0]['date_created'], dt_format).replace(tzinfo=datetime.timezone.utc)

    metadata = {
        'nasa_id': response_data['data'][0]['nasa_id'], 
        'title': response_data['data'][0]['title'],
        'date_created': date_created_dt,
        'description': response_data['data'][0]['description'],
        'image_href': image_href,
        'original_image_file_name': image_href.split('/')[-1],
        'image_file_extension': '.' + image_href.split('.')[-1]
    }
    return metadata

def download_bytes(url: str) -> bytes:
    api_client = BaseApiClient(url)
    response = api_client.make_get_request('')
    return response.content

def write_rows_to_s3(row_itr: Iterator[Row]):
    client = boto3.client("s3")
    for row in row_itr:
        bucket, key = get_bucket_and_key_from_s3_url(row.s3_url)
        client.put_object(Body=row.data, Bucket=bucket, Key=key)

NASA_IMAGE_API_PAGE_PARSED_SPARK_DF_SCHEMA = StructType([
    StructField("nasa_id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("date_created", TimestampType(), True),
    StructField("image_href", StringType(), True),
    StructField("original_image_file_name", StringType(), True),
    StructField("image_file_extension", StringType(), True)
])

def main() -> None:

    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel(PY_SPARK_LOG_LEVEL_MAP[PY_LOG_LEVEL])

    nasa_api_client = NasaImageApiClient(base_url=NASA_IMAGE_API_BASE_URL, api_key=NASA_API_KEY)

    # request one page of results to estimate the page count
    response = nasa_api_client.make_get_request(
        NasaImageApiClient.NASA_IMAGE_API_SEARCH_ENDPOINT,
        query_params={
            'q': MOON_SEARCH_QUERY,
            'media_type': IMAGE_MEDIA_TYPE,
            'page_size': 100
        }
    )

    # estimate number of pages to parallelize requests to the image api
    est_num_pages = nasa_api_client.estimate_number_pages_in_paginated_result(response)
    page_ids = list(range(1, est_num_pages + 1)) # pagination is 1-indexed
    pages_rdd = sc.parallelize(page_ids)

    logger.warning(f"Parallelizing NASA API requests over {est_num_pages} estimated response pages.")

    # perform the requests
    images_parsed_rdd = pages_rdd.map(lambda page_id: make_nasa_api_search_request_and_get_json(page_id)) \
        .flatMap(lambda x: x) \
        .map(lambda page_json: parse_nasa_image_api_search_hit(page_json))

    num_images = images_parsed_rdd.count()
    logger.warning(f"Retrieved {num_images} total images.")
    
    # convert to dataframe
    images_parsed_df = spark.createDataFrame(images_parsed_rdd, NASA_IMAGE_API_PAGE_PARSED_SPARK_DF_SCHEMA)

    # run udf to download images
    download_bytes_udf = udf(download_bytes, BinaryType())
    images_parsed_df = images_parsed_df.withColumn('image_bytes', download_bytes_udf(col("image_href")))

    # format the output url of the images
    images_prefix = 's3://' + os.path.join(S3_BUCKET_NAME, S3_KEY_PREFIX, S3_IMAGES_OUTPUT_LOCATION) + '/'
    logger.warning(f"Images will be uploaded to {images_prefix}")
    images_parsed_df = images_parsed_df.withColumn('image_s3_url', concat(lit(images_prefix), col('nasa_id'), col('image_file_extension')))

    # split images and records since they will be written separately
    images_df = images_parsed_df.select(col("image_s3_url").alias("s3_url"), col("image_bytes").alias("data"))
    records_df = images_parsed_df.select("nasa_id", "title", "description", "date_created", "image_href", "original_image_file_name", "image_s3_url")

    records_location = 's3://' + os.path.join(S3_BUCKET_NAME, S3_KEY_PREFIX, S3_RECORDS_OUTPUT_LOCATION)
    logger.warning(f"Metadata records will be uploaded to {records_location}")
    records_df.write.format("parquet").mode("Overwrite").save(records_location)

    images_df.foreachPartition(write_rows_to_s3)

if __name__ == "__main__":
    main()