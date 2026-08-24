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

    # --------------------------------------------------------
    # English
    # --------------------------------------------------------

    if "black" in title_lower:
        return "Black"

    elif "green" in title_lower:
        return "Green"

    elif "blue" in title_lower:
        return "Blue"

    elif "white" in title_lower:
        return "White"

    elif "grey" in title_lower:
        return "Grey"

    elif "gray" in title_lower:
        return "Gray"

    elif "silver" in title_lower:
        return "Silver"

    elif "gold" in title_lower:
        return "Gold"

    elif "purple" in title_lower:
        return "Purple"

    elif "pink" in title_lower:
        return "Pink"

    elif "red" in title_lower:
        return "Red"

    elif "titanium" in title_lower:
        return "Titanium"

    elif "glacier blue" in title_lower:
        return "Glacier Blue"

    # --------------------------------------------------------
    # Polish
    # --------------------------------------------------------

    elif "czarn" in title_lower:
        return "Black"

    elif "zielon" in title_lower:
        return "Green"

    elif "niebiesk" in title_lower:
        return "Blue"

    elif "biały" in title_lower or "bialy" in title_lower:
        return "White"

    elif "szary" in title_lower:
        return "Grey"

    elif "srebrny" in title_lower:
        return "Silver"

    elif "złoty" in title_lower or "zloty" in title_lower:
        return "Gold"

    elif "fioletowy" in title_lower:
        return "Purple"

    elif "różowy" in title_lower or "rozowy" in title_lower:
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

            # ------------------------------------------------
            # Only target product
            # ------------------------------------------------

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
            # in visible text, so first try the title.
            #
            # Examples:
            #
            # Redmi A7 Pro 4/64GB
            # Redmi Note 15 6/128GB
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

                print(
                    "RAM / STORAGE mismatch:",
                    ram,
                    storage
                )

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

            # Explicitly unavailable
            if (
                "produkt niedostępny"
                in card_text_lower
                or
                "brak w magazynie"
                in card_text_lower
                or
                "niedostępny"
                in card_text_lower
            ):

                availability = "Unavailable"

            # Explicitly available
            elif (
                "dostępny"
                in card_text_lower
                or
                "dostepny"
                in card_text_lower
            ):

                availability = "Available"

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
            # The card may contain several prices:
            #
            # current price
            # lowest price
            # regular price
            #
            # For now, take the first visible price candidate.

            price = None

            price_candidates = card.locator(
                "text=/\\d+[,.]\\d{2}\\s*zł/"
            )

            if price_candidates.count() > 0:

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