import os
import time
import requests
from bs4 import BeautifulSoup

import tldextract
from urllib.parse import urlparse


# Source
base_url = "https://igod.gov.in/advanced_search_more/{}/5"

# Range of offsets to iterate through
offsets = range(10, 20000, 5)

# Manually input headers and cookies here
headers = {
    "Cookie": "citrix_ns_id==; XSRF-TOKEN=%3D; igod-session=eyJ%3D",
    "Host":"igod.gov.in",
    "Referer":"https://igod.gov.in/advanced_search?keyword_web=&url=&cat_id_search=&sector_id=&state_id=&submit=submit&as_fid=",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}


# Create a session to persist headers and cookies
session = requests.Session()
session.headers.update(headers)

# Function to save unique links to file
def save(extracted_links):
    existing_links = set()
    base_urls = "./civic_media_scout/base_urls.txt"
    if os.path.exists(base_urls):
        with open(base_urls, "r", encoding="utf-8") as f:
            existing_links = set(line.strip() for line in f)
    new_links = [link for link in extracted_links if link not in existing_links]
    if new_links:
        with open(base_urls, "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(link + "\n")


def sort_urls_by_domain_and_path(urls):
    def sort_key(url):
        parsed = urlparse(url)
        ext = tldextract.extract(parsed.netloc)
        base_domain = f"{ext.domain}.{ext.suffix}"
        subdomain = ext.subdomain
        path = parsed.path
        return (base_domain, subdomain, path)

    return sorted(urls, key=sort_key)


def sort_urls():
    base_urls = "./civic_media_scout/base_urls.txt"
    with open(base_urls, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    sorted_urls = sort_urls_by_domain_and_path(urls)

    # Optionally write back to a file
    with open(base_urls, "w", encoding="utf-8") as f:
        for url in sorted_urls:
            f.write(url + "\n")


# Iterate through the URLs
for offset in offsets:
    # List to store extracted URLs
    extracted_links = []
    url = base_url.format(offset)
    print(f"{url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with class 'search-title'
        for a_tag in soup.find_all('a', class_='search-title'):
            href = a_tag.get('href')
            if href and href.startswith("http"):
                extracted_links.append(href)

    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
    finally:
        save(extracted_links)
        print(f"Extracted {len(extracted_links)} links")
        time.sleep(1)

sort_urls()

