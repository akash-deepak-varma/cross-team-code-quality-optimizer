from pathlib import Path

from analyzer.ast_analyzer import analyze_ast
from analyzer.complexity import analyze_complexity
from analyzer.lint_analyzer import analyze_lint
from analyzer.security_analyzer import analyze_security


def analyze_file(file_path: str):

    path = Path(file_path)

    source_code = path.read_text(
        encoding="utf-8"
    )

    return {
        "file": path.name,

        "ast": analyze_ast(
            source_code
        ),

        "complexity": analyze_complexity(
            path
        ),

        "lint": analyze_lint(
            path
        ),

        "security": analyze_security(
            path
        )
    }