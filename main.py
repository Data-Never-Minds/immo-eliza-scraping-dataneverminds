import requests
from bs4 import BeautifulSoup
import json

url = "https://www.immoweb.be/fr/annonce/maison/a-vendre/ixelles/1050/11075842"
r = requests.get(url)
c = r.content
#print(r.status_code)

soup = BeautifulSoup(c, "html.parser")

script_tags = soup.find_all("script", attrs={"type": "text/javascript"})

for script in script_tags:
    if "window.classified" in script.get_text():
        script_text = script.get_text()
        json_string = script_text.split('window.classified = ', 1)[1]
        json_string = json_string.rsplit(';', 1)[0]

        classified_data = json.loads(json_string)
        #print(classified_data)
        break

print("Property ID:", classified_data['id'])

my_dict = classified_data['property']

location = my_dict.get('location', {})
locality = location.get('locality', 'Default Value')
print("Locality name:", locality)

postalCode = my_dict['location']['postalCode']
print("Postal code:", postalCode)

living_area = my_dict['netHabitableSurface']
print("Living area:", living_area)

kitchen = my_dict['kitchen']
if kitchen:
    print("Equipped kitchen:", 1)
else:
    print("Equipped kitchen:", 0)

fireplaceCount = my_dict['fireplaceCount']
if fireplaceCount:
    print("Open fire:", 1)
else:
    print("Open fire:", 0)

terraceSurface = my_dict['terraceSurface']
if terraceSurface:
    print("Terrace:", terraceSurface)
else:
    print("Terrace:", 0)

gardenSurface = my_dict['gardenSurface']
if gardenSurface:
    print("Garden:", gardenSurface)
else:
    print("Garden:", 0)

netHabitableSurface = my_dict['netHabitableSurface']
if netHabitableSurface:
    print("Living area in m²:", netHabitableSurface)
else:
    print("Living area not found")

hasSwimmingPool = my_dict['hasSwimmingPool']
if hasSwimmingPool:
    print("Swimming pool:", 1)
else:
    print("Swimming pool:", 0)

property_type = classified_data['property']['type']
print(f"Type of Property: {property_type}")

number_of_rooms = classified_data['property'].get('bedroomCount', 0)
print(f"Number of Rooms: {number_of_rooms}")

furnished = 1 if classified_data['transaction'].get('sale', {}).get('isFurnished', False) else 0
print(f"Furnished: {furnished}")

sale_type = classified_data['transaction']['subtype'] if classified_data['transaction']['subtype'] != 'LIFE_SALE' else None
print(f"Type of Sale: {sale_type}")

price = classified_data['transaction']['sale']['price']
print(f"Price: {price}")
