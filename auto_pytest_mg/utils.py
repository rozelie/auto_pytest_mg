"""Miscellaneous utility functions."""
import inflection
from isort import place_module


def to_snake_case(word: str) -> str:
    """Converts a word to snake_case."""
    return inflection.underscore(word)


def is_stdlib_module(module: str) -> bool:
    """Determines if a module is within the standard library."""
    return place_module(module) == "STDLIB"
