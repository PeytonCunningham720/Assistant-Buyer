"""
executive_dashboard.py - Main executive overview with KPI cards and summary charts

The "at a glance" view showing key metrics, revenue by category,
monthly trends, and top performing gyms.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import draw_kpi_card, style_barh, style_chart_basic, format_currency_axis


def create_executive_dashboard(sales_df, inventory_df, po_df):
    """Create the executive dashboard with KPI cards and summary charts."""
    
    fig = plt.figure(figsize=(20, 13), facecolor=COLORS['light'])
    
    # Title bar
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
                      subtitle=c['subtitle'], accent_color=c['color'])
    
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
    
    ax2.fill_between(x_pos, monthly_rev.values, alpha=0.12, color=COLORS['accent'], zorder=2)
    ax2.plot(x_pos, monthly_rev.values, color=COLORS['accent'], linewidth=2.2,
             marker='o', markersize=5, markerfacecolor='white',
             markeredgecolor=COLORS['accent'], markeredgewidth=1.8, zorder=3)
    
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
