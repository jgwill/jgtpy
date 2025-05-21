import os
import json


def read_value_from_config(var_name_to_read, pds_server_url_default):
    # Check if config.json exists in the current directory
    if os.path.exists("config.json"):
        config_path = "config.json"
    else:
        # Check if config.json exists in $HOME directory
        home_dir = os.path.expanduser("~")
        config_path = os.path.join(home_dir, "config.json")

    # Read the variable value from the config file
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
            variable_value = config.get(var_name_to_read, pds_server_url_default)
    else:
        variable_value = pds_server_url_default

    return variable_value
