"""
po_pipeline.py - Purchase order pipeline status

Shows PO status breakdown (pie) and monthly PO volume/value
to track procurement activity over time.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from config import COLORS, CHARTS_DIR


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
