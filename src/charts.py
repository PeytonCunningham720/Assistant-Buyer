"""
charts.py - All chart generation functions for the retail dashboard

This module contains functions to create each visualization in the dashboard.
Charts are organized by analysis area:
    - Executive Dashboard (overview)
    - Sales Analysis (revenue, trends, categories)
    - Inventory Analysis (stock levels, allocation)
    - Vendor Analysis (performance scorecards)

Each function takes the relevant DataFrames and saves a PNG to CHARTS_DIR.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.config import COLORS, CHARTS_DIR, apply_plot_style
from src.chart_utils import (
    draw_kpi_card, style_barh, style_chart_basic,
    get_threshold_colors, format_currency_axis
)

# Apply consistent styling when module loads
apply_plot_style()


# =============================================================================
# EXECUTIVE DASHBOARD
# =============================================================================

def create_executive_dashboard(sales_df, inventory_df, po_df):
    """
    Create the main executive dashboard with KPI cards and summary charts.
    
    This is the "at a glance" view showing:
    - Key metrics (revenue, margin, in-stock rate, inventory value, vendor OTD)
    - Revenue by category
    - Monthly revenue trend
    - Top performing gyms
    """
    fig = plt.figure(figsize=(20, 13), facecolor=COLORS['light'])
    
    # ── Title bar ──
    fig.text(0.03, 0.965, 'MOVEMENT RETAIL', fontsize=22, fontweight='bold',
             color=COLORS['primary'], va='top')
    fig.text(0.03, 0.940, 'Executive Dashboard  ·  12-Month Performance Summary',
             fontsize=10, color=COLORS['text_light'], va='top')
    fig.text(0.97, 0.965, 'FY 2025', fontsize=11, fontweight='bold',
             color=COLORS['text_light'], va='top', ha='right')
    
    # Accent line under title
    line = plt.Line2D([0.03, 0.97], [0.925, 0.925], transform=fig.transFigure,
                      color=COLORS['secondary'], linewidth=2.5, zorder=10)
    fig.add_artist(line)
    
    # ━━━━━━ KPI CARDS ROW ━━━━━━
    ax_kpi = fig.add_axes([0.0, 0.72, 1.0, 0.20])
    ax_kpi.set_xlim(0, 1)
    ax_kpi.set_ylim(0, 1)
    ax_kpi.axis('off')
    
    # Calculate KPI values
    total_revenue = sales_df['sale_price'].sum()
    total_cost = sales_df['cost'].sum()
    total_margin = total_revenue - total_cost
    margin_pct = total_margin / total_revenue * 100
    
    in_stock_count = len(inventory_df[inventory_df['stock_status'].isin(['In Stock', 'Overstock'])])
    total_skus_locs = len(inventory_df)
    in_stock_rate = in_stock_count / total_skus_locs * 100
    oos_count = len(inventory_df[inventory_df['stock_status'] == 'Out of Stock'])
    
    total_inv_cost = inventory_df['inventory_value_cost'].sum()
    total_inv_retail = inventory_df['inventory_value_retail'].sum()
    
    received_pos = po_df[po_df['status'] == 'Received']
    overall_otd = received_pos['on_time'].mean() * 100 if len(received_pos) > 0 else 0
    
    # Card layout - 5 cards evenly spaced
    card_w, card_h = 0.165, 0.85
    gap = 0.02
    start_x = 0.03
    
    cards = [
        {'label': 'Total Revenue', 'value': f'${total_revenue/1e6:.2f}M',
         'subtitle': f'Gross Margin {margin_pct:.1f}%',
         'color': COLORS['accent']},
        {'label': 'Gross Margin', 'value': f'${total_margin/1e6:.2f}M',
         'subtitle': f'{margin_pct:.1f}% of Revenue',
         'color': COLORS['success']},
        {'label': 'In-Stock Rate', 'value': f'{in_stock_rate:.1f}%',
         'subtitle': f'{oos_count} SKU-locations OOS',
         'color': COLORS['success'] if in_stock_rate >= 85 else COLORS['warning']},
        {'label': 'Inventory at Cost', 'value': f'${total_inv_cost/1e6:.2f}M',
         'subtitle': f'Retail: ${total_inv_retail/1e6:.2f}M',
         'color': COLORS['purple']},
        {'label': 'Vendor On-Time %', 'value': f'{overall_otd:.1f}%',
         'subtitle': f'{len(po_df)} POs Tracked',
         'color': COLORS['teal'] if overall_otd >= 90 else COLORS['warning']},
    ]
    
    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        draw_kpi_card(ax_kpi, cx, 0.08, card_w, card_h,
                      label=c['label'], value_text=c['value'],
                      subtitle=c['subtitle'], accent_color=c['color'],
                      icon_text=c['icon'])
    
    # ━━━━━━ CHART PANELS ROW ━━━━━━
    
    # Panel 1: Revenue by Category
    ax1 = fig.add_axes([0.05, 0.07, 0.27, 0.58])
    ax1.set_facecolor('white')
    
    cat_sales = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=True)
    colors_bar = [COLORS['secondary'] if i == len(cat_sales) - 1
                  else COLORS['accent'] for i in range(len(cat_sales))]
    bars = ax1.barh(range(len(cat_sales)), cat_sales.values, height=0.65,
                    color=colors_bar, edgecolor='none', zorder=3)
    ax1.set_yticks(range(len(cat_sales)))
    ax1.set_yticklabels(cat_sales.index, fontsize=8)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_currency_axis))
    style_barh(ax1, 'Revenue by Category')
    
    # Data labels on bars
    for bar, val in zip(bars, cat_sales.values):
        ax1.text(val + cat_sales.max() * 0.02, bar.get_y() + bar.get_height() / 2,
                 f'${val/1000:.0f}K', va='center', fontsize=7.5,
                 color=COLORS['text_light'], fontweight='medium')
    
    # Panel 2: Monthly Revenue Trend
    ax2 = fig.add_axes([0.38, 0.07, 0.27, 0.58])
    ax2.set_facecolor('white')
    
    sales_df['month'] = sales_df['sale_date'].dt.to_period('M')
    monthly_rev = sales_df.groupby('month')['sale_price'].sum()
    months_str = [str(m) for m in monthly_rev.index]
    x_pos = range(len(monthly_rev))
    
    # Area fill with line
    ax2.fill_between(x_pos, monthly_rev.values, alpha=0.12, color=COLORS['accent'], zorder=2)
    ax2.plot(x_pos, monthly_rev.values, color=COLORS['accent'], linewidth=2.2,
             marker='o', markersize=5, markerfacecolor='white',
             markeredgecolor=COLORS['accent'], markeredgewidth=1.8, zorder=3)
    
    # Highlight peak month
    peak_idx = np.argmax(monthly_rev.values)
    ax2.plot(peak_idx, monthly_rev.values[peak_idx], 'o', markersize=9,
             markerfacecolor=COLORS['secondary'], markeredgecolor='white',
             markeredgewidth=2, zorder=4)
    ax2.annotate(f'Peak\n${monthly_rev.values[peak_idx]/1000:.0f}K',
                 xy=(peak_idx, monthly_rev.values[peak_idx]),
                 xytext=(peak_idx + 0.8, monthly_rev.values[peak_idx] * 1.05),
                 fontsize=7.5, fontweight='bold', color=COLORS['secondary'],
                 arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=1.2))
    
    ax2.set_xticks(list(x_pos))
    ax2.set_xticklabels([m[-3:] for m in months_str], rotation=45, fontsize=7.5)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_currency_axis))
    ax2.set_title('Monthly Revenue Trend', fontsize=11, fontweight='bold',
                  color=COLORS['text'], pad=10, loc='left')
    style_chart_basic(ax2)
    ax2.yaxis.grid(True, color='#EEEEEE', linewidth=0.5)
    ax2.set_axisbelow(True)
    
    # Panel 3: Top 8 Gyms
    ax3 = fig.add_axes([0.71, 0.07, 0.27, 0.58])
    ax3.set_facecolor('white')
    
    gym_sales = sales_df.groupby('gym_name')['sale_price'].sum().nlargest(8).sort_values(ascending=True)
    bars3 = ax3.barh(range(len(gym_sales)), gym_sales.values, height=0.65,
                     color=COLORS['teal'], edgecolor='none', zorder=3, alpha=0.85)
    ax3.set_yticks(range(len(gym_sales)))
    ax3.set_yticklabels([n.replace('Movement ', '') for n in gym_sales.index], fontsize=8)
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(format_currency_axis))
    style_barh(ax3, 'Top 8 Gyms by Revenue')
    
    for bar, val in zip(bars3, gym_sales.values):
        ax3.text(val + gym_sales.max() * 0.02, bar.get_y() + bar.get_height() / 2,
                 f'${val/1000:.0f}K', va='center', fontsize=7.5,
                 color=COLORS['text_light'], fontweight='medium')
    
    # Footer
    fig.text(0.03, 0.015,
             'Data is synthetic — generated for portfolio demonstration purposes only.',
             fontsize=7.5, color=COLORS['text_light'], style='italic')
    fig.text(0.97, 0.015, 'Peyton Cunningham  ·  Movement Climbing Gyms',
             fontsize=7.5, color=COLORS['text_light'], ha='right', fontweight='medium')
    
    plt.savefig(os.path.join(CHARTS_DIR, '00_executive_dashboard.png'),
                bbox_inches='tight', facecolor=COLORS['light'], dpi=200)
    plt.close()
    print("   ✅ Chart 00: Executive Dashboard")


# =============================================================================
# SALES ANALYSIS CHARTS
# =============================================================================

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


def create_margin_analysis(sales_df):
    """Gross margin analysis by category and vendor."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Gross Margin Analysis', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
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
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '03_margin_analysis.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 03: Margin Analysis")


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


def create_top_bottom_sellers(sales_df):
    """Top and bottom products by revenue - identifies winners and markdown candidates."""
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


# =============================================================================
# INVENTORY ANALYSIS CHARTS
# =============================================================================

def create_instock_by_gym(inventory_df):
    """In-stock rate by gym location - key allocation metric."""
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


def create_aged_inventory(inventory_df):
    """Aged and overstock inventory - markdown and transfer candidates."""
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


# =============================================================================
# VENDOR ANALYSIS CHARTS
# =============================================================================

def create_vendor_scorecard(po_df):
    """Vendor performance scorecard - OTD, lead time, spend, variance."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
    fig.suptitle('Vendor Performance Scorecard', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    received_pos = po_df[po_df['status'] == 'Received']
    
    # On-time delivery rate
    ax = axes[0, 0]
    otd = received_pos.groupby('vendor')['on_time'].mean().sort_values(ascending=True) * 100
    colors_otd = get_threshold_colors(otd.values, 85, 92)
    otd.plot(kind='barh', ax=ax, color=colors_otd, edgecolor='none')
    ax.set_title('On-Time Delivery Rate (%)', fontweight='bold')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel('On-Time %')
    ax.set_xlim(0, 105)
    style_chart_basic(ax)
    
    # Average lead time
    ax = axes[0, 1]
    avg_lead = received_pos.groupby('vendor')['lead_time_days'].mean().sort_values(ascending=True)
    avg_lead.plot(kind='barh', ax=ax, color=COLORS['primary'], edgecolor='none')
    ax.set_title('Average Lead Time (Days)', fontweight='bold')
    ax.set_xlabel('Days')
    style_chart_basic(ax)
    
    # Total spend by vendor
    ax = axes[1, 0]
    vendor_spend = po_df.groupby('vendor')['total_cost'].sum().sort_values(ascending=True)
    vendor_spend.plot(kind='barh', ax=ax, color=COLORS['accent'], edgecolor='none')
    ax.set_title('Total PO Spend by Vendor', fontweight='bold')
    ax.set_xlabel('Total Cost ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    style_chart_basic(ax)
    
    # Delivery variance
    ax = axes[1, 1]
    variance = received_pos.groupby('vendor')['delivery_variance_days'].mean().sort_values()
    colors_var = [COLORS['success'] if v <= 0 else COLORS['warning'] if v <= 3
                  else COLORS['danger'] for v in variance.values]
    variance.plot(kind='barh', ax=ax, color=colors_var, edgecolor='none')
    ax.set_title('Average Delivery Variance (Days)', fontweight='bold')
    ax.set_xlabel('Days (negative = early, positive = late)')
    ax.axvline(x=0, color='black', linewidth=1)
    style_chart_basic(ax)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '08_vendor_scorecard.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 08: Vendor Performance Scorecard")


def create_po_pipeline(po_df):
    """Purchase order pipeline - status breakdown and monthly volume."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Purchase Order Pipeline', fontsize=16,
                 fontweight='bold', color=COLORS['text'])
    
    # PO status pie chart
    po_status = po_df['status'].value_counts()
    status_colors_po = {
        'Received': COLORS['success'],
        'In Transit': COLORS['warning'],
        'Open': COLORS['accent']
    }
    colors_po = [status_colors_po.get(s, 'gray') for s in po_status.index]
    ax1.pie(po_status.values, labels=po_status.index, colors=colors_po,
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
    ax1.set_title('PO Status Breakdown', fontweight='bold')
    
    # Monthly PO volume and value
    po_df['po_month'] = pd.to_datetime(po_df['po_date']).dt.to_period('M')
    monthly_pos = po_df.groupby('po_month').agg(
        num_pos=('po_number', 'count'),
        total_value=('total_cost', 'sum')
    )
    monthly_pos.index = monthly_pos.index.astype(str)
    
    ax2_twin = ax2.twinx()
    ax2.bar(range(len(monthly_pos)), monthly_pos['num_pos'], color=COLORS['accent'],
            alpha=0.7, label='# of POs', edgecolor='none')
    ax2_twin.plot(range(len(monthly_pos)), monthly_pos['total_value'],
                  color=COLORS['secondary'], linewidth=2, marker='o', label='PO Value ($)')
    ax2.set_title('Monthly PO Volume & Value', fontweight='bold')
    ax2.set_ylabel('Number of POs')
    ax2_twin.set_ylabel('PO Value ($)')
    ax2_twin.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2.set_xticks(range(len(monthly_pos)))
    ax2.set_xticklabels(monthly_pos.index, rotation=45)
    ax2.spines['top'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '11_po_pipeline.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 11: PO Pipeline")


# =============================================================================
# CATEGORY DEEP-DIVE
# =============================================================================

def create_shoe_deep_dive(sales_df, inventory_df, products_df):
    """Deep-dive into climbing shoes - key category for any climbing retailer."""
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
