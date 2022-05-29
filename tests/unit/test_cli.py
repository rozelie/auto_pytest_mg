from auto_pytest_mg.cli import main, version_callback

MODULE_PATH = "auto_pytest_mg.cli"


def test_version_callback(mocker):
    print_version = mocker.MagicMock()
    mock_print = mocker.patch(f"{MODULE_PATH}.console.print")
    mock_version = mocker.patch(f"{MODULE_PATH}.version")
    sys_exit = mocker.patch(f"{MODULE_PATH}.sys.exit")

    version_callback(print_version)

    mock_print.assert_called_once_with(
        f"[yellow]auto_pytest_mg[/] version: [bold blue]{mock_version}[/]"
    )
    sys_exit.assert_called_once()


def test_main(mocker, tmp_path):
    file_path = tmp_path
    print_version = mocker.MagicMock()
    mock_mgast = mocker.patch(f"{MODULE_PATH}.mg_ast.MGAST")
    mocker.patch(f"{MODULE_PATH}.app.command")

    main(file_path, print_version)

    mock_mgast.from_file.assert_called_once_with(file_path)
    mock_mgast.from_file.return_value.write_mg_test_file.assert_called_once()
