from datetime import datetime
import pandas as pd
import numpy as np
import math
import random
import time
import multiprocessing as mp
import json
from tqdm import tqdm

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

from datetime import timedelta

# Return a random datetime between to datetime objects
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def loan_cashflow_lender(terms):
    overall_rate = terms['cash_rate'] + (terms['interest_reserve_rate'] * terms['interest_reserve_term']) + terms['origination_points'] + terms['origination_points_deferred']
    date_range = pd.date_range(terms['date_originated'], periods = terms['periods'], freq = terms['frequency'])
    cash = round_up((terms['cash_rate'] / 360) * terms['principal'], 2)
    interest_reserve = round_up((terms['interest_reserve_rate'] * terms['interest_reserve_term']) * terms['principal'] * 365/360, 2)
    origination_fee = terms['origination_points'] * terms['principal']
    origination_fee_deferred = terms['origination_points_deferred'] * terms['principal']
    payoff = cash + origination_fee_deferred + terms['principal']
    net_funding = -(terms['principal'] - origination_fee - interest_reserve)

    net_funding = pd.DataFrame(data = {'tag': 'net_funding', 'value' : net_funding}, index = pd.Index([terms['date_originated']]))
    payoff = pd.DataFrame(data = {'tag': 'payoff', 'value' : payoff}, index = pd.Index([terms['date_payoff']]))

    daily = pd.DataFrame(data = {'tag': 'cash_pay', 'value' : cash}, index = date_range)
    monthly = daily.groupby(pd.Grouper(freq='M')).sum()
    monthly.loc[:,'tag'] = 'cash_pay'

    appends = [net_funding, payoff]
    daily = daily.append(appends)
    monthly = monthly.append(appends)

    daily_cf = monthly.groupby(pd.Grouper(freq='D')).sum()['value']
    monthly_cf = monthly.groupby(pd.Grouper(freq='M')).sum()['value']
    daily_irr = (1 + np.irr(daily_cf)) ** 365 - 1
    monthly_irr = (1 + np.irr(monthly_cf)) ** 12 - 1
    result = {'terms' : terms, 'lender_cf' : monthly_cf, 'irr' : monthly_irr}
    return(result)
    
def loan_term_generator():
    principal = random.uniform(1000000,50000000)
    cash_rate = random.uniform(0.05,0.09)
    interest_reserve_rate = random.uniform(0, 0.05)
    interest_reserve_term = random.random()
    origination_points = random.uniform(0, 0.01)
    origination_points_deferred = random.uniform(0, 0.01)
    date_originated = random_date(datetime.strptime('2020-01-01', '%Y-%m-%d'), datetime.strptime('2022-01-01', '%Y-%m-%d'))
    date_payoff = date_originated + timedelta(int(random.uniform(12,24))*365/12)
    terms = {'principal':principal,'cash_rate':cash_rate,'interest_reserve_rate':interest_reserve_rate,'interest_reserve_term':interest_reserve_term,'origination_points':origination_points,'origination_points_deferred':origination_points_deferred,'date_originated':date_originated,'date_payoff':date_payoff,'periods':365,'frequency':'D'}
    return(terms)

terms = {'principal':10000000,
 'cash_rate':0.05,
 'interest_reserve_rate':.05,
 'interest_reserve_term':0.5,
 'origination_points':0.025,
 'origination_points_deferred':0.025,
 'date_originated':datetime.strptime('2019-01-01', '%Y-%m-%d'),
 'date_payoff':datetime.strptime('2020-01-01', '%Y-%m-%d'),
'periods':365,
'frequency':'D'} # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

if __name__ == '__main__':
    with mp.Pool(mp.cpu_count()-1) as p:
        scenarios = []
        for i in tqdm(range(100)):
            scenarios.append(loan_term_generator())
        r = list(tqdm(p.imap(loan_cashflow_lender, scenarios), total=len(scenarios)))
    with open('data.txt', 'w') as outfile:
        try:
            json.dump(r, outfile, default = str)
        except:
            print("Error")
    with open('data.txt') as json_file:
        try:
            data = json.load(json_file)
            for l in data[0:10]:
                print(l['irr'])
        except:
            print("Error")