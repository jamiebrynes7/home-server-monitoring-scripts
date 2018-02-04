class DataSourceBase:
    """The abstract base class for a data source.

    Any class which inherits from this class should implement collect() and setup_task(scheduler).

    Args:
        name (str): The name of this data collection instance
        application (DataCollectionApplication): The application instance that owns this data 
            source.
            
    Attributes:
        name (str): The name of this data collection instance
        config (dict): Data Sources Configuration
    """

    def __init__(self, name, application):
        self.name = name
        self.config = application.get_config(self.name)

    def collect(self):
        """
        Function for collection of the underlying data.
        Should be implemented by the child class.
        """
        raise NotImplementedError(
            "Child class of DataSourceBase should have implemented collect().")

    def setup_task(self, scheduler):
        """
        Function for setting up a reoccuring task for this data source.
        Should be implemented by the child class.
        """
        raise NotImplementedError(
            "Child class of DataSourceBase should have implemented setup_task(scheduler).")
