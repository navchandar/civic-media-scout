import os
import json
from urllib.parse import urlparse
from html_generator import read_json_file

# Load the entries from data.json
input_file = "data.json"

# Create output directory if it doesn't exist
output_dir = os.path.join("public", "domains")
os.makedirs(output_dir, exist_ok=True)

# Load the main entries.json file
print(f"Reading {input_file}")
entries = read_json_file(input_file)

# Organize entries by domain
domain_map = {}
for entry in entries:
    source_url = entry.get("Source URL", "")
    if not source_url:
        continue
    domain = urlparse(source_url).netloc
    if domain not in domain_map:
        domain_map[domain] = []
    domain_map[domain].append(entry)

# Write each domain's entries to a separate JSON file
for domain, domain_entries in domain_map.items():
    domain_file = os.path.join(output_dir, f"{domain}.json")
    with open(domain_file, 'w', encoding='utf-8') as f:
        json.dump(domain_entries, f, indent=2)
    print(f"Added: {domain_file} with {len(domain_entries)} entries")

print(f"✅ Processed {len(domain_map)} domains from {len(entries)} total entries.")

