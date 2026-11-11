
from pathlib import Path
from matcher import find_matches
from llm_extractor import extract_report
from validator import is_valid, check_facts
import csv


def read_report(filename):
    reports = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            reports.append(row)

    return reports


def process_reports(raw_reports):
    processed = []

    for report in raw_reports:
        extracted = extract_report(report["report"])

        # Validate extracted information
        if not is_valid(extracted):
            print("Invalid report:", report["id"])
            continue

        if not check_facts(extracted, report["report"]):
            print("Fact check failed:", report["id"])
            continue

        # Combine original and extracted details
        processed.append({
            "id": report["id"],
            "date": report["date"],
            "report": report["report"],
            **extracted
        })

    return processed

def write_reports(matches, lost_reports, found_reports):

    from pathlib import Path
    from collections import defaultdict

    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    # Check for double claims
    claims = defaultdict(set)

    for match in matches:
        claims[match["found_id"]].add(match["lost_id"])

    # Save matches.csv
    match_rows = []

    for match in matches:
        row = match.copy()
        row["reasons"] = "; ".join(row["reasons"])
        row["double_claim"] = len(claims[row["found_id"]]) > 1
        match_rows.append(row)

    with open(output_folder / "matches.csv", "w",
              newline="", encoding="utf-8") as file:

        if match_rows:
            fieldnames = list(match_rows[0].keys())

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(match_rows)

        else:
            file.write("No matches found\n")

    # Save no_match.csv
    matched_lost = {m["lost_id"] for m in matches}

    no_match = [
        r for r in lost_reports
        if r["id"] not in matched_lost
    ]

    with open(output_folder / "no_match.csv", "w",
              newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "date", "report"],
            extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(no_match)

    # Save unclaimed.csv
    matched_found = {m["found_id"] for m in matches}

    unclaimed = [
        r for r in found_reports
        if r["id"] not in matched_found
    ]

    with open(output_folder / "unclaimed.csv", "w",
              newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "date", "report"],
            extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(unclaimed)

    # Save summary.txt
    double_claims = [
        item for item, lost_ids in claims.items()
        if len(lost_ids) > 1
    ]

    with open(output_folder / "summary.txt", "w",
              encoding="utf-8") as file:

        file.write("LOST AND FOUND MATCHER SUMMARY\n")
        file.write("------------------------------\n")
        file.write(f"Lost reports: {len(lost_reports)}\n")
        file.write(f"Found reports: {len(found_reports)}\n")
        file.write(f"Suggested matches: {len(matches)}\n")
        file.write(f"No-match lost reports: {len(no_match)}\n")
        file.write(f"Unclaimed found reports: {len(unclaimed)}\n")
        file.write(f"Possible double claims: {len(double_claims)}\n")

        for item in double_claims:
            file.write(
                f"Found item {item} suggested for: "
                + ", ".join(sorted(claims[item])) + "\n"
            )

    print("\nAll output files saved in the outputs folder!")


if __name__ == "__main__":

    # Read CSV files
    lost_raw = read_report("data/lost.csv")
    found_raw = read_report("data/found.csv")

    # Extract and validate details
    lost_reports = process_reports(lost_raw)
    found_reports = process_reports(found_raw)

    print("Lost reports processed:", len(lost_reports))
    print("Found reports processed:", len(found_reports))

    # Find matches
    matches = find_matches(lost_reports, found_reports)

    print("\nMATCHING RESULTS")

    for match in matches:
        print(match)
write_reports(matches, lost_reports, found_reports)