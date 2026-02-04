"""
sales_by_region.py - Regional sales performance comparison

Compares revenue and average transaction value across
Movement's geographic regions.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_sales_by_region(sales_df):
    """Regional sales performance comparison."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Regional Sales Performance', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # Revenue by region
    region_rev = sales_df.groupby('region')['sale_price'].sum().sort_values(ascending=False)
    region_rev.plot(kind='bar', ax=ax1, color=COLORS['primary'], edgecolor='none')
    ax1.set_title('Revenue by Region', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)
    style_chart_basic(ax1)
    
    # Average transaction value by region
    region_avg = sales_df.groupby('region')['sale_price'].mean().sort_values(ascending=False)
    region_avg.plot(kind='bar', ax=ax2, color=COLORS['purple'], edgecolor='none')
    ax2.set_title('Average Transaction Value by Region', fontweight='bold')
    ax2.set_ylabel('Avg Sale Price ($)')
    ax2.tick_params(axis='x', rotation=45)
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '02_sales_by_region.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 02: Sales by Region")
