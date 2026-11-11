
from datetime import datetime

def score_pair(lost, found):
    # Convert dates
    lost_date = datetime.strptime(lost["date"], "%Y-%m-%d")
    found_date = datetime.strptime(found["date"], "%Y-%m-%d")

    # Rule 1: Reports must be within 30 days
    if abs((found_date - lost_date).days) > 30:
        return None

    # Rule 2: Item type must be the same
    if lost["item"] != found["item"]:
        return None

    # "other" items cannot automatically match
    if lost["item"] == "other":
        return None

    # Rule 3: Reject different colours
    if (lost["colour"] and found["colour"]
            and lost["colour"] != found["colour"]):
        return None

    # Rule 4: Reject different brands
    if (lost["brand"] and found["brand"]
            and lost["brand"].lower() != found["brand"].lower()):
        return None

    # Calculate score
    score = 0
    reasons = []

    if lost["colour"] and lost["colour"] == found["colour"]:
        score += 2
        reasons.append("Same colour (+2)")

    if (lost["brand"] and found["brand"]
            and lost["brand"].lower() == found["brand"].lower()):
        score += 2
        reasons.append("Same brand (+2)")

    if (lost["place"] and found["place"]
            and lost["place"].lower() == found["place"].lower()):
        score += 1
        reasons.append("Same place (+1)")

    if score >= 3:
        status = "Likely"
    elif score >= 1:
        status = "Possible"
    else:
        return None

    return {
        "score": score,
        "status": status,
        "reasons": reasons
    }

def find_matches(lost_reports, found_reports):
    all_matches = []

    for lost in lost_reports:
        for found in found_reports:

            result = score_pair(lost, found)

            if result is not None:
                match = {
                    "lost_id": lost["id"],
                    "found_id": found["id"],
                    "score": result["score"],
                    "status": result["status"],
                    "reasons": result["reasons"]
                }

                all_matches.append(match)

    # Sort highest scores first
    all_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return all_matches



if __name__ == "__main__":

    lost_reports = [
        {
            "id": "L01",
            "date": "2026-10-05",
            "item": "phone",
            "colour": "black",
            "brand": "Samsung",
            "place": "library"
        }
    ]

    found_reports = [
        {
            "id": "F01",
            "date": "2026-10-05",
            "item": "phone",
            "colour": "black",
            "brand": "Samsung",
            "place": "library"
        }
    ]

    results = find_matches(lost_reports, found_reports)

    print("All Matching Results:")
    for match in results:
        print(match)

   