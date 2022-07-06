# Business Locator Google Maps API

### Install dependencies
```bash
pip install -r requirements.txt
```

### Create your API credentials
* Sign up to Google and get your API Key
* Enable Geocoding API, Maps JavaScript API and Places API
* Rename **creds-sample.py** into **creds.py** and put in your API Key

### Create folders
* Create a folder on your root directory called `csvfiles`
* Create a folder on your root directory called `no_google_business_address`

### Create your input
* Rename **sample_search_query.csv** to **search_query.csv**
* The Script uses **search_query.csv** as input where the first column is `query`

### Output
* The output is saved in the `csvfiles` folder
* Businesses who don't have GMB will be extracted and saved on `no_google_business_address` folder

### Disclaimer
* This script uses Google Maps API so it will be the user's responsibility to keep track of his/her API usage.