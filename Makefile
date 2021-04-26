PYTHON = python

.PHONY: help
help:
	@echo "make build         # build docker image"
	@echo "make lint          # check linting"
	@echo "make flake8        # alias for `make lint`"
	@echo "make run           # run docker container
	@echo "make help          # show this help"

.PHONY: build
build:
	docker build -t bot .

.PHONY: run
run:
	docker run -e 'SECRET_TOKEN=$(token)' -t bot

.PHONY: lint
lint:
	$(PYTHON) -m flake8 -j1
	
.PHONY: flake8
flake8:
	$(PYTHON) -m flake8 -j1