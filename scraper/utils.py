import requests
from bs4 import BeautifulSoup
import pandas as pd

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
