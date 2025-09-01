"""
File handling utilities for Brainlife.io apps.
"""

import os
import shutil


def read_optional_files(config, out_dir_name):
    """Read all optional files given to the App.

    Parameters
    ----------
    config: dict
        Dictionary containing all the parameters of the App.
    out_dir_name: str
        Name of the output directory of the App.

    Returns
    -------
    config: dict 
        Dictionary with parameters minus the optional files entries.  
    files_dict: dict
        Dictionary containing paths to optional files:
        - cross_talk_file: str or None
        - calibration_file: str or None  
        - events_file: str or None
        - head_pos_file: str or None
        - channels_file: str or None
        - destination: str or None
    """
    files_dict = {}
    
    # From meg/fif datatype #
    
    # Read the crosstalk file 
    if 'crosstalk' in config.keys():
        cross_talk_file = config.pop('crosstalk')
        if cross_talk_file is not None:
            if os.path.exists(cross_talk_file) is False:
                cross_talk_file = None
            else: 
                shutil.copy2(cross_talk_file, os.path.join(out_dir_name, 'crosstalk_meg.fif'))
    else:
        cross_talk_file = None
    files_dict['cross_talk_file'] = cross_talk_file

    # Read the calibration file
    if 'calibration' in config.keys():
        calibration_file = config.pop('calibration')
        if calibration_file is not None:
            if os.path.exists(calibration_file) is False:
                calibration_file = None
            else:
                shutil.copy2(calibration_file, os.path.join(out_dir_name, 'calibration_meg.dat'))  
    else:
        calibration_file = None
    files_dict['calibration_file'] = calibration_file
    
    # Read the events file
    if 'events' in config.keys():
        events_file = config.pop('events')
        if events_file is not None:
            if os.path.exists(events_file) is False:
                events_file = None
    else:
        events_file = None
    files_dict['events_file'] = events_file

    # Read head pos file
    if 'headshape' in config.keys():
        head_pos_file = config.pop('headshape')
        if head_pos_file is not None:
            if os.path.exists(head_pos_file) is False:
                head_pos_file = None
    else:
        head_pos_file = None
    files_dict['head_pos_file'] = head_pos_file

    # Read channels file
    if 'channels' in config.keys():
        channels_file = config.pop('channels')
        if channels_file is not None: 
            if os.path.exists(channels_file) is False:
                channels_file = None  
    else:
        channels_file = None 
    files_dict['channels_file'] = channels_file

    # Read destination file
    if 'destination' in config.keys():
        destination = config.pop('destination')
        if destination is not None:
            if os.path.exists(destination) is False:
                destination = None
    else:
        destination = None
    files_dict['destination'] = destination

    # Handle override files (from meg/fif-override datatype)
    _handle_override_files(config, out_dir_name, files_dict)
    
    return config, files_dict


def _handle_override_files(config, out_dir_name, files_dict):
    """Handle override files from meg/fif-override datatype."""
    
    # Destination override
    if 'destination_override' in config.keys():
        destination_override = config.pop('destination_override')
        if os.path.exists(destination_override) is False: 
            if files_dict['destination'] is not None:
                shutil.copy2(files_dict['destination'], os.path.join(out_dir_name, 'destination.fif'))
        else:
            shutil.copy2(destination_override, os.path.join(out_dir_name, 'destination.fif'))
            files_dict['destination'] = destination_override
    else: 
        if files_dict['destination'] is not None:
            shutil.copy2(files_dict['destination'], os.path.join(out_dir_name, 'destination.fif'))

    # Head pos override
    if 'headshape_override' in config.keys():
        head_pos_file_override = config.pop('headshape_override')
        if os.path.exists(head_pos_file_override) is False:
            if files_dict['head_pos_file'] is not None:
                shutil.copy2(files_dict['head_pos_file'], os.path.join(out_dir_name, 'headshape.pos'))
        else:
            shutil.copy2(head_pos_file_override, os.path.join(out_dir_name, 'headshape.pos'))
            files_dict['head_pos_file'] = head_pos_file_override
    else:
        if files_dict['head_pos_file'] is not None:
            shutil.copy2(files_dict['head_pos_file'], os.path.join(out_dir_name, 'headshape.pos'))

    # Channels override
    if 'channels_override' in config.keys():
        channels_file_override = config.pop('channels_override')
        if os.path.exists(channels_file_override) is False:
            if files_dict['channels_file'] is not None:
                shutil.copy2(files_dict['channels_file'], os.path.join(out_dir_name, 'channels.tsv'))
        else:
            shutil.copy2(channels_file_override, os.path.join(out_dir_name, 'channels.tsv'))
            files_dict['channels_file'] = channels_file_override
    else:
        if files_dict['channels_file'] is not None:
            shutil.copy2(files_dict['channels_file'], os.path.join(out_dir_name, 'channels.tsv'))       
        
    # Events override
    if "events_override" in config.keys():
        events_file_override = config.pop('events_override')
        if os.path.exists(events_file_override) is False:
            if files_dict['events_file'] is not None:
                shutil.copy2(files_dict['events_file'], os.path.join(out_dir_name, 'events.tsv'))
        else:
            shutil.copy2(events_file_override, os.path.join(out_dir_name, 'events.tsv'))
            files_dict['events_file'] = events_file_override
    else:
        if files_dict['events_file'] is not None:
            shutil.copy2(files_dict['events_file'], os.path.join(out_dir_name, 'events.tsv'))


def copy_optional_files(files_dict, out_dir_name):
    """Copy optional files to output directory if they exist.
    
    Parameters
    ----------
    files_dict : dict
        Dictionary of optional file paths.
    out_dir_name : str
        Output directory path.
    """
    file_mappings = {
        'cross_talk_file': 'crosstalk_meg.fif',
        'calibration_file': 'calibration_meg.dat',
        'events_file': 'events.tsv',
        'head_pos_file': 'headshape.pos',
        'channels_file': 'channels.tsv',
        'destination': 'destination.fif'
    }
    
    for key, filename in file_mappings.items():
        if files_dict.get(key) is not None:
            shutil.copy2(files_dict[key], os.path.join(out_dir_name, filename))


def ensure_output_dirs(*dir_names):
    """Ensure output directories exist.
    
    Parameters
    ----------
    *dir_names : str
        Variable number of directory names to create.
    """
    for dir_name in dir_names:
        os.makedirs(dir_name, exist_ok=True)
