import re


def clean_price(price_text):

    if price_text is None:
        return None

    text = str(price_text).strip()

    text = text.replace("Cena:", "")
    text = text.replace("zł", "")
    text = text.replace("PLN", "")
    text = text.replace(" ", "")

    text = re.sub(
        r"[^0-9,.]",
        "",
        text
    )

    if not text:
        return None

    if "," in text and "." not in text:
        text = text.replace(",", ".")

    elif "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")

    return float(text)


def get_color(title):

    title_lower = title.lower()

    if "czarny" in title_lower:
        return "Black"

    elif "tytanowy" in title_lower:
        return "Titanium"

    elif "fioletowy" in title_lower:
        return "Purple"

    elif "niebieski" in title_lower:
        return "Blue"

    elif "glacier blue" in title_lower:
        return "Glacier Blue"

    elif "zielony" in title_lower:
        return "Green"

    else:
        return "Unknown"


def extract_price(card):

    price_element = card.locator(
        '[data-price-type="final"]'
    ).first

    if price_element.count() == 0:
        return None

    price_text = (
        price_element
        .inner_text()
        .strip()
    )

    return clean_price(price_text)


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

        if product["name"].lower() not in title.lower():
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

        # ----------------------------------------------------
        # RAM
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

        # ----------------------------------------------------
        # STORAGE
        # ----------------------------------------------------

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
        # Match RAM / Storage
        # ----------------------------------------------------

        if (
            re.sub(r"\D", "", str(ram))
            != target_ram
            or
            re.sub(r"\D", "", str(storage))
            != target_storage
        ):
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

        card_text_lower = card_text.lower()

        if (
            "produkt niedostępny" in card_text_lower
            or
            "chwilowo niedostępny" in card_text_lower
        ):

            availability = "Unavailable"

        elif "dostępny" in card_text_lower:

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