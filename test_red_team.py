
from validator import is_valid, check_facts
from matcher import score_pair

# Test 1: Brand guessing
report1 = "Lost my black phone near the library"

response1 = {
    "item": "phone",
    "colour": "black",
    "brand": "Samsung",
    "place": "library",
    "summary": "Black phone near library"
}

print("Test 1 - Brand guessing:",
      "PASS" if not check_facts(response1, report1) else "FAIL")


# Test 2: Vague claim
lost = {
    "date": "2026-10-05",
    "item": "other",
    "colour": None,
    "brand": None,
    "place": None
}

found = {
    "date": "2026-10-05",
    "item": "other",
    "colour": None,
    "brand": None,
    "place": None
}

print("Test 2 - Vague claim:",
      "PASS" if score_pair(lost, found) is None else "FAIL")


# Test 3: Invented colour
report3 = "Lost my phone near the library"

response3 = {
    "item": "phone",
    "colour": "red",
    "brand": None,
    "place": "library",
    "summary": "Red phone near library"
}

print("Test 3 - Invented colour:",
      "PASS" if not check_facts(response3, report3) else "FAIL")
