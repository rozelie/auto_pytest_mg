from typing import Optional

from dataclasses import dataclass
from pathlib import Path

from typer import Argument, Exit, Option

from auto_pytest_mg.console import console


@dataclass
class UserArgs:
    file_path: Path
    project_path: Path
    output_path: Optional[Path]
    use_default_unit_test_path: bool

    def validate(self) -> None:
        if self.output_path and self.use_default_unit_test_path:
            console.print(
                "[red]Can use only one of '-o/--output-path' and '-u/--use-default-unit-test-path'[/red]"
            )
            raise Exit(1)


FILE_PATH = Argument(..., help="Python file path to generate test file for.")
PROJECT_PATH = Option(
    Path().cwd(),
    "-p",
    "--project-path",
    help="Path to the project's root directory (defaults to cwd).",
)
OUTPUT_PATH = Option(
    None,
    "-o",
    "--output-path",
    help="Path to write the generated file to.",
)
USE_DEFAULT_UNIT_TEST_PATH = Option(
    False,
    "-u",
    "--use-default-unit-test-path",
    help="Write the test file to <PROJECT_PATH>/tests/unit/test_<FILE_NAME>.py.",
)
