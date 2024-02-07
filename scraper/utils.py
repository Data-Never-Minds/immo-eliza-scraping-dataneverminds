import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def get_soup(url):
    """Request a webpage and return its BeautifulSoup object."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def to_csv(data: dict, save='data.csv') -> None:
    try:
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(save, index=False)

    except requests.RequestException as error:
        print(f"An error occured: {error}")
        return None

def process_property_detail(detail):
    """Process a single property detail and return a dictionary with all relevant fields."""
    if detail:
        property_dict = {
            "Property ID": detail.get('id', 'N/A'),
            "Locality name": detail['property'].get('location', {}).get('locality', 'N/A'),
            "Postal code": detail['property'].get('location', {}).get('postalCode', 'N/A'),
            "Living area": detail['property'].get('netHabitableSurface', 'N/A'),
            "Number of Rooms": detail['property'].get('bedroomCount', 'N/A'),
            "Price": detail['transaction'].get('sale', {}).get('price', 'N/A'),
            "Type of property": detail['property'].get('type', 'N/A'),
            "Subtype of property": detail['property'].get('subtype', 'N/A'),
            "Type of sale": 'N/A' if detail['transaction'].get('subtype', '') == 'LIFE_SALE' else detail['transaction'].get('subtype', 'N/A'),
            "Furnished": 1 if detail['transaction'].get('sale', {}).get('isFurnished', False) else 0,
            "Open fire": 1 if detail['property'].get('fireplaceExists', False) else 0,
            "Terrace": f"{detail['property'].get('terraceSurface', 'None')}m²" if detail['property'].get('terraceSurface', False) else 'None',
            "Garden": f"{detail['property'].get('gardenSurface', 'None')}m²" if detail['property'].get('gardenSurface', False) else 'None',
            "Swimming pool": 1 if detail['property'].get('hasSwimmingPool', False) else 0,
        }
        return property_dict
    return None

def process_details_concurrently(property_details_list, max_workers=15):
    """Process property details concurrently using threading."""
    all_property_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the process_property_detail function over all property details
        results = executor.map(process_property_detail, property_details_list)

        for result in results:
            if result is not None:
                all_property_data.append(result)

    return all_property_data