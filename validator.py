
import re

# Allowed item categories
ALLOWED_ITEMS = {
    "phone", "wallet", "id_card", "bottle", "bag",
    "earphones", "keys", "umbrella", "calculator",
    "watch", "spectacles", "other"
}

# Ten supported colours
ALLOWED_COLOURS = {
    "black", "white", "red", "blue", "green",
    "yellow", "brown", "silver", "gold", "orange"
}

# Required JSON fields
REQUIRED_FIELDS = {
    "item", "colour", "brand", "place", "summary"
}


# Item category keywords
ITEM_PATTERNS = {
    "id_card": [r"\bid[\s_-]*card\b", r"\bidentity card\b"],
    "earphones": [r"\bearphones?\b"],
    "spectacles": [r"\bspectacles\b", r"\beyeglasses\b", r"\bglasses\b"],
    "calculator": [r"\bcalculator\b"],
    "umbrella": [r"\bumbrella\b"],
    "wallet": [r"\bwallet\b"],
    "bottle": [r"\bbottle\b"],
    "phone": [r"\bphone\b", r"\bmobile\b", r"\bsmartphone\b"],
    "bag": [r"\bbackpack\b", r"\bschool bag\b", r"\bhandbag\b", r"\bbag\b"],
    "watch": [r"\bwrist watch\b", r"\bwatch\b"],
    "keys": [r"\bkeys?\b"]
}


# Function 1: Normalize AI extraction
def normalize_extraction(data, report=None):

    if not isinstance(data, dict):
        return data

    # Convert AI item description into standard category
    item = str(data.get("item", "")).lower().strip()

    normalized_item = "other"

    for category, patterns in ITEM_PATTERNS.items():
        if any(re.search(pattern, item) for pattern in patterns):
            normalized_item = category
            break

    data["item"] = normalized_item

    # Normalize colour
    colour = data.get("colour")

    if isinstance(colour, str):
        colour = colour.lower().strip()
    else:
        colour = None

    # Trust only colours explicitly mentioned in the report
    if report:
        report_text = report.lower()

        mentioned_colours = [
            c for c in ALLOWED_COLOURS
            if re.search(r"\b" + re.escape(c) + r"\b", report_text)
        ]

        if len(mentioned_colours) == 1:
            colour = mentioned_colours[0]
        elif len(mentioned_colours) == 0:
            colour = None
        else:
            colour = None

    data["colour"] = (
        colour if colour in ALLOWED_COLOURS else None
    )

    # Clean brand and place
    for field in ["brand", "place"]:
        if isinstance(data.get(field), str):
            data[field] = data[field].strip()

    return data


# Function 2: Check whether AI response is valid
def is_valid(data):

    if not isinstance(data, dict):
        return False

    if set(data.keys()) != REQUIRED_FIELDS:
        return False

    if not isinstance(data["item"], str):
        return False

    if data["item"] not in ALLOWED_ITEMS:
        return False

    if data["colour"] is not None:
        if not isinstance(data["colour"], str):
            return False

        if data["colour"].lower() not in ALLOWED_COLOURS:
            return False

    if data["brand"] is not None:
        if not isinstance(data["brand"], str) or not data["brand"].strip():
            return False

    if data["place"] is not None:
        if not isinstance(data["place"], str) or not data["place"].strip():
            return False

    if not isinstance(data["summary"], str):
        return False

    if len(data["summary"].split()) > 8:
        return False

    return True


# Function 3: Verify extracted facts against original report
def check_facts(data, report):

    if not is_valid(data):
        return False

    if not isinstance(report, str) or not report.strip():
        return False

    report_text = report.lower()
    report_text = re.sub(r"[^a-z0-9\s]", " ", report_text)
    report_text = " ".join(report_text.split())

    # Check item against original report
    mentioned_items = []

    for category, patterns in ITEM_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, report_text)

            if match:
                mentioned_items.append((match.start(), category))

    if mentioned_items:
        mentioned_items.sort(key=lambda x: x[0])
        expected_item = mentioned_items[0][1]
    else:
        expected_item = "other"

    if data["item"] != expected_item:
        return False

    # Check colour, brand and place
    for field in ["colour", "brand", "place"]:

        value = data[field]

        if value is None:
            continue

        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9\s]", " ", value)
        value = " ".join(value.split())

        if value not in report_text:
            return False

    return True


# Simple testing
if __name__ == "__main__":

    report = "Lost my black Samsung phone near the library"

    ai_response = {
        "item": "black Samsung phone",
        "colour": "black",
        "brand": "Samsung",
        "place": "library",
        "summary": "Black Samsung phone, library"
    }

    corrected = normalize_extraction(ai_response, report)

    print("Corrected AI response:")
    print(corrected)

    print("Valid response:", is_valid(corrected))
    print("Facts verified:", check_facts(corrected, report))
