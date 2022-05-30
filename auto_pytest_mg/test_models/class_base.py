from typing import List

import ast
from dataclasses import dataclass

from auto_pytest_mg import utils
from auto_pytest_mg.test_models.function_test_case import FunctionTestCase


@dataclass
class ClassBase:
    ast_definition: ast.ClassDef

    @property
    def class_name(self) -> str:
        return self.ast_definition.name

    @property
    def fixture_name(self) -> str:
        return utils.to_snake_case(self.class_name)

    @property
    def arg_names(self) -> List[str]:
        names = []
        for node in self.ast_definition.body:
            # Handle classes with class-level arguments (e.g. dataclasses)
            if isinstance(node, ast.AnnAssign):
                names.append(node.target.id)
            elif isinstance(node, ast.FunctionDef) and node.name == "__init__":
                names.extend(FunctionTestCase(node, None).arg_names)

        return names

    @property
    def class_instantiation(self) -> str:
        call_args = " ".join([f"{arg}={arg}," for arg in self.arg_names])
        call_args = call_args[:-1]  # remove trailing comma
        return f"{self.class_name}({call_args})"
