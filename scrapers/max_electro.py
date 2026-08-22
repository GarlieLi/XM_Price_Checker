import re


# ------------------------------------------------------------
# Price
# ------------------------------------------------------------

def clean_price(text):

    if not text:
        return None

    match = re.search(
        r"(\d+[,.]\d{1,2})",
        text
    )

    if not match:
        return None

    return float(
        match.group(1).replace(",", ".")
    )


# ------------------------------------------------------------
# Color
# ------------------------------------------------------------

def get_color(title):

    title_lower = title.lower()

    if "czarny" in title_lower:
        return "Black"

    elif "zielony" in title_lower:
        return "Green"

    elif "niebieski" in title_lower:
        return "Blue"

    elif "biały" in title_lower:
        return "White"

    elif "szary" in title_lower:
        return "Grey"

    elif "srebrny" in title_lower:
        return "Silver"

    elif "złoty" in title_lower:
        return "Gold"

    elif "fioletowy" in title_lower:
        return "Purple"

    elif "różowy" in title_lower:
        return "Pink"

    elif "czerwony" in title_lower:
        return "Red"

    elif "tytanowy" in title_lower:
        return "Titanium"

    else:
        return "Unknown"


# ------------------------------------------------------------
# Products
# ------------------------------------------------------------

def get_products(page, product):

    results = []

    print("Waiting for Max Elektro products...")

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
    # Track whether a matching product was found
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

            # Only target product

            if product["name"].lower() not in title.lower():
                continue

            print()
            print("=" * 60)
            print("MAX ELEKTRO CARD", i)
            print("=" * 60)

            print(
                "TITLE:",
                title
            )

            # ------------------------------------------------
            # Card text
            # ------------------------------------------------

            card_text = (
                card
                .inner_text()
                .strip()
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

            # ------------------------------------------------
            # Storage
            # ------------------------------------------------
            #
            # Current Max Elektro card does not show storage
            # in the visible text for this product.
            #
            # Therefore first try the title.
            #
            # Example:
            # Redmi A7 Pro 4/64GB
            #
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

            # ------------------------------------------------
            # Match RAM / Storage
            # ------------------------------------------------

            if (
                re.sub(r"\D", "", ram)
                != target_ram
                or
                re.sub(r"\D", "", storage)
                != target_storage
            ):

                continue

            # ------------------------------------------------
            # Matching product found
            # ------------------------------------------------

            product_found = True

            print(
                "RAM:",
                ram
            )

            print(
                "STORAGE:",
                storage
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

            card_text_lower = (
                card_text.lower()
            )

            if (
                "produkt dostępny w magazynie"
                in card_text_lower
            ):

                availability = "Available"

            elif (
                "produkt niedostępny"
                in card_text_lower
                or
                "brak w magazynie"
                in card_text_lower
            ):

                availability = "Unavailable"

            else:

                availability = "Unknown"

            print(
                "AVAILABILITY:",
                availability
            )

            # ------------------------------------------------
            # PRICE
            # ------------------------------------------------

            # We want the current selling price.
            #
            # The card contains several prices:
            #
            # 399.00 zł  <- current price
            # 399.00 zł  <- lowest price
            # 549.00 zł  <- regular price
            #
            # Therefore take the price element associated
            # with the current product price.

            price = None

            price_candidates = card.locator(
                "text=/\\d+[,.]\\d{2}\\s*zł/"
            )

            if price_candidates.count() > 0:

                # First visible price is the current price
                price_text = (
                    price_candidates
                    .first
                    .inner_text()
                    .strip()
                )

                price = clean_price(
                    price_text
                )

            # ------------------------------------------------
            # Fallback: extract first price from card text
            # ------------------------------------------------

            if price is None:

                price_match = re.search(
                    r"(\d+[,.]\d{2})\s*zł",
                    card_text
                )

                if price_match:

                    price = float(
                        price_match
                        .group(1)
                        .replace(",", ".")
                    )

            print(
                "PRICE:",
                price
            )

            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

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
                    availability
            })

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
    #
    # The search page did not contain the target product.
    # Treat this as unavailable instead of returning [].
    #
    # ========================================================

    if not product_found:

        print()
        print("=" * 60)
        print("MAX ELEKTRO: TARGET PRODUCT NOT FOUND")
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

    return results