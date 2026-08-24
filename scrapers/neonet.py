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
    # Track whether the correct product + configuration
    # was found
    # --------------------------------------------------------

    product_found = False

    print(
        "Waiting for NEONET products..."
    )

    # ========================================================
    # TARGET RAM / STORAGE
    # ========================================================

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

    print(
        "Target RAM:",
        target_ram
    )

    print(
        "Target Storage:",
        target_storage
    )

    # ========================================================
    # TARGET PRODUCT NAME
    # ========================================================

    target_name = (
        str(product["name"])
        .lower()
        .replace("\u00a0", " ")
        .strip()
    )

    target_name = re.sub(
        r"\s+",
        " ",
        target_name
    )

    print(
        "Target Product:",
        target_name
    )

    # ========================================================
    # WAIT FOR PRODUCT HEADINGS
    # ========================================================

    try:

        page.wait_for_selector(
            "h3",
            timeout=15000
        )

    except Exception:

        print(
            "Could not find NEONET product headings."
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

        return results

    # ========================================================
    # FIND H3 ELEMENTS
    # ========================================================

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

        # ====================================================
        # PRODUCT NAME MATCHING
        # ====================================================

        title_normalized = (
            title
            .lower()
            .replace("\u00a0", " ")
            .strip()
        )

        title_normalized = re.sub(
            r"\s+",
            " ",
            title_normalized
        )

        # ----------------------------------------------------
        # The target product name must appear in the title
        # ----------------------------------------------------

        if target_name not in title_normalized:

            print(
                "Product name mismatch."
            )

            continue

        print(
            "Product name MATCH."
        )

        # ====================================================
        # FIND PRODUCT INFORMATION CONTAINER
        # ====================================================

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

                candidate_text_normalized = (
                    text
                    .lower()
                    .replace("\u00a0", " ")
                )

                candidate_text_normalized = re.sub(
                    r"\s+",
                    " ",
                    candidate_text_normalized
                )

                # ------------------------------------------------
                # The container must contain:
                #
                # 1. target product name
                # 2. product information / price / availability
                # ------------------------------------------------

                if (
                    target_name in candidate_text_normalized
                    and (
                        "pamięć ram" in candidate_text_normalized
                        or "pamięć wbudowana" in candidate_text_normalized
                        or "cena" in candidate_text_normalized
                        or "dodaj do koszyka" in candidate_text_normalized
                        or "ostatnie sztuki" in candidate_text_normalized
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

        # ====================================================
        # CONTAINER NOT FOUND
        # ====================================================

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

        # ====================================================
        # DEBUG: FULL CARD TEXT
        # ====================================================

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
        # EXTRACT RAM
        # ====================================================

        ram = get_ram(
            card_text
        )

        # ====================================================
        # EXTRACT STORAGE
        # ====================================================

        storage = get_storage(
            card_text
        )

        print(
            "Detected RAM:",
            ram
        )

        print(
            "Detected Storage:",
            storage
        )

        # ====================================================
        # MATCH TARGET RAM / STORAGE
        # ====================================================

        ram_number = re.sub(
            r"\D",
            "",
            str(ram)
        )

        storage_number = re.sub(
            r"\D",
            "",
            str(storage)
        )

        if (
            ram_number != target_ram
            or
            storage_number != target_storage
        ):

            print(
                "RAM / Storage mismatch:",
                ram,
                storage
            )

            continue

        print(
            "RAM / Storage MATCH."
        )

        # ----------------------------------------------------
        # We found the correct product configuration
        # ----------------------------------------------------

        product_found = True

        # ====================================================
        # COLOR
        # ====================================================

        color = get_color(
            title
        )

        print(
            "COLOR:",
            color
        )

        # ====================================================
        # AVAILABILITY
        # ====================================================

        availability = get_availability(
            card_text
        )

        print(
            "AVAILABILITY:",
            availability
        )

        # ====================================================
        # PRICE
        # ====================================================

        price = clean_price(
            card_text
        )

        print(
            "PRICE:",
            price
        )

        # ====================================================
        # RESULT
        # ====================================================

        result = {
            "product_name": product["name"],
            "variant": color,
            "ram": ram,
            "storage": storage,
            "price": price,
            "availability": availability
        }

        results.append(
            result
        )

        card_index += 1

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================

    if not product_found:

        print()
        print(
            "=" * 60
        )

        print(
            "NEONET: Target product/configuration not found."
        )

        print(
            "Product:",
            product["name"]
        )

        print(
            "RAM:",
            product["ram"]
        )

        print(
            "Storage:",
            product["storage"]
        )

        print(
            "=" * 60
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


# ============================================================
# COMPATIBILITY FUNCTIONS
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