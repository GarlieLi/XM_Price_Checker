import re


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    text = str(text).strip()

    # Polish non-breaking spaces
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

        # Example:
        # 1.299,99
        if text.rfind(",") > text.rfind("."):

            text = text.replace(".", "")
            text = text.replace(",", ".")

        # Example:
        # 1,299.99
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
    # XIAOMI 17 FAMILY
    #
    # MediaMarkt may add "5G" to:
    # Xiaomi 17
    # Xiaomi 17 Ultra
    #
    # Our product names may not contain 5G.
    #
    # ONLY ignore the 5G difference for the Xiaomi 17 family.
    # ========================================================

    xiaomi_17_family = (
        target_normalized.startswith("xiaomi 17")
        and
        not target_normalized.startswith("xiaomi 17t")
    )

    if xiaomi_17_family:

        target_normalized = re.sub(
            r"\b5g\b",
            "",
            target_normalized
        )

        title_normalized = re.sub(
            r"\b5g\b",
            "",
            title_normalized
        )

        target_normalized = re.sub(
            r"\s+",
            " ",
            target_normalized
        ).strip()

        title_normalized = re.sub(
            r"\s+",
            " ",
            title_normalized
        ).strip()

        print(
            "XIAOMI 17 FAMILY: ignoring 5G difference."
        )

        print(
            "NORMALIZED TARGET AFTER 5G RULE:",
            target_normalized
        )

        print(
            "NORMALIZED TITLE AFTER 5G RULE:",
            title_normalized
        )

    # ========================================================
    # STRICT TOKEN MATCHING
    # ========================================================

    target_tokens = target_normalized.split()

    title_tokens = title_normalized.split()

    product_modifiers = {
        "pro",
        "pro+",
        "ultra",
        "max",
        "lite",
        "plus",
        "5g",
    }

    for start in range(
        len(title_tokens) - len(target_tokens) + 1
    ):

        end = start + len(target_tokens)

        # Exact token sequence required
        if (
            title_tokens[start:end]
            != target_tokens
        ):

            continue

        # ----------------------------------------------------
        # Prevent matching an upgraded/different version
        # ----------------------------------------------------

        if end < len(title_tokens):

            next_token = title_tokens[end]

            if next_token in product_modifiers:

                print(
                    "Product mismatch: website title has "
                    f"additional model version '{next_token}'."
                )

                continue

        print(
            "PRODUCT NAME MATCH: YES"
        )

        return True

    print(
        "Product name mismatch."
    )

    return False


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
    ]

    for phrase in available_phrases:

        if phrase in text:

            return "Available"

    # --------------------------------------------------------
    # Add to cart
    # --------------------------------------------------------

    if (
        "dodaj do koszyka" in text
        or
        "add to cart" in text
    ):

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

    # --------------------------------------------------------
    # Find normal decimal prices
    #
    # Examples:
    # 399,99 zł
    # 799,00 zł
    # --------------------------------------------------------

    price_matches = re.findall(
        r"\b\d{1,5}(?:[ .]\d{3})*[,.]\d{2}\s*zł\b",
        card_text,
        re.IGNORECASE
    )

    if not price_matches:

        return None

    # --------------------------------------------------------
    # Use the first normal product price.
    #
    # Promotional amounts such as:
    # "120 zł do BP"
    #
    # do not have decimal places, so they are excluded.
    # --------------------------------------------------------

    price = clean_price(
        price_matches[0]
    )

    return price

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

    # --------------------------------------------------------
    # 1T / 1TB -> 1000
    # --------------------------------------------------------

    match = re.fullmatch(
        r"(\d+)(T|TB)",
        text
    )

    if match:

        return str(
            int(match.group(1)) * 1000
        )

    # --------------------------------------------------------
    # 512 / 512GB -> 512
    # --------------------------------------------------------

    match = re.search(
        r"\d+",
        text
    )

    if match:

        return match.group()

    return None

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

    # Normalize:
    # 512   -> 512
    # 512GB -> 512
    # 1T    -> 1000
    # 1TB   -> 1000
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
            # Find product title
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

                # ------------------------------------------------
                # Product matching
                # ------------------------------------------------

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
            # RAM / Storage
            #
            # Supported examples:
            #
            # 12 GB / 512 GB
            # 12GB/512GB
            # 12 / 512 GB
            # 12/512 GB
            #
            # 12 GB / 1 TB
            # 12GB/1TB
            # 12 / 1 TB
            # 12/1T
            # ------------------------------------------------

            memory_match = re.search(
                r"(\d+)\s*(?:GB)?\s*/\s*"
                r"(\d+)\s*(GB|TB|T)\b",
                title,
                re.IGNORECASE
            )

            if not memory_match:

                print(
                    "RAM/storage not found in title."
                )

                continue

            ram = memory_match.group(1)

            storage_value = (
                memory_match.group(2)
            )

            storage_unit = (
                memory_match.group(3)
                .upper()
            )

            # ------------------------------------------------
            # Convert TB / T to GB
            # ------------------------------------------------

            if storage_unit in (
                "TB",
                "T"
            ):

                storage = str(
                    int(storage_value) * 1000
                )

            else:

                storage = storage_value

            print(
                "RAM:",
                ram,
                "GB"
            )

            print(
                "STORAGE:",
                storage,
                "GB"
            )

            # ------------------------------------------------
            # Match RAM / Storage
            # ------------------------------------------------

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
            # CARD TEXT
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
                    ram,

                "storage":
                    storage,

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

        # Better formatting for fallback storage
        fallback_storage = str(
            product["storage"]
        )

        if fallback_storage.upper() in (
            "1T",
            "1TB"
        ):

            fallback_storage = "1 TB"

        elif not re.search(
            r"[A-Z]",
            fallback_storage,
            re.IGNORECASE
        ):

            fallback_storage += " GB"

        results.append({

            "product_name":
                product["name"],

            "variant":
                "Unknown",

            "ram":
                str(product["ram"]) + " GB",

            "storage":
                fallback_storage,

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