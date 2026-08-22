import re


print(
    "AVANS MODULE PATH:",
    __file__
)


# ============================================================
# PRICE
# ============================================================

def clean_price(text):

    if not text:
        return None

    # Prefer Polish price patterns containing zł
    matches = re.findall(
        r"(\d[\d\s]*[,.]\d{2})\s*zł",
        text,
        re.IGNORECASE
    )

    if matches:

        value = (
            matches[-1]
            .replace(" ", "")
            .replace(",", ".")
        )

        try:
            return float(value)

        except ValueError:
            pass

    # --------------------------------------------------------
    # Split price format
    #
    # 399
    # 00
    #
    # --------------------------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for i, line in enumerate(lines):

        if re.fullmatch(
            r"\d{1,5}",
            line
        ):

            if i + 1 < len(lines):

                decimal = lines[i + 1]

                if re.fullmatch(
                    r"\d{2}",
                    decimal
                ):

                    try:

                        value = float(
                            f"{line}.{decimal}"
                        )

                        if value >= 50:

                            return value

                    except ValueError:

                        pass

    return None


# ============================================================
# COLOR
# ============================================================

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


# ============================================================
# RAM / STORAGE
# ============================================================

def get_ram_storage(text):

    # --------------------------------------------------------
    # Avans format:
    #
    # Pamięć RAM/Wewnętrzna: 4 GB / 64 GB
    #
    # --------------------------------------------------------

    match = re.search(
        r"Pamięć\s+RAM/Wewnętrzna:\s*"
        r"(\d+)\s*GB\s*/\s*(\d+)\s*GB",
        text,
        re.IGNORECASE
    )

    if not match:

        return None, None

    return (
        f"{match.group(1)} GB",
        f"{match.group(2)} GB"
    )


# ============================================================
# AVAILABILITY
# ============================================================

def get_availability(text):

    if not text:

        return "Unknown"

    text_lower = text.lower()

    # --------------------------------------------------------
    # Explicitly unavailable
    # --------------------------------------------------------

    unavailable_phrases = [

        # English
        "product temporarily unavailable",

        "product unavailable",

        "temporarily unavailable",

        # Polish
        "produkt tymczasowo niedostępny",

        "produkt niedostępny",

        "chwilowo niedostępny",

        "niedostępny",

        "brak w magazynie",
    ]

    for phrase in unavailable_phrases:

        if phrase in text_lower:

            return "Unavailable"

    # --------------------------------------------------------
    # Explicitly available
    # --------------------------------------------------------

    available_phrases = [

        "dodaj do koszyka",

        "dostępny",

        "dostępne",

        "available",

        "jutro",
    ]

    for phrase in available_phrases:

        if phrase in text_lower:

            return "Available"

    # --------------------------------------------------------
    # Unknown
    # --------------------------------------------------------

    return "Unknown"


# ============================================================
# GET PRODUCTS
# ============================================================

def get_products(page, product):

    results = []

    print(
        "Waiting for Avans products..."
    )

    # --------------------------------------------------------
    # Find product titles
    # --------------------------------------------------------

    titles = page.locator(
        "h2"
    )

    count = titles.count()

    print(
        "Total Avans H2:",
        count
    )

    # ========================================================
    # PROCESS PRODUCTS
    # ========================================================

    for i in range(count):

        title_element = titles.nth(i)

        try:

            title = (
                title_element
                .inner_text()
                .strip()
            )

        except Exception:

            continue

        # ----------------------------------------------------
        # Match target product
        # ----------------------------------------------------

        if (
            product["name"].lower()
            not in title.lower()
        ):

            continue

        # ----------------------------------------------------
        # Only target actual smartphone
        # ----------------------------------------------------

        if "smartfon" not in title.lower():

            continue

        print()
        print(
            "=" * 60
        )

        print(
            f"AVANS CARD {len(results)}"
        )

        print(
            "=" * 60
        )

        print(
            "TITLE:",
            title
        )

        # ----------------------------------------------------
        # Find product container
        # ----------------------------------------------------

        try:

            container = (
                title_element
                .locator(
                    "xpath=ancestor::div[contains(@class,'offer-box')]"
                )
                .first
            )

            if container.count() == 0:

                print(
                    "Could not find offer-box."
                )

                continue

        except Exception as e:

            print(
                "Container error:",
                e
            )

            continue

        # ----------------------------------------------------
        # Extract complete product text
        # ----------------------------------------------------

        try:

            text = (
                container
                .inner_text()
                .strip()
            )

        except Exception as e:

            print(
                "Could not read product container:",
                e
            )

            continue

        # ----------------------------------------------------
        # DEBUG CARD TEXT
        # ----------------------------------------------------

        print()
        print(
            "AVANS FULL CARD TEXT:"
        )

        print(
            "-" * 60
        )

        print(
            text
        )

        print(
            "-" * 60
        )

        # ----------------------------------------------------
        # RAM / STORAGE
        # ----------------------------------------------------

        ram, storage = get_ram_storage(
            text
        )

        print(
            "RAM:",
            ram
        )

        print(
            "STORAGE:",
            storage
        )

        # ----------------------------------------------------
        # Target RAM / STORAGE
        # ----------------------------------------------------

        target_ram = str(
            product.get("ram", "")
        ).strip()

        target_storage = str(
            product.get("storage", "")
        ).strip()

        # ----------------------------------------------------
        # Match RAM
        # ----------------------------------------------------

        if ram:

            ram_number = re.sub(
                r"\s*GB",
                "",
                ram,
                flags=re.IGNORECASE
            ).strip()

            if (
                target_ram
                and
                target_ram != ram_number
                and
                target_ram != ram
            ):

                print(
                    "Skipping: RAM mismatch."
                )

                continue

        # ----------------------------------------------------
        # Match STORAGE
        # ----------------------------------------------------

        if storage:

            storage_number = re.sub(
                r"\s*GB",
                "",
                storage,
                flags=re.IGNORECASE
            ).strip()

            if (
                target_storage
                and
                target_storage != storage_number
                and
                target_storage != storage
            ):

                print(
                    "Skipping: storage mismatch."
                )

                continue

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        color = get_color(
            title
        )

        print(
            "COLOR:",
            color
        )

        # ----------------------------------------------------
        # AVAILABILITY
        # ----------------------------------------------------

        availability = get_availability(
            text
        )

        print(
            "AVAILABILITY:",
            availability
        )

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = clean_price(
            text
        )

        print(
            "PRICE:",
            price
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        results.append(
            {
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
            }
        )

    # ========================================================
    # PRODUCT NOT FOUND
    # ========================================================
    #
    # If no matching product/configuration was found
    # anywhere on the page, return Unavailable instead
    # of an empty result.
    #
    # ========================================================

    if not results:

        print()
        print(
            "=" * 60
        )

        print(
            "TARGET PRODUCT NOT FOUND"
        )

        print(
            "Returning Unavailable."
        )

        print(
            "=" * 60
        )

        results.append(
            {
                "product_name":
                    product["name"],

                "variant":
                    "Unknown",

                "ram":
                    (
                        f'{product.get("ram", "")} GB'
                        if product.get("ram")
                        else "Unknown"
                    ),

                "storage":
                    (
                        f'{product.get("storage", "")} GB'
                        if product.get("storage")
                        else "Unknown"
                    ),

                "price":
                    None,

                "availability":
                    "Unavailable"
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
        "AVANS RESULTS:",
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