"""
Data processing utilities for Brainlife.io apps.
"""

import pandas as pd
import mne


def update_data_info_bads(data, channels_file): 
    """Update data.info['bads'] with the info contained in channels.tsv.

    Parameters
    ----------
    data: instance of mne.io.Raw or instance of mne.Epochs
        Data whose info['bads'] needs to be updated.
    channels_file: str
        BIDS compliant channels.tsv corresponding to data.

    Returns
    -------
    data: instance of mne.io.Raw or instance of mne.Epochs
        Data whose info['bads'] has been updated. 
    user_warning_message_channels: str or None
        Message to be displayed on BL UI if data.info['bads'] is updated.
    """ 
    if channels_file is None:
        return data, None
        
    # Convert channels.tsv into a dataframe
    df_channels = pd.read_csv(channels_file, sep='\t')

    # Select bad channels' name
    bad_channels = df_channels[df_channels["status"] == "bad"]['name']
    bad_channels = list(bad_channels.values)

    # Sort them in order to compare them
    original_bads = sorted(data.info['bads'])
    bad_channels_sorted = sorted(bad_channels)

    # Warning message if they are different
    if original_bads != bad_channels_sorted:
        user_warning_message_channels = (
            f'Bad channels from the info of your MEG file are different from '
            f'those in the channels.tsv file. By default, only bad channels from channels.tsv '
            f'are considered as bad: the info of your MEG file is updated with those channels.'
        )
        # Update bad channels
        data.info['bads'] = bad_channels 
    else: 
        user_warning_message_channels = None

    return data, user_warning_message_channels


def validate_input_data(data, expected_type=None):
    """Validate input neuroimaging data.
    
    Parameters
    ----------
    data : mne object
        MNE data object to validate.
    expected_type : type or tuple of types, optional
        Expected data type(s).
        
    Returns
    -------
    bool
        True if data is valid.
        
    Raises
    ------
    ValueError
        If data is invalid or wrong type.
    """
    if data is None:
        raise ValueError("Input data is None")
        
    if expected_type is not None:
        if not isinstance(data, expected_type):
            raise ValueError(f"Expected data type {expected_type}, got {type(data)}")
            
    return True


def get_channel_types_summary(data):
    """Get summary of channel types in the data.
    
    Parameters
    ----------
    data : mne.io.Raw, mne.Epochs, or mne.Evoked
        MNE data object.
        
    Returns
    -------
    dict
        Dictionary with channel type counts and names.
    """
    import numpy as np
    
    ch_types = data.get_channel_types()
    unique_types = np.unique(ch_types)
    
    summary = {}
    for ch_type in unique_types:
        indices = [i for i, x in enumerate(ch_types) if x == ch_type]
        summary[ch_type] = {
            'count': len(indices),
            'names': [data.ch_names[i] for i in indices]
        }
    
    return summary
