#NOT WORKING FOR NOW!!
#EURO BLOCKS ACCESS WITH ANTI BOTS

import re


def clean_price(text):

    if not text:
        return None

    match = re.search(
        r"(\d[\d\s]*[,.]?\d{0,2})\s*zł",
        text,
        re.IGNORECASE
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


def get_color(title):

    title_lower = title.lower()

    colors = {
        "czarny": "Black",
        "zielony": "Green",
        "niebieski": "Blue",
        "biały": "White",
        "szary": "Grey",
        "srebrny": "Silver",
        "złoty": "Gold",
        "fioletowy": "Purple",
        "różowy": "Pink",
        "czerwony": "Red",
        "tytanowy": "Titanium",
    }

    for polish, english in colors.items():

        if polish in title_lower:
            return english

    return "Unknown"


def get_products(page, product):

    results = []

    print("Waiting for EURO products...")

    # --------------------------------------------------------
    # Wait for frontend rendering
    # --------------------------------------------------------

    page.wait_for_timeout(3000)

    body = page.locator("body").inner_text()

    if product["name"].lower() not in body.lower():

        print("Target product not found on EURO page.")

        return results

    # --------------------------------------------------------
    # Product cards
    # --------------------------------------------------------

    # EURO uses product containers with data-productid
    # Find containers that contain the target product title.

    cards = page.locator(
        '[data-productid]'
    )

    print(
        "EURO product containers:",
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
    # Process cards
    # --------------------------------------------------------

    for i in range(cards.count()):

        card = cards.nth(i)

        try:

            card_text = card.inner_text()

        except Exception:

            continue

        # ----------------------------------------------------
        # Product title
        # ----------------------------------------------------

        title_element = card.locator(
            "a"
        ).filter(
            has_text=re.compile(
                re.escape(product["name"]),
                re.IGNORECASE
            )
        ).first

        if title_element.count() == 0:

            continue

        title = (
            title_element
            .inner_text()
            .strip()
        )

        # ----------------------------------------------------
        # Target product
        # ----------------------------------------------------

        if product["name"].lower() not in title.lower():

            continue

        print()
        print("=" * 60)
        print("EURO CARD", i)
        print("=" * 60)

        print("TITLE:", title)

        # ----------------------------------------------------
        # RAM / Storage
        # ----------------------------------------------------

        ram_storage_match = re.search(
            r"(\d+)\s*GB\s*/\s*(\d+)\s*GB",
            title,
            re.IGNORECASE
        )

        if not ram_storage_match:

            ram_storage_match = re.search(
                r"Pamięć RAM/wewnętrzna\s*"
                r"(\d+)\s*GB\s*/\s*(\d+)\s*GB",
                card_text,
                re.IGNORECASE
            )

        if not ram_storage_match:

            print("RAM/STORAGE: Not found")

            continue

        ram_value = ram_storage_match.group(1)
        storage_value = ram_storage_match.group(2)

        ram = f"{ram_value} GB"
        storage = f"{storage_value} GB"

        print("RAM:", ram)
        print("STORAGE:", storage)

        # ----------------------------------------------------
        # Match target RAM / Storage
        # ----------------------------------------------------

        if (
            ram_value != target_ram
            or
            storage_value != target_storage
        ):

            continue

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        color = get_color(title)

        print("COLOR:", color)

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = clean_price(card_text)

        print("PRICE:", price)

        # ----------------------------------------------------
        # AVAILABILITY
        # ----------------------------------------------------

        text_lower = card_text.lower()

        if (
            "do koszyka" in text_lower
            or
            "dostępny" in text_lower
            or
            "najwcześniej u ciebie" in text_lower
        ):

            availability = "Available"

        else:

            availability = "Unknown"

        print(
            "AVAILABILITY:",
            availability
        )

        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        results.append({

            "product_name": product["name"],

            "variant": color,

            "ram": ram,

            "storage": storage,

            "price": price,

            "availability": availability
        })

    return results