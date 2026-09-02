import re


print(
    "NEONET MODULE PATH:",
    __file__
)


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = (
        str(text)
        .replace("\u00a0", " ")
        .strip()
    )

    # --------------------------------------------------------
    # Normal price
    #
    # Examples:
    #
    # 1 899.00 PLN
    # 1899,99 zł
    # 1899.00 zł
    # --------------------------------------------------------

    matches = re.findall(
        r"(\d[\d\s]*[,.]\d{2})\s*(?:PLN|zł)",
        text,
        re.IGNORECASE
    )

    if matches:

        # Usually the first real price with currency is the
        # current product price.
        value = (
            matches[0]
            .replace(" ", "")
            .replace(",", ".")
        )

        try:
            return float(value)

        except ValueError:
            pass

    # --------------------------------------------------------
    # Split price
    #
    # Example:
    #
    # 1 899
    # 00
    # PLN
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*)\s+(\d{2})\s*(?:PLN|zł)",
        text,
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
    # Integer price with currency
    #
    # Example:
    #
    # 1899 PLN
    # 899 zł
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*)\s*(?:PLN|zł)",
        text,
        re.IGNORECASE
    )

    if match:

        value = (
            match.group(1)
            .replace(" ", "")
        )

        try:
            return float(value)

        except ValueError:
            pass

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

    elif "midnight black" in title_lower:
        return "Black"

    elif "mocha brown" in title_lower:
        return "Brown"

    elif "forest green" in title_lower:
        return "Green"

    elif "aurora purple" in title_lower:
        return "Purple"

    elif "ocean teal" in title_lower:
        return "Green"

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
        return "Grey"

    elif re.search(r"\bsilver\b", title_lower):
        return "Silver"

    elif re.search(r"\bgold\b", title_lower):
        return "Gold"

    elif re.search(r"\bpurple\b", title_lower):
        return "Purple"

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

    # --------------------------------------------------------
    # Normalize Pro+
    # --------------------------------------------------------

    text = re.sub(
        r"\bpro\s*\+",
        "pro+",
        text
    )

    # --------------------------------------------------------
    # Remove common punctuation
    # --------------------------------------------------------

    text = re.sub(
        r"[/(),;:_\-]+",
        " ",
        text
    )

    # --------------------------------------------------------
    # Keep letters, numbers, spaces and +
    # --------------------------------------------------------

    text = re.sub(
        r"[^a-z0-9ąćęłńóśźż+\s]",
        " ",
        text
    )

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
    # 5G matching
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

    # --------------------------------------------------------
    # Remove 5G for product-name comparison
    # --------------------------------------------------------

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
    # Find exact product token sequence
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
        # Prevent base model matching Pro / Pro+ / Ultra etc.
        #
        # Example:
        #
        # Redmi Note 15
        #
        # must NOT match:
        #
        # Redmi Note 15 Pro
        # Redmi Note 15 Pro+
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
                    "Product mismatch: additional "
                    f"model version '{next_token}'."
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
# RAM / STORAGE
# ============================================================

def get_configuration_from_title(title):

    title = str(title)

    # --------------------------------------------------------
    # Examples:
    #
    # 8/256 GB
    # 8/256GB
    # 4 / 128 GB
    # --------------------------------------------------------

    match = re.search(
        r"(\d+)\s*/\s*(\d+)\s*GB",
        title,
        re.IGNORECASE
    )

    if match:

        return (
            match.group(1) + " GB",
            match.group(2) + " GB"
        )

    return None, None


def get_ram(text):

    match = re.search(
        r"Pamięć\s+RAM:\s*(\d+)\s*GB",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1) + " GB"

    return "Unknown"


def get_storage(text):

    match = re.search(
        r"Pamięć\s+wbudowana:\s*(\d+)\s*GB",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1) + " GB"

    return "Unknown"


# ============================================================
# AVAILABILITY
# ============================================================

def get_availability(text):

    if not text:
        return "Unknown"

    text_lower = (
        str(text)
        .lower()
        .replace("\u00a0", " ")
    )

    # --------------------------------------------------------
    # Explicitly unavailable FIRST
    # --------------------------------------------------------

    unavailable_phrases = [

        "chwilowo niedostępny",
        "chwilowo niedostępna",
        "produkt niedostępny",
        "produkt niedostępna",
        "niedostępny",
        "niedostępna",
        "brak w magazynie",
        "out of stock",
        "unavailable",

    ]

    for phrase in unavailable_phrases:

        if phrase in text_lower:

            return "Unavailable"

    # --------------------------------------------------------
    # Explicitly available
    # --------------------------------------------------------

    available_phrases = [

        "dodaj do koszyka",
        "add to cart",
        "do koszyka",
        "ostatnie sztuki",
        "available",
        "dostępny",
        "dostępna",
        "wysyłka",
        "free shipping",

    ]

    for phrase in available_phrases:

        if phrase in text_lower:

            return "Available"

    return "Unknown"


# ============================================================
# FIND PRODUCT CARD
# ============================================================

def find_product_card(heading):

    # --------------------------------------------------------
    # Move upwards from the H3.
    #
    # We want the smallest ancestor that looks like one
    # product card, rather than a large container containing
    # several products.
    # --------------------------------------------------------

    for level in range(1, 10):

        try:

            candidate = heading.locator(
                "xpath=" + "/.." * level
            )

            candidate_text = (
                candidate
                .inner_text()
                .strip()
            )

            if not candidate_text:
                continue

            candidate_text_lower = (
                candidate_text
                .lower()
                .replace("\u00a0", " ")
            )

            # ------------------------------------------------
            # Check how many H3 titles are inside.
            #
            # A real product card should normally contain only
            # one product title.
            # ------------------------------------------------

            h3_count = candidate.locator(
                "h3"
            ).count()

            if h3_count > 1:
                continue

            # ------------------------------------------------
            # Product card indicators
            # ------------------------------------------------

            indicators = [

                "pln",
                "zł",
                "dodaj do koszyka",
                "add to cart",
                "niedostępny",
                "dostępny",
                "free shipping",
                "price",

            ]

            if any(
                indicator in candidate_text_lower
                for indicator in indicators
            ):

                print(
                    "Product card found at level:",
                    level
                )

                return candidate

        except Exception:

            continue

    return None


# ============================================================
# GET PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    # --------------------------------------------------------
    # Track whether the correct product + configuration
    # was found
    # --------------------------------------------------------

    product_found = False

    print(
        "Waiting for NEONET products..."
    )

    # ========================================================
    # TARGET RAM / STORAGE
    # ========================================================

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

    # ========================================================
    # WAIT FOR PRODUCT HEADINGS
    # ========================================================

    try:

        page.wait_for_selector(
            "h3",
            timeout=15000
        )

    except Exception:

        print(
            "Could not find NEONET product headings."
        )

        return [
            {
                "product_name": product["name"],
                "variant": "Unknown",
                "ram": str(product["ram"]) + " GB",
                "storage": str(product["storage"]) + " GB",
                "price": None,
                "availability": "Unavailable"
            }
        ]

    # ========================================================
    # FIND H3 ELEMENTS
    # ========================================================

    headings = page.locator(
        "h3"
    )

    count = headings.count()

    print(
        "Total NEONET H3:",
        count
    )

    # ========================================================
    # LOOP THROUGH H3
    # ========================================================

    for i in range(count):

        heading = headings.nth(i)

        try:

            title = (
                heading
                .inner_text()
                .strip()
            )

        except Exception:

            continue

        if not title:
            continue

        print()
        print("=" * 60)
        print(
            "NEONET PRODUCT",
            i
        )
        print("=" * 60)

        print(
            "TITLE:",
            title
        )

        # ====================================================
        # PRODUCT NAME MATCHING
        # ====================================================

        if not matches_product(
            title,
            product
        ):

            continue

        # ====================================================
        # FIND PRODUCT INFORMATION CONTAINER
        #
        # Keep the previous NEONET logic here.
        #
        # We first find an ancestor containing actual product
        # information, then use its parent as the full card.
        # ====================================================

        container = None

        for level in range(1, 9):

            try:

                candidate = heading.locator(
                    "xpath=" + "/.." * level
                )

                candidate_text = (
                    candidate
                    .inner_text()
                    .strip()
                )

                if not candidate_text:
                    continue

                candidate_text_normalized = (
                    candidate_text
                    .lower()
                    .replace("\u00a0", " ")
                )

                candidate_text_normalized = re.sub(
                    r"\s+",
                    " ",
                    candidate_text_normalized
                )

                # ------------------------------------------------
                # The container should contain product information.
                #
                # We do NOT require RAM/storage here because some
                # products, such as Redmi A7 Pro, may not display
                # configuration in the title/container in the same
                # way as other products.
                # ------------------------------------------------

                product_indicators = [

                    "pamięć ram",
                    "pamięć wbudowana",
                    "cena",
                    "zł",
                    "pln",
                    "dodaj do koszyka",
                    "kup teraz",
                    "ostatnie sztuki",
                    "niedostępny",
                    "najwcześniej u ciebie",
                    "najwczesniej u ciebie",

                ]

                if any(
                    indicator in candidate_text_normalized
                    for indicator in product_indicators
                ):

                    # Avoid very large containers containing
                    # multiple product titles.

                    h3_count = candidate.locator(
                        "h3"
                    ).count()

                    if h3_count > 1:
                        continue

                    container = candidate

                    print(
                        "Product container found at level:",
                        level
                    )

                    break

            except Exception:

                continue

        # ====================================================
        # CONTAINER NOT FOUND
        # ====================================================

        if container is None:

            print(
                "Could not find product container."
            )

            continue

        # ====================================================
        # FULL PRODUCT CARD
        # ====================================================

        try:

            product_card = container.locator(
                "xpath=.."
            )

            card_text = (
                product_card
                .inner_text()
                .strip()
            )

            # ------------------------------------------------
            # Safety check:
            #
            # If the parent contains multiple H3 products,
            # use the container itself instead.
            # ------------------------------------------------

            parent_h3_count = product_card.locator(
                "h3"
            ).count()

            if parent_h3_count > 1:

                product_card = container

                card_text = (
                    container
                    .inner_text()
                    .strip()
                )

        except Exception:

            product_card = container

            card_text = (
                container
                .inner_text()
                .strip()
            )

        # ====================================================
        # DEBUG: FULL CARD TEXT
        # ====================================================

        print()
        print(
            "NEONET FULL CARD TEXT:"
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

        # ====================================================
        # EXTRACT RAM / STORAGE
        #
        # IMPORTANT:
        #
        # Extract from the actual product card, NOT only from
        # the title.
        #
        # This fixes products such as Redmi A7 Pro where the
        # title does not contain 4/64.
        # ====================================================

        ram = get_ram(
            card_text
        )

        storage = get_storage(
            card_text
        )

        print(
            "Detected RAM:",
            ram
        )

        print(
            "Detected Storage:",
            storage
        )

        # ====================================================
        # MATCH TARGET RAM / STORAGE
        # ====================================================

        ram_number = re.sub(
            r"\D",
            "",
            str(ram)
        )

        storage_number = re.sub(
            r"\D",
            "",
            str(storage)
        )

        if (
            ram_number != target_ram
            or
            storage_number != target_storage
        ):

            print(
                "RAM / Storage mismatch:",
                ram,
                storage
            )

            continue

        print(
            "RAM / Storage MATCH."
        )

        # ====================================================
        # CORRECT PRODUCT FOUND
        # ====================================================

        product_found = True

        # ====================================================
        # COLOR
        # ====================================================

        color = get_color(
            title
        )

        print(
            "COLOR:",
            color
        )

        # ====================================================
        # AVAILABILITY
        #
        # Use the full product card.
        # ====================================================

        availability = get_availability(
            card_text
        )

        print(
            "AVAILABILITY:",
            availability
        )

        # ====================================================
        # PRICE
        #
        # Use the full product card.
        # ====================================================

        price = clean_price(
            card_text
        )

        print(
            "PRICE:",
            price
        )

        # ====================================================
        # RESULT
        # ====================================================

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

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not product_found:

        print()
        print("=" * 60)

        print(
            "NEONET: Target product/configuration not found."
        )

        print(
            "Product:",
            product["name"]
        )

        print(
            "RAM:",
            product["ram"]
        )

        print(
            "Storage:",
            product["storage"]
        )

        print("=" * 60)

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
        "NEONET RESULTS:",
        len(results)
    )

    print("=" * 60)

    for result in results:

        print(
            result
        )

    return results

# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def get_price_results(page, product):

    return get_products(
        page,
        product
    )


def get_price(page, product):

    return get_products(
        page,
        product
    )