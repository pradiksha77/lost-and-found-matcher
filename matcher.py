
from datetime import datetime


# Function 1: Compare one lost report with one found report
def score_pair(lost, found):

    # Read report details safely
    lost_date = datetime.strptime(lost["date"], "%Y-%m-%d")
    found_date = datetime.strptime(found["date"], "%Y-%m-%d")

    lost_item = str(lost.get("item", "")).lower().strip()
    found_item = str(found.get("item", "")).lower().strip()

    lost_colour = lost.get("colour")
    found_colour = found.get("colour")

    lost_brand = lost.get("brand")
    found_brand = found.get("brand")

    lost_place = lost.get("place")
    found_place = found.get("place")

    # Rule 1: Reports must be within 30 days
    if abs((found_date - lost_date).days) > 30:
        return None

    # Rule 2: Item types must be the same
    if lost_item != found_item:
        return None

    # "other" items cannot automatically match
    if lost_item == "other":
        return None

    # Rule 3: Reject different known colours
    if lost_colour and found_colour:
        if str(lost_colour).lower().strip() != str(found_colour).lower().strip():
            return None

    # Rule 4: Reject different known brands
    if lost_brand and found_brand:
        if str(lost_brand).lower().strip() != str(found_brand).lower().strip():
            return None

    # Calculate matching score
    score = 0
    reasons = []

    # Same colour = 2 points
    if lost_colour and found_colour:
        if str(lost_colour).lower().strip() == str(found_colour).lower().strip():
            score += 2
            reasons.append("Same colour (+2)")

    # Same brand = 2 points
    if lost_brand and found_brand:
        if str(lost_brand).lower().strip() == str(found_brand).lower().strip():
            score += 2
            reasons.append("Same brand (+2)")

    # Same place = 1 point
    if lost_place and found_place:
        if str(lost_place).lower().strip() == str(found_place).lower().strip():
            score += 1
            reasons.append("Same place (+1)")

    # Decide match status
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


# Function 2: Compare all lost reports with all found reports
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
                    "reasons": ", ".join(result["reasons"])
                }

                all_matches.append(match)

    # Sort matches from highest score to lowest
    all_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return all_matches


# Simple testing
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
