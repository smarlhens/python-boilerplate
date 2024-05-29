<p align="center">
  <a href="https://python-poetry.org/" target="blank"><img src="https://python-poetry.org/images/logo-origami.svg" height="100" alt="Poetry logo" /></a>
  <a href="https://pre-commit.com/" target="blank"><img src="https://pre-commit.com/logo.svg" height="100" alt="pre-commit logo" /></a>
  <a href="https://github.com/astral-sh/ruff" target="blank"><img src="https://raw.githubusercontent.com/astral-sh/ruff/8c20f14e62ddaf7b6d62674f300f5d19cbdc5acb/docs/assets/bolt.svg" height="100" alt="ruff logo" style="background-color: #ef5552" /></a>
  <a href="https://bandit.readthedocs.io/" target="blank"><img src="https://raw.githubusercontent.com/pycqa/bandit/main/logo/logo.svg" height="100" alt="bandit logo" /></a>
  <a href="https://docs.pytest.org/" target="blank"><img src="https://raw.githubusercontent.com/pytest-dev/pytest/main/doc/en/img/pytest_logo_curves.svg" height="100" alt="pytest logo" /></a>
</p>

<p align="center">
  <a href="https://docs.docker.com/" target="blank"><img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" height="60" alt="Docker logo" /></a>
  <a href="https://github.com/features/actions" target="blank"><img src="https://avatars.githubusercontent.com/u/44036562" height="60" alt="GitHub Actions logo" /></a>
</p>

# Python boilerplate

[![CodeQL](https://github.com/smarlhens/python-boilerplate/workflows/codeql/badge.svg)](https://github.com/smarlhens/python-boilerplate/actions/workflows/codeql.yml)
[![GitHub CI](https://github.com/smarlhens/python-boilerplate/workflows/ci/badge.svg)](https://github.com/smarlhens/python-boilerplate/actions/workflows/ci.yml)
[![GitHub license](https://img.shields.io/github/license/smarlhens/python-boilerplate)](https://github.com/smarlhens/python-boilerplate)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [What's in the box ?](#whats-in-the-box-)
- [Testing](#testing)
- [Docker](#docker)

---

## Prerequisites

- [Python](https://www.python.org/downloads/) **>=3.12 <3.13** (_tested with 3.12.3_)
- [pre-commit](https://pre-commit.com/#install)
- [poetry](https://python-poetry.org/docs/#installation) **>=1.2.2 <1.9** (_tested with 1.8.3_)
- [docker](https://docs.docker.com/get-docker/) (_optional_)

---

## Installation

1. Clone the git repository

   ```bash
   git clone https://github.com/smarlhens/python-boilerplate.git
   ```

2. Go into the project directory

   ```bash
   cd python-boilerplate/
   ```

3. Checkout working branch

   ```bash
   git checkout <branch>
   ```

4. Enable pre-commit hooks

   ```bash
   pre-commit install
   ```

---

## What's in the box ?

### Poetry

[Poetry](https://python-poetry.org/) is a tool for dependency management and packaging in Python. It allows you to
declare the libraries your project depends on and it will manage (install/update) them for you.

**pyproject.toml file** ([`pyproject.toml`](pyproject.toml)): orchestrate your project and its dependencies
**poetry.lock file** ([`poetry.lock`](poetry.lock)): ensure that the package versions are consistent for everyone
working on your project

For more configuration options and details, see the [configuration docs](https://python-poetry.org/docs/).

### pre-commit

[pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks.

**.pre-commit-config.yaml file** ([`.pre-commit-config.yaml`](.pre-commit-config.yaml)): describes what repositories and
hooks are installed

For more configuration options and details, see the [configuration docs](https://pre-commit.com/).

### ruff

[ruff](https://github.com/charliermarsh/ruff) is an extremely fast Python linter, written in Rust.

Rules are defined in the [`pyproject.toml`](pyproject.toml).

For more configuration options and details, see the [configuration docs](https://github.com/charliermarsh/ruff#configuration).

### mypy

[mypy](http://mypy-lang.org/) is an optional static type checker for Python that aims to combine the benefits of
dynamic (or "duck") typing and static typing.

Rules are defined in the [`pyproject.toml`](pyproject.toml).

For more configuration options and details, see the [configuration docs](https://mypy.readthedocs.io/).

### bandit

[bandit](https://bandit.readthedocs.io/) is a tool designed to find common security issues in Python code.

Rules are defined in the [`pyproject.toml`](pyproject.toml).

For more configuration options and details, see the [configuration docs](https://bandit.readthedocs.io/).

### docformatter

[docformatter](https://github.com/PyCQA/docformatter) is a tool designed to format docstrings to
follow [PEP 257](https://peps.python.org/pep-0257/).

Options are defined in the [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

---

## Testing

We are using [pytest](https://docs.pytest.org/) & [pytest-cov](https://github.com/pytest-dev/pytest-cov) to write tests.

To run tests:

```bash
poetry run pytest tests
```

<details>

<summary>Output</summary>

```text
collected 1 item

tests/test_myapplication.py::test_hello_world PASSED
```

</details>

To run tests with coverage:

```bash
poetry run pytest tests --cov=src
```

<details>

<summary>Output</summary>

```text
collected 1 item

tests/test_myapplication.py::test_hello_world PASSED

---------- coverage: platform linux, python 3.10.4-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
src/myapplication/__init__.py       1      0   100%
src/myapplication/main.py           6      2    67%
---------------------------------------------------
TOTAL                               7      2    71%
```

</details>

---

## Docker

### Build

To build the docker `production` image using [`Dockerfile`](Dockerfile):

```bash
docker build . -t my-python-application:latest
```

To build the docker `development` image using [`Dockerfile`](Dockerfile):

```bash
docker build . --target development -t my-python-application:dev
```

### Run

To run the python app example inside Docker:

```bash
docker run -it --rm my-python-application:latest # or :dev for development
```

<details>

<summary>Output</summary>

```text
Hello World
```

</details>

### Execute command inside container

```bash
docker run -it --rm my-python-application:latest bash
```

---
