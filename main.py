from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd

url_list = []
all_Information = []


def to_csv(data: dict, save='data.csv') -> None:
    try:
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(save, index=False)

    except requests.RequestException as error:
        print(f"Um erro ocorreu: {error}")
        return None


url = "https://www.immoweb.be/fr/annonce/maison/a-vendre/ixelles/1050/11075842"
r = requests.get(url)
c = r.content
# print(r.status_code)

soup = BeautifulSoup(c, "html.parser")

script_tags = soup.find_all("script", attrs={"type": "text/javascript"})

for script in script_tags:
    if "window.classified" in script.get_text():
        script_text = script.get_text()
        json_string = script_text.split('window.classified = ', 1)[1]
        json_string = json_string.rsplit(';', 1)[0]

        classified_data = json.loads(json_string)
        # print(classified_data)
        break


for url in url_list:
    time.sleep(0.2)
    r = requests.get(url)
    c = r.content
    # print(r.status_code)

    soup = BeautifulSoup(c, "html.parser")

    script_tags = soup.find_all("script", attrs={"type": "text/javascript"})

    for script in script_tags:
        if "window.classified" in script.get_text():
            script_text = script.get_text()
            json_string = script_text.split('window.classified = ', 1)[1]
            json_string = json_string.rsplit(';', 1)[0]

            classified_data = json.loads(json_string)
            # print(classified_data)
            break

    classified_data_id = classified_data.get('id')
    print("Property ID:", classified_data['id'])

    my_dict = classified_data['property']

    location = my_dict.get('location', {})
    locality = location.get('locality', 'Default Value')
    print("Locality name:", locality)
    if not location == {}:
        postalCode = my_dict['location']['postalCode']
        print("Postal code:", postalCode)
        country = my_dict['lacation']['country']
        print('Country: ', country)
        region = my_dict['location']['region']
        print('Region:', region)
        province = my_dict['location']['province']
        print('Province: ', province)
        street = my_dict['location']['street']
        print('Street:', street)
        number_house = my_dict['location']['number']
        print('Number: ', number_house)
        box = my_dict['location']['box']
        print("Box: ", box)
        property_name = my_dict['location']['propertyName']
        print("Property Name: ", property_name)
        floor = my_dict['location']['floor']
        print('Floor: ', floor)
        latitude = my_dict['location']['latitude']
        print('Latitude: ', latitude)
        longitude = my_dict['location']['longitude']
        print('Longitude: ', longitude)
        distance = my_dict['location']['distance']
        print("Distance: ", distance)
        aproximated = my_dict['location']['aproximated']
        print('Aproximated: ', aproximated)
        region_code = my_dict['location']['regionCode']
        print('Region Code:', region_code)
        type_residence = my_dict['location']['type']
        print('type of Residence: ', type_residence)
        district = my_dict['location']['district']
        print("District: ", district)
        living_area = my_dict['netHabitableSurface']
        print("Living area:", living_area)
        sea_view = my_dict['location']['hasSeaView']
        print('Has Sea View:', sea_view)

    kitchen = my_dict.get('kitchen')
    kitchen_qnt = 1 if kitchen else 0
    print("Equipped kitchen:", kitchen_qnt)

    if kitchen:
        kitchen_surface = kitchen.get('surface')
        print(kitchen_surface)
        kitchen_type = kitchen.get('type')
        print(kitchen_type)
        kitchen_oven = kitchen.get('hasOven')
        print(kitchen_oven)
        kitchen_micro_wave = kitchen.get('hasMicroWaveOven')
        print(kitchen_micro_wave)
        kitchen_dish_washer = kitchen.get('hasDiswasher')
        print(kitchen_dish_washer)
        kitchen_machine = kitchen.get('hasWashingMachine')
        print(kitchen_machine)
        kitchen_fridge = kitchen.get('hasFridge')
        print(kitchen_fridge)
        kitchen_freezer = kitchen.get('hasFreezer')
        print(kitchen_freezer)
        kitchen_steam_oven = kitchen.get('hasSteamOven')
        print(kitchen_steam_oven)

    fireplaceCount = my_dict['fireplaceCount']
    open_fire = 1 if fireplaceCount else 0

    print("Open fire:", open_fire)

    terraceSurface = my_dict.get('terraceSurface', 0)
    print("Terrace Surface:", terraceSurface)

    gardenSurface = my_dict.get('gardenSurface', 0)
    print("Garden:", gardenSurface)

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

    furnished = 1 if classified_data['transaction'].get(
        'sale', {}).get('isFurnished', False) else 0
    print(f"Furnished: {furnished}")

    sale_type = classified_data['transaction']['subtype'] if classified_data['transaction']['subtype'] != 'LIFE_SALE' else None
    print(f"Type of Sale: {sale_type}")

    price = classified_data['transaction']['sale']['price']
    print(f"Price: {price}")

    if my_dict.get('basemant'):
        print("Basement: ", my_dict['basemant']['surface'])

    dict = {
        "Property ID": classified_data_id,
        "Locality name": locality,
        "Postal code": postalCode,
        "Living area": living_area,
        "Type of Property": property_type,
        "Number of Rooms": number_of_rooms,
        "Equipped kitchen": kitchen_qnt,
        "Furnished": furnished,
        "Type of Sale": sale_type,
        "Price": price,
        "Open fire": open_fire,
        "Terrace": terraceSurface,
        "Garden": gardenSurface,
        "Living area in m²:": netHabitableSurface,
        "Swimming pool": hasSwimmingPool,

    }

    if kitchen:
        dict['kitchenSurface'] = kitchen_surface
        dict['kitchenType'] = kitchen_type
        dict['kitchenOven'] = kitchen_oven
        dict['kitchenMicroWave'] = kitchen_micro_wave
        dict['kitchenDishWasher'] = kitchen_dish_washer
        dict['kitchenWashingMachine'] = kitchen_machine
        dict['kitchenFridge'] = kitchen_fridge
        dict['kitchenFreezer'] = kitchen_freezer
        dict['kitchenSteamOven'] = kitchen_steam_oven

    if not location == {}:
        dict['Postal code'] = postalCode
        dict['Country'] = country
        dict['Region'] = region
        dict['Province'] = province
        dict['Street'] = street
        dict['Number'] = number_house
        dict['Box'] = box
        dict['PropertyName'] = property_name
        dict['Floor'] = floor
        dict['Latitude'] = latitude
        dict['Longitude'] = longitude
        dict['Distance'] = distance
        dict['Aproximated'] = aproximated
        dict['RegionCode'] = region_code
        dict['typeofResidence'] = type_residence
        dict['District'] = district
        dict['Livingarea'] = living_area
        dict['HasSeaView'] = sea_view

    all_Information.append(dict)


to_csv(all_Information)
