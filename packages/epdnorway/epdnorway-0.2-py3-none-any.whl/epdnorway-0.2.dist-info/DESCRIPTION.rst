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

Data Points are now accessible as `dataset.impactAssessments` and `dataset.exchangeFlows`

	pp.pprint(dataset.impactAssessments)

List of possible datapoints are in

	pp.pprint(dataset.EXCHANGE_FLOWS)
	pp.pprint(dataset.LIFE_CYCLE_METHODS)

Data Points are stored as keys, and values in secondary keys in `amounts`  
List possible amounts for modules:

    pp.pprint(dataset.KNOWN_MODULES)

### Get specific datapoints

Example: get the numbers for Global warming potential

	gwp = dataset.exchangeFlows["GWP"]
	pp.print(gwp)
	pp.print(gwp["amounts"]["A1-A3"])


