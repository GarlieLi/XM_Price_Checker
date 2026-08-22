import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

sys.stderr.reconfigure(
    encoding="utf-8"
)

import json

from scrapers import browser_runner
from scrapers import mex
from scrapers import xkom
from scrapers import electro
from scrapers import ktr
from scrapers import msh
from scrapers import max_electro
from scrapers import avans
from scrapers import neonet

SCRAPERS = {
    "MEX": mex,
    "XKOM": xkom,
    "ELECTRO.PL": electro,
    "KTR": ktr,
    "MSH": msh,
    "MAX ELECTRO": max_electro,
    "AVANS": avans,
    "NEONET": neonet
}


def main():

    if len(sys.argv) != 4:
        print(
            "Usage: python run_price_check.py WEBSITE URL PRODUCT_JSON"
        )
        sys.exit(1)

    website = sys.argv[1].strip().upper()
    url = sys.argv[2]

    try:
        product = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print(
            "ERROR: Invalid product JSON:",
            str(e)
        )
        sys.exit(1)

    scraper = SCRAPERS.get(website)

    if scraper is None:
        print(
            f"ERROR: No scraper configured for {website}"
        )
        sys.exit(1)

    print("=" * 50)
    print("Website:", website)
    print("URL:", url)
    print("Product:", product)
    print("=" * 50)

    try:

        result = browser_runner.run_scraper(
            url,
            scraper,
            product
        )

        print(
            "RESULT_JSON:" +
            json.dumps(
                result,
                ensure_ascii=False
            )
        )

    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )

        sys.exit(1)


if __name__ == "__main__":
    main()