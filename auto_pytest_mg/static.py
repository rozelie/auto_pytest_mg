"""Static data."""
INDENT = "    "
"""Standard python block indentation length"""

LINES_BETWEEN_TOP_LEVEL_BLOCKS = "\n\n\n"
"""Lines between top level blocks (functions, classes, fixtures, etc.)"""

HELP_SUMMARY = "\n\n".join(
    [
        "Parse the AST of an input python file to generate a new test file with boilerplate test functions.",
        "Defaults writing to stdout (see -u/-o options for alternatives).",
    ]
)
"""Help summary."""
