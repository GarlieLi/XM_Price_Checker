import re


def clean_price(text):

    if not text:
        return None

    match = re.search(
        r"\d{1,3}(?:[\s\u202f]\d{3})*(?:,\d{1,2})?",
        text
    )

    if not match:
        return None

    price_text = match.group(0)

    # Remove normal spaces and narrow no-break spaces
    price_text = (
        price_text
        .replace(" ", "")
        .replace("\u202f", "")
    )

    # Polish decimal comma -> dot
    price_text = price_text.replace(",", ".")

    return float(price_text)


def get_products(page, product):

    results = []

    print("Waiting for X-kom products...")

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

    # --------------------------------------------------------
    # NEW:
    # Track whether matching product was found
    # --------------------------------------------------------

    matched_product = False

    # --------------------------------------------------------
    # Process cards
    # --------------------------------------------------------

    for i in range(cards.count()):

        card = cards.nth(i)

        # ----------------------------------------------------
        # Product title
        # ----------------------------------------------------

        title_element = card.locator("h3").first

        if title_element.count() == 0:
            continue

        title = (
            title_element
            .inner_text()
            .strip()
        )

        # Only target product
        if product["name"].lower() not in title.lower():
            continue

        print()
        print("=" * 60)
        print("X-KOM CARD", i)
        print("=" * 60)

        print("TITLE:", title)

        # ----------------------------------------------------
        # Card text
        # ----------------------------------------------------

        card_text = card.inner_text()

        # ----------------------------------------------------
        # RAM
        # ----------------------------------------------------

        ram_match = re.search(
            r"Pamięć RAM:\s*([0-9]+\s*GB)",
            card_text,
            re.IGNORECASE
        )

        if not ram_match:
            continue

        ram = ram_match.group(1)

        # ----------------------------------------------------
        # Storage
        # ----------------------------------------------------

        storage_match = re.search(
            r"Pamięć wbudowana:\s*([0-9]+\s*GB)",
            card_text,
            re.IGNORECASE
        )

        if not storage_match:
            continue

        storage = storage_match.group(1)

        # ----------------------------------------------------
        # Match target RAM / Storage
        # ----------------------------------------------------

        if (
            re.sub(r"\D", "", ram)
            != target_ram
            or
            re.sub(r"\D", "", storage)
            != target_storage
        ):
            continue

        # ----------------------------------------------------
        # NEW:
        # We found the requested product/configuration
        # ----------------------------------------------------

        matched_product = True

        print("RAM:", ram)
        print("STORAGE:", storage)

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        title_lower = title.lower()

        if "black" in title_lower:
            color = "Black"

        elif "green" in title_lower:
            color = "Green"

        elif "blue" in title_lower:
            color = "Blue"

        elif "white" in title_lower:
            color = "White"

        elif "gray" in title_lower:
            color = "Gray"

        elif "grey" in title_lower:
            color = "Grey"

        elif "purple" in title_lower:
            color = "Purple"

        elif "silver" in title_lower:
            color = "Silver"

        elif "gold" in title_lower:
            color = "Gold"

        elif "pink" in title_lower:
            color = "Pink"

        elif "red" in title_lower:
            color = "Red"

        else:
            color = "Unknown"

        print("COLOR:", color)

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price_element = card.locator(
            '[data-name="productPrice"] '
            'span[aria-label^="Cena:"]'
        ).first

        if price_element.count() == 0:
            print("PRICE: None")
            continue

        aria_label = price_element.get_attribute(
            "aria-label"
        )

        price = clean_price(
            aria_label
        )

        print("PRICE:", price)

        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        results.append({
            "product_name": product["name"],
            "variant": color,
            "ram": ram,
            "storage": storage,
            "price": price,
            "availability": "Available"
        })

    # --------------------------------------------------------
    # NEW:
    # Product/configuration was not found
    # --------------------------------------------------------

    if not matched_product:

        print()
        print("=" * 60)
        print("X-KOM PRODUCT NOT FOUND")
        print("=" * 60)

        print(
            "Target:",
            product["name"],
            product["ram"],
            product["storage"]
        )

        results.append({
            "product_name": product["name"],
            "variant": "Unknown",
            "ram": f"{target_ram} GB",
            "storage": f"{target_storage} GB",
            "price": None,
            "availability": "Unavailable"
        })

    return results