import re


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = str(text)

    # Remove common labels/currency
    text = (
        text
        .replace("Cena:", "")
        .replace("zł", "")
        .replace("PLN", "")
        .strip()
    )

    # Match Polish price formats:
    #
    # 799
    # 799,00
    # 1 299
    # 1 299,00
    # 1 299,00

    match = re.search(
        r"\d{1,3}(?:[\s\u00a0\u202f]\d{3})*(?:[,.]\d{1,2})?",
        text
    )

    if not match:
        return None

    price_text = match.group(0)

    # Remove normal / non-breaking / narrow spaces
    price_text = (
        price_text
        .replace(" ", "")
        .replace("\u00a0", "")
        .replace("\u202f", "")
        .replace(",", ".")
    )

    try:
        return float(price_text)

    except ValueError:
        return None


# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = (
        str(title)
        .lower()
        .replace("\u00a0", " ")
    )

    # --------------------------------------------------------
    # Marketing colors first
    # --------------------------------------------------------

    if "glacier blue" in title_lower:
        return "Blue"

    elif "ocean blue" in title_lower:
        return "Blue"

    elif "sky blue" in title_lower:
        return "Blue"

    elif "ice blue" in title_lower:
        return "Blue"

    elif "ocean teal" in title_lower:
        return "Green"

    elif "forest green" in title_lower:
        return "Green"

    elif "midnight black" in title_lower:
        return "Black"

    elif "aurora purple" in title_lower:
        return "Purple"

    elif "mocha brown" in title_lower:
        return "Brown"

    # --------------------------------------------------------
    # English basic colors
    # --------------------------------------------------------

    elif re.search(r"\bblack\b", title_lower):
        return "Black"

    elif re.search(r"\bgreen\b", title_lower):
        return "Green"

    elif re.search(r"\bblue\b", title_lower):
        return "Blue"

    elif re.search(r"\bwhite\b", title_lower):
        return "White"

    elif re.search(r"\bgray\b", title_lower):
        return "Grey"

    elif re.search(r"\bgrey\b", title_lower):
        return "Grey"

    elif re.search(r"\bpurple\b", title_lower):
        return "Purple"

    elif re.search(r"\bsilver\b", title_lower):
        return "Silver"

    elif re.search(r"\bgold\b", title_lower):
        return "Gold"

    elif re.search(r"\bpink\b", title_lower):
        return "Pink"

    elif re.search(r"\bbrown\b", title_lower):
        return "Brown"

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

    elif "szar" in title_lower:
        return "Grey"

    elif "srebr" in title_lower:
        return "Silver"

    elif "złot" in title_lower or "zlot" in title_lower:
        return "Gold"

    elif "fiolet" in title_lower:
        return "Purple"

    elif "róż" in title_lower or "roz" in title_lower:
        return "Pink"

    elif "brąz" in title_lower or "braz" in title_lower:
        return "Brown"

    elif "tytan" in title_lower:
        return "Titanium"

    else:
        return "Unknown"


# ============================================================
# PRODUCT MATCHING
# ============================================================

def normalize_product_text(text):

    text = (
        str(text)
        .lower()
        .replace("\u00a0", " ")
        .strip()
    )

    # Normalize Pro+
    text = re.sub(
        r"\bpro\s*\+",
        "pro+",
        text
    )

    # Replace punctuation with spaces
    text = re.sub(
        r"[/(),;:_\-]+",
        " ",
        text
    )

    # Keep letters, numbers, spaces and +
    text = re.sub(
        r"[^a-z0-9ąćęłńóśźż+\s]",
        " ",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def matches_product(title, product):

    title_normalized = normalize_product_text(
        title
    )

    target_normalized = normalize_product_text(
        product["name"]
    )

    print(
        "NORMALIZED TITLE:",
        title_normalized
    )

    print(
        "NORMALIZED TARGET:",
        target_normalized
    )

    # --------------------------------------------------------
    # 5G MATCHING
    # --------------------------------------------------------

    target_has_5g = bool(
        re.search(
            r"\b5g\b",
            target_normalized
        )
    )

    title_has_5g = bool(
        re.search(
            r"\b5g\b",
            title_normalized
        )
    )

    if target_has_5g != title_has_5g:

        print(
            "Product mismatch: 5G version does not match."
        )

        return False

    # Remove 5G before comparing core product names
    target_core = re.sub(
        r"\b5g\b",
        "",
        target_normalized
    )

    title_core = re.sub(
        r"\b5g\b",
        "",
        title_normalized
    )

    target_core = re.sub(
        r"\s+",
        " ",
        target_core
    ).strip()

    title_core = re.sub(
        r"\s+",
        " ",
        title_core
    ).strip()

    target_tokens = target_core.split()
    title_tokens = title_core.split()

    # --------------------------------------------------------
    # Find exact product-name sequence
    # --------------------------------------------------------

    for start in range(
        len(title_tokens) - len(target_tokens) + 1
    ):

        end = start + len(target_tokens)

        if (
            title_tokens[start:end]
            != target_tokens
        ):
            continue

        # ----------------------------------------------------
        # Prevent base model matching a different version
        #
        # Redmi Note 15
        # != Redmi Note 15 Pro
        # != Redmi Note 15 Pro+
        # ----------------------------------------------------

        if end < len(title_tokens):

            next_token = title_tokens[end]

            product_modifiers = {
                "pro",
                "pro+",
                "ultra",
                "max",
                "lite",
                "plus",
            }

            if next_token in product_modifiers:

                print(
                    "Product mismatch: additional model "
                    f"version '{next_token}'."
                )

                continue

        print(
            "Product name MATCH."
        )

        return True

    print(
        "Product name mismatch."
    )

    return False


# ============================================================
# RAM / STORAGE EXTRACTION
# ============================================================

def extract_ram_storage(title, card_text):

    # --------------------------------------------------------
    # Try card specifications first
    # --------------------------------------------------------

    ram_match = re.search(
        r"Pamięć RAM:\s*([0-9]+\s*GB)",
        card_text,
        re.IGNORECASE
    )

    storage_match = re.search(
        r"Pamięć wbudowana:\s*([0-9]+\s*GB)",
        card_text,
        re.IGNORECASE
    )

    ram = (
        ram_match.group(1)
        if ram_match
        else None
    )

    storage = (
        storage_match.group(1)
        if storage_match
        else None
    )

    # --------------------------------------------------------
    # Fallback: title format
    #
    # Example:
    # Xiaomi Redmi Note 15 8/256GB
    # --------------------------------------------------------

    if not ram or not storage:

        title_match = re.search(
            r"\b([0-9]+)\s*/\s*([0-9]+)\s*GB\b",
            title,
            re.IGNORECASE
        )

        if title_match:

            if not ram:
                ram = (
                    title_match.group(1)
                    + " GB"
                )

            if not storage:
                storage = (
                    title_match.group(2)
                    + " GB"
                )

    return ram, storage


# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price(card):

    # --------------------------------------------------------
    # Main X-KOM price selector
    # --------------------------------------------------------

    price_element = card.locator(
        '[data-name="productPrice"] '
        'span[aria-label^="Cena:"]'
    ).first

    if price_element.count() > 0:

        aria_label = price_element.get_attribute(
            "aria-label"
        )

        price = clean_price(
            aria_label
        )

        if price is not None:
            return price

    # --------------------------------------------------------
    # Fallback: any aria-label containing Cena
    # --------------------------------------------------------

    price_element = card.locator(
        'span[aria-label*="Cena"]'
    ).first

    if price_element.count() > 0:

        aria_label = price_element.get_attribute(
            "aria-label"
        )

        price = clean_price(
            aria_label
        )

        if price is not None:
            return price

    # --------------------------------------------------------
    # Final fallback: card text
    # --------------------------------------------------------

    card_text = (
        card
        .inner_text()
        .strip()
    )

    # Look for a price followed by zł
    match = re.search(
        r"\d{1,3}(?:[\s\u00a0\u202f]\d{3})*(?:[,.]\d{1,2})?\s*zł",
        card_text,
        re.IGNORECASE
    )

    if match:

        return clean_price(
            match.group(0)
        )

    return None


# ============================================================
# AVAILABILITY
# ============================================================

def get_availability(card_text):

    card_text_lower = (
        card_text
        .lower()
    )

    # --------------------------------------------------------
    # Explicitly unavailable
    # --------------------------------------------------------

    unavailable_terms = [

        "produkt niedostępny",

        "chwilowo niedostępny",

        "brak w magazynie",

        "niedostępny",

    ]

    for term in unavailable_terms:

        if term in card_text_lower:

            return "Unavailable"

    # --------------------------------------------------------
    # Explicitly available
    # --------------------------------------------------------

    available_terms = [

        "dodaj do koszyka",

        "dostępny",

        "dostepny",

        "kup teraz",

        "w magazynie",

    ]

    for term in available_terms:

        if term in card_text_lower:

            return "Available"

    # --------------------------------------------------------
    # X-KOM search results with a valid current price are
    # normally purchasable products.
    # --------------------------------------------------------

    return "Unknown"


# ============================================================
# PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    print(
        "Waiting for X-kom products..."
    )

    # --------------------------------------------------------
    # Product cards
    # --------------------------------------------------------

    cards = page.locator(
        'div[data-name="productCard"]'
    )

    cards.first.wait_for(
        state="visible",
        timeout=30000
    )

    print(
        "X-kom product cards:",
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

    print(
        "Target RAM:",
        target_ram
    )

    print(
        "Target Storage:",
        target_storage
    )

    print(
        "Target Product:",
        product["name"]
    )

    # --------------------------------------------------------
    # Track matching configuration
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
                "X-KOM PRODUCT",
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

            # ------------------------------------------------
            # Card text
            # ------------------------------------------------

            card_text = (
                card
                .inner_text()
                .strip()
            )

            # ------------------------------------------------
            # RAM / Storage
            # ------------------------------------------------

            ram, storage = extract_ram_storage(
                title,
                card_text
            )

            print(
                "RAM:",
                ram
            )

            print(
                "STORAGE:",
                storage
            )

            if not ram or not storage:

                print(
                    "RAM / Storage not found."
                )

                continue

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
                    "RAM / Storage mismatch."
                )

                continue

            print(
                "RAM / STORAGE MATCH: YES"
            )

            # ------------------------------------------------
            # Matching configuration found
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

            availability = get_availability(
                card_text
            )

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
            # If X-KOM has a valid price but no explicit
            # availability information, treat it as Available.
            # ------------------------------------------------

            if (
                availability == "Unknown"
                and price is not None
            ):

                availability = "Available"

                print(
                    "AVAILABILITY updated to: Available "
                    "(valid price found)"
                )

            # ------------------------------------------------
            # SAVE RESULT
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

            results.append(
                result
            )

        except Exception as e:

            print(
                "ERROR PROCESSING X-KOM CARD:",
                i,
                str(e)
            )

            continue

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not product_found:

        print()
        print("=" * 60)
        print(
            "X-KOM: TARGET PRODUCT/CONFIGURATION NOT FOUND"
        )
        print("=" * 60)

        results.append({

            "product_name":
                product["name"],

            "variant":
                "Unknown",

            "ram":
                f"{target_ram} GB",

            "storage":
                f"{target_storage} GB",

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
        "X-KOM RESULTS:",
        len(results)
    )
    print("=" * 60)

    for result in results:

        print(result)

    return results


# ============================================================
# UNIFIED SCRAPER INTERFACE
# ============================================================

def get_price(page, product):

    return get_products(
        page,
        product
    )