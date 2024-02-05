
## Description
This is a machine learning model to make price predictions on real estate sales in Belgium.
The program does the following:
1. Data collection.
    1. Retrieves URL values for each page
    2. Retrieves information about each listing (e.g: Property ID, Locality name, Postal code, Price etc)
    3. Saves output in a ```csv``` dataset
2. Data Analysis
    1. Cleans and explores data 
    2. Computes key statistics
    3. Summarises insights about the RE market in BE
3. Model Development
    1. Trains a Machine Learning model to predict the price of any property
    2. Evaluates the accuracy of the model
    3. Discusses model limitations
4. Model Deployment
    1. Exposes API that predicts the price of a house
    2. Wraps API in an interactive application

## Installation
Open ```cmd``` on windows or ```terminal``` on mac.
Move into the directory where you want to download the project files. 
```git clone git@github.com:Data-Never-Minds/immo-eliza-scraping-dataneverminds```

Open ```cmd``` if on windows and move into the immo-eliza-scraping-dataneverminds directory.
```cd immo-eliza-scraping-dataneverminds```

## Usage
```pip install -r requirements.txt```

```python3 main.py```

## Visuals
