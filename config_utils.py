"""
Configuration utilities for Brainlife.io apps.
"""

import json


def convert_parameters_to_None(config):
    """Convert parameters whose value is "" into None.

    Parameters
    ----------
    config: dict
        Dictionary containing all the parameters of the App.

    Returns
    -------
    config: dict 
        Dictionary with parameters converted to None where needed.   
    """
    # Convert all "" to None when the App runs on BL
    tmp = dict((k, None) for k, v in config.items() if v == "")
    config.update(tmp)
    return config


def define_kwargs(config):
    """Define kwargs for the mne functions used by the App.

    Parameters
    ----------
    config: dict
        Dictionary containing all the parameters of the App.

    Returns
    -------
    config: dict
        Dictionary containing all the parameters to apply the mne function.
    """ 
    # Delete keys values in config.json when the App is executed on Brainlife
    brainlife_keys = ['_app', '_tid', '_inputs', '_outputs', '_rule']
    
    for key in brainlife_keys:
        if key in config:
            del config[key]
    
    return config


def load_config(config_path='config.json'):
    """Load and preprocess configuration file.
    
    Parameters
    ----------
    config_path : str
        Path to the configuration file.
        
    Returns
    -------
    config : dict
        Processed configuration dictionary.
    """
    with open(config_path, 'r') as config_f:
        config = json.load(config_f)
    
    # Apply standard preprocessing
    config = convert_parameters_to_None(config)
    config = define_kwargs(config)
    
    return config
