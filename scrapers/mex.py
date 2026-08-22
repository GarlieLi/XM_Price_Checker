import re


# ============================================================
# PRICE
# ============================================================

def clean_price(price_text):

    if price_text is None:
        return None

    text = str(price_text).strip()

    text = text.replace("Cena:", "")
    text = text.replace("zł", "")
    text = text.replace("PLN", "")
    text = text.replace(" ", "")

    text = re.sub(
        r"[^0-9,.]",
        "",
        text
    )

    if not text:
        return None

    if "," in text and "." not in text:
        text = text.replace(",", ".")

    elif "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")

    return float(text)


# ============================================================
# OLD SIMPLE PRICE FUNCTION
# ============================================================

def get_price_only(page):

    price_elements = page.locator(
        "span.whole"
    )

    if price_elements.count() == 0:
        raise ValueError(
            "Media Expert price element not found."
        )

    whole = (
        price_elements.first
        .inner_text()
        .strip()
    )

    decimal_elements = page.locator(
        "span.decimal"
    )

    if decimal_elements.count() > 0:

        decimal = (
            decimal_elements.first
            .inner_text()
            .strip()
        )

    else:

        decimal = "00"

    return clean_price(
        f"{whole}.{decimal}"
    )


# ============================================================
# PRODUCT RESULTS
# ============================================================

def get_products(page, product):

    # --------------------------------------------------------
    # Load all products on the page
    # --------------------------------------------------------

    print(
        "Loading all Media Expert products..."
    )

    previous_count = 0
    stable_rounds = 0

    for _ in range(15):

        page.mouse.wheel(
            0,
            1500
        )

        page.wait_for_timeout(
            1000
        )

        current_count = page.locator(
            "h2, h3"
        ).count()

        print(
            "Current h2/h3 count:",
            current_count
        )

        if current_count == previous_count:

            stable_rounds += 1

        else:

            stable_rounds = 0

        previous_count = current_count

        # Stop after the page has stopped
        # adding new elements twice.
        if stable_rounds >= 2:
            break

    print(
        "Finished loading products. Total h2/h3:",
        page.locator("h2, h3").count()
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    results = []

    # Track whether the exact target product
    # (name + RAM + storage) was found.
    product_found = False

    target_name = product["name"].lower()

    titles = page.locator(
        "h2, h3"
    )

    print(
        "Total h2/h3 elements:",
        titles.count()
    )

    # --------------------------------------------------------
    # Polish -> English color mapping
    # --------------------------------------------------------

    color_map = {

        "czarny": "Black",
        "czarna": "Black",
        "czarne": "Black",

        "niebieski": "Blue",
        "niebieska": "Blue",

        "biały": "White",
        "biała": "White",

        "zielony": "Green",
        "zielona": "Green",

        "szary": "Grey",
        "szara": "Grey",

        "fioletowy": "Purple",
        "fioletowa": "Purple",

        "srebrny": "Silver",
        "srebrna": "Silver",

        "złoty": "Gold",
        "złota": "Gold",

        "różowy": "Pink",
        "różowa": "Pink",

        "czerwony": "Red",
        "czerwona": "Red",

        "tytanowy": "Titanium",
        "tytanowa": "Titanium",
    }

    # --------------------------------------------------------
    # Process products
    # --------------------------------------------------------

    for i in range(titles.count()):

        title_element = titles.nth(i)

        title = (
            title_element
            .inner_text()
            .strip()
        )

        # ----------------------------------------------------
        # Check product name
        # ----------------------------------------------------

        if target_name not in title.lower():
            continue

        print()
        print("=" * 60)
        print(
            "PRODUCT:",
            title
        )

        # ----------------------------------------------------
        # Find the offer-box
        # ----------------------------------------------------

        card = title_element.locator(
            "xpath=ancestor::div[contains(@class, 'offer-box')]"
        ).first

        if card.count() == 0:

            print(
                "Offer card not found."
            )

            continue

        card_text = card.inner_text()

        # ----------------------------------------------------
        # Extract color
        # ----------------------------------------------------

        color = ""

        title_lower = title.lower()

        for polish_color, english_color in color_map.items():

            if re.search(
                rf"\b{re.escape(polish_color)}\b",
                title_lower
            ):

                color = english_color
                break

        # If color was not found in the title,
        # try "Kolor obudowy".
        if not color:

            color_match = re.search(
                r"Kolor obudowy:\s*([^\n]+)",
                card_text,
                re.IGNORECASE
            )

            if color_match:

                raw_color = (
                    color_match
                    .group(1)
                    .strip()
                )

                color = color_map.get(
                    raw_color.lower(),
                    raw_color
                )

        print(
            "Color:",
            color
        )

        # ----------------------------------------------------
        # Extract RAM / storage
        # ----------------------------------------------------

        ram = ""
        storage = ""

        memory_match = re.search(
            r"Pamięć RAM/Wewnętrzna:\s*"
            r"(\d+)\s*GB\s*/\s*(\d+)\s*GB",
            card_text,
            re.IGNORECASE
        )

        if memory_match:

            ram = memory_match.group(1)
            storage = memory_match.group(2)

        print(
            "RAM:",
            ram,
            "| Storage:",
            storage
        )

        # ----------------------------------------------------
        # Target RAM / storage
        # ----------------------------------------------------

        target_ram = re.sub(
            r"\D",
            "",
            str(product["ram"])
        )

        target_storage = re.sub(
            r"\D",
            "",
            str(product["storage"])
        )

        if (
            ram != target_ram
            or
            storage != target_storage
        ):

            print(
                "RAM/storage does not match target."
            )

            continue

        # ----------------------------------------------------
        # Exact target product found
        # ----------------------------------------------------

        product_found = True

        # ----------------------------------------------------
        # Availability
        # ----------------------------------------------------

        card_text_lower = card_text.lower()

        if (
            "produkt chwilowo niedostępny"
            in card_text_lower
            or
            "produkt niedostępny"
            in card_text_lower
        ):

            availability = "Unavailable"

        else:

            availability = "Available"

        print(
            "Availability:",
            availability
        )

        # ----------------------------------------------------
        # Price
        # ----------------------------------------------------

        price_element = card.locator(
            "span.whole"
        ).first

        if price_element.count() == 0:

            # An unavailable product may have
            # no price displayed.
            price = None

        else:

            price_text = (
                price_element
                .inner_text()
                .strip()
            )

            price = clean_price(
                price_text
            )

        print(
            "Price:",
            price
        )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        results.append({

            "product_name":
                product["name"],

            "variant":
                color,

            "ram":
                ram,

            "storage":
                storage,

            "price":
                price,

            "availability":
                availability
        })

    # --------------------------------------------------------
    # TARGET PRODUCT NOT FOUND
    # --------------------------------------------------------

    if not product_found:

        print(
            "Target product not found on Media Expert."
        )

        results.append({

            "product_name":
                product["name"],

            "variant":
                "Unknown",

            "ram":
                product["ram"],

            "storage":
                product["storage"],

            "price":
                None,

            "availability":
                "Unavailable"
        })

    return results


# ============================================================
# UNIFIED SCRAPER INTERFACE
# ============================================================

def get_price(page, product=None):

    if product is None:

        return get_price_only(page)

    return get_products(
        page,
        product
    )