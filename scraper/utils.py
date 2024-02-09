import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def get_soup(url):
    """Request a webpage and return its BeautifulSoup object for HTML parsing.

    Args:
        url (str): The URL of the webpage to request.

    Returns:
        BeautifulSoup object: Parsed webpage content for easy data extraction.
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def to_csv(data: list, save='data.csv') -> None:
    """Converts a list of dictionaries to a CSV file, removing duplicates.

    Args:
        data (list): A list of dictionaries where each dictionary represents a row in the CSV.
        save (str, optional): The filename for the saved CSV file. Defaults to 'data.csv'.
    """
    try:
        dataframe = pd.DataFrame(data)
        dataframe = dataframe.drop_duplicates()
        dataframe.to_csv(save, index=False)

    except requests.RequestException as error:
        print(f"An error occured: {error}")
        return None


def process_property_detail(detail):
    """Process a single property detail and return a dictionary with selected property attributes.

    Args:
        detail (dict): A dictionary containing details of a single property.

    Returns:
        dict: A dictionary with processed property details or None if input is invalid.
    """
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
                    "Living area": f"{detail['property'].get('netHabitableSurface', 'None')}" if detail['property'].get('netHabitableSurface', '0') else 'None',
                    "Furnished": 1 if detail['transaction'].get('sale', {}).get('isFurnished', False) else 0,
                    "Open fire": 1 if detail['property'].get('fireplaceExists', False) else 0,
                    "Terrace Surface": f"{detail['property'].get('terraceSurface', 'null')}" if detail['property'].get('terraceSurface', False) else 'None',
                    "Garden Surface": f"{detail['property'].get('gardenSurface', 'null')}" if detail['property'].get('gardenSurface', False) else 'None',
                    "Swimming pool": 1 if detail['property'].get('hasSwimmingPool', False) else 0,

                    "Toilets": f"{detail['property']['toiletCount']}" if detail['property']['toiletCount'] else 'None',
                    "Surface of good": f"{detail['property'].get('land', 'None').get('surface', 'None')}" if detail['property'].get('land') else 'None',
                    "Number of facades": f"{detail['property'].get('building', {}).get('facadeCount', 'None')}" if detail['property'].get('building') else 'None',
                    "Building State": detail['property'].get('building', 'None').get('condition') if detail['property'].get('building') and detail['property']['building'].get('condition') else 'None',
                    # "kitchen": 1 if detail['property'].get('kitchen') else 0,
                }
                if detail['property']['kitchen']:
                    kitchen = detail['property']['kitchen']
                    if kitchen['type']:
                        data = kitchen['type']
                        if not data or data == "NOT_INSTALLED":
                            property_dict['Kitchen_type'] = 'None'
                            property_dict['Kitchen'] = 0
                        else:
                            property_dict['Kitchen'] = 1
                            property_dict['Kitchen_type'] = data
                    else:
                        property_dict['Kitchen_type'] = 'None'
                        property_dict['Kitchen'] = 0
                else:
                    property_dict['Kitchen_type'] = 'None'
                    property_dict['Kitchen'] = 0
                return property_dict
    return None


def get_max_workers():
    """Determine the maximum number of workers for ThreadPoolExecutor.

    Returns:
        int: The default maximum number of worker threads for the executor.
    """
    executor = ThreadPoolExecutor()
    return executor._max_workers


def process_details_concurrently(property_details_list, max_workers=get_max_workers()):
    """Process a list of property details concurrently, using threading to improve efficiency.

    Args:
        property_details_list (list): A list containing property details to be processed.
        max_workers (int, optional): The maximum number of worker threads to use. Defaults to the result of get_max_workers().

    Returns:
        list: A list of dictionaries, each representing processed details of a property.
    """
    all_property_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Map the process_property_detail function over all property details
        results = executor.map(process_property_detail, property_details_list)

        for result in results:
            if result is not None:
                all_property_data.append(result)

    return all_property_data
