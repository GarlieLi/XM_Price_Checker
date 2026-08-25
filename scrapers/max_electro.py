import re


# ------------------------------------------------------------
# Price
# ------------------------------------------------------------

def clean_price(text):

    if not text:
        return None

    match = re.search(
        r"(\d[\d\s]*[,.]\d{1,2})",
        text
    )

    if not match:
        return None

    value = (
        match.group(1)
        .replace(" ", "")
        .replace(",", ".")
    )

    try:
        return float(value)

    except ValueError:
        return None


# ------------------------------------------------------------
# Color
# ------------------------------------------------------------

def get_color(title):

    title_lower = title.lower()

    # --------------------------------------------------------
    # Specific / multi-word colors FIRST
    # --------------------------------------------------------

    if "glacier blue" in title_lower:
        return "Glacier Blue"

    elif "mocha brown" in title_lower:
        return "Mocha Brown"

    elif "ocean teal" in title_lower:
        return "Ocean Teal"

    elif "midnight black" in title_lower:
        return "Midnight Black"

    elif "forest green" in title_lower:
        return "Forest Green"

    elif "aurora purple" in title_lower:
        return "Aurora Purple"

    elif "ocean blue" in title_lower:
        return "Ocean Blue"

    # --------------------------------------------------------
    # English colors
    # --------------------------------------------------------

    elif re.search(r"\bblack\b", title_lower):
        return "Black"

    elif re.search(r"\bgreen\b", title_lower):
        return "Green"

    elif re.search(r"\bblue\b", title_lower):
        return "Blue"

    elif re.search(r"\bwhite\b", title_lower):
        return "White"

    elif re.search(r"\bgrey\b", title_lower):
        return "Grey"

    elif re.search(r"\bgray\b", title_lower):
        return "Gray"

    elif re.search(r"\bsilver\b", title_lower):
        return "Silver"

    elif re.search(r"\bgold\b", title_lower):
        return "Gold"

    elif re.search(r"\bpurple\b", title_lower):
        return "Purple"

    elif re.search(r"\bpink\b", title_lower):
        return "Pink"

    elif re.search(r"\bred\b", title_lower):
        return "Red"

    elif re.search(r"\btitanium\b", title_lower):
        return "Titanium"

    # --------------------------------------------------------
    # Polish colors
    # --------------------------------------------------------

    elif "czarn" in title_lower:
        return "Black"

    elif "zielon" in title_lower:
        return "Green"

    elif "niebiesk" in title_lower:
        return "Blue"

    elif "biały" in title_lower or "bialy" in title_lower:
        return "White"

    elif "szary" in title_lower:
        return "Grey"

    elif "srebrny" in title_lower:
        return "Silver"

    elif "złoty" in title_lower or "zloty" in title_lower:
        return "Gold"

    elif "fioletowy" in title_lower:
        return "Purple"

    elif "różowy" in title_lower or "rozowy" in title_lower:
        return "Pink"

    elif "czerwony" in title_lower:
        return "Red"

    elif "tytanowy" in title_lower:
        return "Titanium"

    else:
        return "Unknown"


# ------------------------------------------------------------
# Product Matching
# ------------------------------------------------------------

def matches_product(title, product):

    title_lower = (
        title
        .lower()
        .replace("\u00a0", " ")
        .strip()
    )

    target_name = (
        product["name"]
        .lower()
        .replace("\u00a0", " ")
        .strip()
    )

    # --------------------------------------------------------
    # Remove 5G from product name for the core-name check.
    #
    # Example:
    #
    # Target:
    # Redmi Note 15 Pro+ 5G
    #
    # Website:
    # Redmi Note 15 Pro+ 8/256GB ... 5G ...
    #
    # "Redmi Note 15 Pro+ 5G" is therefore NOT a direct
    # substring of the title.
    # --------------------------------------------------------

    target_core = re.sub(
        r"\s+5g\b",
        "",
        target_name,
        flags=re.IGNORECASE
    ).strip()

    # --------------------------------------------------------
    # Core product name must match
    # --------------------------------------------------------

    if target_core not in title_lower:

        print(
            "Product name mismatch."
        )

        return False

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Prevent:
    #
    # Redmi Note 15 Pro
    #
    # from matching:
    #
    # Redmi Note 15 Pro+
    #
    # --------------------------------------------------------

    if (
        "pro+" not in target_core
        and
        re.search(r"\bpro\+", title_lower)
    ):

        print(
            "Product mismatch: target is Pro, "
            "but title is Pro+."
        )

        return False

    # --------------------------------------------------------
    # If target is Pro+, title must contain Pro+
    # --------------------------------------------------------

    if "pro+" in target_core:

        if "pro+" not in title_lower:

            print(
                "Product mismatch: target is Pro+."
            )

            return False

    # --------------------------------------------------------
    # 5G requirement
    # --------------------------------------------------------

    if "5g" in target_name:

        if not re.search(r"\b5g\b", title_lower):

            print(
                "Product mismatch: target requires 5G."
            )

            return False

    # --------------------------------------------------------
    # Product matches
    # --------------------------------------------------------

    return True


# ------------------------------------------------------------
# Price Extraction
# ------------------------------------------------------------

def extract_price(card):

    card_text = (
        card
        .inner_text()
        .strip()
    )

    card_text_lower = card_text.lower()

    # --------------------------------------------------------
    # Unavailable products have no current selling price
    # --------------------------------------------------------

    if (
        "produkt niedostępny" in card_text_lower
        or
        "brak w magazynie" in card_text_lower
    ):

        return None

    # --------------------------------------------------------
    # CURRENT PRICE - split format
    #
    # Example:
    #
    # 1699
    # 00
    # zł
    #
    # Cena regularna
    #
    # We specifically look for the price immediately before
    # "Cena regularna".
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*)\s+(\d{2})\s*zł\s*"
        r"Cena\s+regularna",
        card_text,
        re.IGNORECASE
    )

    if match:

        value = (
            match.group(1)
            .replace(" ", "")
            + "."
            + match.group(2)
        )

        try:

            return float(value)

        except ValueError:

            pass

    # --------------------------------------------------------
    # CURRENT PRICE - normal format
    #
    # Example:
    #
    # 1699.00 zł
    #
    # Cena regularna
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*[,.]\d{2})\s*zł\s*"
        r"Cena\s+regularna",
        card_text,
        re.IGNORECASE
    )

    if match:

        value = (
            match.group(1)
            .replace(" ", "")
            .replace(",", ".")
        )

        try:

            return float(value)

        except ValueError:

            pass

    # --------------------------------------------------------
    # Fallback
    #
    # If the page has a different structure, take the first
    # normal price.
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*[,.]\d{2})\s*zł",
        card_text,
        re.IGNORECASE
    )

    if match:

        value = (
            match.group(1)
            .replace(" ", "")
            .replace(",", ".")
        )

        try:

            return float(value)

        except ValueError:

            pass

    return None


# ------------------------------------------------------------
# Products
# ------------------------------------------------------------

def get_products(page, product):

    results = []

    print(
        "Waiting for Max Elektro products..."
    )

    # --------------------------------------------------------
    # Product cards
    # --------------------------------------------------------

    cards = page.locator(
        "div.product_cart-item"
    )

    print(
        "Max Elektro product cards:",
        cards.count()
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
    # Track whether matching product was found
    # --------------------------------------------------------

    product_found = False

    # --------------------------------------------------------
    # Process cards
    # --------------------------------------------------------

    for i in range(cards.count()):

        card = cards.nth(i)

        try:

            # ------------------------------------------------
            # Product title
            # ------------------------------------------------

            title_element = card.locator(
                "h3"
            ).first

            if title_element.count() == 0:

                continue

            title = (
                title_element
                .inner_text()
                .strip()
            )

            print()
            print("=" * 60)
            print(
                "MAX ELEKTRO CARD",
                i
            )
            print("=" * 60)

            print(
                "TITLE:",
                title
            )

            # ------------------------------------------------
            # Product matching
            # ------------------------------------------------

            if not matches_product(
                title,
                product
            ):

                continue

            print(
                "PRODUCT NAME MATCH: YES"
            )

            # ------------------------------------------------
            # Card text
            # ------------------------------------------------

            card_text = (
                card
                .inner_text()
                .strip()
            )

            print()
            print(
                "CARD TEXT:"
            )
            print(
                "-" * 60
            )
            print(
                card_text
            )
            print(
                "-" * 60
            )

            # ------------------------------------------------
            # RAM
            # ------------------------------------------------

            ram_match = re.search(
                r"Pamięć RAM\s*\(GB\)\s*([0-9]+)",
                card_text,
                re.IGNORECASE
            )

            if not ram_match:

                print(
                    "RAM not found."
                )

                continue

            ram = (
                ram_match.group(1)
                + " GB"
            )

            print(
                "RAM:",
                ram
            )

            # ------------------------------------------------
            # Storage
            #
            # Example:
            #
            # Redmi Note 15 Pro+ 8/256GB
            # ------------------------------------------------

            storage_match = re.search(
                r"\d+\s*/\s*(\d+)\s*GB",
                title,
                re.IGNORECASE
            )

            if not storage_match:

                print(
                    "STORAGE not found."
                )

                continue

            storage = (
                storage_match.group(1)
                + " GB"
            )

            print(
                "STORAGE:",
                storage
            )

            # ------------------------------------------------
            # RAM / Storage matching
            # ------------------------------------------------

            ram_match_value = re.sub(
                r"\D",
                "",
                ram
            )

            storage_match_value = re.sub(
                r"\D",
                "",
                storage
            )

            if (
                ram_match_value != target_ram
                or
                storage_match_value != target_storage
            ):

                print(
                    "RAM / STORAGE MATCH: NO"
                )

                continue

            print(
                "RAM / STORAGE MATCH: YES"
            )

            # ------------------------------------------------
            # Matching product found
            # ------------------------------------------------

            product_found = True

            # ------------------------------------------------
            # COLOR
            # ------------------------------------------------

            color = get_color(
                title
            )

            print(
                "COLOR:",
                color
            )

            # ------------------------------------------------
            # AVAILABILITY
            # ------------------------------------------------

            card_text_lower = (
                card_text
                .lower()
            )

            # ------------------------------------------------
            # Explicitly unavailable
            # ------------------------------------------------

            if (
                "produkt niedostępny"
                in card_text_lower
                or
                "brak w magazynie"
                in card_text_lower
                or
                "chwilowo niedostępny"
                in card_text_lower
            ):

                availability = "Unavailable"

            # ------------------------------------------------
            # Explicitly available
            # ------------------------------------------------

            elif (
                "dostępny"
                in card_text_lower
                or
                "dostepny"
                in card_text_lower
                or
                "dodaj do koszyka"
                in card_text_lower
                or
                "ostatnie sztuki"
                in card_text_lower
            ):

                availability = "Available"

            # ------------------------------------------------
            # Unknown
            # ------------------------------------------------

            else:

                availability = "Unknown"

            print(
                "AVAILABILITY:",
                availability
            )

            # ------------------------------------------------
            # PRICE
            # ------------------------------------------------

            price = extract_price(
                card
            )

            print(
                "PRICE:",
                price
            )

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

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
                    availability
            }

            print(
                "RESULT:",
                result
            )

            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

            results.append(
                result
            )

        except Exception as e:

            print(
                "ERROR PROCESSING CARD:",
                i,
                str(e)
            )

            continue

    # ========================================================
    # NO MATCHING PRODUCT
    # ========================================================

    if not product_found:

        print()
        print("=" * 60)
        print(
            "MAX ELEKTRO: TARGET PRODUCT NOT FOUND"
        )
        print("=" * 60)

        print(
            "Product:",
            product["name"]
        )

        print(
            "RAM:",
            product["ram"]
        )

        print(
            "STORAGE:",
            product["storage"]
        )

        print(
            "Availability: Unavailable"
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
                "Unavailable"
        })

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print(
        "MAX ELEKTRO RESULTS:",
        len(results)
    )
    print("=" * 60)

    for result in results:

        print(
            result
        )

    return results