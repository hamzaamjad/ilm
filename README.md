# What is Ilm?
Ilm (علم) is the Arabic word for **knowledge**. In the context of this directory, it is a collection of Python packages designed to assist with the aggregation or generation of **data**, which can be transformed into **information** -- data with context. Users can process information as they please in the pursuit of **knowledge** -- understanding, experience and accumulated learning.

## Ilm - XBRL (IN DEVELOPMENT)
`ilm-xbrl` is an lxml-based XBRL parser for U.S. Public Company Filings. It facilitates, at scale:
  1. The retreival & storage of XBRL files
  2. Parsing & light-weight analysis of XBRL files, whether locally stored or retreived on an ad-hoc basis.

## Ilm - Loan Modeler(IN DEVELOPMENT)
`ilm-loanmodeler` is a generator -- it randomly generates loan terms and calculates associated cash flows (assuming the loan performs). Loans can be amoritizing or non-amoritizing. A loan object consists of:
  1. Loan Terms
  2. Loan Schedule
  3. Lender Cash Flows
  4. Metadata for use in other analysis packages
  
  Generating loans is simple:
  ```python
  from ilm-loanmodeler import generate_loan_terms, generate_loan
  
  terms = generate_loan_terms()
  print(terms)
  ```
  ```python
  {'principal':10000000,
 'cash_rate':0.1,
 'interest_reserve_rate':0.0,
 'interest_reserve_term':1,
 'origination_points':0.0,
 'origination_points_deferred':0.0,
 'date_originated':datetime.strptime('2020-01-01', '%Y-%m-%d'),
 'date_payoff':datetime.strptime('2021-01-01', '%Y-%m-%d'),
 'amortization_term':0
}
  ```
  ```python
  generate_loan(terms)
  ```

## Ilm - Fund (NOT STARTED)
`ilm-fund` is an aggregator -- it combines cash flows from a provided asset-universe into a blended fund model, netting out simulated management fees and fund expenses. It is intended to be used with `ilm-loanmodeler` to generate simulated fund models for private debt funds.
