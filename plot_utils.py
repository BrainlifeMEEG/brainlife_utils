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


def save_plot_to_base64(fig, close_fig=True):
    """Convert matplotlib figure to base64 string.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Matplotlib figure to convert.
    close_fig : bool
        Whether to close the figure after conversion.
        
    Returns
    -------
    str
        Base64 encoded string of the figure.
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    
    # Convert to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    if close_fig:
        plt.close(fig)
    
    return image_base64


def save_figure_with_base64(fig, filepath, close_fig=True):
    """Save figure to file and return base64 string.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Matplotlib figure to save.
    filepath : str
        Path where to save the figure.
    close_fig : bool
        Whether to close the figure after saving.
        
    Returns
    -------
    str
        Base64 encoded string of the figure.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to file
    fig.savefig(filepath, bbox_inches='tight', dpi=150)
    
    # Get base64 string
    base64_str = save_plot_to_base64(fig, close_fig=close_fig)
    
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
