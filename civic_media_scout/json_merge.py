import json
from datetime import datetime

from html_generator import read_json_file, sort_saved_json


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


def main():
    json1 = read_json_file("data.json")
    for entry in json1:
        url = str(entry.get("Source URL"))
        if url and url.endswith("/"):
            new_url = url.strip("/")
            for item in json1:
                link = str(item.get("Source URL"))
                if link == new_url:
                    print(
                        url,
                        parse_date(item["Last Update"]),
                        parse_date(entry["Last Update"]),
                    )
                    entry["Source URL"] = link
                    if parse_date(item["Last Update"]) > parse_date(
                        entry["Last Update"]
                    ):
                        json1.remove(entry)

    for entry in json1:
        url = str(entry.get("Source URL"))
        if url and not url.endswith("/"):
            entry["Source URL"] = (url + "/")
            
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(json1, f, ensure_ascii=False, indent=4)
    sort_saved_json("data.json")
    
    json1 = read_json_file("data.json")
    json2 = read_json_file("old_data.json")
    merged_json = merge_json_data(json1, json2)
    with open("merged.json", "w", encoding="utf-8") as f:
        json.dump(merged_json, f, ensure_ascii=False, indent=4)
    print("Output saved to:merged.json")
    sort_saved_json("merged.json")


if __name__ == "__main__":
    main()
