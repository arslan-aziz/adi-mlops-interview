include .env

.PHONY=build,run,test

build:
	docker build -t adi_nasa_images .

run:
	docker run -it \
		-e NASA_API_KEY=${NASA_API_KEY} \
		-e S3_BUCKET_NAME=${S3_BUCKET_NAME} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e SEARCH_RESULT_SAMPLING_FACTOR=${SEARCH_RESULT_SAMPLING_FACTOR} \
		adi_nasa_images run

test:
	docker run -it \
		-e NASA_API_KEY=${NASA_API_KEY} \
		-e S3_BUCKET_NAME=${S3_BUCKET_NAME} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} adi_nasa_images test

shell:
	docker run -it \
		-e NASA_API_KEY=${NASA_API_KEY} \
		-e S3_BUCKET_NAME=${S3_BUCKET_NAME} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} adi_nasa_images

.env:
	touch .env
