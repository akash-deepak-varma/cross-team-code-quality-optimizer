import subprocess
import json


def analyze_lint(file_path):

    result = subprocess.run(
        [
            "ruff",
            "check",
            str(file_path),
            "--output-format",
            "json"
        ],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return []

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []