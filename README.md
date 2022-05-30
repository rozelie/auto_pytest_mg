# auto_pytest_mg (Automatic pytest Mock Generator)

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/auto_pytest_mg.svg)](https://pypi.org/project/auto_pytest_mg/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage Report](assets/images/coverage.svg)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/rozelie/auto_pytest_mg/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![GitHub](https://img.shields.io/badge/GitHub%20-58a6ff.svg)](https://github.com/psf/black)
[![PyPi](https://img.shields.io/badge/PyPi%20-003d61.svg)](https://pypi.org/project/auto-pytest-mg/)
</div>


auto_pytest_mg generates a test skeleton for a given python file. This skeleton includes:
- fixtures that mock all non-standard library imported names
- a boilerplate test for every class method and property
- a boilerplate test for every function
- `mocker` and `mg` fixtures for all tests
  - `mocker`: [pytest-mock](https://pypi.org/project/pytest-mock/)
  - `mg`: [pytest-mocker-generator](https://github.com/pksol/pytest-mock-generator) 
    - If you're unfamiliar with pytest-mock-generator, you can read up on usage information in their [README](https://github.com/pksol/pytest-mock-generator#readme).


It is not auto_pytest_mg's goal to produce the entirety of the test. The creation of test mocks and 
asserts is delegated to pytest-mocker-generator via the `mg` fixture and the 
`mg.generate_uut_mocks_with_asserts(...)` call.

This package is a static analysis tool and will not execute any of your code.


## Usage
```bash
# install the package
pip install auto_pytest_mg

# go to project's source root
cd my_project

# pass the file to generate tests for
auto_pytest_mg my_project/my_file.py
```

# Example

Source file located at `my_project/my_file.py`
```python
# my_project/my_file.py
import requests

class MyClass:

    def __init__(self, a: int):
        self.a = a

    def method(self) -> int:
        return self.a


def get(url: str) -> requests.Response:
    return requests.get(url)
```

Running `auto_pytest_mg my_project/my_file.py` will then output to stdout the generated test file:

```python
import pytest

from my_project.my_file import get, MyClass


MODULE_PATH = "my_project.my_file"


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch(f"{MODULE_PATH}.requests")



@pytest.fixture
def my_class(mocker):
    a = mocker.MagicMock()
    return MyClass(a=a)


class TestMyClass:
    def test__init__(self, mocker):
        a = mocker.MagicMock()

        my_class_ = MyClass(a=a)

    def test_method(self, mocker, mg, my_class):
        mg.generate_uut_mocks_with_asserts(my_class.method)

        result = my_class.method()


      
def test_get(mocker, mg):
    url = mocker.MagicMock()
    mg.generate_uut_mocks_with_asserts(get)

    result = get(url=url)
```

## Similar packages
- [pyguin](https://pynguin.readthedocs.io/en/latest/)
  - Executes given source code and uses a genetic algorithm to produce test cases
  - Can output to unittest/pytest test styles
- [pythoscope](https://github.com/mkwiatkowski/pythoscope)
  - Last updated in 2016
  - Performs static analysis, does not run your code.
  - Outputs unittest test style only

## Development
See [DEVELOPMENT.md](./DEVELOPMENT.md)


## License

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/rozelie/auto_pytest_mg/blob/master/LICENSE) for more details.


## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
