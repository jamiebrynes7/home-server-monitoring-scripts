[![Build Status](https://travis-ci.org/jamiebrynes7/home-server-monitoring-scripts.svg?branch=master)](https://travis-ci.org/jamiebrynes7/home-server-monitoring-scripts)

# Home Server Monitoring

This is my collection of scripts with scheduler for monitoring my home server and areas of my life. These all feed into an InfluxDB instance which is queried by Grafana to visualise the data.

There are modules for:

* Transmission (torrent client) statistics
* Goodreads statistics

## Getting Started

### Requirements

* Python 3 

### Set-up

These scripts should be portable across systems with a small change in the config file.

1. Clone/download this repository.
2. Install the python requirements with `pip install -r requirements.txt` 
3. Run the controller application with `python data_collection.py` 
