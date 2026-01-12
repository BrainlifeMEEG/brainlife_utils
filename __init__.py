"""
Brainlife.io MNE Apps Shared Utilities

This package contains shared utility functions for Brainlife.io neuroimaging apps.
"""

from .config_utils import convert_parameters_to_None, define_kwargs, load_config, get_inputs_names
from .file_utils import read_optional_files, copy_optional_files, ensure_output_dirs
from .data_utils import update_data_info_bads, validate_input_data, get_channel_types_summary
from .report_utils import (
    message_optional_files_in_reports, 
    create_product_json, 
    add_image_to_product, 
    add_info_to_product,
    add_plotly_to_product,
    add_raw_info_to_product
)
from .plot_utils import setup_matplotlib_backend, save_plot_to_base64, save_figure_with_base64, create_standard_plot_layout

__version__ = "1.0.0"
__all__ = [
    "convert_parameters_to_None",
    "define_kwargs",
    "load_config",
    "get_inputs_names",
    "read_optional_files",
    "copy_optional_files", 
    "ensure_output_dirs",
    "update_data_info_bads",
    "validate_input_data",
    "get_channel_types_summary",
    "message_optional_files_in_reports",
    "create_product_json",
    "add_image_to_product",
    "add_info_to_product",
    "add_plotly_to_product",
    "add_raw_info_to_product",
    "setup_matplotlib_backend",
    "save_plot_to_base64",
    "save_figure_with_base64",
    "create_standard_plot_layout"
]
