import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def scrape_website(url, keywords):
    try:
        # Fetch and parse the main page
        soup = fetch_and_parse(url)
        if not soup:
            return

        # Process links and find keywords
        found_keywords = process_links(soup, url, keywords)

        # Display results
        display_results(found_keywords)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")


def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def process_links(soup, base_url, keywords):
    found_keywords = {}
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        link_text = fetch_link_text(full_url)
        if link_text:
            check_keywords(link_text, full_url, keywords, found_keywords)
    return found_keywords


def fetch_link_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        link_soup = BeautifulSoup(response.text, 'html.parser')
        return link_soup.get_text().lower()
    except requests.RequestException:
        return None


def check_keywords(link_text, url, keywords, found_keywords):
    for word in keywords:
        if word.lower() in link_text:
            if word not in found_keywords:
                found_keywords[word] = []
            found_keywords[word].append(url)


def display_results(found_keywords):
    if found_keywords:
        print("Found Keywords in the following pages:")
        for word, links in found_keywords.items():
            print(f"\n{word} found in:")
            for link in links:
                print(f" - {link}")
    else:
        print("No keywords found on the linked pages.")

if __name__ == '__main__':
    url = input("Enter the URL to scrape: ").strip()
    words_input = input("Enter keywords to search (comma separated): ").strip()
    keywords = [word.strip() for word in words_input.split(',') if word.strip()]
    scrape_website(url, keywords)
