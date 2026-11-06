from typing import Any


# Fields that may expose proprietary implementation details
# or information about the developer's environment.
SENSITIVE_KEYS = {
    # File / environment information
    "file",
    "filename",
    "path",
    "filepath",
    "file_path",

    # Source-code location information
    "lineno",
    "endline",
    "line",
    "end_line",
    "col_offset",
    "end_col_offset",
    "location",
    "end_location",

    # Function / code identifiers
    "name",
    "variable_name",
    "variable_names",

    # Automated source-code fixes
    "fix",
    "edits",

    # External references
    "url",

    # Possible source-code content
    "source",
    "source_code",
    "code",
    "content",

    # Comments
    "comment",
    "comments",
}


def remove_sensitive_fields(data: Any) -> Any:
    """
    Recursively remove sensitive fields from
    analyzer output.

    The original data is not modified.
    A sanitized copy is returned.
    """

    if isinstance(data, dict):

        return {
            key: remove_sensitive_fields(value)
            for key, value in data.items()
            if key.lower() not in SENSITIVE_KEYS
        }

    if isinstance(data, list):

        return [
            remove_sensitive_fields(item)
            for item in data
        ]

    return data


def complexity_bucket(value: int) -> str:
    """
    Convert exact cyclomatic complexity
    into a privacy-preserving range.
    """

    if value <= 5:
        return "1-5"

    if value <= 10:
        return "6-10"

    if value <= 20:
        return "11-20"

    return "21+"


def length_bucket(value: int) -> str:
    """
    Convert exact function length into
    a privacy-preserving range.
    """

    if value <= 10:
        return "1-10"

    if value <= 25:
        return "11-25"

    if value <= 50:
        return "26-50"

    return "51+"


def parameter_bucket(value: int) -> str:
    """
    Convert exact parameter count into
    a privacy-preserving range.
    """

    if value <= 2:
        return "0-2"

    if value <= 5:
        return "3-5"

    return "6+"


def create_safe_summary(raw_result: dict) -> dict:
    """
    Convert raw analyzer output into a
    privacy-preserving summary.

    The output does NOT contain:

    - file names
    - file paths
    - function names
    - line numbers
    - source code
    - exact complexity values
    - Ruff source-code fixes
    """

    ast_result = raw_result.get("ast", {})
    complexity_result = raw_result.get("complexity", {})

    functions = ast_result.get("functions", [])

    # ---------------------------------------------
    # Extract complexity values locally
    # ---------------------------------------------

    complexity_values = []

    if isinstance(complexity_result, dict):

        for file_results in complexity_result.values():

            if not isinstance(file_results, list):
                continue

            for item in file_results:

                if not isinstance(item, dict):
                    continue

                complexity = item.get("complexity")

                if isinstance(complexity, int):
                    complexity_values.append(
                        complexity
                    )

    # ---------------------------------------------
    # Calculate aggregate complexity
    # ---------------------------------------------

    if complexity_values:

        max_complexity = max(
            complexity_values
        )

        average_complexity = (
            sum(complexity_values)
            / len(complexity_values)
        )

    else:

        max_complexity = 0
        average_complexity = 0

    # ---------------------------------------------
    # Create privacy-safe function information
    # ---------------------------------------------

    safe_functions = []

    for index, function in enumerate(functions):

        if not isinstance(function, dict):
            continue

        complexity = 0

        if index < len(complexity_values):
            complexity = complexity_values[index]

        safe_functions.append(
            {
                "complexity_bucket":
                    complexity_bucket(
                        complexity
                    ),

                "length_bucket":
                    length_bucket(
                        function.get(
                            "lines",
                            0
                        )
                    ),

                "parameter_bucket":
                    parameter_bucket(
                        function.get(
                            "parameters",
                            0
                        )
                    )
            }
        )

    # ---------------------------------------------
    # Final privacy-safe result
    # ---------------------------------------------

    return {
        "language": "python",

        "metrics": {
            "function_count":
                ast_result.get(
                    "function_count",
                    0
                ),

            "class_count":
                ast_result.get(
                    "class_count",
                    0
                ),

            "max_complexity_bucket":
                complexity_bucket(
                    max_complexity
                ),

            "average_complexity_bucket":
                complexity_bucket(
                    round(
                        average_complexity
                    )
                )
        },

        "functions": safe_functions
    }


def sanitize_analysis(raw_result: dict) -> dict:
    """
    Main privacy pipeline.

    Step 1:
        Remove fields that may expose
        proprietary information.

    Step 2:
        Convert useful metrics into
        privacy-preserving buckets.

    Returns:
        Safe data that can eventually
        be exposed through MCP.
    """

    cleaned_result = remove_sensitive_fields(
        raw_result
    )

    safe_result = create_safe_summary(
        cleaned_result
    )

    return safe_result