from pathlib import Path

from auto_pytest_mg.mg_file_gen import _get_mg_test_file_path, write_mg_test_file

MODULE_PATH = f"auto_pytest_mg.mg_file_gen"


def test_write_mg_test_file(mocker):
    file_path = mocker.MagicMock()
    mock__generate_mg_test_file_text = mocker.patch(f"{MODULE_PATH}._generate_mg_test_file_text")
    mock__get_mg_test_file_path = mocker.patch(f"{MODULE_PATH}._get_mg_test_file_path")
    mock_console = mocker.patch(f"{MODULE_PATH}.console")

    write_mg_test_file(file_path)

    mock__generate_mg_test_file_text.assert_called_once_with(file_path)
    mock__get_mg_test_file_path.assert_called_once_with(file_path)
    mock__get_mg_test_file_path.return_value.write_text.assert_called_once_with(
        mock__generate_mg_test_file_text.return_value
    )
    mock_console.print.assert_called_once_with(
        f"Generated test file at [green]{mock__get_mg_test_file_path.return_value.absolute()}[/green]"
    )


def test__get_mg_test_file_path():
    file_path = Path("file.py")

    mg_test_file_path = _get_mg_test_file_path(file_path)

    assert file_path.parent == mg_test_file_path.parent
    assert mg_test_file_path.name == "test_file.py"
