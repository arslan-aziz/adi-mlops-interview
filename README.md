### Objective
This repo is a demonstration of a Spark application that reads images from the NASA
Image Search API (https://images-api.nasa.gov/) and stores them in an S3 bucket.

The application is containerized with Docker for the sake of portability.

### Usage
The application requires several environment variables to run.
The environment variables can be supplied by creating a .env file at the root of this repo 
where each line is a pair `key=value`.
- S3_BUCKET_NAME: Name of S3 bucket to store results.
- AWS_ACCESS_KEY_ID: AWS access key id credential.
- AWS_SECRET_ACCESS_KEY: AWS secret access key credential.
- NASA_API_KEY: API key for the NASA data APIs.
- SEARCH_RESULT_SAMPLING_FACTOR: Factor downsample the results pulled from the NASA API.
    The NASA APIs are rate-limited to 1000 requests per hour. Try increasing this
    parameter if errors occur due to excessive request retries.

Use the provided Makefile to interact with this repo:
- `make build`: Build the Docker image.
- `make test`: Run unit tests.
- `make run`: Run the Spark application.
- `make shell`: Drop into an interactive bash shell in the container (for debugging purposes).

### Assumptions and Approach
This application is a data pipeline that assumes the following
- The only source being ingested is the NASA Image API.
- The relevant query is for "moon" images. Although it is trivial to 
    expand this application to take the search query as a runtime argument.
- The output of the pipeline is metadata and images written to S3 to support a ML workflow.

The pipeline was implemented using Spark to demonstrate scalability for uses cases
where the data sizes per batch job can vary greatly.

The application is Dockerized for portability and a Makefile is provided for ease of use.

In implementing the pipeline, care was taken to abstract business logic from the Spark
DSL so that unit testing was simplified. Custom logging was implemented to output
intermediate statuses to the console as the pipeline runs.
