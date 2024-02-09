from scraper.immoweb_scraper import get_links_concurrently, fetch_details_concurrently
from scraper.utils import to_csv, process_details_concurrently, get_max_workers
import time


def main():
    """
    Main function to scrape real estate property data from the Immoweb website.

    Steps:
    1. Collect property links concurrently from multiple pages.
    2. Fetch details for the collected property URLs concurrently.
    3. Process the fetched property details concurrently, preparing data for CSV output.
    4. Save the processed data into a CSV file.
    """
    start = time.time()
    base_url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={}&orderBy=relevance'

    # Fetch property links
    url_list = get_links_concurrently(base_url, pages=33)

    # Fetch details concurrently for the collected URLs
    print("Fetching details for collected properties...")
    property_details_list = fetch_details_concurrently(url_list)

    # Process details concurrently and collect data for CSV
    print("Processing property details...")
    all_property_data = process_details_concurrently(
        property_details_list, max_workers=get_max_workers())

    # Save the collected data to CSV
    to_csv(all_property_data, '.\data\property_data.csv')
    print("Results saved to property_data.csv")

    end = time.time()
    print("Time Taken: {:.6f}s".format(end-start))
    print("Time Taken: {:.6f}m".format((end-start)/60))


if __name__ == "__main__":
    main()
