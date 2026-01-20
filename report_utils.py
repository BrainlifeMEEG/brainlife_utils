"""
Report generation utilities for Brainlife.io apps.

This module provides utilities for creating and managing product.json files
that integrate with Brainlife.io's visualization and reporting interface.

Supported item types:
    - info, warning, error, danger, success: Text messages
    - image/png: Base64-encoded PNG images
    - plotly: Interactive Plotly plots with data and layout
"""

import json
import base64
import os


# Allowed message types in product.json
ALLOWED_MESSAGE_TYPES = {'info', 'warning', 'error', 'danger', 'success'}
ALLOWED_ITEM_TYPES = ALLOWED_MESSAGE_TYPES | {'image/png', 'plotly'}


def _validate_message_item(item):
    """Validate a message item (info, warning, error, danger, success).
    
    Parameters
    ----------
    item : dict
        Item to validate.
        
    Returns
    -------
    bool
        True if valid, raises ValueError otherwise.
    """
    if not isinstance(item, dict):
        raise ValueError("Message item must be a dictionary")
    
    if 'type' not in item:
        raise ValueError("Message item must have 'type' key")
    
    if item['type'] not in ALLOWED_MESSAGE_TYPES:
        raise ValueError(f"Message type '{item['type']}' not in {ALLOWED_MESSAGE_TYPES}")
    
    if 'msg' not in item:
        raise ValueError("Message item must have 'msg' key")
    
    if not isinstance(item['msg'], str):
        raise ValueError("Message 'msg' value must be a string")
    
    return True


def _validate_image_item(item):
    """Validate an image item (image/png).
    
    Parameters
    ----------
    item : dict
        Item to validate.
        
    Returns
    -------
    bool
        True if valid, raises ValueError otherwise.
    """
    if not isinstance(item, dict):
        raise ValueError("Image item must be a dictionary")
    
    if 'type' not in item:
        raise ValueError("Image item must have 'type' key")
    
    if item['type'] != 'image/png':
        raise ValueError(f"Image type must be 'image/png', got '{item['type']}'")
    
    if 'name' not in item:
        raise ValueError("Image item must have 'name' key")
    
    if not isinstance(item['name'], str):
        raise ValueError("Image 'name' must be a string")
    
    if 'base64' not in item:
        raise ValueError("Image item must have 'base64' key")
    
    if not isinstance(item['base64'], str):
        raise ValueError("Image 'base64' must be a string")
    
    return True


def _validate_plotly_item(item):
    """Validate a Plotly plot item.
    
    Parameters
    ----------
    item : dict
        Item to validate.
        
    Returns
    -------
    bool
        True if valid, raises ValueError otherwise.
    """
    if not isinstance(item, dict):
        raise ValueError("Plotly item must be a dictionary")
    
    if 'type' not in item or item['type'] != 'plotly':
        raise ValueError("Plotly item must have type='plotly'")
    
    if 'name' not in item:
        raise ValueError("Plotly item must have 'name' key")
    
    if not isinstance(item['name'], str):
        raise ValueError("Plotly 'name' must be a string")
    
    if 'data' not in item:
        raise ValueError("Plotly item must have 'data' key")
    
    if not isinstance(item['data'], list):
        raise ValueError("Plotly 'data' must be a list")
    
    # Validate each data point
    for i, point in enumerate(item['data']):
        if not isinstance(point, dict):
            raise ValueError(f"Plotly data point {i} must be a dictionary")
    
    if 'layout' not in item:
        raise ValueError("Plotly item must have 'layout' key")
    
    if not isinstance(item['layout'], dict):
        raise ValueError("Plotly 'layout' must be a dictionary")
    
    return True


def _validate_product_item(item):
    """Validate a single product item.
    
    Parameters
    ----------
    item : dict
        Item to validate.
        
    Returns
    -------
    bool
        True if valid, raises ValueError otherwise.
    """
    if not isinstance(item, dict):
        raise ValueError("Product item must be a dictionary")
    
    if 'type' not in item:
        raise ValueError("Product item must have 'type' key")
    
    item_type = item['type']
    
    # Validate based on type
    if item_type in ALLOWED_MESSAGE_TYPES:
        return _validate_message_item(item)
    elif item_type in {'image/png', 'image/jpeg', 'image/svg+xml'}:
        return _validate_image_item(item)
    elif item_type == 'plotly':
        return _validate_plotly_item(item)
    else:
        raise ValueError(f"Unknown product item type: '{item_type}'")


def message_optional_files_in_reports(files_dict):
    """Create messages regarding the presence of optional files for reports.

    Parameters
    ----------
    files_dict : dict
        Dictionary containing optional file paths.

    Returns
    -------
    dict
        Dictionary with report messages for each file type.
    """ 
    messages = {}
    
    file_types = {
        'calibration_file': 'calibration',
        'cross_talk_file': 'cross-talk', 
        'head_pos_file': 'headshape',
        'destination': 'destination'
    }
    
    for key, file_type in file_types.items():
        if files_dict.get(key) is None:
            messages[f'report_{key}'] = f'No {file_type} file provided'
        else:
            messages[f'report_{key}'] = f'{file_type.title()} file provided'
    
    return messages


def create_product_json(items, output_path='product.json', unstructured_data=None):
    """Create product.json file for Brainlife.io interface.
    
    Creates a JSON file containing structured items for Brainlife.io visualization
    and optional unstructured data fields.
    
    Parameters
    ----------
    items : list
        List of items to include in product.json. Each item should be a dict
        with valid Brainlife.io item structure (validated).
    output_path : str
        Path where to save the product.json file. Default: 'product.json'
    unstructured_data : dict, optional
        Optional dictionary of unstructured metadata (e.g., metrics, labels).
        These will be added to the root level of the product.json.
        
    Raises
    ------
    ValueError
        If any item in the list fails validation.
    TypeError
        If items is not a list or unstructured_data is not a dict.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    
    if unstructured_data is not None and not isinstance(unstructured_data, dict):
        raise TypeError("unstructured_data must be a dictionary or None")
    
    # Validate all items
    for i, item in enumerate(items):
        try:
            _validate_product_item(item)
        except ValueError as e:
            raise ValueError(f"Invalid item at index {i}: {str(e)}")
    
    # Build product data
    product_data = {'brainlife': items}
    
    # Add unstructured data at root level if provided
    if unstructured_data:
        product_data.update(unstructured_data)
    
    # Write to file
    try:
        with open(output_path, 'w') as outfile:
            json.dump(product_data, outfile, indent=2)
    except IOError as e:
        raise IOError(f"Failed to write product.json to {output_path}: {str(e)}")


def add_raw_info_to_product(items_list, raw):
    """Add structured MNE raw data information to the product list.
    
    Adds multiple info messages with key raw data parameters to the product
    items list for display in the Brainlife.io interface:
    - Channel types and counts
    - Sampling frequency
    - Recording duration
    - Digitized head points count
    - Filter settings (highpass/lowpass)
    - Projector information
    
    Parameters
    ----------
    items_list : list
        List to append the info items to.
    raw : mne.io.Raw
        MNE raw data object.
        
    Raises
    ------
    AttributeError
        If raw does not have expected MNE attributes.
    """
    import mne
    
    # Channel information with type counts
    ch_types = raw.get_channel_types()
    ch_type_counts = {}
    for ch_type in ch_types:
        count = sum(1 for t in raw.get_channel_types() if t == ch_type)
        ch_type_counts[ch_type] = count
    ch_types_msg = f"Channel types: {', '.join([f'{count} {ch_type}' for ch_type, count in sorted(ch_type_counts.items())])}"
    add_info_to_product(items_list, ch_types_msg)
    
    # Sampling frequency
    sfreq = raw.info['sfreq']
    add_info_to_product(items_list, f"Sampling frequency: {sfreq} Hz")
    
    # Duration and number of time points
    n_times = raw.n_times
    duration = raw.times[-1]
    add_info_to_product(items_list, f"Duration: {duration:.2f} seconds ({n_times} time points)")
    
    # Digitized head points
    if raw.info['dig']:
        dig_count = len(raw.info['dig'])
        add_info_to_product(items_list, f"Digitized head points: {dig_count}")
    else:
        add_info_to_product(items_list, "Digitized head points: None")
    
    # Filters
    if raw.info['highpass'] is not None or raw.info['lowpass'] is not None:
        highpass = raw.info['highpass'] if raw.info['highpass'] is not None else "None"
        lowpass = raw.info['lowpass'] if raw.info['lowpass'] is not None else "None"
        add_info_to_product(items_list, f"Filters: High-pass={highpass} Hz, Low-pass={lowpass} Hz")
    else:
        add_info_to_product(items_list, "Filters: None")
    
    # Projectors
    if raw.info['projs']:
        n_projs = len(raw.info['projs'])
        add_info_to_product(items_list, f"Projectors: {n_projs} SSP projector(s)")
    else:
        add_info_to_product(items_list, "Projectors: None")


def add_image_to_product(images_list, name, base64_data=None, filepath=None):
    """Add a PNG image to the product list.
    
    Adds a base64-encoded PNG image to the product items list for visualization
    in the Brainlife.io interface.
    
    Parameters
    ----------
    images_list : list
        List to append the image item to.
    name : str
        Name/description of the image for display.
    base64_data : str, optional
        Base64 encoded image data. Either this or filepath must be provided.
    filepath : str, optional
        Path to image file (will be converted to base64). Either this or 
        base64_data must be provided.
        
    Raises
    ------
    ValueError
        If neither base64_data nor filepath is provided.
    FileNotFoundError
        If filepath is provided but the file does not exist.
    """
    # Get base64 data
    if base64_data is None and filepath is not None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")
        with open(filepath, 'rb') as f:
            base64_data = base64.b64encode(f.read()).decode('utf-8')
    elif base64_data is None:
        raise ValueError("Either base64_data or filepath must be provided")
    
    # Validate base64_data is a string
    if not isinstance(base64_data, str):
        raise ValueError("base64_data must be a string")
    
    # Validate name is a string
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    
    # Create and validate item
    item = {
        'type': 'image/png',
        'name': name,
        'base64': base64_data
    }
    
    try:
        _validate_image_item(item)
    except ValueError as e:
        raise ValueError(f"Invalid image item: {str(e)}")
    
    images_list.append(item)


def add_info_to_product(items_list, message, msg_type='info'):
    """Add an info/warning/error message to the product list.
    
    Adds a text message to the product items list for display in the 
    Brainlife.io interface.
    
    Parameters
    ----------
    items_list : list
        List to append the message item to.
    message : str
        Information message text.
    msg_type : str
        Type of message: 'info', 'warning', 'error', 'danger', or 'success'.
        Default: 'info'
        
    Raises
    ------
    ValueError
        If msg_type is not in the allowed set.
    """
    # Validate message type
    if msg_type not in ALLOWED_MESSAGE_TYPES:
        raise ValueError(f"msg_type must be one of {ALLOWED_MESSAGE_TYPES}, got '{msg_type}'")
    
    # Validate message is a string
    if not isinstance(message, str):
        message = str(message)
    
    # Create and validate item
    item = {
        'type': msg_type,
        'msg': message
    }
    
    try:
        _validate_message_item(item)
    except ValueError as e:
        raise ValueError(f"Invalid message item: {str(e)}")
    
    items_list.append(item)


def add_plotly_to_product(items_list, name, data, layout):
    """Add a Plotly plot to the product list.
    
    Adds an interactive Plotly plot to the product items list for visualization
    in the Brainlife.io interface.
    
    Parameters
    ----------
    items_list : list
        List to append the plot item to.
    name : str
        Name/title of the plot for display.
    data : list of dict
        List of data points, where each point is a dictionary with keys like
        'x', 'y', etc. Example: [{"x": '2014-06-11', "y": 10}, ...]
    layout : dict
        Layout configuration for the plot. Can include keys like 'start', 'end',
        'title', 'xaxis', 'yaxis', etc.
        
    Raises
    ------
    ValueError
        If data is not a list of dictionaries or layout is not a dict.
    """
    # Validate name is a string
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    
    # Validate data is a list
    if not isinstance(data, list):
        raise ValueError("data must be a list of dictionaries")
    
    # Validate layout is a dict
    if not isinstance(layout, dict):
        raise ValueError("layout must be a dictionary")
    
    # Create and validate item
    item = {
        'type': 'plotly',
        'name': name,
        'data': data,
        'layout': layout
    }
    
    try:
        _validate_plotly_item(item)
    except ValueError as e:
        raise ValueError(f"Invalid plotly item: {str(e)}")
    
    items_list.append(item)


def create_mne_report_with_data(data, title='MNE Report', **kwargs):
    """Create MNE report with standard data sections.
    
    Parameters
    ----------
    data : mne object
        MNE data object (Raw, Epochs, Evoked).
    title : str
        Report title.
    **kwargs
        Additional keyword arguments for report sections.
        
    Returns
    -------
    mne.Report
        MNE report object.
    """
    import mne
    
    report = mne.Report(title=title)
    
    # Add appropriate sections based on data type
    if hasattr(data, 'plot_psd'):
        try:
            report.add_raw(data, title=f'{type(data).__name__} data', psd=True)
        except Exception:
            # Fallback if add_raw fails
            report.add_html(title='Data Info', html=f'<pre>{str(data.info)}</pre>')
    
    return report


def plot_digitized_head_points_3d(raw, items_list=None, output_dir='out_figs'):
    """Plot 3D digitized head points if available.
    
    Creates a 3D visualization of digitized head points from MNE raw data.
    If available, also plots electrode positions for reference.
    
    Parameters
    ----------
    raw : mne.io.Raw
        MNE raw data object.
    items_list : list, optional
        List to append the visualization image to. If None, image is not added
        to product but filepath is still returned.
    output_dir : str
        Directory where to save the figure. Default: 'out_figs'
        
    Returns
    -------
    str or None
        Base64 encoded image string if successful, None otherwise.
    """
    import mne
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    # Check if digitized head points exist
    if not raw.info['dig']:
        return None
    
    try:
        # Extract digitized head points
        dig_points = [d['r'] for d in raw.info['dig']]
        dig_points = np.array(dig_points)
        
        # Create 3D plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot digitized head points
        ax.scatter(dig_points[:, 0], dig_points[:, 1], dig_points[:, 2], 
                  c='red', marker='o', s=30, alpha=0.8, label='Digitized Head Points')
        
        # Also plot electrode positions if available for reference
        try:
            positions = raw._get_channel_positions()
            if positions is not None and np.any(~np.isnan(positions)):
                ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                          c='blue', marker='^', s=50, alpha=0.6, label='Electrodes')
        except Exception:
            pass
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Digitized Head Points')
        ax.legend()
        fig.tight_layout()
        
        # Save and convert to base64
        os.makedirs(output_dir, exist_ok=True)
        from .plot_utils import save_figure_with_base64
        
        filepath = os.path.join(output_dir, 'digitized_head_points_3d.png')
        img_base64 = save_figure_with_base64(fig, filepath, dpi_file=150, dpi_base64=80)
        
        # Add to product items if list provided
        if items_list is not None:
            add_image_to_product(items_list, 'Digitized Head Points (3D)', 
                               base64_data=img_base64)
        
        return img_base64
        
    except Exception as e:
        if items_list is not None:
            add_info_to_product(items_list, 
                              f"Could not plot digitized head points: {str(e)}", 
                              'warning')
        return None

