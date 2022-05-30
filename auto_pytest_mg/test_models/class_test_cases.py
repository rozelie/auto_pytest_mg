"""Provides an interface to generate mocked code blocks from ast.ClassDef."""
from typing import List, Optional

import ast
from dataclasses import dataclass

from auto_pytest_mg.static import INDENT
from auto_pytest_mg.test_models.class_base import ClassBase
from auto_pytest_mg.test_models.function_test_case import FunctionTestCase


@dataclass
class ClassTestCases(ClassBase):
    """Generates mock data for ast.ClassDef."""

    ast_definition: ast.ClassDef

    @property
    def test_cases(self) -> str:
        class_definition = f"class Test{self.class_name}:"
        method_lines = []
        if self.__init__test:
            method_lines.append(self.__init__test)

        method_lines.extend(
            [method.test_case for method in self.methods if not method.function_name == "__init__"]
        )
        method_lines_separated = "\n\n".join(method_lines)
        return "\n".join([class_definition, method_lines_separated])

    @property
    def methods(self) -> List[FunctionTestCase]:
        return [
            FunctionTestCase(method, parent_class=self)
            for method in self.ast_definition.body
            if isinstance(method, ast.FunctionDef)
        ]

    @property
    def __init__test(self) -> Optional[str]:
        if not self.arg_names:
            return None

        function_definition = f"{INDENT}def test__init__(self, mocker):"
        arg_mocks = [f"{INDENT * 2}{arg_name} = mocker.MagicMock()" for arg_name in self.arg_names]
        class_instantiation = f"{INDENT * 2}{self.fixture_name}_ = {self.class_instantiation}"
        return "\n".join([function_definition, *arg_mocks, "", class_instantiation])
