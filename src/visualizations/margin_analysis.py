"""
margin_analysis.py - Gross margin analysis by category and vendor

Shows margin percentages by category and total margin dollars by vendor
to identify most profitable product lines and supplier relationships.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic, get_threshold_colors


def create_margin_analysis(sales_df):
    """Gross margin analysis by category and vendor."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    
    # Get date range from the data for context
    date_min = sales_df['sale_date'].min().strftime('%b %Y')
    date_max = sales_df['sale_date'].max().strftime('%b %Y')
    
    # Main title with date range subtitle
    fig.suptitle('Gross Margin Analysis', fontsize=16,
                 fontweight='bold', color=COLORS['text'], y=0.98)
    fig.text(0.5, 0.92, f'{date_min} – {date_max}', ha='center',
             fontsize=10, color=COLORS['text_light'], style='italic')
    
    # Margin % by category
    cat_margin = sales_df.groupby('category').agg(
        total_revenue=('sale_price', 'sum'),
        total_cost=('cost', 'sum')
    )
    cat_margin['margin_pct'] = (
        (cat_margin['total_revenue'] - cat_margin['total_cost']) /
        cat_margin['total_revenue'] * 100
    ).round(1)
    cat_margin = cat_margin.sort_values('margin_pct', ascending=True)
    
    colors_margin = get_threshold_colors(cat_margin['margin_pct'].values, 40, 50)
    cat_margin['margin_pct'].plot(kind='barh', ax=ax1, color=colors_margin, edgecolor='none')
    ax1.set_title('Gross Margin % by Category', fontweight='bold')
    ax1.set_xlabel('Margin %')
    ax1.axvline(x=50, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='50% Target')
    ax1.legend()
    style_chart_basic(ax1)
    
    # Margin $ by vendor
    vendor_margin = sales_df.groupby('vendor').agg(
        total_revenue=('sale_price', 'sum'),
        total_cost=('cost', 'sum')
    )
    vendor_margin['margin_dollars'] = vendor_margin['total_revenue'] - vendor_margin['total_cost']
    vendor_margin = vendor_margin.sort_values('margin_dollars', ascending=True)
    
    vendor_margin['margin_dollars'].plot(kind='barh', ax=ax2, color=COLORS['accent'], edgecolor='none')
    ax2.set_title('Gross Margin $ by Vendor', fontweight='bold')
    ax2.set_xlabel('Margin ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    style_chart_basic(ax2)
    
    plt.tight_layout(rect=[0, 0, 1, 0.90])  # Make room for subtitle
    plt.savefig(os.path.join(CHARTS_DIR, '03_margin_analysis.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 03: Margin Analysis")
