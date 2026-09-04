import re


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = str(text).strip()

    text = text.replace("\xa0", " ")

    # Remove spaces
    text = text.replace(" ", "")

    # Keep only digits, comma and dot
    text = re.sub(
        r"[^0-9,.]",
        "",
        text
    )

    if not text:
        return None

    # Polish decimal format
    if "," in text and "." not in text:

        text = text.replace(",", ".")

    # Both thousand separator and decimal separator
    elif "," in text and "." in text:

        # Example: 1.299,99
        if text.rfind(",") > text.rfind("."):

            text = text.replace(".", "")
            text = text.replace(",", ".")

        # Example: 1,299.99
        else:

            text = text.replace(",", "")

    try:

        return float(text)

    except ValueError:

        return None


# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = (
        str(title)
        .lower()
        .replace("\xa0", " ")
    )

    # --------------------------------------------------------
    # Marketing / combined color names
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
    # Polish colors
    # --------------------------------------------------------

    color_map = {

        "czarn": "Black",

        "zielon": "Green",

        "niebiesk": "Blue",

        "biały": "White",
        "bialy": "White",

        "szar": "Grey",

        "srebr": "Silver",

        "złot": "Gold",
        "zlot": "Gold",

        "fiolet": "Purple",

        "róż": "Pink",
        "roz": "Pink",

        "brąz": "Brown",
        "braz": "Brown",

        "tytan": "Titanium",
    }

    for polish_color, english_color in color_map.items():

        if polish_color in title_lower:

            return english_color

    # --------------------------------------------------------
    # English colors
    # --------------------------------------------------------

    if re.search(r"\bblack\b", title_lower):
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

    return "Unknown"


# ============================================================
# PRODUCT MATCHING
# ============================================================

def normalize_product_text(text):

    text = (
        str(text)
        .lower()
        .replace("\xa0", " ")
        .strip()
    )

    # Normalize Pro+
    text = re.sub(
        r"\bpro\s*\+",
        "pro+",
        text
    )

    # Replace common punctuation with spaces
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

    # ========================================================
    # SPECIAL CASE:
    # Xiaomi 17 family
    #
    # Ignore 5G naming difference for Xiaomi 17 family,
    # but NOT Xiaomi 17T family.
    # ========================================================

    xiaomi_17_family = (
        target_normalized.startswith("xiaomi 17")
        and
        not target_normalized.startswith("xiaomi 17t")
    )

    # ========================================================
    # SPECIAL CASE:
    # POCO X8 family
    #
    # Ignore 5G naming difference.
    # ========================================================

    poco_x8_family = (
        target_normalized.startswith("poco x8")
    )

    ignore_5g_difference = (
        xiaomi_17_family
        or
        poco_x8_family
    )

    # ========================================================
    # STYLUS / BUNDLE MATCHING
    #
    # Do not mix:
    #
    # Xiaomi Pad 8
    #
    # with:
    #
    # Xiaomi Pad 8 + Stylus
    # Xiaomi Pad 8 with Stylus
    # ========================================================

    target_has_stylus = bool(
        re.search(
            r"\bstylus\b",
            target_normalized
        )
    )

    title_has_stylus = bool(
        re.search(
            r"\bstylus\b",
            title_normalized
        )
    )

    if target_has_stylus != title_has_stylus:

        print(
            "Product mismatch: Stylus bundle does not match."
        )

        return False

    # ========================================================
    # 4G / LTE MATCHING
    #
    # IMPORTANT:
    #
    # Do NOT apply this rule globally.
    #
    # Only protect the base Redmi Pad 2 from being mixed
    # with Redmi Pad 2 4G / LTE versions.
    # ========================================================

    is_base_redmi_pad_2 = bool(
        re.fullmatch(
            r"redmi pad 2",
            target_normalized
        )
    )

    if is_base_redmi_pad_2:

        title_has_lte_or_4g = bool(
            re.search(
                r"\b(?:4g|lte)\b",
                title_normalized
            )
        )

        target_has_lte_or_4g = bool(
            re.search(
                r"\b(?:4g|lte)\b",
                target_normalized
            )
        )

        if target_has_lte_or_4g != title_has_lte_or_4g:

            print(
                "Product mismatch: Redmi Pad 2 connectivity "
                "version does not match."
            )

            return False

    # ========================================================
    # 5G MATCHING
    #
    # Strict for normal products.
    #
    # Ignore only for:
    # - Xiaomi 17 family
    # - POCO X8 family
    # ========================================================

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

    if not ignore_5g_difference:

        if target_has_5g != title_has_5g:

            print(
                "Product mismatch: 5G version does not match."
            )

            return False

    else:

        print(
            "SPECIAL PRODUCT FAMILY: "
            "ignoring 5G difference."
        )

    print(
        "CONNECTIVITY MATCH: YES"
    )

    # ========================================================
    # REMOVE CONNECTIVITY WORDS FOR PRODUCT NAME MATCHING
    #
    # We already checked them above.
    #
    # Remove:
    # - 5G
    # - 4G
    # - LTE
    # ========================================================

    title_core = re.sub(
        r"\b(?:5g|4g|lte)\b",
        "",
        title_normalized
    )

    target_core = re.sub(
        r"\b(?:5g|4g|lte)\b",
        "",
        target_normalized
    )

    title_core = re.sub(
        r"\s+",
        " ",
        title_core
    ).strip()

    target_core = re.sub(
        r"\s+",
        " ",
        target_core
    ).strip()

    title_tokens = title_core.split()

    target_tokens = target_core.split()

    # ========================================================
    # PRODUCT MODIFIERS
    #
    # Prevent shorter products from matching longer versions.
    #
    # Example:
    #
    # Redmi Pad 2
    #
    # must NOT match:
    #
    # Redmi Pad 2 Pro
    # Redmi Pad 2 Pro 5G
    # ========================================================

    product_modifiers = {
        "pro",
        "pro+",
        "ultra",
        "max",
        "lite",
        "plus",
    }

    # ========================================================
    # FIND PRODUCT TOKENS IN ORDER
    #
    # Allow specifications between product-name words.
    #
    # Example:
    #
    # Target:
    # Redmi Pad 2 Pro 5G
    #
    # Website:
    # Redmi Pad 2 Pro 12 1 5G 6GB 128GB
    #
    # ========================================================

    position = 0

    matched_positions = []

    for target_token in target_tokens:

        found = False

        while position < len(title_tokens):

            if title_tokens[position] == target_token:

                matched_positions.append(
                    position
                )

                position += 1

                found = True

                break

            position += 1

        if not found:

            print(
                "Product name mismatch."
            )

            return False

    # ========================================================
    # PREVENT SHORTER MODEL MATCHING LONGER MODEL
    #
    # Check the word immediately after the last matched
    # product-name token.
    # ========================================================

    if matched_positions:

        last_position = matched_positions[-1]

        if last_position + 1 < len(title_tokens):

            next_token = title_tokens[
                last_position + 1
            ]

            if next_token in product_modifiers:

                # Only reject if that modifier is NOT already
                # part of the target product name.
                if next_token not in target_tokens:

                    print(
                        "Product mismatch: website title has "
                        f"additional model version '{next_token}'."
                    )

                    return False

    print(
        "PRODUCT NAME MATCH: YES"
    )

    return True


# ============================================================
# STORAGE NORMALIZATION
# ============================================================

def normalize_storage(value):

    if value is None:
        return None

    text = (
        str(value)
        .upper()
        .replace(" ", "")
    )

    # 1T / 1TB -> 1000
    match = re.fullmatch(
        r"(\d+)(T|TB)",
        text
    )

    if match:

        return str(
            int(match.group(1)) * 1000
        )

    # 512 / 512GB -> 512
    match = re.search(
        r"\d+",
        text
    )

    if match:

        return match.group()

    return None


# ============================================================
# MEMORY EXTRACTION
# ============================================================

def extract_memory(text):

    if not text:
        return None, None

    text = (
        str(text)
        .replace("\xa0", " ")
    )

    # --------------------------------------------------------
    # Supported formats:
    #
    # 12GB/512GB
    # 12 GB / 512 GB
    # 12GB 512GB
    # 12 GB 512 GB
    # 12/512
    #
    # Also:
    #
    # 12+512GB
    # 12 GB + 512 GB
    # 12GB+512GB
    # --------------------------------------------------------

    patterns = [

        # 12 GB / 512 GB
        r"\b(\d+)\s*GB\s*/\s*(\d+)\s*(GB|TB|T)\b",

        # 12 GB + 512 GB
        r"\b(\d+)\s*GB\s*\+\s*(\d+)\s*(GB|TB|T)\b",

        # 12+512GB
        r"\b(\d+)\s*\+\s*(\d+)\s*(GB|TB|T)\b",

        # 12GB 512GB
        r"\b(\d+)\s*GB\s+(\d+)\s*(GB|TB|T)\b",

        # 12 / 512 GB
        r"\b(\d+)\s*/\s*(\d+)\s*(GB|TB|T)\b",

        # 12/512
        r"\b(\d+)\s*/\s*(\d+)\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if not match:
            continue

        ram = match.group(1)

        storage_value = match.group(2)

        # Some patterns have a storage unit,
        # while 12/512 does not.
        storage_unit = (
            match.group(3)
            if len(match.groups()) >= 3
            else "GB"
        )

        if storage_unit:

            storage_unit = storage_unit.upper()

        else:

            storage_unit = "GB"

        if storage_unit in ("TB", "T"):

            storage = str(
                int(storage_value) * 1000
            )

        else:

            storage = storage_value

        return ram, storage

    return None, None


# ============================================================
# AVAILABILITY
# ============================================================

def get_availability(card_text):

    text = (
        str(card_text)
        .lower()
    )

    # --------------------------------------------------------
    # Explicitly unavailable
    # --------------------------------------------------------

    unavailable_phrases = [

        "niestety dostawa nie jest możliwa",

        "produkt niedostępny",

        "chwilowo niedostępny",

        "niedostępny online",

        "brak dostępności",

        "brak w magazynie",
    ]

    for phrase in unavailable_phrases:

        if phrase in text:

            return "Unavailable"

    # --------------------------------------------------------
    # Explicitly available
    # --------------------------------------------------------

    available_phrases = [

        "dostępny online",

        "available online",

        "place your order",

        "złóż zamówienie",

        "dostarczymy",

        "dostawa już jutro",

        "dodaj do koszyka",
    ]

    for phrase in available_phrases:

        if phrase in text:

            return "Available"

    return "Unknown"


# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price(card):

    card_text = (
        card
        .inner_text()
        .strip()
    )

    # Examples:
    #
    # 399,99 zł
    # 799,00 zł
    # 1 299,00 zł
    # 1.299,00 zł

    price_matches = re.findall(
        r"\b\d{1,5}(?:[ .]\d{3})*[,.]\d{2}\s*zł\b",
        card_text,
        re.IGNORECASE
    )

    if not price_matches:

        return None

    return clean_price(
        price_matches[0]
    )


# ============================================================
# FALLBACK STORAGE FORMAT
# ============================================================

def format_storage(value):

    text = str(value).strip()

    if text.upper() in (
        "1T",
        "1TB"
    ):

        return "1 TB"

    if re.fullmatch(
        r"\d+",
        text
    ):

        return text + " GB"

    return text


# ============================================================
# PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    product_found = False

    print(
        "Waiting for MediaMarkt products..."
    )

    # --------------------------------------------------------
    # Product cards
    # --------------------------------------------------------

    cards = page.locator(
        'article[data-test="mms-product-card"]'
    )

    count = cards.count()

    print(
        "MediaMarkt product cards:",
        count
    )

    if count == 0:

        print(
            "No MediaMarkt product cards found."
        )

        return results

    # --------------------------------------------------------
    # Target RAM / Storage
    # --------------------------------------------------------

    target_ram = re.sub(
        r"\D",
        "",
        str(product["ram"])
    )

    target_storage = normalize_storage(
        product["storage"]
    )

    print(
        "TARGET PRODUCT:",
        product["name"]
    )

    print(
        "TARGET RAM:",
        target_ram
    )

    print(
        "TARGET STORAGE:",
        target_storage,
        "GB"
    )

    # --------------------------------------------------------
    # Count matching genuine product cards
    #
    # Used only for safe fallback when MediaMarkt does not
    # display RAM/storage in the title.
    # --------------------------------------------------------

    matching_cards = []

    for i in range(count):

        card = cards.nth(i)

        links = card.locator("a")

        for j in range(links.count()):

            try:

                text = (
                    links.nth(j)
                    .inner_text()
                    .strip()
                )

            except Exception:

                continue

            if not text:

                continue

            if matches_product(
                text,
                product
            ):

                matching_cards.append(i)

                break

    print(
        "MATCHING PRODUCT CARDS:",
        matching_cards
    )

    # --------------------------------------------------------
    # Process cards
    # --------------------------------------------------------

    for i in range(count):

        card = cards.nth(i)

        print()
        print("=" * 60)

        print(
            "MEDIAMARKT CARD",
            i
        )

        print("=" * 60)

        try:

            # ------------------------------------------------
            # Find matching product title
            # ------------------------------------------------

            links = card.locator("a")

            title = ""

            for j in range(links.count()):

                link = links.nth(j)

                try:

                    text = (
                        link
                        .inner_text()
                        .strip()
                    )

                except Exception:

                    continue

                if not text:

                    continue

                if matches_product(
                    text,
                    product
                ):

                    title = text

                    break

            if not title:

                print(
                    "Matching product title not found."
                )

                continue

            print(
                "TITLE:",
                title
            )

            # ------------------------------------------------
            # CARD TEXT
            # ------------------------------------------------

            card_text = (
                card
                .inner_text()
                .strip()
            )

            # ------------------------------------------------
            # Extract RAM/storage
            #
            # First try title.
            # Then try complete card text.
            # ------------------------------------------------

            ram, storage = extract_memory(
                title
            )

            if ram is None:

                print(
                    "RAM/storage not found in title."
                )

                print(
                    "Trying complete card text..."
                )

                ram, storage = extract_memory(
                    card_text
                )

            # ------------------------------------------------
            # SAFE FALLBACK
            #
            # Some MediaMarkt cards do not display memory.
            #
            # Only use target configuration when there is
            # exactly one matching genuine product card.
            # ------------------------------------------------

            if ram is None:

                if len(matching_cards) == 1:

                    print(
                        "MEMORY NOT DISPLAYED ON CARD."
                    )

                    print(
                        "SAFE FALLBACK: only one matching "
                        "product card found."
                    )

                    ram = target_ram

                    storage = target_storage

                else:

                    print(
                        "RAM/storage not found and fallback "
                        "is not safe."
                    )

                    continue

            actual_ram = re.sub(
                r"\D",
                "",
                str(ram)
            )

            actual_storage = normalize_storage(
                storage
            )

            print(
                "ACTUAL RAM:",
                actual_ram
            )

            print(
                "ACTUAL STORAGE:",
                actual_storage,
                "GB"
            )

            # ------------------------------------------------
            # Match RAM / Storage
            # ------------------------------------------------

            if (
                actual_ram != target_ram
                or
                actual_storage != target_storage
            ):

                print(
                    "RAM/storage does not match."
                )

                continue

            print(
                "RAM/STORAGE MATCH: YES"
            )

            # ------------------------------------------------
            # Target product found
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
            # SAVE RESULT
            # ------------------------------------------------

            result = {

                "product_name":
                    product["name"],

                "variant":
                    color,

                "ram":
                    actual_ram,

                "storage":
                    actual_storage,

                "price":
                    price,

                "availability":
                    availability,
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
                "ERROR PROCESSING CARD:",
                i,
                str(e)
            )

            continue

    # ========================================================
    # TARGET PRODUCT NOT FOUND
    # ========================================================

    if not product_found:

        print()
        print("=" * 60)

        print(
            "Target product not found on MediaMarkt."
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
                format_storage(
                    product["storage"]
                ),

            "price":
                None,

            "availability":
                "Unavailable",
        })

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 60)

    print(
        "MEDIAMARKT RESULTS:",
        len(results)
    )

    print("=" * 60)

    for result in results:

        print(
            result
        )

    return results


# ============================================================
# UNIFIED SCRAPER INTERFACE
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