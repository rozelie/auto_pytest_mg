# type: ignore[attr-defined]
from typing import List

import ast
from dataclasses import dataclass

import inflection

from auto_pytest_mg.mg_function import MGFunction
from auto_pytest_mg.static import INDENT


@dataclass
class MGClass:
    definition: ast.ClassDef

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def mock_fixture_name(self) -> str:
        return f"{inflection.underscore(self.name)}"

    @property
    def arg_names(self) -> List[str]:
        names = []
        for node in self.definition.body:
            # Handle classes with class-level arguments (e.g. dataclasses)
            if isinstance(node, ast.AnnAssign):
                names.append(node.target.id)
            elif isinstance(node, ast.FunctionDef) and node.name == "__init__":
                names.extend(MGFunction(node, None).arg_names)

        return names

    @property
    def methods(self) -> List[MGFunction]:
        return [
            MGFunction(method, parent_class=self)
            for method in self.definition.body
            if isinstance(method, ast.FunctionDef)
        ]

    def get_fixture_text(self) -> str:
        lines = [
            "@pytest.fixture",
            f"def {self.mock_fixture_name}(mocker):",
        ]
        if not self.arg_names:
            lines.append(f"{INDENT}return {self.name}()")
        else:
            for arg in self.arg_names:
                lines.append(f"{INDENT}{arg} = mocker.MagicMock()")
            call_args = [f"{arg}={arg}," for arg in self.arg_names]
            lines.extend(
                [
                    f"{INDENT}return {self.name}(",
                    *[f"{INDENT}{INDENT}{instance_var}" for instance_var in call_args],
                    f"{INDENT})",
                ]
            )

        return "\n".join(lines)

    def get_test_text(self) -> str:
        class_definition = f"class Test{self.name}:"
        method_lines = [method.get_method_test_text() for method in self.methods]
        method_lines_separated = "\n\n".join(method_lines)
        return "\n".join([class_definition, method_lines_separated])
