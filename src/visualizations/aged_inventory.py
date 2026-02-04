"""
aged_inventory.py - Overstock and slow-moving inventory analysis

Identifies markdown and transfer candidates by showing
overstock by category and slow movers by vendor.
"""

import os
import matplotlib.pyplot as plt

from src.config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_aged_inventory(inventory_df):
    """Aged and overstock inventory analysis."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Aged & Overstock Inventory Analysis', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # Overstock by category
    overstock = inventory_df[inventory_df['stock_status'] == 'Overstock']
    if len(overstock) > 0:
        overstock_by_cat = overstock.groupby('category')['inventory_value_cost'].sum().sort_values(ascending=True)
        overstock_by_cat.plot(kind='barh', ax=ax1, color=COLORS['warning'], edgecolor='none')
        ax1.set_title('Overstock Value by Category (at Cost)', fontweight='bold')
        ax1.set_xlabel('Inventory Value ($)')
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    else:
        ax1.text(0.5, 0.5, 'No overstock identified', ha='center', va='center', fontsize=14)
        ax1.axis('off')
    
    # Slow movers by vendor
    slow_movers = inventory_df[inventory_df['weeks_of_supply'] > 12]
    if len(slow_movers) > 0:
        slow_by_vendor = slow_movers.groupby('vendor')['inventory_value_cost'].sum().sort_values(ascending=True)
        slow_by_vendor.plot(kind='barh', ax=ax2, color=COLORS['danger'], edgecolor='none')
        ax2.set_title('Slow-Moving Inventory by Vendor (at Cost)', fontweight='bold')
        ax2.set_xlabel('Inventory Value ($)')
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    else:
        ax2.text(0.5, 0.5, 'No slow movers identified', ha='center', va='center', fontsize=14)
        ax2.axis('off')
    
    for ax in [ax1, ax2]:
        style_chart_basic(ax)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '07_aged_inventory.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 07: Aged Inventory Analysis")
