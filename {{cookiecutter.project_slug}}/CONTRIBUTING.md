# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

{{ cookiecutter.project_name }} could always use more documentation, whether as part of the official {{ cookiecutter.project_name }} docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `{{ cookiecutter.project_slug }}` for local development.

1. Fork the `{{ cookiecutter.project_slug }}` repo on GitHub.
2. Clone your fork locally:
   ```bash
   git clone git@github.com:your_name_here/{{ cookiecutter.project_slug }}.git
   ```

3. Ensure you have Poetry installed. If not, install it:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Install your local copy and development dependencies:
   ```bash
   cd {{ cookiecutter.project_slug }}/
   poetry install --with dev
   ```

5. Create a branch for local development:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the quality checks and tests:
   ```bash
   poetry run make lint
   poetry run make test
   # Or run tests for all Python environments
   poetry run make test-all
   ```

7. Commit your changes and push your branch to GitHub:
   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```
   请遵循我们的[提交消息规范](./COMMIT_CONVENTION.md)，以确保变更日志能够正确生成。

8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python {{ cookiecutter.python_version }} and above. Check the GitHub Actions workflow results for your PR to ensure tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```bash
poetry run pytest tests/test_specific_feature.py
```

## Deploying

A reminder for the maintainers on how to deploy. Make sure all your changes are committed (including an entry in CHANGELOG.md). Then run:

```bash
poetry version patch  # possible: major / minor / patch / etc.
git commit -am "Bump version"
git tag v$(poetry version -s)
git push
git push --tags
```

GitHub Actions will then deploy to PyPI if tests pass.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
