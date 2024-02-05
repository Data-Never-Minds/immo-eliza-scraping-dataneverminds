from bs4 import BeautifulSoup
import requests
import time
import threading

url_list = []


def get_link(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    return soup


for x in range(1, 2):
    time.sleep(0.2)
    for a in get_link(f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={x}&orderBy=relevance').find_all('a', attrs={"class": "card__title-link"}):
        url_list.append(a.get("href"))


for url in url_list:
    print(get_link(url).find_all('tr', attrs={
          "class": 'classified-table__row'}))
