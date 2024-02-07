import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from .utils import get_soup  
import time

def get_links(base_url, pages=2):
    """Fetch property links from multiple pages."""
    url_list = []
    for x in range(1, pages + 1):
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
            json_string = script_text.split('window.classified = ', 1)[1].rsplit(';', 1)[0]
            results = json.loads(json_string)
            return results

def fetch_details_concurrently(url_list):
    """Fetch property details for a list of URLs concurrently."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        futures = {executor.submit(get_property_details, url): url for url in url_list}
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
