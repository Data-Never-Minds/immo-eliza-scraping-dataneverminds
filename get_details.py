import requests
from bs4 import BeautifulSoup
import json

url = "https://www.immoweb.be/fr/annonce/maison/a-vendre/ixelles/1050/11075842"
r = requests.get(url)
c = r.content
#print(r.status_code)

soup = BeautifulSoup(c, "html.parser")

if soup.find("span"):
    soup.find("span").decompose()

print(soup.text.strip())
