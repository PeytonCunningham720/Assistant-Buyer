"""
data_generator.py - Synthetic data generation for retail analysis

This module creates realistic fake data for sales, inventory, and purchase orders.
All data is synthetic - no real Movement business data is used.

Functions:
    - generate_sales_data: 12 months of transaction-level sales
    - generate_inventory_data: current inventory snapshot across all gyms
    - generate_po_data: purchase order history with vendor performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from config import (
    RANDOM_SEED, GYM_LOCATIONS, VENDORS, PRODUCTS,
    SIZE_MULTIPLIERS, SIZE_CAPACITY, CATEGORY_FREQUENCY, SEASONALITY
)

# Set seed for reproducibility - same "random" data every run
np.random.seed(RANDOM_SEED)


def get_base_dataframes():
    """
    Convert the config dictionaries to DataFrames for easier manipulation.
    Also calculates margin metrics for products.
    
    Returns:
        tuple: (gyms_df, products_df) - DataFrames ready for data generation
    """
    gyms_df = pd.DataFrame(GYM_LOCATIONS)
    products_df = pd.DataFrame(PRODUCTS)
    
    # Calculate margin metrics - these are key for buying decisions
    products_df['margin_pct'] = (
        (products_df['retail'] - products_df['cost']) / products_df['retail'] * 100
    ).round(1)
    products_df['margin_dollars'] = (products_df['retail'] - products_df['cost']).round(2)
    
    return gyms_df, products_df


def generate_sales_data(gyms_df, products_df, months=12):
    """
    Generate realistic sales transaction data.
    
    Logic:
    - Larger gyms sell more (size multiplier)
    - Some categories sell more frequently than others (chalk vs ropes)
    - Sales follow seasonal patterns (peak in fall, slow in summer)
    - ~10% of transactions have a discount applied
    
    Args:
        gyms_df: DataFrame of gym locations
        products_df: DataFrame of products
        months: Number of months of history to generate
        
    Returns:
        DataFrame with one row per unit sold (transaction-level detail)
    """
    sales_records = []
    start_date = datetime(2025, 2, 1)  # 12 months ending Jan 2026
    
    for month_offset in range(months):
        # Figure out what month/year we're generating
        current_month = (start_date.month + month_offset - 1) % 12 + 1
        current_year = start_date.year + (start_date.month + month_offset - 1) // 12
        season_factor = SEASONALITY[current_month]
        
        # Loop through every gym
        for _, gym in gyms_df.iterrows():
            gym_size_mult = SIZE_MULTIPLIERS[gym['size']]
            
            # Loop through every product
            for _, product in products_df.iterrows():
                # Calculate expected sales based on category, gym size, and season
                cat_freq = CATEGORY_FREQUENCY.get(product['category'], 5)
                expected_units = cat_freq * gym_size_mult * season_factor
                
                # Use Poisson distribution for realistic variance
                # (some months sell more, some less, clustered around expected)
                actual_units = max(0, int(np.random.poisson(expected_units)))
                
                if actual_units > 0:
                    # Spread sales across the month
                    days_in_month = 28 if current_month == 2 else (
                        30 if current_month in [4, 6, 9, 11] else 31
                    )
                    
                    # Create one record per unit sold
                    for _ in range(actual_units):
                        sale_day = np.random.randint(1, days_in_month + 1)
                        sale_date = datetime(
                            current_year, current_month, min(sale_day, days_in_month)
                        )
                        
                        # ~10% of sales have a discount
                        discount_pct = 0
                        if np.random.random() < 0.10:
                            discount_pct = np.random.choice([10, 15, 20])
                        
                        sale_price = product['retail'] * (1 - discount_pct / 100)
                        
                        sales_records.append({
                            'sale_date': sale_date,
                            'gym_id': gym['gym_id'],
                            'gym_name': gym['gym_name'],
                            'region': gym['region'],
                            'sku': product['sku'],
                            'product_name': product['name'],
                            'category': product['category'],
                            'vendor': product['vendor'],
                            'units_sold': 1,
                            'retail_price': product['retail'],
                            'sale_price': round(sale_price, 2),
                            'cost': product['cost'],
                            'discount_pct': discount_pct,
                        })
    
    # Convert to DataFrame and add calculated fields
    sales_df = pd.DataFrame(sales_records)
    sales_df['gross_margin'] = (sales_df['sale_price'] - sales_df['cost']).round(2)
    sales_df['margin_pct'] = (
        (sales_df['gross_margin'] / sales_df['sale_price']) * 100
    ).round(1)
    
    return sales_df


def generate_inventory_data(gyms_df, products_df):
    """
    Generate current inventory snapshot for all gym/product combinations.
    
    Logic:
    - Par levels based on product category and gym size
    - Actual on-hand varies around 70% of par (simulates real-world variance)
    - Calculates weeks of supply based on average sales velocity
    - Assigns stock status based on weeks of supply thresholds
    
    Args:
        gyms_df: DataFrame of gym locations
        products_df: DataFrame of products
        
    Returns:
        DataFrame with inventory status for each SKU at each location
    """
    inventory_records = []
    
    for _, gym in gyms_df.iterrows():
        cap = SIZE_CAPACITY[gym['size']]
        
        for _, product in products_df.iterrows():
            # Set par level based on category - chalk needs deep stock
            if product['category'] == 'Chalk':
                par_level = int(25 * cap)
            elif product['category'] in ['Climbing Shoes', 'Apparel']:
                par_level = int(10 * cap)
            elif product['category'] in ['Harnesses', 'Chalk Bags']:
                par_level = int(8 * cap)
            else:
                par_level = int(5 * cap)
            
            # Generate actual on-hand with variance around 70% of par
            on_hand = max(0, int(np.random.normal(par_level * 0.7, par_level * 0.3)))
            
            # Estimate weekly sales velocity
            avg_weekly_sales = max(0.5, np.random.normal(par_level * 0.15, par_level * 0.05))
            
            # Calculate weeks of supply - key metric for reordering
            weeks_of_supply = round(on_hand / avg_weekly_sales, 1) if avg_weekly_sales > 0 else 0
            
            # Assign stock status based on weeks of supply
            if on_hand == 0:
                stock_status = 'Out of Stock'
            elif weeks_of_supply < 2:
                stock_status = 'Critical Low'
            elif weeks_of_supply < 4:
                stock_status = 'Low'
            elif weeks_of_supply > 12:
                stock_status = 'Overstock'
            else:
                stock_status = 'In Stock'
            
            # Random days since last receipt (for aging analysis)
            days_since_receipt = np.random.randint(1, 60)
            
            inventory_records.append({
                'gym_id': gym['gym_id'],
                'gym_name': gym['gym_name'],
                'region': gym['region'],
                'gym_size': gym['size'],
                'sku': product['sku'],
                'product_name': product['name'],
                'category': product['category'],
                'vendor': product['vendor'],
                'par_level': par_level,
                'on_hand': on_hand,
                'avg_weekly_sales': round(avg_weekly_sales, 1),
                'weeks_of_supply': weeks_of_supply,
                'stock_status': stock_status,
                'cost': product['cost'],
                'retail': product['retail'],
                'inventory_value_cost': round(on_hand * product['cost'], 2),
                'inventory_value_retail': round(on_hand * product['retail'], 2),
                'days_since_last_receipt': days_since_receipt,
            })
    
    return pd.DataFrame(inventory_records)


def generate_po_data(products_df, num_pos=120):
    """
    Generate purchase order history with vendor performance data.
    
    Logic:
    - POs spread across the year with varying sizes
    - Delivery performance based on vendor reliability scores
    - Reliable vendors deliver early/on-time, unreliable ones are late
    - Tracks expected vs actual delivery dates
    
    Args:
        products_df: DataFrame of products (needed to pick items for each PO)
        num_pos: Number of purchase orders to generate
        
    Returns:
        DataFrame with PO header information and performance metrics
    """
    po_records = []
    vendors_list = list(VENDORS.keys())
    
    for i in range(num_pos):
        # Pick a random vendor
        vendor = np.random.choice(vendors_list)
        vendor_info = VENDORS[vendor]
        
        # Generate PO date somewhere in the past year
        days_ago = np.random.randint(1, 365)
        po_date = datetime(2025, 2, 1) + timedelta(days=365 - days_ago)
        
        # Calculate expected delivery based on vendor lead time
        expected_delivery = po_date + timedelta(days=vendor_info['lead_time_days'])
        
        # Simulate delivery variance based on reliability
        if np.random.random() < vendor_info['reliability']:
            # Reliable delivery: on-time or slightly early
            delivery_variance = np.random.randint(-3, 2)
        else:
            # Late delivery: 3-15 days late
            delivery_variance = np.random.randint(3, 15)
        
        actual_delivery = expected_delivery + timedelta(days=delivery_variance)
        
        # Determine PO status based on dates
        if actual_delivery <= datetime(2026, 1, 31):
            status = 'Received'
            on_time = delivery_variance <= 0
        elif po_date + timedelta(days=vendor_info['lead_time_days']) > datetime(2026, 1, 31):
            status = 'Open'
            actual_delivery = None
            on_time = None
        else:
            status = 'In Transit'
            actual_delivery = None
            on_time = None
        
        # Generate PO line items (1-6 different products)
        vendor_products = products_df[products_df['vendor'] == vendor]
        max_lines = max(2, min(6, len(vendor_products) + 1))
        num_lines = np.random.randint(1, max_lines)
        selected_products = vendor_products.sample(min(num_lines, len(vendor_products)))
        
        # Calculate PO totals
        total_cost = 0
        total_units = 0
        for _, prod in selected_products.iterrows():
            qty = np.random.randint(10, 100)
            total_units += qty
            total_cost += qty * prod['cost']
        
        po_records.append({
            'po_number': f'PO-2025-{i+1:04d}',
            'vendor': vendor,
            'po_date': po_date,
            'expected_delivery': expected_delivery,
            'actual_delivery': actual_delivery,
            'status': status,
            'on_time': on_time,
            'total_units': total_units,
            'total_cost': round(total_cost, 2),
            'num_line_items': len(selected_products),
            'lead_time_days': vendor_info['lead_time_days'],
            'delivery_variance_days': delivery_variance if status == 'Received' else None,
        })
    
    return pd.DataFrame(po_records)
