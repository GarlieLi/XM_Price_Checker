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

    elif "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")

    try:
        return float(text)

    except ValueError:
        return None


# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = title.lower()

    color_map = {

        "czarny": "Black",
        "czarna": "Black",
        "czarne": "Black",

        "zielony": "Green",
        "zielona": "Green",
        "zielone": "Green",

        "niebieski": "Blue",
        "niebieska": "Blue",
        "niebieskie": "Blue",

        "biały": "White",
        "biała": "White",
        "białe": "White",

        "szary": "Grey",
        "szara": "Grey",
        "szare": "Grey",

        "fioletowy": "Purple",
        "fioletowa": "Purple",
        "fioletowe": "Purple",

        "srebrny": "Silver",
        "srebrna": "Silver",
        "srebrne": "Silver",

        "złoty": "Gold",
        "złota": "Gold",
        "złote": "Gold",

        "różowy": "Pink",
        "różowa": "Pink",
        "różowe": "Pink",

        "czerwony": "Red",
        "czerwona": "Red",
        "czerwone": "Red",

        "tytanowy": "Titanium",
        "tytanowa": "Titanium",
        "tytanowe": "Titanium",
    }

    for polish_color, english_color in color_map.items():

        if re.search(
            rf"\b{re.escape(polish_color)}\b",
            title_lower
        ):
            return english_color

    return "Unknown"


# ============================================================
# AVAILABILITY
# ============================================================

def get_availability(card_text):

    text = card_text.lower()

    # --------------------------------------------------------
    # Explicitly unavailable
    # --------------------------------------------------------

    unavailable_phrases = [

        "niestety dostawa nie jest możliwa",

        "produkt niedostępny",

        "chwilowo niedostępny",

        "niedostępny online",

        "brak dostępności",
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

    # --------------------------------------------------------
    # Unknown
    # --------------------------------------------------------

    return "Unknown"


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

    target_storage = re.sub(
        r"\D",
        "",
        str(product["storage"])
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

        # ----------------------------------------------------
        # Product title
        # ----------------------------------------------------

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

            if (
                product["name"].lower()
                in text.lower()
            ):

                title = text

                break

        if not title:

            print(
                "Product title not found."
            )

            continue

        print(
            "TITLE:",
            title
        )

        # ----------------------------------------------------
        # Product name match
        # ----------------------------------------------------

        if (
            product["name"].lower()
            not in title.lower()
        ):

            print(
                "Product name does not match."
            )

            continue

        # ----------------------------------------------------
        # RAM / Storage
        #
        # Example:
        #
        # Smartfon XIAOMI Redmi A7 Pro
        # 4G (LTE) 4 GB/ 64 GB Czarny
        # ----------------------------------------------------

        memory_match = re.search(
            r"(\d+)\s*GB\s*/\s*(\d+)\s*GB",
            title,
            re.IGNORECASE
        )

        if not memory_match:

            print(
                "RAM/storage not found in title."
            )

            continue

        ram = memory_match.group(1)

        storage = memory_match.group(2)

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

        # ----------------------------------------------------
        # Match RAM / Storage
        # ----------------------------------------------------

        if (
            ram != target_ram
            or
            storage != target_storage
        ):

            print(
                "RAM/storage does not match."
            )

            continue

        # ----------------------------------------------------
        # Target product found
        # ----------------------------------------------------

        product_found = True

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        color = get_color(title)

        print(
            "COLOR:",
            color
        )

        # ----------------------------------------------------
        # CARD TEXT
        # ----------------------------------------------------

        card_text = (
            card
            .inner_text()
            .strip()
        )

        # ----------------------------------------------------
        # AVAILABILITY
        # ----------------------------------------------------

        availability = get_availability(
            card_text
        )

        print(
            "AVAILABILITY:",
            availability
        )

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = None

        # Look specifically for normal product prices:
        #
        # 399,99 zł
        # 399,00 zł
        #
        # This avoids promotional badges such as:
        #
        # 120 zł do BP

        price_matches = re.findall(
            r"\b\d{1,5}[,.]\d{2}\s*zł\b",
            card_text,
            re.IGNORECASE
        )

        if price_matches:

            price = clean_price(
                price_matches[0]
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
                product["ram"],

            "storage":
                product["storage"],

            "price":
                None,

            "availability":
                "Unavailable",
        })

    return results