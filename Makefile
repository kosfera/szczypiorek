#
# Makefile
#
SHELL := /bin/bash

help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'



#
# DEVELOPMENT
#
.PHONY: venv
venv:
	poetry shell

.PHONY: install
install:
	poetry install

.PHONY: lint
lint:  ## lint the cosphere_api & tests
	echo -n '\n[CHECKER] check if code fulfills quality criteria\n'
	flake8 --ignore N818,D100,D101,D102,D103,D104,D105,D106,D107,D202,D204,W504,W606 tests && \
	flake8 --ignore N818,D100,D101,D102,D103,D104,D105,D106,D107,D202,D204,W504,W606 szczypiorek



#
# TESTS
#
.PHONY: test
test:  ## run selected tests
	py.test --cov=./szczypiorek --cov-fail-under=90 -r w -s -vv $(tests)

.PHONY: test_all
test_all:  ## run all available tests
	py.test --cov=./szczypiorek --cov-fail-under=90 -r w -s -vv tests

.PHONY: coverage
coverage:  # render html coverage report
	coverage html -d coverage_html && google-chrome coverage_html/index.html



#
# DEPLOYMENT
#
deploy_to_pypi:
	poetry publish --build
