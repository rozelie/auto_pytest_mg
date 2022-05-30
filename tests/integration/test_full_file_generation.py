from typing import Optional

import re
from dataclasses import dataclass

import pytest

from auto_pytest_mg.test_generator import TestGenerator

MODULE_PATH = f"auto_pytest_mg.test_generator"


@dataclass
class SourceText:
    input_text: str
    expected_text: str
    expected_import_re: Optional[str] = None
    expected_module_path_constant_re: Optional[str] = None


FUNCTION_NO_ARGS_SOURCE_TEXT = SourceText(
    input_text="""\
def function_no_args() -> None:
    ...
""",
    expected_text="""\
def test_function_no_args(mocker, mg):
    mg.generate_uut_mocks_with_asserts(function_no_args)

    result = function_no_args()
""",
    expected_import_re=r"from .*testing_file import function_no_args",
)

FUNCTION_WITH_ARGS_SOURCE_TEXT = SourceText(
    input_text="""\
def function_with_args(a, b) -> None:
    ...
""",
    expected_text="""\
def test_function_with_args(mocker, mg):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    mg.generate_uut_mocks_with_asserts(function_with_args)

    result = function_with_args(a=a, b=b)
""",
    expected_import_re=r"from .*testing_file import function_with_args",
)

CLASS_WITH_INIT_SOURCE_TEXT = SourceText(
    input_text="""\
class ClassWithInit:

    def __init__(self, a, b):
        self.a = a
        self.b = b
""",
    expected_text="""\
@pytest.fixture
def class_with_init(mocker):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    return ClassWithInit(a=a, b=b)


class TestClassWithInit:
    def test__init__(self, mocker):
        a = mocker.MagicMock()
        b = mocker.MagicMock()

        class_with_init_ = ClassWithInit(a=a, b=b)
""",
    expected_import_re=r"from .*testing_file import ClassWithInit",
)
DATACLASS_SOURCE_TEXT = SourceText(
    input_text="""\
@dataclass
class DataClass:
    a: str
    b: int

    @property
    def property_(self) -> None:
        ...

    def method(self) -> None:
        ...

    def method_with_args(self, a, b) -> None:
        ...

""",
    expected_text="""\
@pytest.fixture
def data_class(mocker):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    return DataClass(a=a, b=b)


class TestDataClass:
    def test__init__(self, mocker):
        a = mocker.MagicMock()
        b = mocker.MagicMock()

        data_class_ = DataClass(a=a, b=b)

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
""",
    expected_import_re=r"from .*testing_file import DataClass",
)

IMPORTS_STDLIB_TEXT = SourceText(
    input_text="""\
import sys
""",
    expected_text="",
    expected_module_path_constant_re=r'MODULE_PATH = ".*testing_file"',
)

IMPORTS_NON_STDLIB_TEXT = SourceText(
    input_text="""\
import requests
""",
    expected_text="""\
@pytest.fixture
def mock_requests(mocker):
    return mocker.patch(f"{MODULE_PATH}.requests")
""",
    expected_module_path_constant_re=r'MODULE_PATH = ".*testing_file"',
)


@pytest.mark.parametrize(
    ["source_text"],
    (
        [FUNCTION_NO_ARGS_SOURCE_TEXT],
        [FUNCTION_WITH_ARGS_SOURCE_TEXT],
        [CLASS_WITH_INIT_SOURCE_TEXT],
        [DATACLASS_SOURCE_TEXT],
        [IMPORTS_STDLIB_TEXT],
        [IMPORTS_NON_STDLIB_TEXT],
    ),
)
def test_input_and_expected_file_text(mocker, tmp_path, source_text):
    file_path = tmp_path / "testing_file.py"
    file_path.write_text(source_text.input_text)
    test_file_path = tmp_path / "test_testing_file.py"
    mocker.patch(f"{MODULE_PATH}.console")

    TestGenerator.from_file(file_path, file_path.parent).write_file(test_file_path)
    test_file_text = test_file_path.read_text()
    module_import_line = None
    module_path_constant_line = None
    for line in test_file_text.splitlines():
        if line.startswith("from"):
            module_import_line = line
        elif line.startswith("MODULE_PATH"):
            module_path_constant_line = line

    assert source_text.expected_text in test_file_text
    if source_text.expected_import_re and module_import_line:
        assert re.match(source_text.expected_import_re, module_import_line)
    if source_text.expected_module_path_constant_re and module_path_constant_line:
        assert re.match(source_text.expected_module_path_constant_re, module_path_constant_line)
