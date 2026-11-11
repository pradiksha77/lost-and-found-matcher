
from matcher import score_pair


# Sample lost report
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


# Test 6: Other items cannot automatically match
lost_other = {
    "date": "2026-10-05",
    "item": "other",
    "colour": "black",
    "brand": None,
    "place": "library"
}

found_other = {
    "date": "2026-10-05",
    "item": "other",
    "colour": "black",
    "brand": None,
    "place": "library"
}


# Evaluation test cases
tests = [
    ("Perfect match", lost, found1, True, 5),
    ("Different item", lost, found2, False, None),
    ("Different colour", lost, found3, False, None),
    ("Different brand", lost, found4, False, None),
    ("More than 30 days", lost, found5, False, None),
    ("Other item rejection", lost_other, found_other, False, None)
]


# Run all tests
print("\nLOST AND FOUND MATCHER - EVALUATION")
print("-----------------------------------")

passed_count = 0

for name, lost_item, found_item, expected, expected_score in tests:

    result = score_pair(lost_item, found_item)

    passed = (
        (result is not None) == expected
        and (
            result is None
            or result["score"] == expected_score
        )
    )

    if passed:
        passed_count += 1

    print(
        name,
        ":",
        "PASS" if passed else "FAIL"
    )

print("-----------------------------------")
print("Tests passed:", passed_count, "/", len(tests))
print("Evaluation completed.")
