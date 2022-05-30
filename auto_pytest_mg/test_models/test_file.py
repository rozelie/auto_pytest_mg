"""Generates fixtures and test cases given a python file."""
from typing import Any, List

import ast
from dataclasses import dataclass
from pathlib import Path

from typer import Exit, prompt

from auto_pytest_mg import utils
from auto_pytest_mg.console import console
from auto_pytest_mg.static import LINES_BETWEEN_TOP_LEVEL_BLOCKS
from auto_pytest_mg.test_models.class_fixture import ClassFixture
from auto_pytest_mg.test_models.class_test_cases import ClassTestCases
from auto_pytest_mg.test_models.function_test_case import FunctionTestCase
from auto_pytest_mg.test_models.import_fixtures import ImportFixture, ImportFromFixtures


@dataclass
class TestFile:
    file_path: Path
    project_path: Path
    import_fixtures: List[ImportFixture]
    import_from_fixtures: List[ImportFromFixtures]
    class_fixtures: List[ClassFixture]
    class_test_cases: List[ClassTestCases]
    function_tests: List[FunctionTestCase]

    @classmethod
    def from_source_file(cls, file_path: Path, project_path: Path) -> "TestFile":
        ast_ = ast.parse(file_path.read_text())

        def _load_class_instances_for_ast_nodes(load_cls: Any, if_ast_cls: Any) -> List[Any]:
            return [load_cls(node) for node in ast_.body if isinstance(node, if_ast_cls)]

        return cls(
            file_path=file_path,
            project_path=project_path,
            import_fixtures=_load_class_instances_for_ast_nodes(ImportFixture, ast.Import),
            import_from_fixtures=_load_class_instances_for_ast_nodes(
                ImportFromFixtures, ast.ImportFrom
            ),
            class_fixtures=_load_class_instances_for_ast_nodes(ClassFixture, ast.ClassDef),
            class_test_cases=_load_class_instances_for_ast_nodes(ClassTestCases, ast.ClassDef),
            function_tests=_load_class_instances_for_ast_nodes(FunctionTestCase, ast.FunctionDef),
        )

    def write(self, file_path: Path) -> None:
        if file_path.exists():
            overwrite = prompt(
                f"File already exists at {file_path.absolute()} - overwrite it? [Y/n]"
            )
            if overwrite != "Y":
                console.print(f"[red]Exiting, will not overwrite the file.[/red]")
                raise Exit(0)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(self.file_text)
        console.print(f"Generated test file at [green]{file_path.absolute()}[/green]")

    @property
    def file_text(self) -> str:
        file_body = LINES_BETWEEN_TOP_LEVEL_BLOCKS.join(
            [
                self.import_lines,
                f'MODULE_PATH = "{self.dotted_module_path}"',
                *[i.fixture for i in self.import_fixtures if not utils.is_stdlib_module(i.name)],
                *[
                    i.fixtures
                    for i in self.import_from_fixtures
                    if not utils.is_stdlib_module(i.module)  # type: ignore
                ],
                *[c.fixture for c in self.class_fixtures],
                *[c.test_cases for c in self.class_test_cases],
                *[f.test_case for f in self.function_tests],
            ]
        )
        return f"{file_body}\n"

    @property
    def import_lines(self) -> str:
        all_function_and_class_names = [
            *[f.function_name for f in self.function_tests],
            *[c.class_name for c in self.class_test_cases],
        ]
        return (
            f"import pytest\n\n"
            f"from {self.dotted_module_path} import {', '.join(sorted(all_function_and_class_names))}"
        )

    @property
    def dotted_module_path(self) -> str:
        file_relative_to_project_root = self.file_path.absolute().relative_to(
            self.project_path.absolute()
        )
        module_path_parts = ".".join(file_relative_to_project_root.parts[:-1])
        module_name = self.file_path.stem.replace(".py", "")
        if module_path_parts:
            return f"{module_path_parts}.{module_name}"
        else:
            return module_name
