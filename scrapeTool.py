import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url, keywords):
    try:
        # Fetch the website content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        found_keywords = {}

        # Check each link on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            try:
                link_response = requests.get(full_url)
                link_response.raise_for_status()
                link_soup = BeautifulSoup(link_response.text, 'html.parser')
                link_text = link_soup.get_text().lower()

                for word in keywords:
                    if word.lower() in link_text:
                        if word not in found_keywords:
                            found_keywords[word] = []
                        found_keywords[word].append(full_url)
            except requests.RequestException:
                continue

        # Display results
        if found_keywords:
            print("Found Keywords in the following pages:")
            for word, links in found_keywords.items():
                print(f"\n{word} found in:")
                for link in links:
                    print(f" - {link}")
        else:
            print("No keywords found on the linked pages.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    url = input("Enter the URL to scrape: ").strip()
    words_input = input("Enter keywords to search (comma separated): ").strip()
    keywords = [word.strip() for word in words_input.split(',') if word.strip()]
    scrape_website(url, keywords)
