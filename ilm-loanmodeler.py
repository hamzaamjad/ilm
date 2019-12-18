from datetime import datetime
from dateutil.relativedelta import relativedelta
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
    return(math.ceil(n * multiplier) / multiplier)

# Return a random datetime between to datetime objects
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return(start + datetime.timedelta(seconds=random_second))

terms = {'principal':10000000,
 'cash_rate':0.05,
 'interest_reserve_rate':.05,
 'interest_reserve_term':0.5,
 'origination_points':0.025,
 'origination_points_deferred':0.025,
 'date_originated':datetime.strptime('2019-01-01', '%Y-%m-%d'),
 'date_payoff':datetime.strptime('2020-01-01', '%Y-%m-%d')
}

def generate_loan_terms():
    principal = random.uniform(1000000,50000000)
    cash_rate = random.uniform(0.05,0.09)
    interest_reserve_rate = random.uniform(0, 0.05)
    interest_reserve_term = random.random()
    origination_points = random.uniform(0, 0.01)
    origination_points_deferred = random.uniform(0, 0.01)
    date_originated = random_date(datetime.strptime('2020-01-01', '%Y-%m-%d'), datetime.strptime('2022-01-01', '%Y-%m-%d'))
    date_payoff = date_originated + datetime.timedelta(int(random.uniform(12,24))*365/12)
    terms = {'principal':principal,'cash_rate':cash_rate,'interest_reserve_rate':interest_reserve_rate,'interest_reserve_term':interest_reserve_term,'origination_points':origination_points,'origination_points_deferred':origination_points_deferred,'date_originated':date_originated,'date_payoff':date_payoff,'periods':365,'frequency':'D'}
    return(terms)

def generate_loan(terms, amortizing = True, amortization_terms = {'term' : 30}):
    '''
    Periodic transactions.
    '''
    # Loan cash flows are calculated on a daily basis. Generate range of dates between origination and payoff date
    # # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    term = (terms['date_payoff'] - terms['date_originated']).days
    date_range = pd.date_range(terms['date_originated'], periods = term, freq = 'D')

    # Daily payment. Round up to nearest cent. 365/360 day convention
    # When loan is amortizing, value represents Principal + Interest
    # When loan is non-amortizing, value represents Interest
    rate_daily = terms['cash_rate'] / 360
    if amortizing:
        n = ((terms['date_originated'] + relativedelta(years = amortization_terms['term'])) - terms['date_originated']).days
        payment = round_up(((((1+rate_daily) ** n) * rate_daily) / (((1+rate_daily) ** n) - 1)) * terms['principal'], 2)
    else:
        payment = round_up(rate_daily * terms['principal'], 2)
    return(payment)

    # Interest reserve (ir) is an 'account' with a 'balance' -- we net daily ir expense against it providing balance over time
    # ir balance is calculated upfront. We then calculate the daily ir expense based on the ir term
    ir_balance = round_up((terms['interest_reserve_rate'] * terms['interest_reserve_term']) * terms['principal'] * 365/360, 2)
    '''
    Round up if calculation returns fractional days.
    Gives borrower an additional day of interest reserve credit if the interest reserve isn't outstanding for the full term of the loan.
    '''
    ir_term = round_up(term * terms['interest_reserve_term'],0)
    ir = ir_balance / ir_term

    '''
    One-time transactions
    '''
    rate = terms['cash_rate'] + (terms['interest_reserve_rate'] * terms['interest_reserve_term']) + terms['origination_points'] + terms['origination_points_deferred']
    points_in = terms['origination_points'] * terms['principal']
    points_out = terms['origination_points_deferred'] * terms['principal']
    payoff = terms['principal'] + points_out
    net_funding = -(terms['principal'] - points_in - ir_balance)

    '''
    {
        'net_funding' : [{'2019-01-01' : -1000}],
        'cash' : [{'2019-01-01' : 1}]
    }
    '''

    # Create loan schedule

    net_funding = pd.DataFrame(data = {'tag': 'net_funding', 'value' : net_funding}, index = pd.Index([terms['date_originated']]))
    payoff = pd.DataFrame(data = {'tag': 'payoff', 'value' : payoff}, index = pd.Index([terms['date_payoff']]))

    daily = pd.DataFrame(data = {'tag': 'cash_pay', 'value' : payment}, index = date_range)
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

print(generate_loan(terms))
print(generate_loan(terms, amortizing = False))

# Parallel processing example, needs to be updated
'''
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
'''