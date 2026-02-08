"""
vendor_scorecard.py - Vendor performance scorecard

Four-panel view of vendor metrics: on-time delivery rate,
lead time, total spend, and delivery variance.
"""

import os
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR
from chart_utils import style_chart_basic, get_threshold_colors


def create_vendor_scorecard(po_df):
    """Vendor performance scorecard - OTD, lead time, spend, variance."""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
    
    # Get date range from the data for context
    date_min = po_df['po_date'].min().strftime('%b %Y')
    date_max = po_df['po_date'].max().strftime('%b %Y')
    
    fig.suptitle('Vendor Performance Scorecard', fontsize=16,
                 fontweight='bold', color=COLORS['text'], y=0.98)
    fig.text(0.5, 0.95, f'{date_min} – {date_max}', ha='center',
             fontsize=10, color=COLORS['text_light'], style='italic')
    
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
    
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(os.path.join(CHARTS_DIR, '08_vendor_scorecard.png'),
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 08: Vendor Performance Scorecard")