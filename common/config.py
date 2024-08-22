import yaml
import os

def load_config(yaml_file: str) -> dict:
    """
    Load configuration from a yaml file and return it as a dictionary.
    
    Args:
        path (str): Path to the yaml file
        
    Returns:
        dict: Configuration as a dictionary
    """
    # Get the working directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    path = os.path.join(parent_dir, f"filters/{yaml_file}")
    print(f"Loading configuration from path: {path}")

    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at path: {path}")