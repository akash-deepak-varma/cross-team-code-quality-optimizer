import json

from analyzer.analyzer import analyze_file
from privacy.sanitizer import sanitize_analysis


# --------------------------------------------------
# Analyze the source code locally
# --------------------------------------------------

raw_result = analyze_file(
    "test_code/sample.py"
)


# --------------------------------------------------
# Apply privacy protection
# --------------------------------------------------

safe_result = sanitize_analysis(
    raw_result
)


# --------------------------------------------------
# Display privacy-safe result
# --------------------------------------------------

print(
    json.dumps(
        safe_result,
        indent=2
    )
)