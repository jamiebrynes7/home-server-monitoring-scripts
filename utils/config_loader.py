import json

def load_application_config(config_path):
    """Loads the JSON configuration file.

    Args:
        config_path (str): The path to the config.json file.
    
    Return:
        config (dict): The raw JSON structure
    """
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config
        