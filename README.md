# Brainlife Utils

Shared utility library for Brainlife.io neuroimaging applications. This package provides common functionality for configuration handling, file operations, data processing, plotting, and report generation across the suite of MNE-Python based apps.

## Overview

`brainlife_utils` eliminates code duplication across Brainlife.io applications by providing:
- **Configuration handling** - Load, validate, and preprocess app configurations
- **File operations** - Create output directories, handle optional files
- **Data utilities** - Data validation, channel type summaries, bad channel handling
- **Report generation** - Create `product.json` for Brainlife.io interface
- **Plotting utilities** - Matplotlib setup for headless execution, figure conversion

## Installation

As a git submodule in each app:

```bash
git submodule add https://github.com/BrainlifeMEEG/brainlife_utils.git brainlife_utils
```

## Usage

### Basic Setup

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product
)

# Set up environment
setup_matplotlib_backend()
config = load_config()
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Your app logic here...

# Generate output
create_product_json()
add_raw_info_to_product(raw)
add_image_to_product('path/to/figure.png', 'Figure Title')
add_info_to_product('Processing complete', 'success')
```

## Modules

### config_utils.py

Configuration loading and parameter handling.

#### Functions

- **`load_config(config_path='config.json')`** - Load and preprocess configuration file
  - Converts empty strings to `None`
  - Removes Brainlife-specific metadata keys
  - Returns processed configuration dictionary

- **`convert_parameters_to_None(config)`** - Convert empty string parameters to None
  - Handles parameter validation for optional fields
  - Returns updated config dictionary

- **`define_kwargs(config)`** - Prepare configuration for MNE function calls
  - Removes Brainlife internal keys (`_app`, `_tid`, `_inputs`, etc.)
  - Returns cleaned configuration dictionary

- **`get_inputs_names(config_path='config.json')`** - Extract input metadata from config
  - Retrieves tags and datatype_tags before preprocessing
  - Useful for understanding app data dependencies

#### Example

```python
from brainlife_utils import load_config

config = load_config()
data_file = config['mne']
channels = config.get('channels')  # Returns None if not specified
```

### file_utils.py

File and directory handling utilities.

#### Functions

- **`ensure_output_dirs(*dir_names)`** - Create standard output directories
  - Creates `out_dir`, `out_figs`, `out_report` as needed
  - Safe to call multiple times (idempotent)
  - Example: `ensure_output_dirs('out_dir', 'out_figs', 'out_report')`

- **`read_optional_files(config, out_dir_name)`** - Handle optional input files
  - Reads and validates optional files from config
  - Copies files to output directory with standardized names
  - Returns dictionary with file paths
  - Supports: crosstalk, calibration, events, head_pos, channels, destination

- **`copy_optional_files(files_dict, out_dir_name)`** - Copy optional files to output
  - Complements `read_optional_files`
  - Handles file validation and path management

#### Example

```python
from brainlife_utils import ensure_output_dirs, read_optional_files

ensure_output_dirs('out_dir', 'out_figs', 'out_report')
files_dict = read_optional_files(config, 'out_dir')
```

### data_utils.py

Data processing and validation utilities.

#### Functions

- **`update_data_info_bads(data, bads_list)`** - Update bad channel information
  - Safely updates `data.info['bads']` with provided list
  - Validates channel names against existing channels
  - Returns updated data object

- **`validate_input_data(data_path, expected_type='raw')`** - Validate input data file
  - Checks if file exists and is readable
  - Verifies data type (raw, epochs, evoked, ica)
  - Provides informative error messages

- **`get_channel_types_summary(data)`** - Get summary of channel types
  - Returns dictionary with channel type counts
  - Example: `{'eeg': 32, 'meg': 120, 'misc': 2}`
  - Useful for validation and reporting

#### Example

```python
from brainlife_utils import update_data_info_bads, get_channel_types_summary

raw.info['bads'] = update_data_info_bads(raw, ['EEG001', 'MEG0111'])
channel_summary = get_channel_types_summary(raw)
print(f"Channels: {channel_summary}")
```

### plot_utils.py

Matplotlib setup and figure utilities.

#### Functions

- **`setup_matplotlib_backend()`** - Configure matplotlib for headless execution
  - Sets backend to 'Agg' for non-interactive use
  - Required for HPC and Docker container environments
  - Call at application start

- **`save_plot_to_base64(fig, close_fig=True, dpi=100)`** - Convert figure to base64
  - Encodes matplotlib figure as base64 PNG
  - Useful for embedding in reports
  - Parameters:
    - `dpi`: resolution (lower = smaller file size)
    - `close_fig`: whether to close figure after conversion

- **`save_figure_with_base64(fig, filepath, close_fig=True, dpi_file=150, dpi_base64=100)`** - Save figure and get base64
  - Saves figure to file at high resolution (default 150 dpi)
  - Returns base64 encoded version at lower resolution (default 100 dpi)
  - Efficient for both file storage and web display

- **`create_standard_plot_layout(title, xlabel, ylabel, figsize=(12, 6))`** - Create standard plot
  - Returns pre-configured matplotlib figure and axes
  - Consistent styling across apps

#### Example

```python
from brainlife_utils import setup_matplotlib_backend, save_figure_with_base64
import matplotlib.pyplot as plt

setup_matplotlib_backend()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title('Example Plot')

base64_img = save_figure_with_base64(fig, 'out_figs/plot.png')
```

### report_utils.py

Report generation and product.json management.

#### Functions

- **`create_product_json(filepath='product.json')`** - Initialize product.json
  - Creates empty Brainlife.io product file
  - Sets up structure for Brainlife visualization
  - Call once at the start of output generation

- **`add_info_to_product(message, msg_type='info', filepath='product.json')`** - Add text message
  - Adds status/info messages to product.json
  - Types: `'info'`, `'success'`, `'warning'`, `'error'`, `'danger'`
  - Example: `add_info_to_product('Processed 100 epochs', 'success')`

- **`add_image_to_product(filepath, title, description='', filepath_json='product.json')`** - Add figure
  - Adds PNG image with title to product.json
  - Automatically encodes image as base64
  - Example: `add_image_to_product('out_figs/plot.png', 'ICA Components')`

- **`add_raw_info_to_product(raw, filepath='product.json')`** - Add raw data metadata
  - Extracts and formats raw data information:
    - Number and types of channels
    - Sampling frequency
    - Duration
    - Filter settings
    - Projectors
  - Useful for quality control reports

- **`add_plotly_to_product(plotly_dict, title, filepath='product.json')`** - Add interactive plot
  - Adds interactive Plotly visualization to product.json
  - Requires Plotly figure dictionary with 'data' and 'layout' keys
  - Enables interactive exploration in Brainlife interface

- **`plot_digitized_head_points_3d(raw, show=True)`** - Visualize digitized points
  - Creates 3D visualization of head digitization points
  - Useful for electrode/sensor position validation
  - Works with MEG and EEG data

- **`message_optional_files_in_reports(report, files_dict, out_dir_name)`** - Add optional file info to report
  - Documents optional files used in processing
  - Adds to MNE Report object

#### Example

```python
from brainlife_utils import (
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product
)

# Initialize
create_product_json()

# Add messages
add_info_to_product('Loading data...', 'info')

# Process data...

# Add outputs
add_raw_info_to_product(raw)
add_image_to_product('out_figs/components.png', 'ICA Components')
add_info_to_product('Processing complete', 'success')
```

## Complete App Example

```python
"""
Example Brainlife.io App using brainlife_utils
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

import mne
import matplotlib.pyplot as plt

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product,
    get_channel_types_summary
)

# Setup
setup_matplotlib_backend()
ensure_output_dirs('out_dir', 'out_figs', 'out_report')
config = load_config()
create_product_json()

# Load data
add_info_to_product('Loading data...', 'info')
raw = mne.io.read_raw_fif(config['mne'], preload=True)
channel_summary = get_channel_types_summary(raw)
add_info_to_product(f'Loaded {len(raw.ch_names)} channels: {channel_summary}', 'info')

# Process
add_info_to_product('Processing...', 'info')
if config.get('l_freq') and config.get('h_freq'):
    raw.filter(l_freq=config['l_freq'], h_freq=config['h_freq'])

# Visualize
fig = raw.plot_psd(show=False, fmax=50)
plt.savefig('out_figs/psd.png', dpi=150)
plt.close()

# Save outputs
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)

# Report
add_raw_info_to_product(raw)
add_image_to_product('out_figs/psd.png', 'Power Spectral Density')
add_info_to_product('Processing complete', 'success')

print("Done!")
```

## Error Handling

All functions include proper error handling with informative messages:

```python
from brainlife_utils import load_config

try:
    config = load_config()
except FileNotFoundError:
    print("config.json not found in current directory")
except json.JSONDecodeError:
    print("config.json is not valid JSON")
```

## Best Practices

1. **Always call `setup_matplotlib_backend()` early** - Required for headless execution
2. **Use `ensure_output_dirs()` before file operations** - Guarantees directories exist
3. **Call `create_product_json()` once at start** - Initializes output for Brainlife
4. **Add info messages throughout processing** - Provides user feedback and debugging
5. **Use `add_raw_info_to_product()` for data descriptions** - Automatic metadata extraction
6. **Validate optional parameters** - Check for None values from config

## Contributing

To add new utilities:
1. Add function to appropriate module (or create new module if needed)
2. Include comprehensive docstrings (NumPy format)
3. Update this README with function description and examples
4. Test with multiple apps before merging

## License

Copyright (c) 2020 Brainlife.io

See LICENSE file for details.

## Authors

- Maximilien Chaumon (ICM)
- Contributed by: Brainlife team and collaborators

## References

- [MNE-Python](https://mne.tools/)
- [Brainlife.io](https://brainlife.io/)
- [NumPy Docstring Format](https://numpydoc.readthedocs.io/)
