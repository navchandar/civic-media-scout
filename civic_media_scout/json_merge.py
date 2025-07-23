import json
from datetime import datetime

from html_generator import sort_saved_json


def read_json_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except (ValueError, TypeError):
        return datetime.min  # fallback for invalid or missing dates


def merge_json_data(json1, json2):
    merged = {}

    for entry in json1 + json2:
        url = entry.get("Source URL")
        if not url:
            continue

        if url not in merged:
            merged[url] = entry
        else:
            existing = merged[url]
            if parse_date(entry.get("Last Update")) > parse_date(
                existing.get("Last Update")
            ):
                merged[url] = entry

    return list(merged.values())


if __name__ == "__main__":
    json1 = read_json_file("data.json")
    json2 = read_json_file("old_data.json")

    merged_json = merge_json_data(json1, json2)

    with open("merged.json", "w", encoding="utf-8") as f:
        json.dump(merged_json, f, ensure_ascii=False, indent=4)
    print("Output saved to:merged.json")

    sort_saved_json("merged.json")
