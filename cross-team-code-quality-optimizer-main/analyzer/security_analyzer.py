import subprocess
import json


def analyze_security(file_path):

    result = subprocess.run(
        [
            "bandit",
            "-r",
            str(file_path),
            "-f",
            "json"
        ],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        return {}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}