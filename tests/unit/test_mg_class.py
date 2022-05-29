import ast

import pytest

from auto_pytest_mg.mg_class import MGClass


@pytest.fixture
def mg_class(mocker):
    definition = mocker.MagicMock()
    definition.name = "ClassName"
    return MGClass(definition=definition)


@pytest.fixture
def class_level_arg(mocker):
    class_level_arg = mocker.MagicMock(spec=ast.AnnAssign)
    class_level_arg.target = mocker.MagicMock(id="class_level_arg")
    return class_level_arg


class TestMGClass:
    def test__init__(self, mocker):
        definition = mocker.MagicMock()

        mg_class_ = MGClass(definition=definition)

        assert mg_class_.definition == definition

    def test_name(self, mg_class):
        assert mg_class.name == "ClassName"

    def test_mock_fixture_name(self, mg_class):
        assert mg_class.mock_fixture_name == "class_name"

    def test_arg_names__no_args(self, mg_class):
        mg_class.definition.body = []

        arg_names = mg_class.arg_names

        assert arg_names == []

    def test_arg_names__class_level_arg(self, mg_class, class_level_arg):
        mg_class.definition.body = [class_level_arg]

        arg_names = mg_class.arg_names

        assert arg_names == ["class_level_arg"]

    def test_arg_names__from__init__(self, mg_class, ast_init_function):
        mg_class.definition.body = [ast_init_function]

        arg_names = mg_class.arg_names

        assert arg_names == ["a"]

    def test_methods(self, mocker, mg_class, ast_method):
        not_a_method = mocker.MagicMock(spec=ast.AnnAssign)
        mg_class.definition.body = [ast_method, not_a_method]

        methods = mg_class.methods

        assert len(methods) == 1
        assert methods[0].name == "method"

    def test_get_fixture_text__no_arg_names(self, mg_class):
        fixture_text = mg_class.get_fixture_text()

        assert (
            fixture_text
            == """\
@pytest.fixture
def class_name(mocker):
    return ClassName()"""
        )

    def test_get_fixture_text__with_arg_names(self, mocker, mg_class):
        arg_1 = mocker.MagicMock(spec=ast.AnnAssign)
        arg_1.target = mocker.MagicMock(id="arg_1")
        arg_2 = mocker.MagicMock(spec=ast.AnnAssign)
        arg_2.target = mocker.MagicMock(id="arg_2")
        mg_class.definition.body = [arg_1, arg_2]

        fixture_text = mg_class.get_fixture_text()

        assert (
            fixture_text
            == """\
@pytest.fixture
def class_name(mocker):
    arg_1 = mocker.MagicMock()
    arg_2 = mocker.MagicMock()
    return ClassName(arg_1=arg_1, arg_2=arg_2)"""
        )

    def test_get_test_text__no_init(self, mg_class, ast_method):
        mg_class.definition.body = [ast_method]

        test_text = mg_class.get_test_text()

        assert (
            test_text
            == """\
class TestClassName:
    def test_method(self, mocker, mg, class_name):
        mg.generate_uut_mocks_with_asserts(class_name.method)

        result = class_name.method()"""
        )

    def test_get_test_text__with_init(self, mg_class, ast_init_function):
        mg_class.definition.body = [ast_init_function]

        test_text = mg_class.get_test_text()

        assert (
            test_text
            == """\
class TestClassName:
    def test__init__(self, mocker):
        a = mocker.MagicMock()

        class_name_ = ClassName(a=a)"""
        )
