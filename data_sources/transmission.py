import transmissionrpc

from .data_source_base import DataSourceBase
from ..utils.influxutils import InfluxMetricData, upload_metric

class TransmissionDataSource(DataSourceBase):
    """The class for Transmission data collection.

    Args:
        name (str): The name of this data collection instance.
        application (DataCollectionApplication): The application instance
        that owns this data source.

    Attributes:
        name [inherited] (str): The name of this data collection instance.
        config [inherited] (dict): Data source configuration.
        transmission_client (transmissionrpc.Client): The RPC client connected
        to transmission
    """

    def __init__(self, name, application):
        super().__init__(self, name, application)
        self.transmission_client = transmissionrpc.Client(
            self.config["host"],
            self.config["port"])
    
    def collect(self):
        """Function for collection of the underlying data."""
        torrents = self.transmission_client.get_torrents()

        download = sum(torrent.rateDownload for torrent in torrents)
        upload = sum(torrent.rateUpload for torrent in torrents)
        self.add_new_data_point(download, upload)
    
    def setup_task(self, scheduler):
        """Function for setting up a reoccuring task for this data source.
        
        Args:
            scheduler (Schedule): The scheduler object
        """
        scheduler.every(1).minutes.do(self.collect)

    def add_new_data_point(self, download, upload):
        """Uploads the data point to Influx.

        Args:
            download (float): The download rate in B/s
            upload (float): The upload rate in B/s
        """
        influx_dp = InfluxMetricData(
            self.config["table"],
            {"source": self.config["source_filter"]},
            {"download": download, "upload": upload}
        )
        upload_metric(self.config["database"], influx_dp)
        