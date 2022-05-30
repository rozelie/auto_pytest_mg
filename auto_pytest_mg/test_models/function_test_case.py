"""Generates a test case given ast.FunctionDef."""
from typing import TYPE_CHECKING, List, Optional

import ast
from dataclasses import dataclass

from auto_pytest_mg.static import INDENT

if TYPE_CHECKING:
    from auto_pytest_mg.test_models.class_fixture import MockedClass


@dataclass
class FunctionTestCase:
    """Generates a test case given ast.FunctionDef.

    If provided with a parent class, the function is assumed to be a method.
    """

    ast_definition: ast.FunctionDef
    parent_class: Optional["MockedClass"] = None

    @property
    def function_name(self) -> str:
        """The function's name."""
        return self.ast_definition.name

    @property
    def arg_names(self) -> List[str]:
        """Get the function's argument names."""
        return [arg.arg for arg in self.ast_definition.args.args if arg.arg not in {"self", "cls"}]

    @property
    def test_case(self) -> str:
        """Generated test case."""
        return f"{self.test_definition}\n{self.test_body}"

    @property
    def test_definition(self) -> str:
        """The test's definition."""
        if self.is_method:
            return f"{INDENT}def test_{self.function_name}(self, mocker, mg, {self.parent_class.fixture_name}):"  # type: ignore

        return f"def test_{self.function_name}(mocker, mg):"

    @property
    def test_body(self) -> str:
        """The test's body."""
        if self.is_method:
            watched_object = f"{self.parent_class.fixture_name}.{self.function_name}"  # type: ignore
            indent = INDENT * 2
        else:
            watched_object = self.function_name
            indent = INDENT

        return "\n".join(
            [
                f"{indent}{line}" if line else ""
                for line in [
                    *self.arrange_variables,
                    f"mg.generate_uut_mocks_with_asserts({watched_object})",
                    "",
                    self.function_call,
                ]
            ]
        )

    @property
    def is_method(self) -> bool:
        """Determines if this function is a method."""
        return self.parent_class is not None

    @property
    def is_property(self) -> bool:
        """Determines if this function is a property."""
        for decorator in self.ast_definition.decorator_list:
            try:
                if decorator.id in {"property", "cached_property"}:
                    return True
            except AttributeError:
                continue

        return False

    @property
    def arrange_variables(self) -> List[str]:
        """The arrange variables mocking out all function arguments."""
        return [f"{arg_name} = mocker.MagicMock()" for arg_name in self.arg_names]

    @property
    def function_call(self) -> str:
        """The function call of the test."""
        if self.is_method:
            watched_obj = f"{self.parent_class.fixture_name}.{self.function_name}"  # type: ignore
        else:
            watched_obj = self.function_name

        call_args = " ".join([f"{arg}={arg}," for arg in self.arg_names])
        call_args = call_args[:-1]  # remove trailing comma
        function_call = "" if self.is_property else f"({call_args})"
        return f"result = {watched_obj}{function_call}"
