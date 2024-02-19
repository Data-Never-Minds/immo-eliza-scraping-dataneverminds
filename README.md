# Immo Eliza - Price Prediction Model

## Description
Our project is to create a price prediction model for Belgian Real Estate. So far, we created a data scraper using requests and beautifulsoup to fetch data from Immoweb. The preliminary data we retrieved and our initial analysis are included in the repositary.

The data scraper:
  1. Retrieves URL values for each page
  2. Retrieves information about each listing (e.g: Property ID, Locality name, Postal code, Price etc)
  3. Parses the information to a dictionary
  4. Saves output in a ```csv``` dataset


## Installing the scraper
Open ```cmd``` on windows or ```terminal``` on mac.\
Move into the directory where you want to download the project files.\
```git clone git@github.com:Data-Never-Minds/immo-eliza-scraping-dataneverminds```

Open ```cmd``` if on windows and move into the immo-eliza-scraping-dataneverminds directory.\
```cd immo-eliza-scraping-dataneverminds```

## Usage
```pip install -r requirements.txt```

```python3 main.py```

## Visuals
![property_data](data-never-minds.png)
