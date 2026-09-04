import subprocess
import sys
import json


PROJECT_FOLDER = r"C:\Users\New\.vscode\Python_projects\XM_Price_Checker"

PRODUCT = {
    "target_id": "P10-12-512",
    "name": "POCO X8 Pro",
    "model": "P19",
    "ram": "12",
    "storage": "512"
}

URL = (
    "https://www.mediaexpert.pl/search?query[menu_item]=&query[querystring]=POCO%20X8%20Pro%2012%2F512"
)


print("=" * 60)
print("MEX RUNNER TEST")
print("=" * 60)

print("Product:")
print(json.dumps(
    PRODUCT,
    indent=2,
    ensure_ascii=False
))

print()
print("URL:", URL)

print()
print("=" * 60)
print("PROCESS OUTPUT")
print("=" * 60)


result = subprocess.run(
    [
        sys.executable,
        f"{PROJECT_FOLDER}\\run_price_check.py",
        "MEX",
        URL,
        json.dumps(PRODUCT, ensure_ascii=False)
    ],
    capture_output=True,
    text=True
)


print(result.stdout)


if result.returncode != 0:

    print("=" * 60)
    print("PROCESS ERROR")
    print("=" * 60)

    print(result.stderr)

    raise RuntimeError(
        "MEX runner test failed."
    )


# ------------------------------------------------------------
# Parse RESULT_JSON
# ------------------------------------------------------------

parsed_result = None

for line in result.stdout.splitlines():

    if line.startswith("RESULT_JSON:"):

        json_text = line.replace(
            "RESULT_JSON:",
            "",
            1
        ).strip()

        parsed_result = json.loads(
            json_text
        )

        break


if parsed_result is None:

    raise ValueError(
        "No RESULT_JSON returned."
    )


print()
print("=" * 60)
print("PARSED RESULT")
print("=" * 60)

print(
    json.dumps(
        parsed_result,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("=" * 60)
print("TEST FINISHED")
print("=" * 60)