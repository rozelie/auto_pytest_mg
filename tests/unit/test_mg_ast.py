import pytest

from auto_pytest_mg.mg_ast import MGAST

MODULE_PATH = "auto_pytest_mg.mg_ast"


@pytest.fixture
def mock_console(mocker):
    mock_console_ = mocker.patch(f"{MODULE_PATH}.console")
    return mock_console_


@pytest.fixture
def mgast(mocker, tmp_path):
    file_path = tmp_path
    functions = mocker.MagicMock()
    classes = mocker.MagicMock()
    imports = mocker.MagicMock()
    imports_from = mocker.MagicMock()
    return MGAST(
        file_path=file_path,
        functions=functions,
        classes=classes,
        imports=imports,
        imports_from=imports_from,
    )


class TestMGAST:
    def test_from_file(
        self, mocker, mg, mgast, ast_import, ast_import_from, ast_class, ast_function
    ):
        file_path = mocker.MagicMock()
        mock_parse = mocker.patch(f"{MODULE_PATH}.ast.parse")
        mock_parse.return_value.body = [ast_import, ast_import_from, ast_class, ast_function]
        mg.generate_uut_mocks_with_asserts(mgast.from_file)

        mgast_ = mgast.from_file(file_path=file_path)

        assert mgast_.file_path == file_path
        assert len(mgast_.imports) == 1
        assert len(mgast_.imports_from) == 1
        assert len(mgast_.classes) == 1
        assert len(mgast_.functions) == 1

    def test_write_mg_test_file(self, mocker, mg, mgast, mock_console):
        mgast.write_mg_test_file()

        assert mgast.mg_test_file_path.read_text() == mgast.mg_test_file_text
        mock_console.print.assert_called_once_with(
            f"Generated test file at [green]{mgast.mg_test_file_path.absolute()}[/green]"
        )
