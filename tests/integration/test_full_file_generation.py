# type: ignore[attr-defined]
from dataclasses import dataclass

import pytest

from auto_pytest_mg.mg_file_gen import write_mg_test_file

MODULE_PATH = f"auto_pytest_mg.mg_file_gen"


@dataclass
class SourceText:
    input_text: str
    expected_text: str


FUNCTION_NO_ARGS_SOURCE_TEXT = SourceText(
    input_text="""\
def function_no_args() -> None:
    ...
""",
    expected_text="""\
import pytest

from testing_file import function_no_args


def test_function_no_args(mocker, mg):
    mg.generate_uut_mocks_with_asserts(function_no_args)

    result = function_no_args()
""",
)

FUNCTION_WITH_ARGS_SOURCE_TEXT = SourceText(
    input_text="""\
def function_with_args(a, b) -> None:
    ...
""",
    expected_text="""\
import pytest

from testing_file import function_with_args


def test_function_with_args(mocker, mg):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    mg.generate_uut_mocks_with_asserts(function_with_args)

    result = function_with_args(a, b)
""",
)

CLASS_WITH_INIT_SOURCE_TEXT = SourceText(
    input_text="""\
class ClassWithInit:

    def __init__(self, a, b):
        self.a = a
        self.b = b
""",
    expected_text="""\
import pytest

from testing_file import ClassWithInit


@pytest.fixture
def class_with_init(mocker):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    return ClassWithInit(
        a=a,
        b=b,
    )


class TestClassWithInit:
    def test__init__(self, mocker):
        a = mocker.MagicMock()
        b = mocker.MagicMock()

        class_with_init = ClassWithInit(
            a=a,
            b=b,
        )
""",
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
import pytest

from testing_file import DataClass


@pytest.fixture
def data_class(mocker):
    a = mocker.MagicMock()
    b = mocker.MagicMock()
    return DataClass(
        a=a,
        b=b,
    )


class TestDataClass:
    def test__init__(self, mocker):
        a = mocker.MagicMock()
        b = mocker.MagicMock()

        data_class = DataClass(
            a=a,
            b=b,
        )

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

        result = data_class.method_with_args(a, b)
""",
)


@pytest.mark.parametrize(
    ["source_text"],
    (
        [FUNCTION_NO_ARGS_SOURCE_TEXT],
        [FUNCTION_WITH_ARGS_SOURCE_TEXT],
        [CLASS_WITH_INIT_SOURCE_TEXT],
        [DATACLASS_SOURCE_TEXT],
    ),
)
def test_input_and_expected_file_text(mocker, tmp_path, source_text):
    file_path = tmp_path / "testing_file.py"
    file_path.write_text(source_text.input_text)
    test_file_path = tmp_path / "test_testing_file.py"
    mocker.patch(f"{MODULE_PATH}._get_mg_test_file_path", return_value=test_file_path)
    mocker.patch(f"{MODULE_PATH}.logger.info")

    write_mg_test_file(file_path)
    nice = test_file_path.read_text()

    assert test_file_path.read_text() == source_text.expected_text