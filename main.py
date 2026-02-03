"""
main.py - Entry point for the Retail Analysis Dashboard

This is the script you run to generate the full analysis.
It orchestrates all the pieces:
    1. Generate synthetic data
    2. Export raw data to CSV
    3. Create all visualizations
    4. Print summary report

Usage:
    python main.py

Or from the project root:
    python src/main.py

Author: Peyton Cunningham
Project: Movement Climbing Gyms - Assistant Buyer Portfolio
"""

import os
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Import project modules
from config import DATA_DIR, apply_plot_style
from data_generator import (
    get_base_dataframes,
    generate_sales_data,
    generate_inventory_data,
    generate_po_data
)
from charts import (
    create_executive_dashboard,
    create_sales_by_category,
    create_sales_by_region,
    create_margin_analysis,
    create_monthly_trend,
    create_top_bottom_sellers,
    create_instock_by_gym,
    create_inventory_status,
    create_aged_inventory,
    create_allocation_analysis,
    create_vendor_scorecard,
    create_po_pipeline,
    create_shoe_deep_dive
)
from summary import print_summary


def main():
    """
    Main execution function - runs the complete analysis pipeline.
    """
    # ─────────────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────────────
    print("=" * 70)
    print("RETAIL BUYING & ALLOCATION ANALYSIS DASHBOARD")
    print("Movement Climbing Gyms")
    print("=" * 70)
    
    # ─────────────────────────────────────────────────────────────────────
    # STEP 1: GENERATE DATA
    # ─────────────────────────────────────────────────────────────────────
    print("\n📦 Generating synthetic retail data...")
    
    # Get base DataFrames from config
    gyms_df, products_df = get_base_dataframes()
    
    # Generate all datasets
    sales_df = generate_sales_data(gyms_df, products_df)
    inventory_df = generate_inventory_data(gyms_df, products_df)
    po_df = generate_po_data(products_df)
    
    # Print generation stats
    print(f"   ✅ {len(sales_df):,} sales transactions generated")
    print(f"   ✅ {len(inventory_df):,} inventory records generated")
    print(f"   ✅ {len(po_df):,} purchase orders generated")
    print(f"   ✅ {len(products_df)} SKUs across {len(gyms_df)} gym locations")
    
    # ─────────────────────────────────────────────────────────────────────
    # STEP 2: EXPORT RAW DATA
    # ─────────────────────────────────────────────────────────────────────
    sales_df.to_csv(os.path.join(DATA_DIR, 'sales_data.csv'), index=False)
    inventory_df.to_csv(os.path.join(DATA_DIR, 'inventory_data.csv'), index=False)
    po_df.to_csv(os.path.join(DATA_DIR, 'purchase_orders.csv'), index=False)
    products_df.to_csv(os.path.join(DATA_DIR, 'product_catalog.csv'), index=False)
    gyms_df.to_csv(os.path.join(DATA_DIR, 'gym_locations.csv'), index=False)
    
    print("\n💾 Raw data exported to output/data/")
    
    # ─────────────────────────────────────────────────────────────────────
    # STEP 3: CREATE VISUALIZATIONS
    # ─────────────────────────────────────────────────────────────────────
    print("\n📊 Running analyses and generating visualizations...\n")
    
    # Apply consistent plot styling
    apply_plot_style()
    
    # Executive Dashboard - the main overview
    create_executive_dashboard(sales_df, inventory_df, po_df)
    
    # Sales Analysis
    create_sales_by_category(sales_df)
    create_sales_by_region(sales_df)
    create_margin_analysis(sales_df)
    create_monthly_trend(sales_df)
    create_top_bottom_sellers(sales_df)
    
    # Inventory Analysis
    create_instock_by_gym(inventory_df)
    create_inventory_status(inventory_df)
    create_aged_inventory(inventory_df)
    create_allocation_analysis(inventory_df, sales_df)
    
    # Vendor Analysis
    create_vendor_scorecard(po_df)
    create_po_pipeline(po_df)
    
    # Category Deep-Dive
    create_shoe_deep_dive(sales_df, inventory_df, products_df)
    
    # ─────────────────────────────────────────────────────────────────────
    # STEP 4: PRINT SUMMARY
    # ─────────────────────────────────────────────────────────────────────
    print_summary(sales_df, inventory_df, po_df)


if __name__ == '__main__':
    main()
