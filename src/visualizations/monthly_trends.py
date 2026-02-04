"""
monthly_trends.py - Monthly sales trends over time

Shows revenue trend line and stacked category breakdown
to identify seasonal patterns and category mix changes.
"""

import os
import matplotlib.pyplot as plt

from src.config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_monthly_trend(sales_df):
    """Monthly sales trends - revenue and units by category."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor='white')
    fig.suptitle('Monthly Sales Trends', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    sales_df['month'] = sales_df['sale_date'].dt.to_period('M')
    
    # Total monthly revenue trend
    monthly_rev = sales_df.groupby('month')['sale_price'].sum()
    monthly_rev.index = monthly_rev.index.astype(str)
    
    ax1.fill_between(range(len(monthly_rev)), monthly_rev.values,
                     alpha=0.15, color=COLORS['accent'])
    ax1.plot(range(len(monthly_rev)), monthly_rev.values, color=COLORS['accent'],
             linewidth=2.2, marker='o', markersize=5, markerfacecolor='white',
             markeredgecolor=COLORS['accent'], markeredgewidth=1.8)
    ax1.set_title('Total Monthly Revenue', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.set_xticks(range(len(monthly_rev)))
    ax1.set_xticklabels(monthly_rev.index, rotation=45)
    style_chart_basic(ax1)
    
    # Stacked units by category
    monthly_cat = sales_df.groupby(['month', 'category'])['units_sold'].sum().unstack(fill_value=0)
    monthly_cat.index = monthly_cat.index.astype(str)
    monthly_cat.plot(kind='bar', stacked=True, ax=ax2, colormap='Set2', edgecolor='none')
    ax2.set_title('Monthly Units Sold by Category', fontweight='bold')
    ax2.set_ylabel('Units Sold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax2.tick_params(axis='x', rotation=45)
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '04_monthly_trends.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 04: Monthly Sales Trends")
