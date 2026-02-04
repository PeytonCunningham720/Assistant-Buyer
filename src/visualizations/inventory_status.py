"""
inventory_status.py - Overall inventory health overview

Shows stock status distribution (pie) and weeks of supply histogram
to assess overall inventory health across the network.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_inventory_status(inventory_df):
    """Overall inventory health - status distribution and weeks of supply."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Inventory Health Overview', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # Status pie chart
    status_counts = inventory_df['stock_status'].value_counts()
    status_colors = {
        'In Stock': COLORS['success'],
        'Low': COLORS['warning'],
        'Critical Low': '#E67E22',
        'Out of Stock': COLORS['danger'],
        'Overstock': COLORS['accent'],
    }
    colors_pie = [status_colors.get(s, 'gray') for s in status_counts.index]
    ax1.pie(status_counts.values, labels=status_counts.index, colors=colors_pie,
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    ax1.set_title('Stock Status Distribution', fontweight='bold')
    
    # Weeks of supply histogram
    wos = inventory_df[inventory_df['on_hand'] > 0]['weeks_of_supply']
    ax2.hist(wos, bins=30, color=COLORS['primary'], edgecolor='white', alpha=0.8)
    ax2.axvline(x=4, color=COLORS['success'], linestyle='--', linewidth=2,
                label='Min Target (4 wks)')
    ax2.axvline(x=12, color=COLORS['warning'], linestyle='--', linewidth=2,
                label='Max Target (12 wks)')
    ax2.set_title('Weeks of Supply Distribution', fontweight='bold')
    ax2.set_xlabel('Weeks of Supply')
    ax2.set_ylabel('Number of SKU-Locations')
    ax2.legend()
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '06_inventory_status.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 06: Inventory Status Overview")
