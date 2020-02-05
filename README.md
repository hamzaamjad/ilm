# What is Ilm?
Ilm (علم) is the Arabic word for **knowledge**. In the context of this directory, it is a collection of Python packages designed to assist with the aggregation or generation of **data**, which can be transformed into **information** -- data with context. Users can process information as they please in the pursuit of **knowledge** -- understanding, experience and accumulated learning.

## Ilm - General Setup
Some of the libraries below require credentials -- Credentials are stored in _ilm.ini_ -- an `.ini` file generated in the working directory by calling `generate_ini()`. Functions in libraries will make use of credentails stored in `ilm.ini` -- users don't have to worry about key management.

```python
# Create blank ilm.ini file in working directory
>>> generate_ini()

'ilm.ini created. Saved in /Users/hamzaamjad/OneDrive/Code/ilm/ilm-census'

# Can add multiple values. The following are supported: geocoding (Google Maps Geocoding API)
>>> ini_google({'geocoding' : 'your_key_here'})

'Keys successfuly inserted:'
'----------------------------'
'geocoding | your_key_here'

# Test .ini file to see if key was stored
>>> read_ini('Google APIs','geocoding')

'your_key_here'
```

Below is a list of functions to add credentials to `ilm.ini`:

|Function|Parameters|Example|
|---|---|---|
|ini_google|{'api' : 'api_key'}|`ini_google({'geocoding' : 'your_key'})`|

## Ilm - Census (IN DEVELOPMENT - ACTIVE)
`ilm-census` provides helper functions to understand and extract Demographic data produced by the U.S. Census Bureau. Users can:
  1. Geocode an address and retreive its associated geographic identifiers
  ```python
  >>> geocode_address("1600 Pennsylvania Ave NW, Washington, DC 20500") # Google Geocoding API

# Dictionary formatted for display
  {
    'address': '1600 Pennsylvania Ave NW, Washington, DC 20500, USA',
    'location': {'lat': 38.8976633, 'lng': -77.0365739}
  }
  ```
  2. View Census datasets and their associated metadata
  3. Extract and load data from various Census datasets into flat files

  For Google Geocoding API Key, please visit the following: [Geocoding API - Get an API Key](https://developers.google.com/maps/documentation/geocoding/get-api-key)

## Ilm - XBRL (IN DEVELOPMENT - PAUSED)
`ilm-xbrl` is an lxml-based XBRL parser for U.S. Public Company Filings. It facilitates, at scale:
  1. The retrieval & storage of XBRL files
  2. Parsing & light-weight analysis of XBRL files, whether locally stored or retrieved on an ad-hoc basis

## Ilm - Loan (IN DEVELOPMENT - PAUSED)
`ilm-loan` is a generator -- it randomly generates loan terms and calculates associated cash flows (assuming the loan performs). Loans can be amoritizing or non-amoritizing. A loan object consists of:
  1. Loan Terms
  2. Loan Schedule
  3. Lender Cash Flows
  4. Metadata for use in other analysis packages

## Ilm - Fund (NOT STARTED)
`ilm-fund` is an aggregator -- it combines cash flows from a provided asset-universe into a blended fund model, netting out simulated management fees and fund expenses. It is intended to be used with `ilm-loanmodeler` to generate simulated fund models for private debt funds.
