
import re

ALLOWED_ITEMS = {
    "phone", "wallet", "id_card", "bottle", "bag",
    "earphones", "keys", "umbrella", "calculator",
    "watch", "spectacles", "other"
}

COLOURS = {
    "black", "white", "red", "blue", "green",
    "yellow", "brown", "pink", "purple", "orange"
}

PLACES = [
    "computer lab", "maths block", "sports ground",
    "main gate", "bus stop", "classroom",
    "library", "canteen"
]

def extract_report(report):
    text = report.lower()

    # Identify item
    item = "other"

    keywords = {
        "phone": ["phone", "mobile"],
        "wallet": ["wallet"],
        "id_card": ["id card"],
        "bottle": ["bottle"],
        "bag": ["bag", "backpack"],
        "earphones": ["earphones"],
        "keys": ["keys"],
        "umbrella": ["umbrella"],
        "calculator": ["calculator"],
        "watch": ["watch"],
        "spectacles": ["spectacles", "glasses"]
    }

    for category, words in keywords.items():
        if any(word in text for word in words):
            item = category
            break

    # Identify colour
    colour = None
    for c in COLOURS:
        if re.search(r"\b" + c + r"\b", text):
            colour = c
            break

    # Identify brand
    brand = None
    for b in ["Samsung", "Casio"]:
        if b.lower() in text:
            brand = b

    # Identify place
    place = None
    for p in PLACES:
        if p in text:
            place = p
            break

    # Create short summary
    summary = " ".join(report.split()[:5])

    return {
        "item": item,
        "colour": colour,
        "brand": brand,
        "place": place,
        "summary": summary
    }

if __name__ == "__main__":

    sample_report = "Lost my black Samsung phone near the library"

    result = extract_report(sample_report)

    print("Original Report:")
    print(sample_report)

    print("\nExtracted Details:")
    print(result)
