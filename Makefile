.DEFAULT_GOAL := build
.PHONY: build publish package coverage test lint docs
PROJ_SLUG = survey_analysis
CLI_NAME = survey_analysis
LINTER = flakehell lint
SHELL = bash

build:
	poetry build

run:
	$(CLI_NAME) run

submit:
	$(CLI_NAME) submit

freeze:
	poetry export --without-hashes -o requirements.txt

lint:
	# Sort the python import statements
	$(LINTER) $(PROJ_SLUG)

test: lint
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/

quicktest:
	py.test --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

docs: coverage
	mkdir -p docs/source/_static
	mkdir -p docs/source/_templates
	cd docs && $(MAKE) html
	

answers:
	cd docs && $(MAKE) html
	xdg-open docs/build/html/index.html

package: clean docs
	poetry build

publish: package
	poetry publish

clean :
	rm -rf dist \
	rm -rf docs/build \
	rm -rf *.egg-info
	coverage erase

reformat:
	isort .
	black .
