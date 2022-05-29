import ast

import pytest


@pytest.fixture
def ast_import(mocker):
    import_ = mocker.MagicMock(spec=ast.Import)
    import_alias = mocker.MagicMock(spec=ast.alias)
    import_alias.name = "a_module"
    import_.names = [import_alias]
    return import_


@pytest.fixture
def ast_import_from(mocker):
    import_from = mocker.MagicMock(spec=ast.ImportFrom)
    import_from_alias = mocker.MagicMock(spec=ast.alias)
    import_from_alias.name = "from_a_module"
    import_from.names = [import_from_alias]
    return import_from


@pytest.fixture
def ast_class(mocker):
    class_ = mocker.MagicMock(spec=ast.ClassDef)
    class_.name = "class"
    class_.args = mocker.MagicMock()
    class_.args.args = []
    class_.decorator_list = []
    return class_


@pytest.fixture
def ast_function(mocker):
    function = mocker.MagicMock(spec=ast.FunctionDef)
    function.name = "function"
    function.args = mocker.MagicMock()
    function.args.args = []
    function.decorator_list = []
    return function


@pytest.fixture
def ast_init_function(mocker, ast_function):
    ast_function.name = "__init__"
    ast_function.args.args = [mocker.MagicMock(arg="self"), mocker.MagicMock(arg="a")]
    return ast_function


@pytest.fixture
def ast_method(ast_function):
    ast_function.name = "method"
    return ast_function
