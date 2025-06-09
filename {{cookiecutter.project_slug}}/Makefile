{% if cookiecutter.package_manager == "Poetry" %}
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint \
	changelog changelog-init docker docker-build docker-run docker-clean poetry-install

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
	poetry run ruff check src tests
	poetry run ruff format --check src tests
	poetry run black --check src tests
	poetry run isort --check src tests
	poetry run mypy src
	# 检查调试语句
	! grep -r "import pdb" src tests
	! grep -r "breakpoint()" src tests
	# 检查合并冲突
	! grep -r "<<<<<<< HEAD" src tests docs

format: ## format code
	poetry run ruff format src tests
	poetry run black src tests
	poetry run isort src tests

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	poetry run pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	poetry run python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	poetry run tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	poetry run pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	poetry run coverage run --source {{ cookiecutter.project_slug }} -m pytest
	poetry run coverage report -m --fail-under=85
	poetry run coverage html
{%- endif %}
	$(BROWSER) htmlcov/index.html

docs: ## generate MkDocs documentation
	poetry run mkdocs build
	$(BROWSER) site/index.html

servedocs: ## serve documentation locally with live reload
	poetry run mkdocs serve

release: dist ## package and upload a release
	poetry publish

dist: clean ## builds source and wheel package
	poetry build
	ls -l dist

install: clean ## install the package
	poetry install

dev-install: clean ## install the package and development dependencies
	poetry install --with dev

poetry-install: ## install Poetry if it's not installed
	curl -sSL https://install.python-poetry.org | python3 -

changelog: ## 从最新标签开始生成CHANGELOG
	poetry run python scripts/generate_changelog.py --config .changelog.yml --verbose

changelog-init: ## 生成完整项目历史的CHANGELOG
	poetry run python scripts/generate_changelog.py --since $(shell git rev-list --max-parents=0 HEAD) --config .changelog.yml --verbose

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
{% else %}
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint \
	changelog changelog-init docker docker-build docker-run docker-clean pdm-install

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
	pdm run ruff check src tests
	pdm run ruff format --check src tests
	pdm run black --check src tests
	pdm run isort --check src tests
	pdm run mypy src
	# 检查调试语句
	! grep -r "import pdb" src tests
	! grep -r "breakpoint()" src tests
	# 检查合并冲突
	! grep -r "<<<<<<< HEAD" src tests docs

format: ## format code
	pdm run ruff format src tests
	pdm run black src tests
	pdm run isort src tests

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	pdm run pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	pdm run python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	pdm run tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	pdm run pytest --cov=src --cov-report=term --cov-report=html --cov-fail-under=85
{%- else %}
	pdm run coverage run --source {{ cookiecutter.project_slug }} -m pytest
	pdm run coverage report -m --fail-under=85
	pdm run coverage html
{%- endif %}
	$(BROWSER) htmlcov/index.html

docs: ## generate MkDocs documentation
	pdm run mkdocs build
	$(BROWSER) site/index.html

servedocs: ## serve documentation locally with live reload
	pdm run mkdocs serve

release: dist ## package and upload a release
	pdm publish

dist: clean ## builds source and wheel package
	pdm build
	ls -l dist

install: clean ## install the package
	pdm install

dev-install: clean ## install the package and development dependencies
	pdm install --dev

pdm-install: ## install PDM if it's not installed
	python -m pip install --user pdm

changelog: ## 从最新标签开始生成CHANGELOG
	pdm run python scripts/generate_changelog.py --config .changelog.yml --verbose

changelog-init: ## 生成完整项目历史的CHANGELOG
	pdm run python scripts/generate_changelog.py --since $(shell git rev-list --max-parents=0 HEAD) --config .changelog.yml --verbose

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
{% endif %}
