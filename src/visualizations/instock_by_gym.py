"""
instock_by_gym.py - In-stock rate by gym location

Key allocation metric showing which gyms need inventory attention.
Color-coded by performance threshold (90% target).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic, get_threshold_colors


def create_instock_by_gym(inventory_df):
    """In-stock rate by gym location."""
    
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')
    
    gym_instock = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    ).sort_values(ascending=True)
    
    colors_is = get_threshold_colors(gym_instock.values, 80, 90)
    gym_instock.plot(kind='barh', ax=ax, color=colors_is, edgecolor='none')
    ax.set_title('In-Stock Rate by Gym Location', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('In-Stock Rate (%)')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=1, alpha=0.7, label='90% Target')
    
    # Value labels
    for i, (v, name) in enumerate(zip(gym_instock.values, gym_instock.index)):
        ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=8)
    
    # Legend explaining colors
    legend_elements = [
        mpatches.Patch(color=COLORS['success'], label='≥ 90% (Target)'),
        mpatches.Patch(color=COLORS['warning'], label='80-90% (Needs Attention)'),
        mpatches.Patch(color=COLORS['danger'], label='< 80% (Critical)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    style_chart_basic(ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '05_instock_by_gym.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 05: In-Stock Rate by Gym")
