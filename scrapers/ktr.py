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

    # Remove spaces and non-breaking spaces
    text = text.replace(" ", "")
    text = text.replace("\xa0", "")

    # Keep only numbers, comma and dot
    text = re.sub(
        r"[^0-9,.]",
        "",
        text
    )

    if not text:
        return None

    # Polish format:
    # 1.899,99 -> 1899.99
    if "," in text and "." in text:

        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "")
            text = text.replace(",", ".")

        else:
            text = text.replace(",", "")

    # 1899,99 -> 1899.99
    elif "," in text:
        text = text.replace(",", ".")

    try:
        price = float(text)

    except ValueError:
        return None

    # A single digit such as "1" is almost certainly
    # an incomplete price fragment, not a real phone price.
    if price < 10:
        return None

    return price

# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = title.lower()

    color_map = {

        # ----------------------------------------------------
        # BLACK
        # ----------------------------------------------------

        "midnight black": "Black",
        "czarny": "Black",
        "czarna": "Black",
        "czarne": "Black",
        "black": "Black",

        # ----------------------------------------------------
        # BLUE
        # ----------------------------------------------------

        "glacier blue": "Blue",
        "ocean blue": "Blue",
        "niebieski": "Blue",
        "niebieska": "Blue",
        "blue": "Blue",

        # ----------------------------------------------------
        # TITANIUM
        # ----------------------------------------------------

        "tytanowy": "Titanium",
        "tytanowa": "Titanium",
        "titanium": "Titanium",

        # ----------------------------------------------------
        # PURPLE
        # ----------------------------------------------------

        "aurora purple": "Purple",
        "fioletowy": "Purple",
        "fioletowa": "Purple",
        "lawendowy": "Purple",
        "lawendowa": "Purple",
        "purple": "Purple",

        # ----------------------------------------------------
        # GREEN
        # ----------------------------------------------------

        "forest green": "Green",
        "zielony": "Green",
        "zielona": "Green",
        "green": "Green",

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

        "mocha brown": "Brown",
        "brązowy": "Brown",
        "brązowa": "Brown",
        "brown": "Brown",

    }

    # Check longer names first
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

    # Text after Redmi Note number
    after_note = text[match.end():].strip()

    # Check version
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

def product_name_matches(title, target_name):

    title_lower = title.lower()
    target_lower = target_name.lower()

    # Normalize spacing
    title_lower = re.sub(r"\s+", " ", title_lower).strip()
    target_lower = re.sub(r"\s+", " ", target_lower).strip()

    # --------------------------------------------------------
    # Basic requirement:
    # target product name must appear
    # --------------------------------------------------------

    if target_lower not in title_lower:
        return False

    # --------------------------------------------------------
    # Redmi Note 15 family protection
    #
    # Prevent:
    # Redmi Note 15 -> Redmi Note 15 Pro
    # Redmi Note 15 -> Redmi Note 15 Pro+
    # --------------------------------------------------------

    target_has_pro = bool(
        re.search(r"\bpro\+?\b", target_lower)
    )

    title_has_pro = bool(
        re.search(r"\bpro\+?\b", title_lower)
    )

    # Target does NOT contain Pro,
    # but title does → wrong product
    if not target_has_pro and title_has_pro:
        return False

    # --------------------------------------------------------
    # Distinguish Pro from Pro+
    # --------------------------------------------------------

    target_has_pro_plus = "pro+" in target_lower
    title_has_pro_plus = "pro+" in title_lower

    if target_has_pro_plus != title_has_pro_plus:
        return False

    # --------------------------------------------------------
    # Distinguish 5G versions
    # --------------------------------------------------------

    target_has_5g = "5g" in target_lower

    title_has_5g = bool(
        re.search(r"\b5g\b", title_lower)
    )

    if target_has_5g != title_has_5g:
        return False

    return True

def extract_price(card):

    price_element = card.locator(
        '[data-price-type="final"]'
    ).first

    if price_element.count() == 0:
        return None

    # Try several levels because KTR may split
    # the whole price across nested HTML elements.
    candidates = []

    # Exact element
    try:
        candidates.append(
            price_element.inner_text().strip()
        )
    except:
        pass

    # Parent
    try:
        candidates.append(
            price_element.locator("xpath=..").inner_text().strip()
        )
    except:
        pass

    # Grandparent
    try:
        candidates.append(
            price_element.locator("xpath=../..").inner_text().strip()
        )
    except:
        pass

    for price_text in candidates:

        price = clean_price(price_text)

        if price is not None:
            return price

    return None

# ============================================================
# PRODUCTS
# ============================================================

def get_products(page, product):

    cards = page.locator(
        'div[data-name="listingTile"]'
    )

    results = []

    print(
        "KTR product cards:",
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
    # Process product cards
    # --------------------------------------------------------

    for i in range(cards.count()):

        card = cards.nth(i)

        # ----------------------------------------------------
        # Product title
        # ----------------------------------------------------

        title_element = card.locator("h2").first

        if title_element.count() == 0:
            continue

        title = (
            title_element
            .inner_text()
            .strip()
        )

        # ----------------------------------------------------
        # Match product name
        # ----------------------------------------------------

        if not product_name_matches(
            title,
            product["name"]
            ):
            continue

        print()
        print("=" * 60)
        print("KTR PRODUCT", i)
        print("=" * 60)

        print(
            "TITLE:",
            title
        )

        # ----------------------------------------------------
        # Card text
        # ----------------------------------------------------

        card_text = (
            card
            .inner_text()
            .strip()
        )

        print()
        print("CARD TEXT:")
        print("-" * 60)
        print(card_text)
        print("-" * 60)

        # ----------------------------------------------------
        # EXCLUDE OUTLET PRODUCTS
        # ----------------------------------------------------

        if "outlet" in card_text.lower():

            print(
                "SKIPPING OUTLET PRODUCT"
            )

            continue

        # ----------------------------------------------------
        # RAM / STORAGE
        # ----------------------------------------------------
        #
        # First try product specifications.
        # If a specification is missing, fall back to
        # extracting RAM/storage from the product title.
        #
        # Example:
        # Xiaomi Redmi 17 4/128GB Zielony
        # ----------------------------------------------------

        ram_match = re.search(
            r"Pamięć RAM:\s*([0-9]+\s*GB)",
            card_text,
            re.IGNORECASE
        )

        ram = (
            ram_match.group(1)
            if ram_match
            else None
        )

        storage_match = re.search(
            r"Pamięć Flash:\s*([0-9]+\s*GB)",
            card_text,
            re.IGNORECASE
        )

        storage = (
            storage_match.group(1)
            if storage_match
            else None
        )

        # ----------------------------------------------------
        # FALLBACK: RAM / STORAGE FROM TITLE
        # ----------------------------------------------------

        title_memory_match = re.search(
            r"(\d+)\s*/\s*(\d+)\s*GB",
            title,
            re.IGNORECASE
        )

        if title_memory_match:

            if ram is None:

                ram = (
                    title_memory_match.group(1)
                    + " GB"
                )

            if storage is None:

                storage = (
                    title_memory_match.group(2)
                    + " GB"
                )

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

        color = get_color(title)

        print(
            "COLOR:",
            color
        )

        # ----------------------------------------------------
        # AVAILABILITY
        # ----------------------------------------------------
        #
        # Check unavailable phrases first.
        # Then check positive availability signals.
        # ----------------------------------------------------

        card_text_lower = card_text.lower()

        if (
            "produkt niedostępny" in card_text_lower
            or
            "chwilowo niedostępny" in card_text_lower
        ):

            availability = "Unavailable"

        elif (
            "produkt dostepny w magazynie" in card_text_lower
            or
            "produkt dostępny w magazynie" in card_text_lower
            or
            "dostępny w salonach" in card_text_lower
            or
            "dodaj do koszyka" in card_text_lower
            or
            "do koszyka" in card_text_lower
        ):

            availability = "Available"

        else:

            availability = "Unknown"

        print(
            "AVAILABILITY:",
            availability
        )

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = extract_price(card)

        print(
            "PRICE:",
            price
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        result = {
            "product_name": product["name"],
            "variant": color,
            "ram": ram,
            "storage": storage,
            "price": price,
            "availability": availability,
        }

        print(
            "RESULT:",
            result
        )

        results.append(result)

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not results:

        print()
        print(
            "KTR: Target product not found."
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