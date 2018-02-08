import time
import os

import schedule

from .utils.config_loader import load_application_config

from .data_sources.goodreads import GoodreadsDataSource
from .data_sources.transmission import TransmissionDataSource

class DataCollectionApplication:
    """This class contains the logic for the main data collection application.

    Attributes:
        scheduler (Schedule): The scheduler object.
        config (dict): The configuration of the application.
        sources (list): A list of the current data collection sources.
    """

    _CONFIG_PATH = "/config.json"
    _CONFIG_TO_SOURCE = {
        "goodreads": GoodreadsDataSource,
        "transmission": TransmissionDataSource
    }

    def __init__(self):
        self.scheduler = schedule.default_scheduler
        absolute_config_fp = os.path.dirname(os.path.realpath(__file__)) + self._CONFIG_PATH
        self.config = load_application_config(absolute_config_fp)
        self.sources = []

    def create_sources(self):
        """Set-up all of our sources listed in the config."""
        for application in self.config:
            data_source = self._CONFIG_TO_SOURCE[application](application, self)
            data_source.setup_task(self.scheduler)
            self.sources.append(data_source)
    
    def start(self):
        """Initialises all of the sources and starts operation"""
        self.create_sources()
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_config(self, application):
        """Helper function to return the application-specific config."""
        return self.config[application]


if __name__ == "__main__":
    app = DataCollectionApplication()
    app.start()
