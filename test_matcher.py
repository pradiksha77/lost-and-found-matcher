
from matcher import score_pair

lost = {
    "date": "2026-10-05",
    "item": "phone",
    "colour": "black",
    "brand": "Samsung",
    "place": "library"
}

# Test 1: Perfect match
found1 = {
    "date": "2026-10-05",
    "item": "phone",
    "colour": "black",
    "brand": "Samsung",
    "place": "library"
}

# Test 2: Different item
found2 = {
    "date": "2026-10-05",
    "item": "wallet",
    "colour": "black",
    "brand": "Samsung",
    "place": "library"
}

# Test 3: Different colour
found3 = {
    "date": "2026-10-05",
    "item": "phone",
    "colour": "red",
    "brand": "Samsung",
    "place": "library"
}

# Test 4: Different brand
found4 = {
    "date": "2026-10-05",
    "item": "phone",
    "colour": "black",
    "brand": "Apple",
    "place": "library"
}

# Test 5: More than 30 days apart
found5 = {
    "date": "2026-11-15",
    "item": "phone",
    "colour": "black",
    "brand": "Samsung",
    "place": "library"
}

tests = [
    ("Perfect match", lost, found1, True),
    ("Different item", lost, found2, False),
    ("Different colour", lost, found3, False),
    ("Different brand", lost, found4, False),
    ("More than 30 days", lost, found5, False)
]

for name, lost_item, found_item, expected in tests:
    result = score_pair(lost_item, found_item)
    passed = (result is not None) == expected

    print(name, ":", "PASS" if passed else "FAIL")
