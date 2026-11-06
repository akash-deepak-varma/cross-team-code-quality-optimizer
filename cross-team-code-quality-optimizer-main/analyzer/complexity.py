import subprocess
import json


def analyze_complexity(file_path):

    result = subprocess.run(
        [
            "radon",
            "cc",
            str(file_path),
            "-j"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "error": result.stderr
        }

    if not result.stdout.strip():
        return {}

    return json.loads(result.stdout)