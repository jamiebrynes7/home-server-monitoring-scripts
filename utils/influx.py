import requests

def upload_metrics(db_name, metric, tags, data, timestamp=None):
    """
    Send metrics to InfluxDB via HTTP API
    @param db_name String : Name of Influx database to write to.
    @param metric String : Name of metric to write to.
    @param tags dict : Dictionary of tag key to value pairs
    @param data dict : Dictionary of data key to value pairs
    @param timestamp dict : Dictionary of timestamp, precision pair for the timestamp
    """
    url = 'http://localhost:8086/write?db=' + db_name
    if timestamp:
        url += "&precision=" + timestamp["precision"]

    payload = str(metric)
    for key, value in tags.items():
        payload += "," + str(key) + "=" + str(value)
    payload += " "
    for key, value in data.items():
        payload += str(key) + "=" + str(value) + ","
    payload = payload[:len(payload) - 1]

    if timestamp:
        payload += " " + str(timestamp["timestamp"])

    requests.post(url=url, payload=payload)

def retrieve_metrics(db_name, query):
    """
    Retrieve metrics from InfluxDB via HTTP API
    @param db_name String : Name of Influx database to read from
    @param query String : Database query to execute
    """
    url = "http://localhost:8086/query?db=" + db_name + "&q=" + query
    req = requests.get(url)
    return req.text
