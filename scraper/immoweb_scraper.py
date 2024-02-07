import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from .utils import get_soup
import time


def get_links(base_url, pages):
    """Fetch property links from multiple pages."""
    url_list = []
    for x in range(1, pages+1):
        print(f"Extracting URLs from Page {x}")
        full_url = base_url.format(x)
        soup = get_soup(full_url)
        for a in soup.find_all('a', attrs={"class": "card__title-link"}):
            url_list.append(a.get("href"))
    return url_list


def get_property_details(url):
    """Get details from a single property page."""
    soup = get_soup(url)
    script_tags = soup.find_all("script", attrs={"type": "text/javascript"})
    for script in script_tags:
        if "window.classified" in script.get_text():
            script_text = script.get_text()
            json_string = script_text.split('window.classified = ', 1)[
                1].rsplit(';', 1)[0]
            results = json.loads(json_string)
            return results


def get_links_concurrently(base_url, pages=15):
    """Fetch property links from multiple pages concurrently."""
    def fetch_links_from_page(page_number):
        """Function to fetch links from a single page."""
        page_url = base_url.format(page_number)
        soup = get_soup(page_url)
        links = [a.get("href") for a in soup.find_all(
            'a', attrs={"class": "card__title-link"})]
        return links

    url_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all pages to be fetched concurrently
        future_to_page = {executor.submit(
            fetch_links_from_page, page): page for page in range(1, pages + 1)}

        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                page_links = future.result()
                url_list.extend(page_links)
                print(f"Extracted URLs from Page {page}")
            except Exception as exc:
                print(f"Page {page} generated an exception: {exc}")

    return url_list


def fetch_details_concurrently(url_list):
    """Fetch property details for a list of URLs concurrently."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        futures = {executor.submit(
            get_property_details, url): url for url in url_list}
        results = []
        for future in futures:
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (futures[future], exc))
        end = time.time()
        print("Time Taken: {:.6f}s".format(end-start))
    return results
