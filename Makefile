IMAGE ?= timezones

docker_build:
	docker build . --tag "${IMAGE}"

run_service:
	docker container run -p 8000:8000 ${IMAGE}

lint_typecheck:
	docker run -v ./src:/app/src ${IMAGE} pylint src/ &
	docker run -v ./src:/app/src ${IMAGE} mypy src/
