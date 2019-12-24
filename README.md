# What is Ilm?
Ilm (علم) is the Arabic word for **knowledge**. In the context of this directory, it is a collection of Python packages designed to assist with the aggregation or generation of **data**, which can be transformed into **information** -- data with context. Users can process information as they please in the pursuit of **knowledge** -- understanding, experience and accumulated learning.

## Ilm - XBRL
#### In Development
`ilm-xbrl` is an lxml-based XBRL parser for U.S. Public Company Filings. It facilitates, at scale:
  1. The retreival & storage of XBRL files
  2. Parsing & light-weight analysis of XBRL files, whether locally stored or retreived on an ad-hoc basis.

## Ilm - Loan Modeler
#### In Development
`ilm-loanmodeler` is a generator -- it randomly generates loan terms and calculates associated cash flows (assuming the loan performs). Loans can be amoritizing or non-amoritizing. A loan object consists of:
  1. Loan Terms
  2. Loan Schedule
  3. Lender Cash Flows
  4. Metadata for use in other analysis packages
  
  Generating loans is simple:
  ```python
  import ilm-loanmodeler
  
  terms = generate_terms() # Generate terms
  loan = generate_loan(terms) # Create loan
  metrics = calculate_metrics(loan) # Calculate metrics
  ```

## Ilm - Fund
#### Not Started
`ilm-fund` is an aggregator -- it combines cash flows from a provided asset-universe into a blended fund model, netting out simulated management fees and fund expenses. It is intended to be used with `ilm-loanmodeler` to generate simulated fund models for private debt funds.
