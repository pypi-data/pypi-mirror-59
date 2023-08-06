# epdnorway

Python module (pypi.org) to consume XML data from https://digi.epd-norge.no/ into any python project.

## Requirements

python v3.7

## Usage

	pip install epdnorway

Example usage:

	from epdnorway import *
	import pprint as pp

query dataset and show a json list result
	res = epdnorway.list_query("limtre")
	pp.pprint(res)

get a specific dataset, e.g. first of results
	dataset = epdnorway.DataSet(res[0]["uuid"])

### list flow datapoints

get the numbers for Global warming potential

	gwp = dataset.exchangeFlows["GWP"] 
