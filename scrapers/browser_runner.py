import sys
from playwright.sync_api import sync_playwright


def run_scraper(url, scraper, product):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless= False,
        )

        page = browser.new_page()

        print("Opening:", url)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Page loaded.")

        result = scraper.get_products(
            page,
            product
        )

        print("Results:", result)

        browser.close()

        return result


if __name__ == "__main__":

    print(
        "browser_runner.py is designed "
        "to be called by a separate process."
    )