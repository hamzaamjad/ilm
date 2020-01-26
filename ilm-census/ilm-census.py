import requests
import pandas as pd
import numpy as np

def datasets_census(dataset = False, vintage = False):
    urls = ['https://api.census.gov/data/2010.json','https://api.census.gov/data.json']
    datasets = pd.DataFrame()
    for url in urls:
        response = requests.get(url)
        response = response.json()
        df = pd.DataFrame(response['dataset'])
        if 'c_isTimeseries' not in df.columns:
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

datasets = datasets_census(vintage = 2017)
datasets
