import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

import json
import subprocess


product = {
    "target_id": "SOMALIAA-4-64",
    "name": "Redmi A7 pro",
    "model": "SOMALIAA",
    "ram": "4",
    "storage": "64"
}

url = (
    "https://mediamarkt.pl/pl/search.html?query=Redmi%20A7%20pro%204%2F64"
)


print("=" * 60)
print("MEDIAMARKT RUNNER TEST")
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


script = (
    r"C:\Users\garli\Python_Projects"
    r"\XM_Price_Checker\run_price_check.py"
)

result = subprocess.run(
    [
        sys.executable,
        script,
        "MSH",
        url,
        json.dumps(
            product,
            ensure_ascii=False
        )
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

print(result.stdout)

if result.returncode != 0:

    print("=" * 60)
    print("PROCESS ERROR")
    print("=" * 60)

    print(result.stderr)

    raise RuntimeError(
        "MediaMarkt runner test failed."
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