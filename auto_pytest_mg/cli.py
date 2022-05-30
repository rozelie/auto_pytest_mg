from typing import Optional

from pathlib import Path

import typer

from auto_pytest_mg import args, static
from auto_pytest_mg.args import UserArgs
from auto_pytest_mg.console import console
from auto_pytest_mg.test_generator import TestGenerator

app = typer.Typer(name="auto_pytest_mg", help=static.HELP_SUMMARY, add_completion=False)


@app.command(name="", help=static.HELP_SUMMARY)
def main(
    file_path: Path = args.FILE_PATH,
    project_path: Path = args.PROJECT_PATH,
    output_path: Optional[Path] = args.OUTPUT_PATH,
    use_default_unit_test_path: bool = args.USE_DEFAULT_UNIT_TEST_PATH,
) -> None:
    user_args = UserArgs(**locals())
    user_args.validate()
    test_generator = TestGenerator.from_file(
        file_path=user_args.file_path, project_path=user_args.project_path
    )
    _output_test(user_args, test_generator)


def _output_test(user_args: UserArgs, test_generator: TestGenerator) -> None:
    if user_args.output_path:
        test_generator.write_file(user_args.output_path)
    elif user_args.use_default_unit_test_path:
        unit_test_path = (
            user_args.project_path / "tests" / "unit" / f"test_{user_args.file_path.stem}.py"
        )
        test_generator.write_file(unit_test_path)
    else:
        console.print(test_generator.tests)
