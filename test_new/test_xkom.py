import sys

# Make Windows PowerShell output UTF-8
sys.stdout.reconfigure(
    encoding="utf-8"
)

import json
import subprocess


# ============================================================
# TEST PRODUCT
# ============================================================

product = {
    "target_id": "SOMALIAA-4-64",
    "name": "Redmi A7 pro",
    "model": "SOMALIAA",
    "ram": "4",
    "storage": "64"
}


# ============================================================
# TEST URL
# ============================================================

url = (
    "https://www.x-kom.pl/szukaj?q=Redmi%20A7%20pro%204%2F64"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("X-KOM RUNNER TEST")
print("=" * 60)

print("Product:")

print(
    json.dumps(
        product,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("URL:", url)

print()
print("=" * 60)
print("PROCESS OUTPUT")
print("=" * 60)


# ============================================================
# RUN PRICE CHECK
# ============================================================

script = (
    r"C:\Users\New\.vscode\Python_projects"
    r"\XM_Price_Checker\run_price_check.py"
)


result = subprocess.run(
    [
        sys.executable,
        script,
        "XKOM",
        url,
        json.dumps(
            product,
            ensure_ascii=False
        )
    ],
    capture_output=True,
    text=True,
    encoding="utf-8"
)


# ============================================================
# SHOW PROCESS OUTPUT
# ============================================================

print(result.stdout)


# ============================================================
# CHECK PROCESS
# ============================================================

if result.returncode != 0:

    print("=" * 60)
    print("PROCESS ERROR")
    print("=" * 60)

    print(result.stderr)

    raise RuntimeError(
        "X-KOM runner test failed."
    )


# ============================================================
# PARSE RESULT_JSON
# ============================================================

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


# ============================================================
# SHOW PARSED RESULT
# ============================================================

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


# ============================================================
# FINISHED
# ============================================================

print()
print("=" * 60)
print("TEST FINISHED")
print("=" * 60)