import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def get_soup(url):
    """Request a webpage and return its BeautifulSoup object."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def to_csv(data: list, save='data.csv') -> None:
    try:
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(save, index=False)

    except requests.RequestException as error:
        print(f"An error occured: {error}")
        return None


def process_property_detail(detail):
    """Process a single property detail and return a dictionary with all relevant fields."""
    if detail:
        property_type = detail['property'].get('type')
        if property_type != 'HOUSE_GROUP':
            if property_type != 'APARTMENT_GROUP':

                property_dict = {
                    "Property ID": detail['id'],
                    "Locality name": detail['property'].get('location', {}).get('locality', 'null'),
                    "Postal code": detail['property'].get('location', {}).get('postalCode', '0'),
                    "Price": f"{detail['transaction'].get('sale', {}).get('price')}" if detail['transaction'].get('sale', {}).get('price') else 0,
                    "Type of property": detail['property'].get('type', 'N/A'),
                    "Subtype of property": detail['property'].get('subtype', 'N/A'),
                    "Type of sale": "N/A" if detail['transaction'].get('subtype', '') == 'LIFE_SALE' else detail['transaction'].get('subtype', 'N/A'),
                    "Number of Rooms": f"{detail['property'].get('bedroomCount', '0')}" if detail['property'].get('bedroomCount', '0') else 0,
                    "Living area": f"{detail['property'].get('netHabitableSurface', '0')}" if detail['property'].get('netHabitableSurface', '0') else 0,
                    "Furnished": 1 if detail['transaction'].get('sale', {}).get('isFurnished', False) else 0,
                    "Open fire": 1 if detail['property'].get('fireplaceExists', False) else 0,
                    "Terrace Surface": f"{detail['property'].get('terraceSurface', 'null')}" if detail['property'].get('terraceSurface', False) else 0,
                    "Garden Surface": f"{detail['property'].get('gardenSurface', 'null')}" if detail['property'].get('gardenSurface', False) else 0,
                    "Swimming pool": 1 if detail['property'].get('hasSwimmingPool', False) else 0,
                    "Kitchen": 1 if detail['property'].get('kitchen') else 0,
                    "Toilets": detail['property']['toiletCount'],
                    "Number of facades": detail['property'].get('building', {}).get('facadeCount', 0) if detail['property'].get('building') else 0,
                    "Building State": detail['property'].get('building', {}).get('condition') if detail['property'].get('building') and detail['property']['building'].get('condition') else 'None'
                }
                # If not 'GROUP_HOUSE', add the details to all_property_data
                return property_dict
    return None


def process_details_concurrently(property_details_list, max_workers=16):
    """Process property details concurrently using threading."""
    all_property_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the process_property_detail function over all property details
        results = executor.map(process_property_detail, property_details_list)

        for result in results:
            if result is not None:
                all_property_data.append(result)

    return all_property_data
