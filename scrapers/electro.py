import re


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = str(text).strip()

    # Remove currency labels
    text = text.replace("zł", "")
    text = text.replace("PLN", "")

    # Remove spaces
    text = text.replace(" ", "")

    # Find price
    match = re.search(
        r"(\d+(?:[,.]\d+)?)",
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

        # ----------------------------------------------------
        # BLACK
        # ----------------------------------------------------

        "czarny": "Black",
        "czarna": "Black",
        "czarne": "Black",
        "black": "Black",
        "midnight black": "Black",

        # ----------------------------------------------------
        # BLUE
        # ----------------------------------------------------

        "niebieski": "Blue",
        "niebieska": "Blue",
        "blue": "Blue",
        "glacier blue": "Blue",
        "ocean blue": "Blue",

        # ----------------------------------------------------
        # TITANIUM
        # ----------------------------------------------------

        "tytanowy": "Titanium",
        "tytanowa": "Titanium",
        "titanium": "Titanium",

        # ----------------------------------------------------
        # PURPLE
        # ----------------------------------------------------

        "fioletowy": "Purple",
        "fioletowa": "Purple",
        "purple": "Purple",
        "aurora purple": "Purple",
        "lawendowy": "Purple",
        "lawendowa": "Purple",
        "lavender": "Purple",

        # ----------------------------------------------------
        # GREEN
        # ----------------------------------------------------

        "zielony": "Green",
        "zielona": "Green",
        "green": "Green",
        "forest green": "Green",

        # ----------------------------------------------------
        # WHITE
        # ----------------------------------------------------

        "biały": "White",
        "biała": "White",
        "white": "White",

        # ----------------------------------------------------
        # GREY
        # ----------------------------------------------------

        "szary": "Grey",
        "szara": "Grey",
        "grey": "Grey",
        "gray": "Grey",

        # ----------------------------------------------------
        # SILVER
        # ----------------------------------------------------

        "srebrny": "Silver",
        "srebrna": "Silver",
        "silver": "Silver",

        # ----------------------------------------------------
        # GOLD
        # ----------------------------------------------------

        "złoty": "Gold",
        "złota": "Gold",
        "gold": "Gold",

        # ----------------------------------------------------
        # PINK
        # ----------------------------------------------------

        "różowy": "Pink",
        "różowa": "Pink",
        "pink": "Pink",

        # ----------------------------------------------------
        # BROWN
        # ----------------------------------------------------

        "brązowy": "Brown",
        "brązowa": "Brown",
        "brown": "Brown",
        "mocha brown": "Brown",

    }

    # Check longer/descriptive names first
    for color_name in sorted(
        color_map.keys(),
        key=len,
        reverse=True
    ):

        if re.search(
            rf"\b{re.escape(color_name)}\b",
            title_lower
        ):

            return color_map[color_name]

    return "Unknown"

# ============================================================
# PRODUCT MATCHING
# ============================================================

def normalize_product_name(text):

    text = str(text).lower()

    # Normalize Pro+
    text = re.sub(
        r"pro\s*\+",
        "pro+",
        text
    )

    # Remove unnecessary punctuation
    text = re.sub(
        r"[^a-z0-9+]+",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def get_redmi_note_signature(text):

    text = normalize_product_name(text)

    # Find Redmi Note number
    match = re.search(
        r"\bredmi note (\d+)\b",
        text
    )

    if not match:
        return None

    model_number = match.group(1)

    # Check Pro / Pro+
    after_note = text[match.end():].strip()

    if re.match(
        r"^pro\+",
        after_note
    ):
        version = "pro+"

    elif re.match(
        r"^pro\b",
        after_note
    ):
        version = "pro"

    else:
        version = "standard"

    # Check 5G
    has_5g = bool(
        re.search(
            r"\b5g\b",
            text
        )
    )

    return (
        model_number,
        version,
        has_5g
    )


def product_name_matches(target_name, title):

    target_normalized = normalize_product_name(
        target_name
    )

    title_normalized = normalize_product_name(
        title
    )

    # --------------------------------------------------------
    # STRICT MATCHING FOR REDMI NOTE PRODUCTS
    # --------------------------------------------------------

    if (
        "redmi note" in target_normalized
        and
        "redmi note" in title_normalized
    ):

        target_signature = get_redmi_note_signature(
            target_name
        )

        title_signature = get_redmi_note_signature(
            title
        )

        if (
            target_signature is not None
            and
            title_signature is not None
        ):

            return (
                target_signature
                ==
                title_signature
            )

    # --------------------------------------------------------
    # OTHER PRODUCTS
    # --------------------------------------------------------

    # Exact normalized phrase match
    pattern = (
        r"(?:^|\s)"
        +
        re.escape(target_normalized)
        +
        r"(?:$|\s)"
    )

    return bool(
        re.search(
            pattern,
            title_normalized
        )
    )


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

        if not product_name_matches(
            product["name"],
            title
        ):

            continue

        print()

        print("=" * 60)
        print("ELECTRO PRODUCT", i)
        print("=" * 60)

        print(
            "TITLE:",
            title
        )

        print(
            "PRODUCT NAME MATCH: YES"
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

        print(
            "RAM / STORAGE MATCH: YES"
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
        # ----------------------------------------------------
        #
        # Electro has a dedicated
        # .product-show-offer-unavailable
        # element when unavailable.
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

        result = {

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

        }

        results.append(
            result
        )

        print(
            "RESULT:",
            result
        )

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not results:

        print()

        print(
            "Electro: Target product not found."
        )

        results.append({

            "product_name":
                product["name"],

            "variant":
                "Unknown",

            "ram":
                str(product["ram"]) + " GB",

            "storage":
                str(product["storage"]) + " GB",

            "price":
                None,

            "availability":
                "Unavailable",

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