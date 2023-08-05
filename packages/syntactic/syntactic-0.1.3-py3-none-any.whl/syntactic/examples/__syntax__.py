"""Some example transformers.

.. warning::

    This module's transformers are examples intended for inspiration. They are fragile and
    not expected to be used in projects.

"""


# TODO Use a real parser.

import re


def bangbang_greeting(source: str) -> str:
    """Replace !! with a greeting."""
    return source.replace("!!", 'print("hello")')


def unicode_lambdas(source: str) -> str:
    """Replace unicode lambda."""
    return source.replace("λ", "lambda ")


def transform_sql_literals(source: str) -> str:
    """Replace sql literals.

    Inspired by https://github.com/felixfbecker/node-sql-template-strings sql template
    strings.
    """
    pattern = r"((?:sql|SQL)`)(.*)(`)"
    names = []

    def transform_sql_string(literal_match: re.Match) -> str:
        def replace(m) -> str:

            names.append(m.group().strip("{}"))

            return "?"

        subbed = re.sub(r"(\{\w+\})", replace, literal_match.group(2))
        context = "" + ", " + "[" + ", ".join(names) + "]"

        return repr(subbed) + context

    return re.sub(pattern, transform_sql_string, source)
