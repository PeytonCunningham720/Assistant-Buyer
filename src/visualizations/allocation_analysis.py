"""
allocation_analysis.py - Inventory allocation efficiency

Shows inventory-to-sales ratios by gym and stock status
distribution by region to identify allocation imbalances.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic, get_threshold_colors


def create_allocation_analysis(inventory_df, sales_df):
    """Allocation efficiency - inventory-to-sales ratios and regional distribution."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Allocation Efficiency Analysis', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # Inventory-to-sales ratio by gym
    gym_inv = inventory_df.groupby('gym_name')['inventory_value_cost'].sum()
    gym_rev = sales_df.groupby('gym_name')['sale_price'].sum()
    comparison = pd.DataFrame({'inventory': gym_inv, 'revenue': gym_rev}).dropna()
    comparison['inv_to_sales_ratio'] = (comparison['inventory'] / comparison['revenue'] * 100).round(1)
    comparison = comparison.sort_values('inv_to_sales_ratio', ascending=True)
    
    colors_alloc = get_threshold_colors(comparison['inv_to_sales_ratio'].values, 18, 25, invert=True)
    comparison['inv_to_sales_ratio'].plot(kind='barh', ax=ax1, color=colors_alloc, edgecolor='none')
    ax1.set_title('Inventory-to-Sales Ratio by Gym', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Inventory as % of Revenue')
    style_chart_basic(ax1)
    
    # Stock status by region
    region_status = inventory_df.groupby(['region', 'stock_status']).size().unstack(fill_value=0)
    region_status_pct = region_status.div(region_status.sum(axis=1), axis=0) * 100
    
    status_order = ['Out of Stock', 'Critical Low', 'Low', 'In Stock', 'Overstock']
    available_statuses = [s for s in status_order if s in region_status_pct.columns]
    status_colors_map = {
        'Out of Stock': COLORS['danger'],
        'Critical Low': '#E67E22',
        'Low': COLORS['warning'],
        'In Stock': COLORS['success'],
        'Overstock': COLORS['accent'],
    }
    
    region_status_pct[available_statuses].plot(
        kind='barh', stacked=True, ax=ax2,
        color=[status_colors_map[s] for s in available_statuses], edgecolor='none'
    )
    ax2.set_title('Stock Status by Region (%)', fontweight='bold')
    ax2.set_xlabel('Percentage')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '10_allocation_analysis.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 10: Allocation Analysis")
