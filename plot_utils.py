"""
Plotting and visualization utilities for Brainlife.io apps.
"""

import matplotlib
import matplotlib.pyplot as plt
import base64
import os
from io import BytesIO


def setup_matplotlib_backend():
    """Set up matplotlib backend for headless execution."""
    matplotlib.use('Agg')


def save_plot_to_base64(fig, close_fig=True, dpi=100):
    """Convert matplotlib figure to base64 string.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Matplotlib figure to convert.
    close_fig : bool
        Whether to close the figure after conversion.
    dpi : int
        Resolution for the image. Default: 100 (lower quality for smaller file size)
        
    Returns
    -------
    str
        Base64 encoded string of the figure.
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=dpi)
    buffer.seek(0)
    
    # Convert to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    if close_fig:
        plt.close(fig)
    
    return image_base64


def save_figure_with_base64(fig, filepath, close_fig=True, dpi_file=150, dpi_base64=100):
    """Save figure to file and return base64 string.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Matplotlib figure to save.
    filepath : str
        Path where to save the figure.
    close_fig : bool
        Whether to close the figure after saving.
    dpi_file : int
        Resolution for the saved file. Default: 150 (higher quality)
    dpi_base64 : int
        Resolution for the base64 encoding. Default: 100 (smaller file size for product.json)
        
    Returns
    -------
    str
        Base64 encoded string of the figure (at dpi_base64 resolution).
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to file with higher quality
    fig.savefig(filepath, bbox_inches='tight', dpi=dpi_file)
    
    if close_fig:
        plt.close(fig)
    
    # Get base64 string with lower quality for smaller size
    base64_str = save_plot_to_base64(fig, close_fig=close_fig, dpi=dpi_base64)
    
    return base64_str


def create_standard_plot_layout(nrows=1, ncols=1, figsize=None):
    """Create standard plot layout for Brainlife apps.
    
    Parameters
    ----------
    nrows : int
        Number of subplot rows.
    ncols : int  
        Number of subplot columns.
    figsize : tuple, optional
        Figure size (width, height).
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object.
    axes : matplotlib.axes.Axes or array of Axes
        Axes object(s).
    """
    if figsize is None:
        figsize = (10, 6) if nrows == 1 and ncols == 1 else (12, 8)
        
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    
    return fig, axes
