import requests
from bs4 import BeautifulSoup
import json

url = "https://www.immoweb.be/fr/annonce/maison/a-vendre/ixelles/1050/11075842"
r = requests.get(url)
c = r.content
#print(r.status_code)

soup = BeautifulSoup(c, "html.parser")

# Find all rows in the table
all_rows = soup.find_all('tr', attrs={"class": 'classified-table__row'})

# Initialize lists to store headers and data
headers = []
data = []

# Iterate over each row and extract headers and data
for row in all_rows:
    header = row.find('th', {"class":"classified-table__header"})
    data_cell = row.find('td', {"class":"classified-table__data"})

    if header and data_cell:
        headers.append(header.get_text(strip=True))
        data.append(data_cell.get_text(strip=True))

# Use zip to iterate over headers and data together
for header, data_cell in zip(headers, data):
    print(f"{header}, {data_cell}")
