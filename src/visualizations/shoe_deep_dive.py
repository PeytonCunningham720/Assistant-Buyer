"""
shoe_deep_dive.py - Climbing shoes category deep-dive

Detailed analysis of the climbing shoes category including
revenue by model, beginner vs advanced mix, in-stock rates, and trends.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic, get_threshold_colors


def create_shoe_deep_dive(sales_df, inventory_df, products_df):
    """Deep-dive into climbing shoes category."""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
    fig.suptitle('Category Deep-Dive: Climbing Shoes', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    shoes_sales = sales_df[sales_df['category'] == 'Climbing Shoes'].copy()
    shoes_inv = inventory_df[inventory_df['category'] == 'Climbing Shoes']
    
    # Revenue by shoe model
    ax = axes[0, 0]
    shoe_rev = shoes_sales.groupby('product_name')['sale_price'].sum().sort_values(ascending=True)
    shoe_rev.plot(kind='barh', ax=ax, color=COLORS['accent'], edgecolor='none')
    ax.set_title('Revenue by Shoe Model', fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    style_chart_basic(ax)
    
    # Beginner vs Advanced pie
    ax = axes[0, 1]
    shoes_products = products_df[products_df['category'] == 'Climbing Shoes']
    shoes_with_sub = shoes_sales.merge(shoes_products[['sku', 'subcategory']], on='sku')
    sub_rev = shoes_with_sub.groupby('subcategory')['sale_price'].sum()
    sub_rev.plot(kind='pie', ax=ax, colors=[COLORS['accent'], COLORS['secondary']],
                 autopct='%1.1f%%', textprops={'fontsize': 12})
    ax.set_title('Beginner vs Advanced Shoe Sales', fontweight='bold')
    ax.set_ylabel('')
    
    # In-stock rate by gym for shoes
    ax = axes[1, 0]
    shoe_instock = shoes_inv.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    ).sort_values(ascending=True)
    colors_shoe = get_threshold_colors(shoe_instock.values, 70, 85)
    shoe_instock.plot(kind='barh', ax=ax, color=colors_shoe, fontsize=7, edgecolor='none')
    ax.set_title('Shoe In-Stock Rate by Gym', fontweight='bold')
    ax.set_xlabel('In-Stock %')
    style_chart_basic(ax)
    
    # Monthly shoe revenue trend
    ax = axes[1, 1]
    shoes_sales['month'] = shoes_sales['sale_date'].dt.to_period('M')
    monthly_shoes = shoes_sales.groupby('month')['sale_price'].sum()
    monthly_shoes.index = monthly_shoes.index.astype(str)
    
    ax.fill_between(range(len(monthly_shoes)), monthly_shoes.values,
                    alpha=0.15, color=COLORS['secondary'])
    ax.plot(range(len(monthly_shoes)), monthly_shoes.values, color=COLORS['secondary'],
            linewidth=2, marker='o', markersize=5, markerfacecolor='white',
            markeredgecolor=COLORS['secondary'], markeredgewidth=1.8)
    ax.set_title('Monthly Shoe Revenue Trend', fontweight='bold')
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.set_xticks(range(len(monthly_shoes)))
    ax.set_xticklabels(monthly_shoes.index, rotation=45)
    style_chart_basic(ax)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '12_shoe_deep_dive.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 12: Climbing Shoe Deep-Dive")
