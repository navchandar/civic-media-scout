import argparse
import asyncio
import json
import os
import random
import re
import time
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import aiohttp
import requests
import tldextract
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Suppress warning from urllib3 during request
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
json_file = "data.json"

# Semaphore to limit concurrent requests
semaphore = asyncio.Semaphore(10)

# Initialize parser
parser = argparse.ArgumentParser()

header = {
    "accept-encoding": "gzip, deflate",
    "accept-language": "en,en-US;q=0.9,en-IN;q=0.8",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "Referer": "https://www.google.com/",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}


# Define patterns for social media URLs
social_media_url_patterns = {
    "X Corp": "//x.com",
    "Twitter": "twitter.com",
    "Facebook": "facebook.com",
    "Instagram": "instagram.com",
    "YouTube": "youtube.com",
}


# Function to extract HTML content from url
def extract_html(url):
    try:
        response = requests.get(
            url, verify=False, timeout=20, headers=header, stream=False
        )
        response.raise_for_status()
        # override encoding by real educated guess as provided by chardet
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error loading url {url}: {e}")
        return None


# Function to check if a given url is html or a file
def is_content_type_html(url):
    try:
        # Perform a HEAD request to retrieve headers
        response = requests.head(url, timeout=20, headers=header)

        # Check if the request was successful (status code 200 or 2xx)
        if response.status_code // 100 == 2:
            # Check if the "Content-Type" header contains "text/html"
            content_type = response.headers.get("Content-Type", "")
            if "text/html" in content_type:
                return True  # The URL has a 'text/html' Content-Type header
            else:
                return False  # The URL does not have a 'text/html' Content-Type header
        else:
            return False  # Request failed with a non-2xx status code

    except requests.exceptions.RequestException as e:
        print(f"Error accessing url head {url}: {e}")
        return False


# Function to extract social media links
def extract_social_links(soup):
    social_links = {}
    ignore_list = [
        "/intent/",
        "/sharer/",
        "/share?",
        "/sharer.php",
        "explore/locations",
        "/p/",
        "/watch?",
        "facebook.com/#",
        "twitter.com/#",
        "instagram.com/#",
        "youtube.com/#",
        "/login",
        "/embed/",
        "profile.php",
        "/hashtag/",
        "invites/contact",
    ]
    for platform, pattern in social_media_url_patterns.items():
        # Search for links containing the social media pattern
        link = soup.find("a", href=lambda href: href and pattern in href.lower())
        if link and not (any(word in link["href"] for word in ignore_list)):
            social_links[platform] = link["href"]
    return social_links


# filter and deduplicate given list of items to avoid false positives
# Phone number & emails are usually never less than 8 chars
def filter_list(list_object, limiting_length=8):
    filtered_list = list(
        {
            item.strip()
            for item in list_object
            if item and len(item.strip()) >= limiting_length
        }
    )
    return filtered_list


# Function to extract email addresses
def extract_email_addresses(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    # email_pattern = (
    #     r"\b[A-Za-z0-9._%+-]+(?:\s?\[dot\]\s?|\s?\.\s?|\s?)"
    #     r"(?:[A-Za-z0-9._%+-]+(?:\s?\[at\]\s?|\s?\@\s?)[A-Za-z0-9.-]+\s?)"
    #     r"(?:\s?\[dot\]\s?|\s?\.\s?)(?:[A-Za-z]{2,7})\b"
    # )
    text = text.replace(" at nic dot in", "@nic.in")
    text = text.replace(" [at] ", "@").replace(" [dot] ", ".")
    text = text.replace("[at]", "@").replace("[dot]", ".")
    emails = re.findall(email_pattern, text)
    emails = filter_list(emails)
    ignore_list = ["webadmin", "webmaster"]
    emails = [
        email.replace("[at]", "@").replace("[dot]", ".").replace(" ", "")
        for email in emails
        if not (any(word in email for word in ignore_list))
    ]
    return emails


# Function to extract telephone numbers
def extract_telephone_numbers(text):
    phone_pattern = (
        r"(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|"
        r"(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)|"
        r"(\+91)?(-)?\s*?(91)?\s*?([6-9]{1}\d{2})-?\s*?(\d{3})-?\s*?(\d{4})"
    )
    phones = re.findall(phone_pattern, text)
    # Flatten the list of tuples into a single list
    phones = [phone for phone_tuple in phones for phone in phone_tuple if phone]
    return filter_list(phones)


# Function gather other links from given page and to remove unnecessary queries / anchors
def extract_other_links(soup, main_url, visited_urls):
    main_links = set()
    final_list = list()

    # Get all other links within this page even if no social data found
    links = soup.find_all("a", href=True)

    if links:
        # Extract the links into one list with absolute URLs
        absolute_urls = []
        for link in links:
            if not link or not link["href"]:
                continue
            href = link["href"]
            if not any(uri in href for uri in ("mailto", "tel")):
                if href.startswith(("http:", "https:")):
                    absolute_urls.append(href)
                else:
                    absolute_urls.append(urljoin(main_url, href))

        for url in absolute_urls:
            parsed_url = urlparse(url)
            main_link = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            main_links.add(main_link)

        # remove unnecessary links from the set
        for url in main_links:
            url = url.strip()
            for visited in visited_urls:
                if url not in visited:
                    final_list.append(url)

    return sorted(list(set(final_list)))


# Gather contact information from given webpage and store them in the data list
async def save_data_from(soup, url, data):
    if not url.endswith("/"):
        url = url + "/"
    extracted_data = {"Source URL": url}
    # Extract social media links, phone numbers and emails
    social_links = extract_social_links(soup)
    phones = extract_telephone_numbers(soup.text)
    emails = extract_email_addresses(soup.text)
    # Extract the page title if not found, use the website domain
    try:
        title = soup.title.string.strip()
    except:
        title = urlparse(url).netloc
    title = re.sub(r"\s+", " ", title).strip(" |/-")
    extracted_data["Page Title"] = title or urlparse(url).netloc
    print("Page Title:", extracted_data["Page Title"])

    if social_links or phones or emails:
        extracted_data.update(social_links)
        if phones:
            extracted_data["Phone"] = phones
        if emails:
            extracted_data["Email"] = emails

        # Store last update time in IST
        extracted_data["Last Update"] = str(
            datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        )
        print(extracted_data)
        data.append(extracted_data)

        # Incremental save data when possible
        async with asyncio.Lock():
            save_json(data)

        # Sleep to not overload server with requests
        await asyncio.sleep(random.uniform(1, 2.5))


def extract_tld(url):
    # Use tldextract to extract the TLD and domain components
    ext = tldextract.extract(url)
    # Return the TLD
    return ext.suffix


def extract_main_domain(url) -> str:
    # Use tldrextract to get the domain from url
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"


def sort_json(json_content):
    sorted_json_list = sorted(
        json_content,
        key=lambda x: (
            f"{extract_main_domain(x['Source URL'])}",
            x["Source URL"],
        ),
    )
    return sorted_json_list


def filter_keys(d, exclude=["Last Update"]):
    return {k: v for k, v in d.items() if k not in exclude}


# Save dict list into a JSON file
def save_json(json_content, indent=4):
    existing_data = {}

    # Load and index existing data
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing = sort_json(existing)
            existing_data = {item["Source URL"]: item for item in existing}

    # Check if new data introduces any changes
    updated = False
    for new_item in json_content:
        source_url = new_item["Source URL"]
        if (source_url not in existing_data) or (
            filter_keys(existing_data[source_url]) != filter_keys(new_item)
        ):
            existing_data[source_url] = new_item
            updated = True

    if not updated:
        return

    # Save only if there are updates
    updated_data = sort_json(list(existing_data.values()))
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=indent)
    print("Output saved to:", json_file)


def old_crawl_more(url, visited_urls, max_depth, data, filtered_links):
    """
    Crawl additional links with the same TLD but different domains.
    """
    base_domain = extract_tld(url)

    for link in filtered_links:
        if not link.startswith("http") or link in visited_urls:
            continue

        # Check if the link has a different domain but the same TLD
        if extract_tld(link) != base_domain:
            continue

        # Add in visited URLs to avoid loading site if not html
        visited_urls.add(link)

        if is_content_type_html(link) and max_depth > 1:
            print(
                f"Crawling: {link} | Data: {len(data)} | Visited: {len(visited_urls)}"
            )
            crawl_website(link, visited_urls, max_depth - 1, data)


def old_crawl_website(url, visited_urls, max_depth=2, data=[]):
    """
    Crawl a website and recursively follow links with the same TLD.
    """
    if data is None:
        data = []

    if max_depth == 0 or url in visited_urls:
        return data

    try:
        print(f"Visiting: {url}")
        soup = extract_html(url)
        if not soup:
            time.sleep(random.uniform(0.5, 1.0))
            return data

        visited_urls.add(url)
        data = save_data_from(soup, url, data)

        new_links = extract_other_links(soup, url, visited_urls)
        print(f"Found {len(new_links)} new URLs")

        crawl_more(url, visited_urls, max_depth, data, new_links)

    except Exception as e:
        print(f"Error crawling {url}: {e}")
        traceback.print_exc()

    return data


async def crawl_more(session, url, visited_urls, max_depth, data, filtered_links):
    base_domain = extract_tld(url)
    tasks = []
    for link in filtered_links:
        if not link.startswith("http") or link in visited_urls:
            continue
        if extract_tld(link) != base_domain:
            continue
        visited_urls.add(link)
        tasks.append(crawl_website(session, link, visited_urls, max_depth - 1, data))
    await asyncio.gather(*tasks)


async def crawl_website(session, url, visited_urls, max_depth=2, data=[]):
    if max_depth == 0 or url in visited_urls:
        return
    visited_urls.add(url)
    soup = await fetch_html(session, url)
    if not soup:
        await asyncio.sleep(random.uniform(0.5, 1.0))
        return
    await save_data_from(soup, url, data)
    if max_depth > 1:
        new_links = extract_other_links(soup, url, visited_urls)
        print(f"Found {len(new_links)} new URLs")
        await crawl_more(session, url, visited_urls, max_depth, data, new_links)


async def fetch_html(session, url):
    async with semaphore:
        try:
            print(f"Visiting: {url}")
            async with session.get(url, headers=header, ssl=False) as response:
                if "text/html" in response.headers.get("Content-Type", ""):
                    text = await response.text()
                    return BeautifulSoup(text, "html.parser")
        except Exception as e:
            print(f"Error loading url {url}: {e}")
    return None


async def get_base_urls():
    """Get base urls from txt file"""
    base_urls = "./civic_media_scout/base_urls.txt"
    with open(base_urls, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def old_main():
    parser.add_argument(
        "-d",
        "--max_depth",
        type=int,
        default=3,
        help="The depth of crawling needed from each website. Higher the depth, longer the runtime. (default: 3)",
    )
    args = parser.parse_args()
    max_depth = args.max_depth

    # Use set to avoid revisiting the same URLs
    visited_urls = set()
    for website in get_base_urls():
        data_rows = crawl_website(website, visited_urls, max_depth)
        print(len(data_rows))
        save_json(data_rows)


async def main_async(max_depth):
    visited_urls = set()
    data = []
    base_urls = await get_base_urls()
    print(f"Found {len(base_urls)} links in base_urls.txt file")

    async with aiohttp.ClientSession(timeout=ClientTimeout(total=30)) as session:
        tasks = [
            crawl_website(session, url, visited_urls, max_depth, data)
            for url in base_urls
        ]
        await asyncio.gather(*tasks)
    save_json(data)
    print(f"Saved {len(data)} records to {json_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--max_depth", type=int, default=3, help="Depth of crawling (default: 3)"
    )
    args = parser.parse_args()
    asyncio.run(main_async(args.max_depth))
