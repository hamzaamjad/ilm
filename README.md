# What is Ilm?
Ilm (علم) is the Arabic word for **knowledge**. In the context of this directory, it is a collection of Python packages designed to assist with the aggregation or generation of **data**, which can be transformed into **information** -- data with context. Users can process information as they please in the pursuit of **knowledge** -- understanding, experience and accumulated learning.

## Ilm - Census (IN DEVELOPMENT - ACTIVE)
`ilm-census` provides helper functions to understand and extract Demographic data produced by the U.S. Census Bureau. Users can:
  1. Geocode an address and retreive its associated geographic identifiers
  2. View datasets and their associated data made available by the U.S. Census Bureau
  3. Extract and load data from various Census datasets into flat files

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
