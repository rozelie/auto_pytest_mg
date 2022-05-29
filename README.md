# auto_pytest_mg (Automatic pytest Mock Generator)

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/auto_pytest_mg.svg)](https://pypi.org/project/auto_pytest_mg/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/rozelie/auto_pytest_mg/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage Report](assets/images/coverage.svg)
</div>

- GitHub: [https://github.com/rozelie/auto_pytest_mg](https://github.com/rozelie/auto_pytest_mg)
- GitHub Releases: [https://github.com/rozelie/auto_pytest_mg/releases](https://github.com/rozelie/auto_pytest_mg/releases)
- PyPi: [https://pypi.org/project/auto-pytest-mg/](https://pypi.org/project/auto-pytest-mg/)

auto_pytest_mg parses the AST of an input python file to generate a new test file with boilerplate
test functions. Rendered tests include the `mocker` and `mg` fixtures which are available via the 
[pytest-mock](https://pypi.org/project/pytest-mock/) and [pytest-mocker-generator](https://pypi.org/project/pytest-mock-generator/) 
packages, respectively.  


## Usage
```bash
# install the package
pip install auto_pytest_mg

# go to project's source root
cd my_project

# pass the file to generate tests for
auto_pytest_mg my_project/my_file.py
```

## Example

Source file located at `my_project/my_file.py`
```python
# my_project/my_file.py
from dataclasses import dataclass


@dataclass
class DataClass:
    a: str
    b: int

    @property
    def property_(self) -> None:
        ...

    def method(self) -> None:
        ...

    def method_with_args(self, a: int, b: str) -> None:
        ...

def a_function():
    ...
```

Running `auto_pytest_mg my_project/my_file.py` then generates `my_project/test_my_file.py`:

```python
# my_project/test_my_file.py
import pytest

from my_project.my_file import a_function, DataClass


@pytest.fixture
def data_class(mocker):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    return DataClass(a=a, b=b)


class TestDataClass:
    def test__init__(self, mocker):
        a = mocker.MagicMock()
        b = mocker.MagicMock()

        return DataClass(a=a, b=b)

    def test_property_(self, mocker, mg, data_class):
        mg.generate_uut_mocks_with_asserts(data_class.property_)

        result = data_class.property_

    def test_method(self, mocker, mg, data_class):
        mg.generate_uut_mocks_with_asserts(data_class.method)

        result = data_class.method()

    def test_method_with_args(self, mocker, mg, data_class):
        a = mocker.MagicMock()
        b = mocker.MagicMock()
        mg.generate_uut_mocks_with_asserts(data_class.method_with_args)

        result = data_class.method_with_args(a=a, b=b)


def test_a_function(mocker, mg):
    mg.generate_uut_mocks_with_asserts(a_function)

    result = a_function()
```

# Development

## Makefile usage

[`Makefile`](https://github.com/rozelie/auto_pytest_mg/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make format
```

Codestyle checks only, without rewriting files:

```bash
make check-format
```

> Note: `check-format` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-format && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/rozelie/auto_pytest_mg/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## Build and Release

Building a new version of the application contains steps:

1. Bump the version of your package `poetry version {(major|minor|patch)}`
1. `git add pyproject.toml`
1. Commit and push `git commit -m "Updating to version: v{version}"`
1. Create a release on GitHub
1. `poetry publish --build`


## 🛡 License

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/rozelie/auto_pytest_mg/blob/master/LICENSE) for more details.


## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
