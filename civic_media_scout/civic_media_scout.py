import json
import os
import random
import re
import time
import traceback
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import requests
import tldextract
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Suppress warning from urllib3 during request
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Define patterns for social media URLs
social_media_url_patterns = {
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
        soup = BeautifulSoup(response.text, "html.parser")
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
def save_data_from(soup, url, data):
    extracted_data = dict()
    extracted_data["Source URL"] = url

    # Extract social media links, phone numbers and emails
    social_links = extract_social_links(soup)
    phones = extract_telephone_numbers(soup.text)
    emails = extract_email_addresses(soup.text)
    # Extract the page title if not found, use the website domain
    try:
        title = soup.title.string.strip()
    except:
        title = urlparse(url).netloc
    title = title.replace("\r\n", " ").replace("\n", " ").replace("  ", " ")
    title = title.strip().strip("|").strip("/").strip().replace("  ", " ")
    if (not title) or ("" == title):
        title = urlparse(url).netloc

    print("Page Title:", title)
    extracted_data["Page Title"] = title

    # save the data to output only if any contact info found
    if social_links or phones or emails:
        if social_links:
            extracted_data = {**extracted_data, **social_links}
        if phones:
            extracted_data["Phone"] = phones
        if emails:
            extracted_data["Email"] = emails

        # Store last update time in IST
        extracted_data["Last Update"] = str(
            datetime.utcnow() + timedelta(hours=5, minutes=30)
        )
        print(extracted_data)
        print("")
        data.append(extracted_data)

        # Sleep to not overload server with requests
        time.sleep(random.uniform(1.5, 2.5))
    return data


def extract_tld(url):
    # Use tldextract to extract the TLD and domain components
    ext = tldextract.extract(url)
    # Return the TLD
    return ext.suffix


def extract_main_domain(url):
    # Use tldrextract to get the domain from url
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"


def sort_json(json_content):
    sorted_json_list = sorted(
        json_content, key=lambda x: extract_main_domain(x["Source URL"])
    )
    return sorted_json_list


# Save dict list into a JSON file
def save_json(json_content, indent=4):
    json_file = "data.json"
    existing_data = {}
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing = sort_json(existing)
            # Create a dictionary with "Source URL" as keys
            existing_data = {item["Source URL"]: item for item in existing}

    # Update the dictionary with new data
    for new_item in json_content:
        source_url = new_item["Source URL"]
        existing_data[source_url] = new_item

    # Convert the updated dictionary back to a list
    updated_data = list(existing_data.values())
    updated_data = sort_json(updated_data)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=indent)
    print("Output saved to:", json_file)


def crawl_more(
    url,
    visited_urls,
    max_depth,
    data,
    filtered_links,
):
    # Find and crawl linked websites with different domains but same TLD
    base_domain = extract_tld(url)
    for absolute_url in filtered_links:
        parsed_link = urlparse(absolute_url)
        # Check if the link has a different domain but the same TLD
        if parsed_link and extract_tld(absolute_url) == base_domain:
            absolute_url = str(absolute_url)
            if absolute_url.startswith("http") and absolute_url not in visited_urls:
                # Add in visited URLs to avoid loading site if not html
                visited_urls.add(absolute_url)

                # ignore files/other content and only extract html
                if is_content_type_html(absolute_url) and max_depth > 1:
                    print(
                        absolute_url,
                        "data count =",
                        len(data),
                        "visited count =",
                        len(visited_urls),
                    )
                    crawl_website(absolute_url, visited_urls, max_depth - 1, data)


# Function to crawl a website and its linked websites
def crawl_website(url, visited_urls, max_depth=2, data=[]):
    if max_depth == 0:
        return
    try:
        print("url:", url)
        soup = extract_html(url)
        if soup:
            # Add in visited URLs to avoid loading site again
            visited_urls.add(url)

            data = save_data_from(soup, url, data)

            # Deduplicate and filter the links
            new_links = extract_other_links(soup, url, visited_urls)
            print("Found URLs =", len(new_links))

            crawl_more(
                url,
                visited_urls,
                max_depth,
                data,
                new_links,
            )

        else:
            time.sleep(random.uniform(0.5, 1.0))

    except Exception as e:
        print(f"Error crawling {url}: {e}")
        traceback.print_exc()
    return data


if __name__ == "__main__":
    base_urls = "./civic_media_scout/base_urls.txt"
    with open(base_urls, "r", encoding="utf-8") as file:
        starting_urls = [line.strip() for line in file]

    # Use set to avoid revisiting the same URLs
    visited_urls = set()

    for website in starting_urls:
        data_rows = crawl_website(website, visited_urls, 3)
        print(len(data_rows))
        save_json(data_rows)
