"""
sales_by_category.py - Revenue and units sold by product category

Compares performance across product categories to identify
top sellers and potential areas for growth.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_sales_by_category(sales_df):
    """Revenue and units sold broken down by product category."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Sales Performance by Product Category', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # Revenue by category
    cat_revenue = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=False)
    colors_bar = [COLORS['secondary'] if i == 0 else COLORS['accent']
                  for i in range(len(cat_revenue))]
    cat_revenue.plot(kind='bar', ax=ax1, color=colors_bar, edgecolor='none')
    ax1.set_title('Revenue by Category', fontweight='bold', color=COLORS['text'])
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)
    style_chart_basic(ax1)
    
    # Units by category
    cat_units = sales_df.groupby('category')['units_sold'].sum().sort_values(ascending=False)
    colors_bar2 = [COLORS['secondary'] if i == 0 else COLORS['teal']
                   for i in range(len(cat_units))]
    cat_units.plot(kind='bar', ax=ax2, color=colors_bar2, edgecolor='none')
    ax2.set_title('Units Sold by Category', fontweight='bold', color=COLORS['text'])
    ax2.set_ylabel('Units Sold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    ax2.tick_params(axis='x', rotation=45)
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '01_sales_by_category.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 01: Sales by Category")
