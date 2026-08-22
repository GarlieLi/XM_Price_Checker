import re


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = str(text).strip()

    # Remove PLN / zł if present
    text = text.replace("zł", "")
    text = text.replace("PLN", "")
    text = text.replace(" ", "")

    # Find numeric price
    match = re.search(
        r"(\d+[,.]?\d*)",
        text
    )

    if not match:
        return None

    return float(
        match.group(1).replace(",", ".")
    )


# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = title.lower()

    color_map = {
        "czarny": "Black",
        "czarna": "Black",
        "czarne": "Black",

        "tytanowy": "Titanium",
        "tytanowa": "Titanium",

        "fioletowy": "Purple",
        "fioletowa": "Purple",

        "niebieski": "Blue",
        "niebieska": "Blue",

        "zielony": "Green",
        "zielona": "Green",

        "biały": "White",
        "biała": "White",

        "szary": "Grey",
        "szara": "Grey",

        "srebrny": "Silver",
        "srebrna": "Silver",

        "złoty": "Gold",
        "złota": "Gold",

        "różowy": "Pink",
        "różowa": "Pink",

        "czerwony": "Red",
        "czerwona": "Red",
    }

    for polish_color, english_color in color_map.items():

        if re.search(
            rf"\b{re.escape(polish_color)}\b",
            title_lower
        ):
            return english_color

    return "Unknown"


# ============================================================
# PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    print("Waiting for Electro products...")

    # --------------------------------------------------------
    # Find product titles
    # --------------------------------------------------------

    titles = page.locator(
        "h2.name"
    )

    print(
        "Total product titles:",
        titles.count()
    )

    # --------------------------------------------------------
    # Target RAM / Storage
    # --------------------------------------------------------

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
        # Match product name
        # ----------------------------------------------------

        if product["name"].lower() not in title.lower():
            continue

        print()
        print("=" * 60)
        print("ELECTRO PRODUCT", i)
        print("=" * 60)

        print(
            "TITLE:",
            title
        )

        # ----------------------------------------------------
        # Find product container
        # ----------------------------------------------------

        card = title_element.locator(
            "xpath=ancestor::div[contains(@class, 'offer-box')]"
        ).first

        if card.count() == 0:

            print(
                "Could not find product container."
            )

            continue

        # ----------------------------------------------------
        # CARD TEXT
        # ----------------------------------------------------

        card_text = (
            card
            .inner_text()
            .strip()
        )

        # ----------------------------------------------------
        # RAM
        # ----------------------------------------------------

        ram_match = re.search(
            r"Pamięć RAM:\s*([0-9]+\s*GB)",
            card_text,
            re.IGNORECASE
        )

        if ram_match:

            ram = ram_match.group(1)

        else:

            ram = None

        # ----------------------------------------------------
        # STORAGE
        # ----------------------------------------------------

        storage_match = re.search(
            r"Pamięć wbudowana\s*\[GB\]:\s*([0-9]+)",
            card_text,
            re.IGNORECASE
        )

        if storage_match:

            storage = (
                storage_match.group(1)
                + " GB"
            )

        else:

            storage = None

        # ----------------------------------------------------
        # Match RAM / Storage
        # ----------------------------------------------------

        actual_ram = re.sub(
            r"\D",
            "",
            str(ram)
        )

        actual_storage = re.sub(
            r"\D",
            "",
            str(storage)
        )

        if (
            actual_ram != target_ram
            or
            actual_storage != target_storage
        ):

            print(
                "RAM/storage does not match target."
            )

            continue

        print(
            "RAM:",
            ram
        )

        print(
            "STORAGE:",
            storage
        )

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        color = get_color(
            title
        )

        print(
            "COLOR:",
            color
        )

        # ----------------------------------------------------
        # AVAILABILITY
        #
        # Electro has a dedicated:
        # .product-show-offer-unavailable
        #
        # element when the product is unavailable.
        # ----------------------------------------------------

        unavailable_element = card.locator(
            ".product-show-offer-unavailable"
        )

        if unavailable_element.count() > 0:

            availability = "Unavailable"

        else:

            availability = "Available"

        print(
            "AVAILABILITY:",
            availability
        )

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price_element = card.locator(
            "span.whole"
        ).first

        if price_element.count() == 0:

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
            "PRICE:",
            price
        )

        # ----------------------------------------------------
        # SAVE RESULT
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
                availability,
        })

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not results:

        print()
        print(
            "Electro: Target product not found."
        )

        results.append({
            "product_name": product["name"],
            "variant": "Unknown",
            "ram": str(product["ram"]) + " GB",
            "storage": str(product["storage"]) + " GB",
            "price": None,
            "availability": "Unavailable",
        })

    return results

# ============================================================
# UNIFIED SCRAPER INTERFACE
# ============================================================

def get_price(page, product=None):

    if product is None:

        # Electro product-page fallback.
        # Kept for compatibility with the unified
        # scraper interface.

        return None

    return get_products(
        page,
        product
    )