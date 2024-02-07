from bs4 import BeautifulSoup
import requests
import time

def get_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

url_list = []

# Loop through pages
for x in range(1, 2):
    # Construct the URL for each page
    url = f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={x}&orderBy=relevance'

    # Get links from the page
    for a in get_link(url).find_all('a', attrs={"class": "card__title-link"}):
        url_list.append(a.get("href"))

    # Avoid hitting the server too frequently
    time.sleep(0.2)

# Print all collected URLs
for url in url_list:
    print(url)
