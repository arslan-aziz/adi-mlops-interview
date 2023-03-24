import os
import logging

SEARCH_RESULT_SAMPLING_FACTOR = os.environ.get(
    "SEARCH_RESULT_SAMPLING_FACTOR", "1"
)
SEARCH_RESULT_SAMPLING_FACTOR = int(SEARCH_RESULT_SAMPLING_FACTOR)

NASA_IMAGE_API_BASE_URL = os.environ.get(
    "NASA_IMAGE_API_BASE_URL", "https://images-api.nasa.gov/"
)
NASA_API_KEY = os.environ.get("NASA_API_KEY", "")
if NASA_API_KEY == "":
    raise ValueError("Must set the NASA_API_KEY environment variable.")

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "")
if S3_BUCKET_NAME == "":
    raise ValueError("Must set the S3_BUCKET_NAME environment variable.")
S3_KEY_PREFIX = os.environ.get("S3_KEY_PREFIX", "moon_dataset")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
if AWS_SECRET_ACCESS_KEY == "" or AWS_ACCESS_KEY_ID == "":
    raise ValueError("Must set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID.")

__PY_LOG_LEVEL = os.environ.get("PY_LOG_LEVEL", "warning")
# convert to a logging enum
PY_LOG_LEVEL = logging.WARNING
if __PY_LOG_LEVEL.lower() == "critical":
    PY_LOG_LEVEL = logging.CRITICAL
elif __PY_LOG_LEVEL.lower() == "error":
    PY_LOG_LEVEL = logging.ERROR
elif __PY_LOG_LEVEL.lower() == "warning":
    PY_LOG_LEVEL = logging.WARNING
elif __PY_LOG_LEVEL.lower() == "info":
    PY_LOG_LEVEL = logging.INFO
elif __PY_LOG_LEVEL.lower() == "debug":
    PY_LOG_LEVEL = logging.DEBUG

# map python log levels to Spark log levels
PY_SPARK_LOG_LEVEL_MAP = {
    logging.CRITICAL: "FATAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARN",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
}
