"""
top_bottom_sellers.py - Best and worst performing products

Identifies top revenue generators and markdown/discontinue candidates
based on total revenue performance.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic


def create_top_bottom_sellers(sales_df):
    """Top and bottom products by revenue."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Product Performance: Top & Bottom Sellers', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    product_perf = sales_df.groupby('product_name').agg(
        total_revenue=('sale_price', 'sum'),
        total_units=('units_sold', 'sum'),
    ).sort_values('total_revenue', ascending=False)
    
    # Top 10
    top10 = product_perf.head(10).sort_values('total_revenue', ascending=True)
    top10['total_revenue'].plot(kind='barh', ax=ax1, color=COLORS['success'], edgecolor='none')
    ax1.set_title('Top 10 Products by Revenue', fontweight='bold')
    ax1.set_xlabel('Revenue ($)')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    style_chart_basic(ax1)
    
    # Bottom 10
    bottom10 = product_perf.tail(10).sort_values('total_revenue', ascending=True)
    bottom10['total_revenue'].plot(kind='barh', ax=ax2, color=COLORS['danger'], edgecolor='none')
    ax2.set_title('Bottom 10 Products by Revenue\n(Markdown / discontinue candidates)',
                  fontweight='bold', fontsize=10)
    ax2.set_xlabel('Revenue ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    style_chart_basic(ax2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '09_top_bottom_sellers.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 09: Top & Bottom Sellers")
