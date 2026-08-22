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

    # --------------------------------------------------------
    # Normal Polish format
    # 449,00 zł
    # 449.00 zł
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*[,.]\d{2})\s*zł",
        text,
        re.IGNORECASE
    )

    if match:

        value = (
            match.group(1)
            .replace(" ", "")
            .replace(",", ".")
        )

        try:
            return float(value)

        except ValueError:
            pass

    # --------------------------------------------------------
    # Split format
    #
    # 449
    # 00
    # zł
    # --------------------------------------------------------

    match = re.search(
        r"(\d[\d\s]*)\s+(\d{2})\s*zł",
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

    return None


# ============================================================
# COLOR
# ============================================================

def get_color(title):

    title_lower = title.lower()

    # English names used by NEONET
    if "black" in title_lower:
        return "Black"

    elif "green" in title_lower:
        return "Green"

    elif "blue" in title_lower:
        return "Blue"

    # Polish names
    elif "czarn" in title_lower:
        return "Black"

    elif "zielon" in title_lower:
        return "Green"

    elif "niebiesk" in title_lower:
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


# ============================================================
# RAM
# ============================================================

def get_ram(text):

    match = re.search(
        r"Pamięć RAM:\s*(\d+)\s*GB",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1) + " GB"

    return "Unknown"


# ============================================================
# STORAGE
# ============================================================

def get_storage(text):

    match = re.search(
        r"Pamięć wbudowana:\s*(\d+)\s*GB",
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

    text_lower = text.lower()

    # --------------------------------------------------------
    # Explicitly available
    # --------------------------------------------------------

    if "dodaj do koszyka" in text_lower:
        return "Available"

    if "ostatnie sztuki" in text_lower:
        return "Available"

    # --------------------------------------------------------
    # Explicitly unavailable
    # --------------------------------------------------------

    if (
        "chwilowo niedostępny" in text_lower
        or "niedostępny" in text_lower
        or "brak w magazynie" in text_lower
    ):
        return "Unavailable"

    # --------------------------------------------------------
    # Don't guess
    # --------------------------------------------------------

    return "Unknown"


# ============================================================
# GET PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    # --------------------------------------------------------
    # NEW:
    # Track whether the target product was found
    # --------------------------------------------------------

    product_found = False

    print(
        "Waiting for NEONET products..."
    )

    # --------------------------------------------------------
    # Wait for product headings
    # --------------------------------------------------------

    try:

        page.wait_for_selector(
            "h3",
            timeout=15000
        )

    except Exception:

        print(
            "Could not find NEONET product headings."
        )

        # ----------------------------------------------------
        # NEW:
        # No product headings = product not found
        # ----------------------------------------------------

        results.append(
            {
                "product_name": product["name"],
                "variant": "Unknown",
                "ram": str(product["ram"]) + " GB",
                "storage": str(product["storage"]) + " GB",
                "price": None,
                "availability": "Unavailable"
            }
        )

        return results

    # --------------------------------------------------------
    # Find H3 elements
    # --------------------------------------------------------

    headings = page.locator("h3")

    count = headings.count()

    print(
        "Total NEONET H3:",
        count
    )

    card_index = 0

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

        print()
        print(
            f"NEONET H3 {i}:",
            repr(title)
        )

        # ----------------------------------------------------
        # Product matching
        # ----------------------------------------------------

        title_normalized = (
            title
            .lower()
            .replace("\u00a0", " ")
            .strip()
        )

        if "redmi" not in title_normalized:
            continue

        if "a7" not in title_normalized:
            continue

        if "pro" not in title_normalized:
            continue

        # ----------------------------------------------------
        # NEW:
        # We found a matching target product
        # ----------------------------------------------------

        product_found = True

        # ----------------------------------------------------
        # Find product information container
        # ----------------------------------------------------

        container = None

        for level in range(1, 9):

            try:

                candidate = heading.locator(
                    "xpath=" + "/.." * level
                )

                text = (
                    candidate
                    .inner_text()
                    .strip()
                )

                if (
                    "Redmi A7 Pro" in text
                    and (
                        "Pamięć RAM" in text
                        or "Pamięć wbudowana" in text
                        or "Cena" in text
                        or "Dodaj do koszyka" in text
                        or "Ostatnie sztuki" in text
                    )
                ):

                    container = candidate

                    print(
                        "Product container found at level:",
                        level
                    )

                    break

            except Exception:

                continue

        if container is None:

            print(
                "Could not find product container."
            )

            card_index += 1

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

        except Exception:

            product_card = container

            card_text = (
                container
                .inner_text()
                .strip()
            )

        # ----------------------------------------------------
        # DEBUG: FULL CARD TEXT
        # ----------------------------------------------------

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
        # EXTRACT DATA
        # ====================================================

        ram = get_ram(
            card_text
        )

        storage = get_storage(
            card_text
        )

        color = get_color(
            title
        )

        price = clean_price(
            card_text
        )

        availability = get_availability(
            card_text
        )

        # ====================================================
        # DEBUG OUTPUT
        # ====================================================

        print()
        print(
            "=" * 60
        )
        print(
            f"NEONET CARD {card_index}"
        )
        print(
            "=" * 60
        )

        print(
            "TITLE:",
            title
        )

        print(
            "RAM:",
            ram
        )

        print(
            "STORAGE:",
            storage
        )

        print(
            "COLOR:",
            color
        )

        print(
            "PRICE:",
            price
        )

        print(
            "AVAILABILITY:",
            availability
        )

        # ====================================================
        # SAVE RESULT
        # ====================================================

        results.append(
            {
                "product_name": product["name"],
                "variant": color,
                "ram": ram,
                "storage": storage,
                "price": price,
                "availability": availability
            }
        )

        card_index += 1

    # ========================================================
    # NEW:
    # If no matching product was found at all
    # ========================================================

    if not product_found:

        print()
        print(
            "NEONET: Target product not found."
        )

        results.append(
            {
                "product_name": product["name"],
                "variant": "Unknown",
                "ram": str(product["ram"]) + " GB",
                "storage": str(product["storage"]) + " GB",
                "price": None,
                "availability": "Unavailable"
            }
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print(
        "=" * 60
    )
    print(
        "NEONET RESULTS:",
        len(results)
    )
    print(
        "=" * 60
    )

    for result in results:

        print(
            result
        )

    return results