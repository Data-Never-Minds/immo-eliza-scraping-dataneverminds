from bs4 import BeautifulSoup
import requests
import json
from scraper.immoweb_scraper import get_links, fetch_details_concurrently
from scraper.utils import to_csv
import time


def main():
    base_url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={}&orderBy=relevance'

    # Fetch property links
    url_list = get_links(base_url, pages=30)

    # Fetch details concurrently for the collected URLs
    print("Fetching details for collected properties...")
    property_details_list = fetch_details_concurrently(url_list)

    # Print details for each property and collect data for CSV
    all_property_data = []  # List to collect all property data
    for details in property_details_list:
        if details:
            property_dict = {
                "Property ID": details['id'],
                "Locality name": details['property'].get('location', {}).get('locality', 'N/A'),
                "Postal code": details['property'].get('location', {}).get('postalCode', 'N/A'),
                "Living area": details['property'].get('netHabitableSurface', 'N/A'),
                "Number of Rooms": details['property'].get('bedroomCount', 'N/A'),
                "Price": details['transaction'].get('sale', {}).get('price', 'N/A'),
                "Type of property": details['property'].get('type', 'N/A'),
                "Subtype of property": details['property'].get('subtype', 'N/A'),
                "Type of sale": "N/A" if details['transaction'].get('subtype', '') == 'LIFE_SALE' else details['transaction'].get('subtype', 'N/A'),
                # Repetição de "Number of rooms" e "Living area" removida, pois já foram adicionadas acima.
                "Furnished": 1 if details['transaction'].get('sale', {}).get('isFurnished', False) else 0,
                "Open fire": 1 if details['property'].get('fireplaceExists', False) else 0,
                "Terrace": f"{details['property'].get('terraceSurface', 'null')}m²" if details['property'].get('terraceSurface', False) else 'null',
                "Garden": f"{details['property'].get('gardenSurface', 'null')}m²" if details['property'].get('gardenSurface', False) else 'null',
                "Swimming pool": 1 if details['property'].get('hasSwimmingPool', False) else 0,
                # Campos comentados removidos para simplificação. # Ensure details were fetched successfully
            }

            # Collect data for CSV
            all_property_data.append(property_dict)

    # Save the collected data to CSV
    to_csv(all_property_data, 'property_data.csv')
    print("Results saved to property_data.csv")


if __name__ == "__main__":
    main()
