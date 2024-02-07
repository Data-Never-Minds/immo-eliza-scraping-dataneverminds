from scraper.immoweb_scraper import get_links, fetch_details_concurrently
from scraper.utils import to_csv
import time


def main():
    base_url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={}&orderBy=relevance'

    # Fetch property links
    url_list = get_links(base_url, pages=2)  

    # Fetch details concurrently for the collected URLs
    print("Fetching details for collected properties...")
    property_details_list = fetch_details_concurrently(url_list)
  
    # Print details for each property and collect data for CSV
    all_property_data = []  # List to collect all property data
    for details in property_details_list:
        if details:  # Ensure details were fetched successfully
            print("Property ID:", details['id'])
            print("Locality name:", details['property'].get('location', {}).get('locality', 'N/A'))
            print("Postal code:", details['property'].get('location', {}).get('postalCode', 'N/A'))
            print("Living area:", details['property'].get('netHabitableSurface', 'N/A'))
            print("Number of Rooms:", details['property'].get('bedroomCount', 'N/A'))
            print("Price:", details['transaction'].get('sale', {}).get('price', 'N/A'))
            print("Type of property:", details['property'].get('type', 'N/A'))
            print("Subtype of property:", details['property'].get('subtype', 'N/A'))
            print("Type of sale:", "N/A" if details['transaction'].get('subtype', '') == 'LIFE_SALE' else details['transaction'].get('subtype', 'N/A'))
            print("Number of rooms:", details['property'].get('bedroomCount', 'N/A'))
            print("Living area:", details['property'].get('netHabitableSurface', 'N/A'), "m²")
            print("Furnished:", 1 if details['transaction'].get('sale', {}).get('isFurnished', False) else 0)
            print("Open fire:", 1 if details['property'].get('fireplaceExists', False) else 0)
            print("Terrace:", details['property'].get('terraceSurface', 'null'), "m²" if details['property'].get('terraceSurface', False) else '')
            print("Garden:", details['property'].get('gardenSurface', 'null'), "m²" if details['property'].get('gardenSurface', False) else '')
            print("Swimming pool:", 1 if details['property'].get('hasSwimmingPool', False) else 0)
            #print("State of building:", details['property'].get('building', {}).get('condition', 'N/A'))
            #print("Surface of good:", details['property'].get('land', {}).get('surface', 'N/A'), "m²")
            #print("Number of facades:", details['property'].get('building', {}).get('facadeCount', 'N/A'))
            print("--------")

            # Collect data for CSV
            all_property_data.append(details)

    # Save the collected data to CSV
    to_csv(all_property_data, 'property_data.csv')
    print("Results saved to property_data.csv")

if __name__ == "__main__":
    main()

       