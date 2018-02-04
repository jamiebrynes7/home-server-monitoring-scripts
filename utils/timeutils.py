import datetime

def goodreads_timestamp_to_utc(goodreads_timestamp):
    """Converts a Goodreads timestamp into a UTC one.

    Args:
        goodreads_timestamp (string): A time stamp in the following
        format - "Fri Jan 12 10:12:17 -0800 2018"
    
    Return:
        utc_timestamp (int): The UTC timestamp equivalent (in seconds)
    """
    [_, month, day, time, timezone, year] = goodreads_timestamp.split(" ")
    [hour, minute, second] = time.split(":")

    date_time = datetime.datetime(
        int(year), int(month), int(day), 
        int(hour), int(minute), int(second))
    
    timezone_offset = datetime.timedelta(hours=int(timezone[0:3]))
    utc_time = date_time + timezone_offset

    return int((utc_time - datetime.datetime(1970, 1, 1)).total_seconds())
