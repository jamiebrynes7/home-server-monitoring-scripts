import requests

class InfluxTimestampData:
    """Internal representation for an influx timestamp
    
    Args:
        timestamp (int): The timestamp
        precision (str): The precision of the timestamp [ns,u,ms,s,m,h]

    Attributes:
        timestamp (int): The timestamp
        precision (str): The precision of the timestamp [ns,u,ms,s,m,h
    """
    _ACCEPTED_PRECISIONS = {"ns", "u", "ms", "s", "m", "h"}
    def __init__(self, timestamp, precision):
        self.timestamp = timestamp
        if precision not in self._ACCEPTED_PRECISIONS:
            raise ValueError("Precision {0} not found in acceptable list."
                .format(precision))
        self.precision = precision

class InfluxMetricData:
    """Internal representation for an Influx data point.

    Args: 
        metric (str): The metric of the Influx data point.
        tags (Dict): The (key,value) pairs of tags.
        data (Dict): The (key,value) pairs of data.
        timestamp (InfluxTimestampData): The timestamp of the data point
    
    Attributes:
        metric (str): The metric of the Influx data point.
        tags (Dict): The (key,value) pairs of tags.
        data (Dict): The (key,value) pairs of data.
        timestamp (InfluxTimestampData): The timestamp of the data point
    """
    def __init__(self, metric, tags, data, timestamp=None):
        self.metric = metric
        self.tags = tags
        self.data = data
        self.timestamp = timestamp
    
    def __str__(self):
        rtn_str = (str(self.metric) 
            + ",".join((str(key) + "=" + str(value)) for key, value in self.tags.items()) 
            + " " 
            + ",".join((str(key) + "=" + str(value)) for key, value in self.data.items()) 
            + (" " + str(self.timestamp.timestamp) if self.timestamp else ""))
        return rtn_str


def upload_metric(db_name, influx_data_point):
    """Send metrics to InfluxDB via HTTP API

    Args:
        db_name (str): Name of influx database to write to.
        influx_data_point (InfluxMetricData): The data structure containing
        the data to upload.
    """
    url = 'http://localhost:8086/write?db=' + db_name
    if influx_data_point.timestamp:
        url += "&precision=" + influx_data_point.timestamp.precision
    
    payload = str(influx_data_point)

    requests.post(url=url, payload=payload)

def retrieve_metrics(db_name, query):
    """Retrieve metrics from InfluxDB via HTTP API

    Args:
        db_name (str): Name of influx database to read from.
        query (str): Database query to execute
    
    Return:
        results (Dict): Result of the query.
    """
    url = "http://localhost:8086/query?db=" + db_name + "&q=" + query
    req = requests.get(url)
    return req.text
