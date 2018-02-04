import requests
import xmltodict

from .data_source_base import DataSourceBase
from ..utils.influx import retrieve_metrics, upload_metrics
from ..utils.timeutils import goodreads_timestamp_to_utc

class GoodreadsDataSource(DataSourceBase):
    """The class for Goodreads data source collection.

    Args:
        name (str): The name of this data collection instance
        application (DataCollectionApplication): The application instance that owns 
        this data source.

    Attributes:
        name [inherited] (str): The name of this data collection instance
        config [inherited] (dict): Data Sources Configuration
        cached_data (set): List of ISBNs currently stored in Influx
    """

    _API_URL = "https://www.goodreads.com/review/list?v=2"
    _GRAFANA_QUERY = "SELECT * FROM {0} WHERE source={1}"

    def __init__(self, name, application):
        super().__init__(self, name, application)
        self.cached_data = self.fetch_stored_data()

    def collect(self):
        """Function for collection of the underlying data."""

        new_goodreads_data = self.retrieve_latest_data()
        new_entries = self.diff_data(new_goodreads_data)
        self.add_new_data(new_entries)

    def setup_task(self, scheduler):
        """Function for setting up a reoccuring task for this data source.
        
        Args:
            scheduler (Schedule): The scheduler object
        """
        scheduler.every().day.at("00:00").do(self.collect)

    def fetch_stored_data(self):
        """Retreive the existing records in InfluxDB.

        Return:
            stored_data (set): A set of ISBNs that already exist in Influx.
        """
        query_result = retrieve_metrics(
            self.config["database"],
            self._GRAFANA_QUERY.format(
                self.config["table"],
                self.config["source_filter"]
            ))
        values = query_result["results"]["series"]["values"]
        stored_data = set()
        for value in values:
            stored_data.add(value)
        return stored_data

    def retrieve_latest_data(self):
        """Retrieve the details of the "read" shelf from Goodreads

        Return:
            goodreads_data (OrderedDict): Contains the list of books in
            JSON format.
        """
        req_params = {
            "shelf": "read",
            "per_page": 200,
            "sort": "date_read",
            "id": self.config["user_id"],
            "key": self.config["key"]
        }

        req = requests.get(self._API_URL, params=req_params)
        if req.status_code != 200:
            print("Something has gone wrong.")
            raw_json = xmltodict.parse(req.text)
        
        return raw_json["GoodreadsResponse"]["reviews"]["review"]

    def diff_data(self, new_goodreads_data):
        """Compares the cached data against the newly retrieved data.
        
        Note that since the web request returns an ordered list of books in
        date read, once we hit the first book that we've already recorded, we can stop.

        Args:
            new_goodreads_data (OrderedDict): Contains a set of books in JSON format.

        Return:
            new_entries (List): The list of new books that we don't have recorded.
        """
        new_entries = []
        for book in new_goodreads_data:
            if book["book"]["isbn"] in self.cached_data:
                break
            new_entries.append(book)

        return new_entries

    def add_new_data(self, new_entries):
        """Uploads the new data to Influx and updates our cached dataset.

        Args:
            new_entries (List): The list of new books that we don't have recorded.
        """
        for entry in new_entries:
            timestamp = goodreads_timestamp_to_utc(entry["read_at"])
            isbn = entry["book"]["isbn"]
            upload_metrics(
                self.config["database"],
                self.config["table"],
                {"source": self.config["source_filter"]},
                {"isbn": isbn},
                {"timestamp": timestamp, "precision": "s"}
            )
            self.cached_data.add(isbn)
