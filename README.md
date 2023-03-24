### Objective
This repo is a demonstration of a Spark application that reads images from the NASA
Image Search API (https://images-api.nasa.gov/) and stores them in an S3 bucket.

The application is containerized with Docker for the sake of portability.

### Usage
The application requires several environment variables to run.
The environment variables can be supplied by creating a .env file at the root of this repo 
where each line is a pair `key=value`.

Use the provided Makefile to interact with this repo:
- `make build`: Build the Docker image.
- `make test`: Run unit tests.
- `make run`: Run the Spark application.
