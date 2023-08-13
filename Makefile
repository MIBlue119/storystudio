.DEFAULT_GOAL := help
.PHONY:  install lint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install requirements
	pip install poetry
	poetry install

lint: ## lint the repo with blackformatter/isot
	black .
	isort .