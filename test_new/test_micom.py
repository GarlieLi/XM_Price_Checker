import sys
import os
import json
import importlib.util


# ============================================================
# LOAD MICOM MODULE
# ============================================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

micom_path = os.path.join(
    project_root,
    "scrapers",
    "micom.py"
)

print(
    "MICOM MODULE PATH:",
    micom_path
)

spec = importlib.util.spec_from_file_location(
    "micom",
    micom_path
)

micom = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    micom
)


# ============================================================
# PRODUCT
# ============================================================

product = {

    "target_id":
        "P1-16-512",

    "name":
        "Xiaomi 17 Ultra",

    "model":
        "P1",

    "ram":
        "16",

    "storage":
        "512",

}


url = (
    "https://www.mi.com/pl/product/xiaomi-17-ultra/buy/?gid=4223714989"
)


# ============================================================
# PLAYWRIGHT
# ============================================================

from playwright.sync_api import (
    sync_playwright
)


# ============================================================
# TEST
# ============================================================

print(
    "=" * 60
)

print(
    "MICOM RUNNER TEST"
)

print(
    "=" * 60
)

print(
    "Product:"
)

print(
    json.dumps(
        product,
        indent=2,
        ensure_ascii=False
    )
)

print()

print(
    "URL:",
    url
)

print()


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page(
        viewport={
            "width": 1440,
            "height": 1000
        }
    )

    print(
        "Opening:",
        url
    )

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print(
        "Page loaded."
    )

    # --------------------------------------------------------
    # Give Mi.com SPA time to render
    # --------------------------------------------------------

    page.wait_for_timeout(
        5000
    )

    # --------------------------------------------------------
    # Print visible buttons
    # --------------------------------------------------------

    print()
    print(
        "=" * 60
    )

    print(
        "VISIBLE BUTTONS"
    )

    print(
        "=" * 60
    )

    buttons = page.locator(
        "button"
    )

    print(
        "Button count:",
        buttons.count()
    )

    for i in range(
        min(buttons.count(), 100)
    ):

        try:

            text = (
                buttons
                .nth(i)
                .inner_text()
                .strip()
            )

            if text:

                print(
                    f"BUTTON {i}: {text!r}"
                )

        except Exception:
            continue

    # --------------------------------------------------------
    # Print body section around purchase information
    # --------------------------------------------------------

    print()
    print(
        "=" * 60
    )

    print(
        "PAGE TEXT CHECK"
    )

    print(
        "=" * 60
    )

    body_text = (
        page.locator(
            "body"
        )
        .inner_text()
    )

    for line in body_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if any(
            keyword.lower() in line.lower()
            for keyword in [
                "Add to cart",
                "Notify me",
                "Dodaj do koszyka",
                "Powiadom mnie",
                "4GB+64GB",
                "4 GB + 64 GB",
                "Black",
                "Mist Blue",
                "Palm Green",
                "zł"
            ]
        ):

            print(
                line
            )

    # --------------------------------------------------------
    # Run scraper
    # --------------------------------------------------------

    print()
    print(
        "=" * 60
    )

    print(
        "RUNNING MICOM SCRAPER"
    )

    print(
        "=" * 60
    )

    results = micom.get_products(
        page,
        product
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print(
        "=" * 60
    )

    print(
        "MICOM RESULTS:",
        len(results)
    )

    print(
        "=" * 60
    )

    for result in results:

        print(
            result
        )

    print()

    print(
        "RESULT_JSON:"
        +
        json.dumps(
            results,
            ensure_ascii=False
        )
    )

    print()
    print(
        "=" * 60
    )

    print(
        "TEST FINISHED"
    )

    print(
        "=" * 60
    )

    # Keep browser open briefly
    page.wait_for_timeout(
        3000
    )

    browser.close()