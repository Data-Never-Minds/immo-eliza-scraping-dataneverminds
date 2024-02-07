from bs4 import BeautifulSoup
import requests
import json
from scraper.immoweb_scraper import get_links, fetch_details_concurrently, get_links_concurrently
from scraper.utils import to_csv
import time


def main():
    starttimer = time.time()
    base_url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={}&orderBy=relevance'

    # Fetch property links
    url_list = get_links_concurrently(base_url, pages=5)

    # Fetch details concurrently for the collected URLs
    print("Fetching details for collected properties...")
    property_details_list = fetch_details_concurrently(url_list)

    # Print details for each property and collect data for CSV
    all_property_data = []  # List to collect all property data
    for details in property_details_list:

        if details:

            property_dict = {
                "Property ID": details['id'],
                "Locality name": details['property'].get('location', {}).get('locality', 'null'),
                "Postal code": details['property'].get('location', {}).get('postalCode', '0'),
                "Price": f"{details['transaction'].get('sale', {}).get('price')}" if details['transaction'].get('sale', {}).get('price') else 0,
                "Type of property": details['property'].get('type', 'N/A'),
                "Subtype of property": details['property'].get('subtype', 'N/A'),
                "Type of sale": "N/A" if details['transaction'].get('subtype', '') == 'LIFE_SALE' else details['transaction'].get('subtype', 'N/A'),
                "Number of Rooms": f"{details['property'].get('bedroomCount', '0')}" if details['property'].get('bedroomCount', '0') else 0,
                "Living area": f"{details['property'].get('netHabitableSurface', '0')}" if details['property'].get('netHabitableSurface', '0') else 0,
                "Furnished": 1 if details['transaction'].get('sale', {}).get('isFurnished', False) else 0,
                "Open fire": 1 if details['property'].get('fireplaceExists', False) else 0,
                "Terrace Surface": f"{details['property'].get('terraceSurface', 'null')}" if details['property'].get('terraceSurface', False) else 0,
                "Garden Surface": f"{details['property'].get('gardenSurface', 'null')}" if details['property'].get('gardenSurface', False) else 0,
                "Swimming pool": 1 if details['property'].get('hasSwimmingPool', False) else 0,
                "Kitchen": 1 if details['property'].get('kitchen') else 0,
                "Toilets": details['property']['toiletCount']
            }

            if details['property']:
                details_property = details['property']
                if details_property.get('building') and details_property['building'].get('condition'):
                    condition_building = details_property['building'].get(
                        'condition')
                    property_dict["Building State"] = condition_building

            property_type = details['property'].get('type')
            if property_type != 'HOUSE_GROUP':
                if property_type != 'APARTMENT_GROUP':
                    # If not 'GROUP_HOUSE', add the details to all_property_data
                    all_property_data.append(property_dict)

    # Save the collected data to CSV
    to_csv(all_property_data, 'property_data.csv')
    print("Results saved to property_data.csv")

    endtimer = time.time()
    print("TIME GERAL: {:.6f}m".format((endtimer - starttimer)/60))


if __name__ == "__main__":
    main()
