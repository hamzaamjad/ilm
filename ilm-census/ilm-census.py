import requests
import pandas as pd
import numpy as np
import configparser
import os

# Create INI file to store various API credentials
def generate_ini():
    config = configparser.ConfigParser()
    config['Census API'] = {}
    config['Google APIs'] = {}
    with open('ilm.ini', 'w') as configfile:
        config.write(configfile)
    print("ilm.ini created. Saved in", os.getcwd())

# Insert Google API keys into INI file
# ini_google({'geocoding' : 'api_key_here'})
def ini_google(api_keys = {}):
    config = configparser.ConfigParser()
    config.read('ilm.ini')
    google = config['Google APIs']
    try:
        for k, v in api_keys.items():
            google[k] = v
    except:
        print("Error")
    
    with open('ilm.ini', 'w') as configfile:
        config.write(configfile)
    print("Keys successfuly inserted:")
    print("-------------------------------")
    for k, v in api_keys.items():
        print(k,"|",google[k])

# Read a specific variable from INI file
# Typically used in other functions to pass API keys & passwords at runtime
def read_ini(header, variable):
    config = configparser.ConfigParser()
    config.read('ilm.ini')
    header_variable = config[header][variable]
    return(header_variable)

# References Google's Geocoding API
# https://developers.google.com/maps/documentation/geocoding/start
# Uses f-strings, Python 3.6+
def geocode_address(address):
    api_key = read_ini('Google APIs','geocoding')
    address = [x.replace(" ", "+") for x in address.split(",")]
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address[0]},{address[1]},{address[2]}&key={api_key}'
    response = requests.get(url)
    response = response.json()
    try:
        if response['status'] == 'REQUEST_DENIED':
            print(response['status'])
            return(response['error_message'])
        elif response['status'] == 'OK':
            result = response['results'][0]
            output = {'address' : result['formatted_address'], 'location' : result['geometry']['location']}
    except:
        print("Error in geocoding. URL attempted: ", url)
        return(url)
    return(output)

# Expects an 'address' dictionary output by geocode_address
def address_parts(address, location):
    address_parts = [x.strip() for x in address.split(",")]
    output = {'address' : address, 'location' : location, 'address_parts' : {'street' : address_parts[0], 'city' : address_parts[1], 'state' : address_parts[2][:2], 'zip_code' : address_parts[2][-5:], 'country' : address_parts[3]}}
    return(output)

# Expects an 'address' dictionary output by geocode_address, with further modification by address_parts
def address_census_keys(address, location, address_parts, benchmark = 'Public_AR_Current', vintage = 'ACS2019_Current'):
    url = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates'
    layers = ['2010 Census Blocks', 'Secondary School Districts', '2019 State Legislative Districts - Upper', 'County Subdivisions', 'Elementary School Districts', 'Metropolitan Statistical Areas', 'Counties', '2019 State Legislative Districts - Lower', 'Census Block Groups', 'Combined Statistical Areas', '2010 Census ZIP Code Tabulation Areas', 'Census Tracts']
    url_params = {'x' : location['lng'], 'y' : location['lat'], 'benchmark' : benchmark, 'vintage' : vintage, 'layers' : layers, 'format' : 'json'}
    response = requests.get(url, params = url_params)
    result = response.json()['result']
    geographies = {k1: {k2: v2 for k2, v2 in next(iter(v1 or []), dict()).items() if (k2 in ['GEOID', 'CENTLAT', 'BASENAME', 'NAME', 'CENTLON'])} for k1, v1 in result['geographies'].items()}
    output = {'address' : address, 'location' : location, 'address_parts' : address_parts, 'geographies' : geographies}
    return(output)

# Sample call - datasets_census(vintage = 2017)
def datasets_census(dataset = False, vintage = False):
    urls = ['https://api.census.gov/data/2010.json','https://api.census.gov/data.json']
    datasets = pd.DataFrame()
    for url in urls:
        response = requests.get(url)
        response = response.json()
        df = pd.DataFrame(response['dataset'])
        if 'c_isTimeseries' not in list(df):
            df.insert(loc = len(df.columns), column = 'c_isTimeseries', value = np.nan)
            datasets = pd.concat([datasets, df], sort = False, ignore_index = True)
        else:
            datasets = pd.concat([datasets, df], sort = False, ignore_index = True)
            
        if not dataset:
            continue
        else:
            continue
        
        # vintage parameter
        if not vintage:
            continue
        else:
            datasets = datasets[datasets['c_vintage'] == vintage]     
    return(datasets)
