"""
summary.py - Generate summary report of key findings

This module analyzes the generated data and prints actionable insights.
The output is what you'd share in a standup or include in a weekly report.
"""


def print_summary(sales_df, inventory_df, po_df):
    """
    Print a formatted summary of key metrics and actionable insights.
    
    Covers:
    - Revenue & margin metrics
    - Inventory health indicators
    - Vendor performance highlights
    - Action items that need attention
    
    Args:
        sales_df: Sales transaction data
        inventory_df: Current inventory snapshot
        po_df: Purchase order history
    """
    print("\n" + "=" * 70)
    print("SUMMARY OF KEY FINDINGS")
    print("=" * 70)
    
    # ─────────────────────────────────────────────────────────────────────
    # REVENUE & MARGIN
    # ─────────────────────────────────────────────────────────────────────
    total_rev = sales_df['sale_price'].sum()
    total_cost_sold = sales_df['cost'].sum()
    total_gm = total_rev - total_cost_sold
    
    print(f"\n REVENUE & MARGIN")
    print(f"   Total Revenue (12 months):      ${total_rev:>12,.2f}")
    print(f"   Total Cost of Goods Sold:        ${total_cost_sold:>12,.2f}")
    print(f"   Gross Margin:                    ${total_gm:>12,.2f} ({total_gm/total_rev*100:.1f}%)")
    
    # Top category
    top_cat = sales_df.groupby('category')['sale_price'].sum().idxmax()
    top_cat_rev = sales_df.groupby('category')['sale_price'].sum().max()
    print(f"   Top Category:                    {top_cat} (${top_cat_rev:,.2f})")
    
    # ─────────────────────────────────────────────────────────────────────
    # INVENTORY HEALTH
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n INVENTORY HEALTH")
    
    total_inv = inventory_df['inventory_value_cost'].sum()
    in_stock = (inventory_df['stock_status'].isin(['In Stock', 'Overstock']).sum() 
                / len(inventory_df) * 100)
    oos = (inventory_df['stock_status'] == 'Out of Stock').sum()
    overstock = (inventory_df['stock_status'] == 'Overstock').sum()
    
    print(f"   Total Inventory Value (at cost): ${total_inv:>12,.2f}")
    print(f"   Overall In-Stock Rate:           {in_stock:>11.1f}%")
    print(f"   Out-of-Stock SKU-Locations:      {oos:>12}")
    print(f"   Overstock SKU-Locations:         {overstock:>12}")
    
    # ─────────────────────────────────────────────────────────────────────
    # VENDOR PERFORMANCE
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n🤝 VENDOR PERFORMANCE")
    
    received = po_df[po_df['status'] == 'Received']
    if len(received) > 0:
        overall_otd = received['on_time'].mean() * 100
        best_vendor = received.groupby('vendor')['on_time'].mean().idxmax()
        best_otd = received.groupby('vendor')['on_time'].mean().max() * 100
        
        print(f"   Overall On-Time Delivery:        {overall_otd:>11.1f}%")
        print(f"   Best Performing Vendor:           {best_vendor} ({best_otd:.1f}%)")
        
        total_po_spend = po_df['total_cost'].sum()
        print(f"   Total PO Spend (12 months):      ${total_po_spend:>12,.2f}")
    
    # ─────────────────────────────────────────────────────────────────────
    # ACTIONABLE INSIGHTS
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n⚡ ACTIONABLE INSIGHTS")
    
    # Gyms below 80% in-stock
    gym_is = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    )
    low_gyms = gym_is[gym_is < 80]
    
    if len(low_gyms) > 0:
        print(f"   🔴 {len(low_gyms)} gym(s) below 80% in-stock rate — prioritize in next allocation")
        for gym, rate in low_gyms.items():
            print(f"      → {gym}: {rate:.1f}%")
    
    # Overstock value
    overstock_value = inventory_df[inventory_df['stock_status'] == 'Overstock']['inventory_value_cost'].sum()
    if overstock_value > 0:
        print(f"   🟡 ${overstock_value:,.2f} in overstock inventory — review for markdowns or transfers")
    
    # Late vendors
    if len(received) > 0:
        vendor_otd = received.groupby('vendor')['on_time'].mean()
        late_vendors = vendor_otd[vendor_otd < 0.85]
        
        if len(late_vendors) > 0:
            print(f"   🔴 {len(late_vendors)} vendor(s) below 85% on-time delivery:")
            for vendor, rate in late_vendors.items():
                print(f"      → {vendor}: {rate*100:.1f}% on-time")
    
    print("\n" + "=" * 70)
    print("✅ All charts saved to output/charts/")
    print("✅ All data exports saved to output/data/")
    print("=" * 70)
