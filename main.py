
import csv
from pathlib import Path
from collections import defaultdict

from matcher import find_matches
from llm_extractor import extract_report
from validator import is_valid, check_facts, normalize_extraction


# Function 1: Read reports from CSV
def read_report(filename):

    reports = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {"id", "date", "report"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"{filename} must contain id, date and report columns."
            )

        for row in reader:
            if row["id"] and row["date"] and row["report"]:
                reports.append(row)

    return reports


# Function 2: Extract and validate report information
def process_reports(raw_reports):

    processed = []

    for report in raw_reports:

        try:
            # Extract information using AI
            extracted = extract_report(report["report"])

            # Correct common AI category variations
            extracted = normalize_extraction(
                extracted,
                report["report"]
            )

            # Check extracted information
            if not is_valid(extracted):
                print("Invalid report:", report["id"])
                continue

            # Verify facts against original report
            if not check_facts(extracted, report["report"]):
                print("Fact check failed:", report["id"])
                continue

            # Combine original and extracted information
            processed.append({
                "id": report["id"],
                "date": report["date"],
                "report": report["report"],
                **extracted
            })

        except Exception as error:
            print("Error processing report:", report["id"])
            print("Reason:", error)

    return processed


# Function 3: Write all output files
def write_reports(matches, lost_reports, found_reports):

    output_folder = Path("outputs")
    output_folder.mkdir(exist_ok=True)

    # Identify possible double claims
    claims = defaultdict(set)

    for match in matches:
        claims[match["found_id"]].add(match["lost_id"])

    # Save matches.csv
    match_rows = []

    for match in matches:

        row = match.copy()

        # Support either a list or string of reasons
        if isinstance(row["reasons"], list):
            row["reasons"] = "; ".join(row["reasons"])

        row["double_claim"] = (
            len(claims[row["found_id"]]) > 1
        )

        match_rows.append(row)

    with open(
        output_folder / "matches.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "lost_id",
            "found_id",
            "score",
            "status",
            "reasons",
            "double_claim"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(match_rows)

    # Find lost reports without suggested matches
    matched_lost = {
        match["lost_id"] for match in matches
    }

    no_match = [
        report for report in lost_reports
        if report["id"] not in matched_lost
    ]

    # Save no_match.csv
    with open(
        output_folder / "no_match.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "date", "report"]
        )

        writer.writeheader()
        writer.writerows(no_match)

    # Find found reports without suggested matches
    matched_found = {
        match["found_id"] for match in matches
    }

    unclaimed = [
        report for report in found_reports
        if report["id"] not in matched_found
    ]

    # Save unclaimed.csv
    with open(
        output_folder / "unclaimed.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "date", "report"]
        )

        writer.writeheader()
        writer.writerows(unclaimed)

    # Identify double-claimed found items
    double_claims = [
        item for item, lost_ids in claims.items()
        if len(lost_ids) > 1
    ]

    # Save summary.txt
    with open(
        output_folder / "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("LOST AND FOUND MATCHER SUMMARY\n")
        file.write("------------------------------\n")

        file.write(
            f"Lost reports: {len(lost_reports)}\n"
        )

        file.write(
            f"Found reports: {len(found_reports)}\n"
        )

        file.write(
            f"Suggested matches: {len(matches)}\n"
        )

        file.write(
            f"No-match lost reports: {len(no_match)}\n"
        )

        file.write(
            f"Unclaimed found reports: {len(unclaimed)}\n"
        )

        file.write(
            f"Possible double claims: {len(double_claims)}\n"
        )

        for item in double_claims:

            file.write(
                f"\nFound item {item} suggested for: "
                + ", ".join(sorted(claims[item]))
                + "\n"
            )

    print("\nAll four output files saved in the outputs folder!")


# Main program
if __name__ == "__main__":

    # Read original CSV files
    lost_raw = read_report("data/lost.csv")
    found_raw = read_report("data/found.csv")

    # Extract and validate lost reports
    print("Processing lost reports...")
    lost_processed = process_reports(lost_raw)

    # Extract and validate found reports
    print("\nProcessing found reports...")
    found_processed = process_reports(found_raw)

    print("\nPROCESSING SUMMARY")
    print("------------------")

    print(
        "Lost reports successfully processed:",
        len(lost_processed)
    )

    print(
        "Found reports successfully processed:",
        len(found_processed)
    )

    # Compare every valid lost report with every valid found report
    matches = find_matches(
        lost_processed,
        found_processed
    )

    print("\nMATCHING RESULTS")

    for match in matches:
        print(match)

    # Write outputs using ALL original reports
    write_reports(
        matches,
        lost_raw,
        found_raw
    )
