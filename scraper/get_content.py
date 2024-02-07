import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import json

url_list = ['https://www.immoweb.be/en/classified/new-real-estate-project-houses/for-sale/deinze/9800/11122711',
            'https://www.immoweb.be/en/classified/house/for-sale/sprimont/4140/11123021',
            'https://www.immoweb.be/en/classified/bungalow/for-sale/waterloo/1410/11122971',
            'https://www.immoweb.be/en/classified/house/for-sale/dendermonde/9200/11120778']

def house_scrapper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    results = []

    script_tags = soup.find_all("script", attrs={"type": "text/javascript"})

    for script in script_tags:
        if "window.classified" in script.get_text():
            script_text = script.get_text()
            json_string = script_text.split('window.classified = ', 1)[1]
            json_string = json_string.rsplit(';', 1)[0]

            results = json.loads(json_string)
            #results.append(script)

    return results

with ThreadPoolExecutor(max_workers=10) as executor:
    #starts the timer
    start = time.time()
    #for each url do function house_scraper and store result in a future object,
    #all the future objects are stored in the futures list
    futures = [executor.submit(house_scrapper, url) for url in url_list]
    #Once the house_scrapper function is completed for all URLs,
    #the results are gathered. item.result() waits for the function
    #(associated with that particular future) to complete and then returns its
    #result. These results are stored in the results list.
    results =  [item.result() for item in futures]
    #stops the timer
    end = time.time()
    #format the diff time with 6 digits after comma, plus 's'
    print("Time Taken: {:.6f}s".format(end-start))
    print(results)
