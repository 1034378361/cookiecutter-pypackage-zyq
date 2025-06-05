.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 \
	changelog changelog-init docker docker-build docker-run docker-clean

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## run linters
	ruff check src tests
	ruff format --check src tests
	black --check src tests
	isort --check src tests
	mypy src
	# 检查调试语句
	! grep -r "import pdb" src tests
	! grep -r "breakpoint()" src tests
	# 检查合并冲突
	! grep -r "<<<<<<< HEAD" src tests docs

format: ## format code
	ruff format src tests
	black src tests
	isort src tests

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
	coverage report -m --fail-under=85
	coverage html
{%- endif %}
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/{{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python -m build
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	pip install -e .

dev-install: clean ## install the package and development dependencies
	pip install -e ".[dev]"

changelog: ## 从最新标签开始生成CHANGELOG
	python scripts/generate_changelog.py --config .changelog.yml --verbose

changelog-init: ## 生成完整项目历史的CHANGELOG
	python scripts/generate_changelog.py --since $(shell git rev-list --max-parents=0 HEAD) --config .changelog.yml --verbose

{% if cookiecutter.include_docker == 'y' %}
docker: docker-build ## alias for docker-build

docker-build: ## build Docker image
	bash scripts/docker-build.sh latest

docker-build-%: ## build Docker image with specific tag (make docker-build-1.0.0)
	bash scripts/docker-build.sh $*

docker-run: ## run Docker container
	bash scripts/docker-run.sh latest

docker-run-%: ## run Docker container with specific tag (make docker-run-1.0.0)
	bash scripts/docker-run.sh $*

docker-clean: ## remove Docker images for this project
	docker images | grep {{cookiecutter.project_slug}} | awk '{print $$3}' | xargs -r docker rmi
{% endif %}
