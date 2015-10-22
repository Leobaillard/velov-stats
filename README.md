# velov-stats
Getting Velo'V stations metrics for graphing purposes

Fetches data from JCDecaux developer API and pushes them to StatsD/Graphite

[![Build Status](http://jenkins.ttec-junior.fr/buildStatus/icon?job=velov-stats)](http://jenkins.ttec-junior.fr/job/velov-stats)

## Requirements
 - Python 2/3
 - requests: https://pypi.python.org/pypi/requests/
 - pystatsd: https://github.com/jsocol/pystatsd

## Configuration
Create a `config.json` next to the Python script containing these values:
```json
{
	"jcd_apikey": "",
	"jcd_apiurl": "https://api.jcdecaux.com/vls/v1/",
	"jcd_contract": "",
	"jcd_stations": [],
	
	"graphite_host": "",
	"graphite_node": "",
	"statsd_host": "",
	"statsd_port": 8125,
	
	"measure_interval": 60
}

```
