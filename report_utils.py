"""
Report generation utilities for Brainlife.io apps.
"""

import json
import base64
import os


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


def create_product_json(items, output_path='product.json'):
    """Create product.json file for Brainlife.io interface.
    
    Parameters
    ----------
    items : list
        List of items to include in product.json. Each item should be a dict
        with keys like 'type', 'name', 'base64', etc.
    output_path : str
        Path where to save the product.json file.
    """
    product_data = {'brainlife': items}
    
    with open(output_path, 'w') as outfile:
        json.dump(product_data, outfile, indent=2)


def add_image_to_product(images_list, name, base64_data=None, filepath=None):
    """Add an image to the product list.
    
    Parameters
    ----------
    images_list : list
        List to append the image item to.
    name : str
        Name/description of the image.
    base64_data : str, optional
        Base64 encoded image data.
    filepath : str, optional
        Path to image file (will be converted to base64).
    """
    if base64_data is None and filepath is not None:
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                base64_data = base64.b64encode(f.read()).decode('utf-8')
        else:
            raise FileNotFoundError(f"Image file not found: {filepath}")
    
    if base64_data is not None:
        images_list.append({
            'type': 'image/png',
            'name': name,
            'base64': base64_data
        })


def add_info_to_product(items_list, message, msg_type='info'):
    """Add an info message to the product list.
    
    Parameters
    ----------
    items_list : list
        List to append the info item to.
    message : str
        Information message.
    msg_type : str
        Type of message ('info', 'warning', 'error').
    """
    items_list.append({
        'type': msg_type,
        'msg': str(message)
    })


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
