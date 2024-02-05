from bs4 import BeautifulSoup
import requests
import time
import threading
import pandas as pd

url_list = []


def to_csv(data: dict, save='.data.csv'):
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(save, index=False)


def get_link(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html-parse")

    return soup


for x in range(1, 2):
    time.sleep(0.2)
    for a in get_link(f'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={x}&orderBy=relevance').find_all('a', attrs={"class": "card__title-link"}):
        url_list.append(a.get("href"))


data = get_link(url_list[0]).find_all(
    'div', attrs={"class": 'accordion__content'})
print(data)
# for x in data:
#   teste_1 = x.find(
#      'th', attrs={"class": 'classified-table__header'})
# print(teste_1)
# print(x.find('td', attrs={"class": 'classified-table__data'}).content)
