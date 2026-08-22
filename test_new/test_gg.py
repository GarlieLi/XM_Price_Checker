import sys
import os
import json

from playwright.sync_api import sync_playwright


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# ============================================================
# IMPORT GG SCRAPER
# ============================================================

from scrapers import gg


# ============================================================
# TEST PRODUCT
# ============================================================

PRODUCT = {

    "target_id":
        "SOMALIAA-4-64",

    "name":
        "Redmi A7 pro",

    "model":
        "SOMALIAA",

    "ram":
        "4",

    "storage":
        "64"
}


# ============================================================
# URL
# ============================================================

URL = (
    "https://mi-store.pl/"
    "search.php?text=Redmi+A7+Pro+4%2F64"
)


# ============================================================
# TEST
# ============================================================

print(
    "=" * 60
)

print(
    "GG RUNNER TEST"
)

print(
    "=" * 60
)

print(
    "Product:"
)

print(
    json.dumps(
        PRODUCT,
        indent=2,
        ensure_ascii=False
    )
)

print()

print(
    "URL:",
    URL
)

print()

print(
    "=" * 60
)

print(
    "GG MODULE PATH:",
    gg.__file__
)

print(
    "=" * 60
)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page(
        viewport={
            "width": 1440,
            "height": 900
        }
    )

    try:

        print(
            "Opening:",
            URL
        )

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(
            "Page loaded."
        )

        # ----------------------------------------------------
        # Give the website time to render products.
        # ----------------------------------------------------

        page.wait_for_timeout(
            3000
        )

        print(
            "Waiting for GG products..."
        )

        # ----------------------------------------------------
        # Run scraper
        # ----------------------------------------------------

        results = gg.get_products(
            page,
            PRODUCT
        )

        # ----------------------------------------------------
        # Output JSON
        # ----------------------------------------------------

        print()
        print(
            "RESULT_JSON:"
            + json.dumps(
                results,
                ensure_ascii=False
            )
        )

        print()
        print(
            "=" * 60
        )

        print(
            "PARSED RESULT"
        )

        print(
            "=" * 60
        )

        print(
            json.dumps(
                results,
                indent=2,
                ensure_ascii=False
            )
        )

    except Exception as e:

        print()
        print(
            "=" * 60
        )

        print(
            "GG TEST ERROR"
        )

        print(
            "=" * 60
        )

        print(
            repr(e)
        )

    finally:

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

        browser.close()