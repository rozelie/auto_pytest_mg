"""Generates fixtures for given ast.Import or ast.ImportFrom."""
from typing import List, Optional

import ast
from dataclasses import dataclass

from auto_pytest_mg import utils
from auto_pytest_mg.static import INDENT, LINES_BETWEEN_TOP_LEVEL_BLOCKS


@dataclass
class ImportFixture:
    """Generates a fixture for an import from ast.Import"""

    ast_definition: ast.Import

    @property
    def name(self) -> str:
        """The imported module name."""
        return _get_import_names(self.ast_definition.names)[0]

    @property
    def fixture(self) -> str:
        """Fixture mocking the import."""
        return _build_import_fixture(self.name)


@dataclass
class ImportFromFixtures:
    """Generates fixtures for imported names from ast.ImportFrom."""

    ast_definition: ast.ImportFrom

    @property
    def module(self) -> Optional[str]:
        """The imported module name."""
        return self.ast_definition.module

    @property
    def imported_names(self) -> List[str]:
        """All names imported from the module."""
        return _get_import_names(self.ast_definition.names)

    @property
    def fixtures(self) -> str:
        """Fixtures mocking the imported names."""
        return LINES_BETWEEN_TOP_LEVEL_BLOCKS.join(
            [_build_import_fixture(name) for name in self.imported_names]
        )


def _get_import_names(names: List[ast.alias]) -> List[str]:
    """Get imported names from the names attr of ast.Import or ast.ImportFrom."""
    return [name.asname if name.asname else name.name for name in names]


def _build_import_fixture(name: str) -> str:
    """Build an import fixture provided the imported name."""
    return "\n".join(
        [
            "@pytest.fixture",
            f"def mock_{utils.to_snake_case(name)}(mocker):",
            f'{INDENT}return mocker.patch(f"{{MODULE_PATH}}.{name}")',
        ]
    )
