"""Provides an interface to generate mocked code blocks from ast.ClassDef."""
import ast
from dataclasses import dataclass

from auto_pytest_mg.static import INDENT
from auto_pytest_mg.test_models.class_base import ClassBase


@dataclass
class ClassFixture(ClassBase):
    """Generates mock data for ast.ClassDef."""

    ast_definition: ast.ClassDef

    @property
    def fixture(self) -> str:
        lines = ["@pytest.fixture", f"def {self.fixture_name}(mocker):"]
        if not self.arg_names:
            lines.append(f"{INDENT}return {self.class_name}()")
        else:
            for arg in self.arg_names:
                lines.append(f"{INDENT}{arg} = mocker.MagicMock()")

            lines.append(f"{INDENT}return {self.class_instantiation}")

        return "\n".join(lines)
