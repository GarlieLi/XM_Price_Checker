import sys
import json
from pathlib import Path
import subprocess


# ============================================================
# Project root
# ============================================================

project_folder = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(project_folder)
)


# ============================================================
# Test product
# ============================================================

product = {
    "target_id": "O19AE-6-128",
    "name": "Redmi 15",
    "model": "O19AE",
    "ram": "6",
    "storage": "128"
}


URL = (
    "https://www.komputronik.pl/search/category/1?query=Redmi+15+6/128"
)


# ============================================================
# Run
# ============================================================

print("=" * 60)
print("KTR RUNNER TEST")
print("=" * 60)

print("Product:")
print(json.dumps(
    product,
    ensure_ascii=False,
    indent=2
))

print()
print("URL:", URL)
print()


script = project_folder / "run_price_check.py"


result = subprocess.run(
    [
        sys.executable,
        str(script),
        "KTR",
        URL,
        json.dumps(
            product,
            ensure_ascii=False
        )
    ],
    capture_output=True,
    text=True
)


# ============================================================
# Show output
# ============================================================

print("=" * 60)
print("PROCESS OUTPUT")
print("=" * 60)

print(result.stdout)


# ============================================================
# Check process
# ============================================================

if result.returncode != 0:

    print("=" * 60)
    print("PROCESS ERROR")
    print("=" * 60)

    print(result.stderr)

    raise RuntimeError(
        "KTR runner test failed."
    )


# ============================================================
# Extract RESULT_JSON
# ============================================================

result_data = None

for line in result.stdout.splitlines():

    if line.startswith("RESULT_JSON:"):

        json_text = line.replace(
            "RESULT_JSON:",
            "",
            1
        ).strip()

        result_data = json.loads(
            json_text
        )

        break


if result_data is None:

    raise ValueError(
        "RESULT_JSON was not returned."
    )


# ============================================================
# Final result
# ============================================================

print("=" * 60)
print("PARSED RESULT")
print("=" * 60)

print(
    json.dumps(
        result_data,
        ensure_ascii=False,
        indent=2
    )
)


print()
print("=" * 60)
print("TEST PASSED")
print("=" * 60)