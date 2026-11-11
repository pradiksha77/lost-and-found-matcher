
import re

# Allowed item categories
ALLOWED_ITEMS = {
    "phone",
    "wallet",
    "id_card",
    "bottle",
    "bag",
    "earphones",
    "keys",
    "umbrella",
    "calculator",
    "watch",
    "spectacles",
    "other"
}

# Ten supported colours
ALLOWED_COLOURS = {
    "black", "white", "red", "blue", "green",
    "yellow", "brown", "pink", "purple", "orange"
}

# Required JSON fields
REQUIRED_FIELDS = {
    "item", "colour", "brand", "place", "summary"
}

# Function 1: Check whether AI response is valid
def is_valid(data):

    # Check whether response is a dictionary
    if not isinstance(data, dict):
        return False

    # Check whether all required fields are present
    if set(data.keys()) != REQUIRED_FIELDS:
        return False

    # Check item category
    if not isinstance(data["item"], str):
        return False

    if data["item"] not in ALLOWED_ITEMS:
        return False

    # Check colour
    if data["colour"] is not None:
        if not isinstance(data["colour"], str):
            return False

        if data["colour"].lower() not in ALLOWED_COLOURS:
            return False

    # Check brand
    if data["brand"] is not None:
        if not isinstance(data["brand"], str) or not data["brand"].strip():
            return False

    # Check place
    if data["place"] is not None:
        if not isinstance(data["place"], str) or not data["place"].strip():
            return False

    # Check summary
    if not isinstance(data["summary"], str):
        return False

    if len(data["summary"].split()) > 8:
        return False

    return True

# Function 2: Check extracted facts against original report
def check_facts(data, report):

    # Check the basic JSON structure first
    if not is_valid(data):
        return False

    # Convert report into lowercase text
    report_text = report.lower()

    # Remove punctuation for easier comparison
    report_text = re.sub(r"[^a-z0-9\s]", " ", report_text)
    report_text = " ".join(report_text.split())

    # Check colour, brand and place
    for field in ["colour", "brand", "place"]:

        value = data[field]

        # Skip fields containing null
        if value is None:
            continue

        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9\s]", " ", value)
        value = " ".join(value.split())

        # Reject facts not found in original report
        if value not in report_text:
            return False

    return True

# Simple testing
if __name__ == "__main__":

    report = "Lost my black Samsung phone near the library"

    ai_response = {
        "item": "phone",
        "colour": "black",
        "brand": "Samsung",
        "place": "library",
        "summary": "Black Samsung phone, library"
    }

    print("Checking AI response...")

    print("Valid response:", is_valid(ai_response))

    print("Facts verified:", check_facts(ai_response, report))