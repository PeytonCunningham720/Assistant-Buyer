"""
chart_utils.py - Reusable chart styling and helper functions

This module contains helper functions for creating consistent, professional
visualizations across all charts in the dashboard.

Functions:
    - draw_kpi_card: Creates polished KPI cards with icons and values
    - style_barh: Applies consistent styling to horizontal bar charts
    - get_color_scale: Returns colors based on threshold values
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from config import COLORS


def draw_kpi_card(ax, x, y, w, h, label, value_text, subtitle='',
                  accent_color=None, icon_text='', value_fontsize=30):
    """
    Draw a polished KPI card on a matplotlib Axes.
    
    Creates a card with:
    - Rounded rectangle background with soft shadow
    - Colored accent strip on the left edge
    - Large value text centered
    - Label and optional subtitle
    - Optional icon/emoji at the top
    
    Args:
        ax: Matplotlib Axes to draw on (should have axis('off'))
        x, y: Position in axes coordinates (0-1)
        w, h: Width and height in axes coordinates
        label: Text label describing the metric
        value_text: The main value to display (pre-formatted string)
        subtitle: Optional secondary text below the label
        accent_color: Color for the left accent strip (defaults to COLORS['accent'])
        icon_text: Optional emoji or icon character
        value_fontsize: Font size for the main value
    """
    if accent_color is None:
        accent_color = COLORS['accent']
    
    # Shadow - offset slightly down and right for depth effect
    shadow = FancyBboxPatch(
        (x + 0.003, y - 0.006), w, h,
        boxstyle="round,pad=0.012",
        linewidth=0,
        facecolor='#D1D9E6',
        alpha=0.45,
        zorder=0,
        transform=ax.transAxes
    )
    ax.add_patch(shadow)
    
    # Main card background - white with subtle border
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012",
        linewidth=0.8,
        edgecolor=COLORS['border'],
        facecolor='white',
        zorder=1,
        transform=ax.transAxes
    )
    ax.add_patch(card)
    
    # Colored accent strip on left edge - visual indicator
    strip = FancyBboxPatch(
        (x, y), 0.008, h,
        boxstyle="round,pad=0.004",
        linewidth=0,
        facecolor=accent_color,
        zorder=2,
        transform=ax.transAxes
    )
    ax.add_patch(strip)
    
    cx = x + w / 2  # horizontal center of card
    
    # Icon at the top
    if icon_text:
        ax.text(cx, y + h * 0.87, icon_text,
                ha='center', va='center',
                fontsize=16,
                transform=ax.transAxes,
                zorder=3)
    
    # Large value - the main number
    ax.text(cx, y + h * 0.55, value_text,
            ha='center', va='center',
            fontsize=value_fontsize,
            fontweight='bold',
            color=COLORS['primary'],
            transform=ax.transAxes,
            zorder=3)
    
    # Label - describes what the value represents
    ax.text(cx, y + h * 0.30, label,
            ha='center', va='center',
            fontsize=9.5,
            color=COLORS['text_light'],
            fontweight='medium',
            transform=ax.transAxes,
            zorder=3)
    
    # Subtitle - additional context or comparison
    if subtitle:
        ax.text(cx, y + h * 0.12, subtitle,
                ha='center', va='center',
                fontsize=8,
                color=accent_color,
                fontweight='medium',
                transform=ax.transAxes,
                zorder=3)


def style_barh(ax, title, xlabel='', show_grid=True):
    """
    Apply consistent professional styling to horizontal bar charts.
    
    Styling includes:
    - Title positioned left-aligned
    - Clean spines (only left and bottom)
    - Subtle gridlines on x-axis only
    - Consistent text colors
    
    Args:
        ax: Matplotlib Axes to style
        title: Chart title
        xlabel: Label for x-axis
        show_grid: Whether to show vertical gridlines
    """
    ax.set_title(title,
                 fontsize=11,
                 fontweight='bold',
                 color=COLORS['text'],
                 pad=10,
                 loc='left')
    
    ax.set_xlabel(xlabel, fontsize=9, color=COLORS['text_light'])
    
    # Clean up spines - remove top and right
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['border'])
    ax.spines['bottom'].set_color(COLORS['border'])
    
    # Consistent tick styling
    ax.tick_params(axis='both', colors=COLORS['text_light'], labelsize=8)
    
    # Subtle gridlines help read values
    if show_grid:
        ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.5)
        ax.yaxis.grid(False)
    
    ax.set_axisbelow(True)  # grid behind bars


def style_chart_basic(ax, title=''):
    """
    Apply basic styling to any chart - removes clutter.
    
    Args:
        ax: Matplotlib Axes to style
        title: Optional title
    """
    if title:
        ax.set_title(title, fontweight='bold', color=COLORS['text'])
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def get_threshold_color(value, low_thresh, high_thresh, invert=False):
    """
    Return a color based on value thresholds.
    
    Used for color-coding metrics like in-stock rate where
    green = good, yellow = warning, red = bad.
    
    Args:
        value: The numeric value to evaluate
        low_thresh: Below this is danger/warning
        high_thresh: Above this is success
        invert: If True, low values are good (like lead time)
        
    Returns:
        Color string from COLORS palette
    """
    if invert:
        # Lower is better (e.g., lead time, days late)
        if value <= low_thresh:
            return COLORS['success']
        elif value <= high_thresh:
            return COLORS['warning']
        else:
            return COLORS['danger']
    else:
        # Higher is better (e.g., in-stock rate, on-time %)
        if value >= high_thresh:
            return COLORS['success']
        elif value >= low_thresh:
            return COLORS['warning']
        else:
            return COLORS['danger']


def get_threshold_colors(values, low_thresh, high_thresh, invert=False):
    """
    Return a list of colors for a series of values.
    
    Convenience wrapper around get_threshold_color for coloring bar charts.
    
    Args:
        values: Iterable of numeric values
        low_thresh: Below this is danger/warning
        high_thresh: Above this is success
        invert: If True, low values are good
        
    Returns:
        List of color strings
    """
    return [get_threshold_color(v, low_thresh, high_thresh, invert) for v in values]


def format_currency(value, decimals=0):
    """Format a number as currency string."""
    if abs(value) >= 1_000_000:
        return f'${value/1_000_000:.{decimals}f}M'
    elif abs(value) >= 1_000:
        return f'${value/1_000:.{decimals}f}K'
    else:
        return f'${value:.{decimals}f}'


def format_currency_axis(x, p):
    """Formatter function for matplotlib currency axes."""
    if abs(x) >= 1_000_000:
        return f'${x/1_000_000:.1f}M'
    elif abs(x) >= 1_000:
        return f'${x/1_000:.0f}K'
    else:
        return f'${x:.0f}'
