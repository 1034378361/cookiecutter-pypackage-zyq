#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""

import pytest

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_version():
    """Test version import."""
    from {{ cookiecutter.project_slug }} import __version__
    assert __version__
