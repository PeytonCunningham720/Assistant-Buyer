"""
=============================================================================
RETAIL BUYING & ALLOCATION ANALYSIS DASHBOARD
Movement Climbing Gyms - Assistant Buyer Portfolio Project
=============================================================================

Author: Peyton Cunningham
Purpose: Demonstrate retail buying, allocation, and inventory analysis skills
         relevant to the Assistant Buyer - Gear & Allocation role at Movement.

This script generates synthetic retail data for Movement's 30+ gym locations,
performs analysis across three key areas (Inventory & Allocation, Sales Performance,
and Vendor Management), and produces professional visualizations.

All data is synthetic/fake - no real Movement data was used.
=============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

# --- Professional Typography & Style Setup ---
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Helvetica', 'Arial'],
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.labelsize': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#CCCCCC',
    'grid.color': '#EEEEEE',
    'grid.linewidth': 0.6,
})
sns.set_style("whitegrid")

# --- Movement-Inspired Professional Color Palette ---
COLORS = {
    'primary':    '#1B2A4A',   # Deep navy
    'secondary':  '#D94F4F',   # Warm red (Movement)
    'accent':     '#2E86AB',   # Steel blue
    'success':    '#28A745',   # Confident green
    'warning':    '#F5A623',   # Warm amber
    'danger':     '#DC3545',   # Alert red
    'light':      '#F4F6F9',   # Soft gray bg
    'purple':     '#7B61B8',   # Muted purple
    'teal':       '#17A89B',   # Rich teal
    'text':       '#2D3436',   # Near-black text
    'text_light': '#6C757D',   # Gray secondary text
    'border':     '#DEE2E6',   # Subtle border
    'card_bg':    '#FFFFFF',   # Card background
    'card_shadow': '#D1D9E6',  # Shadow color
}

# Gradient-style palettes for charts
CATEGORY_PALETTE = ['#2E86AB', '#D94F4F', '#28A745', '#F5A623',
                    '#7B61B8', '#17A89B', '#E07C4F', '#5B8C5A', '#3D5A80']

# =============================================================================
# SECTION 1: DATA GENERATION
# =============================================================================

GYM_LOCATIONS = [
    {'gym_id': 'MOV-001', 'gym_name': 'Movement Baker', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-002', 'gym_name': 'Movement RiNo', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-003', 'gym_name': 'Movement Englewood', 'city': 'Englewood', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-004', 'gym_name': 'Movement Golden', 'city': 'Golden', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-005', 'gym_name': 'Movement Boulder', 'city': 'Boulder', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-006', 'gym_name': 'Movement Fountain', 'city': 'Colorado Springs', 'state': 'CO', 'region': 'Colorado', 'size': 'Small'},
    {'gym_id': 'MOV-007', 'gym_name': 'Movement Plano', 'city': 'Plano', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-008', 'gym_name': 'Movement Austin', 'city': 'Austin', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-009', 'gym_name': 'Movement Houston', 'city': 'Houston', 'state': 'TX', 'region': 'Texas', 'size': 'Medium'},
    {'gym_id': 'MOV-010', 'gym_name': 'Movement San Francisco', 'city': 'San Francisco', 'state': 'CA', 'region': 'California', 'size': 'Large'},
    {'gym_id': 'MOV-011', 'gym_name': 'Movement Sunnyvale', 'city': 'Sunnyvale', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    {'gym_id': 'MOV-012', 'gym_name': 'Movement Oakland', 'city': 'Oakland', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    {'gym_id': 'MOV-013', 'gym_name': 'Movement Hampden', 'city': 'Baltimore', 'state': 'MD', 'region': 'East Coast', 'size': 'Large'},
    {'gym_id': 'MOV-014', 'gym_name': 'Movement Timonium', 'city': 'Timonium', 'state': 'MD', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-015', 'gym_name': 'Movement Columbia', 'city': 'Columbia', 'state': 'MD', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-016', 'gym_name': 'Movement Richmond', 'city': 'Richmond', 'state': 'VA', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-017', 'gym_name': 'Movement Virginia Beach', 'city': 'Virginia Beach', 'state': 'VA', 'region': 'East Coast', 'size': 'Small'},
    {'gym_id': 'MOV-018', 'gym_name': 'Movement Manassas', 'city': 'Manassas', 'state': 'VA', 'region': 'East Coast', 'size': 'Small'},
    {'gym_id': 'MOV-019', 'gym_name': 'Movement Gowanus', 'city': 'Brooklyn', 'state': 'NY', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-020', 'gym_name': 'Movement Harlem', 'city': 'New York', 'state': 'NY', 'region': 'Northeast', 'size': 'Medium'},
    {'gym_id': 'MOV-021', 'gym_name': 'Movement Portland', 'city': 'Portland', 'state': 'OR', 'region': 'Pacific NW', 'size': 'Large'},
    {'gym_id': 'MOV-022', 'gym_name': 'Movement Sellwood', 'city': 'Portland', 'state': 'OR', 'region': 'Pacific NW', 'size': 'Medium'},
    {'gym_id': 'MOV-023', 'gym_name': 'Movement Wrigleyville', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Large'},
    {'gym_id': 'MOV-024', 'gym_name': 'Movement Lincoln Park', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Medium'},
    {'gym_id': 'MOV-025', 'gym_name': 'Movement Philadelphia', 'city': 'Philadelphia', 'state': 'PA', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-026', 'gym_name': 'Movement King of Prussia', 'city': 'King of Prussia', 'state': 'PA', 'region': 'Northeast', 'size': 'Medium'},
]

gyms_df = pd.DataFrame(GYM_LOCATIONS)

VENDORS = {
    'La Sportiva': {'lead_time_days': 21, 'min_order': 500, 'reliability': 0.92},
    'Petzl': {'lead_time_days': 18, 'min_order': 400, 'reliability': 0.95},
    'Black Diamond': {'lead_time_days': 14, 'min_order': 300, 'reliability': 0.93},
    'Evolv': {'lead_time_days': 21, 'min_order': 400, 'reliability': 0.88},
    'Scarpa': {'lead_time_days': 25, 'min_order': 600, 'reliability': 0.90},
    'Metolius': {'lead_time_days': 10, 'min_order': 200, 'reliability': 0.94},
    'FrictionLabs': {'lead_time_days': 7, 'min_order': 150, 'reliability': 0.97},
    'Beal': {'lead_time_days': 20, 'min_order': 350, 'reliability': 0.91},
    'Mammut': {'lead_time_days': 22, 'min_order': 500, 'reliability': 0.89},
    'prAna': {'lead_time_days': 14, 'min_order': 250, 'reliability': 0.93},
}

PRODUCTS = [
    {'sku': 'SH-001', 'name': 'La Sportiva Tarantula', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'La Sportiva', 'cost': 45.00, 'retail': 89.95, 'size_run': True},
    {'sku': 'SH-002', 'name': 'La Sportiva Finale', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'La Sportiva', 'cost': 50.00, 'retail': 99.95, 'size_run': True},
    {'sku': 'SH-003', 'name': 'La Sportiva Solution', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'La Sportiva', 'cost': 95.00, 'retail': 189.95, 'size_run': True},
    {'sku': 'SH-004', 'name': 'Evolv Defy', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'Evolv', 'cost': 40.00, 'retail': 79.95, 'size_run': True},
    {'sku': 'SH-005', 'name': 'Evolv Shaman', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'Evolv', 'cost': 85.00, 'retail': 169.95, 'size_run': True},
    {'sku': 'SH-006', 'name': 'Scarpa Instinct VS', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'Scarpa', 'cost': 90.00, 'retail': 179.95, 'size_run': True},
    {'sku': 'SH-007', 'name': 'Black Diamond Momentum', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'Black Diamond', 'cost': 42.00, 'retail': 84.95, 'size_run': True},
    {'sku': 'HR-001', 'name': 'Petzl Corax', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Petzl', 'cost': 32.00, 'retail': 64.95, 'size_run': False},
    {'sku': 'HR-002', 'name': 'Black Diamond Momentum Harness', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Black Diamond', 'cost': 30.00, 'retail': 59.95, 'size_run': False},
    {'sku': 'HR-003', 'name': 'Petzl Sitta', 'category': 'Harnesses', 'subcategory': 'Performance', 'vendor': 'Petzl', 'cost': 70.00, 'retail': 139.95, 'size_run': False},
    {'sku': 'HR-004', 'name': 'Mammut Ophir 4 Slide', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Mammut', 'cost': 35.00, 'retail': 69.95, 'size_run': False},
    {'sku': 'CH-001', 'name': 'FrictionLabs Unicorn Dust', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'FrictionLabs', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CH-002', 'name': 'FrictionLabs Gorilla Grip', 'category': 'Chalk', 'subcategory': 'Chunky Chalk', 'vendor': 'FrictionLabs', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'CH-003', 'name': 'Metolius Super Chalk', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Metolius', 'cost': 4.00, 'retail': 9.95, 'size_run': False},
    {'sku': 'CH-004', 'name': 'Black Diamond White Gold', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Black Diamond', 'cost': 5.00, 'retail': 11.95, 'size_run': False},
    {'sku': 'BD-001', 'name': 'Petzl GriGri+', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Petzl', 'cost': 55.00, 'retail': 109.95, 'size_run': False},
    {'sku': 'BD-002', 'name': 'Black Diamond ATC-XP', 'category': 'Belay Devices', 'subcategory': 'Tubular', 'vendor': 'Black Diamond', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'BD-003', 'name': 'Mammut Smart 2.0', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Mammut', 'cost': 15.00, 'retail': 29.95, 'size_run': False},
    {'sku': 'CB-001', 'name': 'Petzl Attache', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Petzl', 'cost': 8.00, 'retail': 16.95, 'size_run': False},
    {'sku': 'CB-002', 'name': 'Black Diamond RockLock', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Black Diamond', 'cost': 7.00, 'retail': 14.95, 'size_run': False},
    {'sku': 'CB-003', 'name': 'Petzl Djinn Quickdraw', 'category': 'Carabiners', 'subcategory': 'Quickdraw', 'vendor': 'Petzl', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'CB-101', 'name': 'Metolius Competition Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Metolius', 'cost': 8.00, 'retail': 17.95, 'size_run': False},
    {'sku': 'CB-102', 'name': 'Mammut Gym Print Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Mammut', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CB-103', 'name': 'Black Diamond Mojo Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Black Diamond', 'cost': 9.00, 'retail': 19.95, 'size_run': False},
    {'sku': 'RP-001', 'name': 'Beal Stinger III 9.4mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Beal', 'cost': 95.00, 'retail': 189.95, 'size_run': False},
    {'sku': 'RP-002', 'name': 'Mammut Crag Classic 9.8mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Mammut', 'cost': 80.00, 'retail': 159.95, 'size_run': False},
    {'sku': 'AP-001', 'name': 'prAna Stretch Zion Pant', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 40.00, 'retail': 85.00, 'size_run': False},
    {'sku': 'AP-002', 'name': 'prAna Bridger Jean', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 35.00, 'retail': 75.00, 'size_run': False},
    {'sku': 'AP-003', 'name': 'Movement Logo Tee', 'category': 'Apparel', 'subcategory': 'Tops', 'vendor': 'prAna', 'cost': 8.00, 'retail': 25.00, 'size_run': False},
    {'sku': 'TR-001', 'name': 'Metolius Simulator 3D', 'category': 'Training', 'subcategory': 'Hangboard', 'vendor': 'Metolius', 'cost': 20.00, 'retail': 44.95, 'size_run': False},
    {'sku': 'TR-002', 'name': 'Metolius Rock Rings', 'category': 'Training', 'subcategory': 'Grip Trainer', 'vendor': 'Metolius', 'cost': 15.00, 'retail': 34.95, 'size_run': False},
]

products_df = pd.DataFrame(PRODUCTS)
products_df['margin_pct'] = ((products_df['retail'] - products_df['cost']) / products_df['retail'] * 100).round(1)
products_df['margin_dollars'] = (products_df['retail'] - products_df['cost']).round(2)


# =============================================================================
# DATA GENERATION FUNCTIONS (unchanged logic)
# =============================================================================

def generate_sales_data(gyms, products, months=12):
    sales_records = []
    size_multipliers = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.6}
    category_frequency = {
        'Chalk': 30, 'Chalk Bags': 8, 'Climbing Shoes': 12, 'Harnesses': 6,
        'Belay Devices': 4, 'Carabiners': 7, 'Apparel': 10, 'Ropes': 2, 'Training': 5,
    }
    seasonality = {
        1: 0.7, 2: 0.75, 3: 0.9, 4: 1.1, 5: 1.2, 6: 1.0,
        7: 0.85, 8: 0.9, 9: 1.15, 10: 1.25, 11: 1.0, 12: 1.1,
    }
    start_date = datetime(2025, 2, 1)
    for month_offset in range(months):
        current_month = (start_date.month + month_offset - 1) % 12 + 1
        current_year = start_date.year + (start_date.month + month_offset - 1) // 12
        season_factor = seasonality[current_month]
        for _, gym in gyms.iterrows():
            gym_size_mult = size_multipliers[gym['size']]
            for _, product in products.iterrows():
                cat_freq = category_frequency.get(product['category'], 5)
                expected_units = cat_freq * gym_size_mult * season_factor
                actual_units = max(0, int(np.random.poisson(expected_units)))
                if actual_units > 0:
                    days_in_month = 28 if current_month == 2 else (30 if current_month in [4, 6, 9, 11] else 31)
                    for _ in range(actual_units):
                        sale_day = np.random.randint(1, days_in_month + 1)
                        sale_date = datetime(current_year, current_month, min(sale_day, days_in_month))
                        discount_pct = 0
                        if np.random.random() < 0.10:
                            discount_pct = np.random.choice([10, 15, 20])
                        sale_price = product['retail'] * (1 - discount_pct / 100)
                        sales_records.append({
                            'sale_date': sale_date, 'gym_id': gym['gym_id'],
                            'gym_name': gym['gym_name'], 'region': gym['region'],
                            'sku': product['sku'], 'product_name': product['name'],
                            'category': product['category'], 'vendor': product['vendor'],
                            'units_sold': 1, 'retail_price': product['retail'],
                            'sale_price': round(sale_price, 2), 'cost': product['cost'],
                            'discount_pct': discount_pct,
                        })
    sales_df = pd.DataFrame(sales_records)
    sales_df['gross_margin'] = (sales_df['sale_price'] - sales_df['cost']).round(2)
    sales_df['margin_pct'] = ((sales_df['gross_margin'] / sales_df['sale_price']) * 100).round(1)
    return sales_df


def generate_inventory_data(gyms, products):
    inventory_records = []
    size_capacity = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.7}
    for _, gym in gyms.iterrows():
        cap = size_capacity[gym['size']]
        for _, product in products.iterrows():
            if product['category'] == 'Chalk':
                par_level = int(25 * cap)
            elif product['category'] in ['Climbing Shoes', 'Apparel']:
                par_level = int(10 * cap)
            elif product['category'] in ['Harnesses', 'Chalk Bags']:
                par_level = int(8 * cap)
            else:
                par_level = int(5 * cap)
            on_hand = max(0, int(np.random.normal(par_level * 0.7, par_level * 0.3)))
            avg_weekly_sales = max(0.5, np.random.normal(par_level * 0.15, par_level * 0.05))
            weeks_of_supply = round(on_hand / avg_weekly_sales, 1) if avg_weekly_sales > 0 else 0
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
            days_since_receipt = np.random.randint(1, 60)
            inventory_records.append({
                'gym_id': gym['gym_id'], 'gym_name': gym['gym_name'],
                'region': gym['region'], 'gym_size': gym['size'],
                'sku': product['sku'], 'product_name': product['name'],
                'category': product['category'], 'vendor': product['vendor'],
                'par_level': par_level, 'on_hand': on_hand,
                'avg_weekly_sales': round(avg_weekly_sales, 1),
                'weeks_of_supply': weeks_of_supply, 'stock_status': stock_status,
                'cost': product['cost'], 'retail': product['retail'],
                'inventory_value_cost': round(on_hand * product['cost'], 2),
                'inventory_value_retail': round(on_hand * product['retail'], 2),
                'days_since_last_receipt': days_since_receipt,
            })
    return pd.DataFrame(inventory_records)


def generate_po_data(products, num_pos=120):
    po_records = []
    vendors_list = list(VENDORS.keys())
    for i in range(num_pos):
        vendor = np.random.choice(vendors_list)
        vendor_info = VENDORS[vendor]
        days_ago = np.random.randint(1, 365)
        po_date = datetime(2025, 2, 1) + timedelta(days=365 - days_ago)
        expected_delivery = po_date + timedelta(days=vendor_info['lead_time_days'])
        if np.random.random() < vendor_info['reliability']:
            delivery_variance = np.random.randint(-3, 2)
        else:
            delivery_variance = np.random.randint(3, 15)
        actual_delivery = expected_delivery + timedelta(days=delivery_variance)
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
        vendor_products = products_df[products_df['vendor'] == vendor]
        max_lines = max(2, min(6, len(vendor_products) + 1))
        num_lines = np.random.randint(1, max_lines)
        selected_products = vendor_products.sample(min(num_lines, len(vendor_products)))
        total_cost = 0
        total_units = 0
        for _, prod in selected_products.iterrows():
            qty = np.random.randint(10, 100)
            total_units += qty
            total_cost += qty * prod['cost']
        po_records.append({
            'po_number': f'PO-2025-{i+1:04d}', 'vendor': vendor,
            'po_date': po_date, 'expected_delivery': expected_delivery,
            'actual_delivery': actual_delivery, 'status': status,
            'on_time': on_time, 'total_units': total_units,
            'total_cost': round(total_cost, 2),
            'num_line_items': len(selected_products),
            'lead_time_days': vendor_info['lead_time_days'],
            'delivery_variance_days': delivery_variance if status == 'Received' else None,
        })
    return pd.DataFrame(po_records)


# =============================================================================
# SECTION 2: GENERATE ALL DATA
# =============================================================================
print("=" * 70)
print("RETAIL BUYING & ALLOCATION ANALYSIS DASHBOARD")
print("Movement Climbing Gyms")
print("=" * 70)
print("\n📦 Generating synthetic retail data...")

sales_df = generate_sales_data(gyms_df, products_df)
inventory_df = generate_inventory_data(gyms_df, products_df)
po_df = generate_po_data(products_df)

print(f"   ✅ {len(sales_df):,} sales transactions generated")
print(f"   ✅ {len(inventory_df):,} inventory records generated")
print(f"   ✅ {len(po_df):,} purchase orders generated")
print(f"   ✅ {len(products_df)} SKUs across {len(VENDORS)} vendors")
print(f"   ✅ {len(gyms_df)} gym locations")

sales_df.to_csv(os.path.join(DATA_DIR, 'sales_data.csv'), index=False)
inventory_df.to_csv(os.path.join(DATA_DIR, 'inventory_data.csv'), index=False)
po_df.to_csv(os.path.join(DATA_DIR, 'purchase_orders.csv'), index=False)
products_df.to_csv(os.path.join(DATA_DIR, 'product_catalog.csv'), index=False)
gyms_df.to_csv(os.path.join(DATA_DIR, 'gym_locations.csv'), index=False)
print("\n💾 Raw data exported to output/data/")


# =============================================================================
# SECTION 3: ANALYSIS & VISUALIZATIONS
# =============================================================================
print("\n📊 Running analyses and generating visualizations...\n")


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Draw a KPI card with rounded rect, icon, and optional sparkline
# ─────────────────────────────────────────────────────────────────────────────

def draw_kpi_card(ax, x, y, w, h, label, value_text, subtitle='',
                  accent_color=COLORS['accent'], icon_text='',
                  sparkline_data=None, value_fontsize=30):
    """
    Draw a polished KPI card on a matplotlib Axes.
    Includes a rounded-rect background, large value, subtitle, and optional sparkline.
    """
    # Card background — rounded rectangle with soft shadow
    shadow = FancyBboxPatch((x + 0.003, y - 0.006), w, h,
                            boxstyle="round,pad=0.012", linewidth=0,
                            facecolor='#D1D9E6', alpha=0.45, zorder=0,
                            transform=ax.transAxes)
    ax.add_patch(shadow)

    card = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.012", linewidth=0.8,
                          edgecolor=COLORS['border'], facecolor='white',
                          zorder=1, transform=ax.transAxes)
    ax.add_patch(card)

    # Accent strip on the left edge
    strip = FancyBboxPatch((x, y), 0.008, h,
                           boxstyle="round,pad=0.004", linewidth=0,
                           facecolor=accent_color, zorder=2,
                           transform=ax.transAxes)
    ax.add_patch(strip)

    cx = x + w / 2  # center-x of card

    # Icon / emoji
    if icon_text:
        ax.text(cx, y + h * 0.87, icon_text, ha='center', va='center',
                fontsize=16, transform=ax.transAxes, zorder=3)

    # Large value
    ax.text(cx, y + h * 0.55, value_text, ha='center', va='center',
            fontsize=value_fontsize, fontweight='bold', color=COLORS['primary'],
            transform=ax.transAxes, zorder=3)

    # Label
    ax.text(cx, y + h * 0.30, label, ha='center', va='center',
            fontsize=9.5, color=COLORS['text_light'], fontweight='medium',
            transform=ax.transAxes, zorder=3)

    # Subtitle
    if subtitle:
        ax.text(cx, y + h * 0.12, subtitle, ha='center', va='center',
                fontsize=8, color=accent_color, fontweight='medium',
                transform=ax.transAxes, zorder=3)


def style_barh(ax, title, xlabel='', show_grid=True):
    """Apply consistent professional styling to horizontal bar charts."""
    ax.set_title(title, fontsize=11, fontweight='bold', color=COLORS['text'],
                 pad=10, loc='left')
    ax.set_xlabel(xlabel, fontsize=9, color=COLORS['text_light'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['border'])
    ax.spines['bottom'].set_color(COLORS['border'])
    ax.tick_params(axis='both', colors=COLORS['text_light'], labelsize=8)
    if show_grid:
        ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.5)
        ax.yaxis.grid(False)
    ax.set_axisbelow(True)


# ─────────────────────────────────────────────────────────────────────────────
# CHART 00: EXECUTIVE DASHBOARD  (★ REDESIGNED)
# ─────────────────────────────────────────────────────────────────────────────

def create_executive_dashboard():
    """
    Professional executive dashboard with KPI cards, sparklines,
    and polished chart panels.
    """
    fig = plt.figure(figsize=(20, 13), facecolor=COLORS['light'])

    # ── Title bar ──
    fig.text(0.03, 0.965, 'MOVEMENT RETAIL', fontsize=22, fontweight='bold',
             color=COLORS['primary'], va='top')
    fig.text(0.03, 0.940, 'Executive Dashboard  ·  12-Month Performance Summary',
             fontsize=10, color=COLORS['text_light'], va='top')
    fig.text(0.97, 0.965, 'FY 2025', fontsize=11, fontweight='bold',
             color=COLORS['text_light'], va='top', ha='right')

    # Thin accent line under title
    line = plt.Line2D([0.03, 0.97], [0.925, 0.925], transform=fig.transFigure,
                      color=COLORS['secondary'], linewidth=2.5, zorder=10)
    fig.add_artist(line)

    # ━━━━━━ TOP ROW: KPI CARDS ━━━━━━
    # Use a single invisible Axes spanning the top for card placement
    ax_kpi = fig.add_axes([0.0, 0.72, 1.0, 0.20])  # x, y, w, h in figure coords
    ax_kpi.set_xlim(0, 1)
    ax_kpi.set_ylim(0, 1)
    ax_kpi.axis('off')

    # --- Compute KPIs ---
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

    total_units = sales_df['units_sold'].sum()
    avg_basket = total_revenue / len(sales_df.groupby(['sale_date', 'gym_id']))

    received_pos = po_df[po_df['status'] == 'Received']
    overall_otd = received_pos['on_time'].mean() * 100 if len(received_pos) > 0 else 0

    # Card positions — 5 cards evenly spaced
    card_w = 0.165
    card_h = 0.85
    gap = 0.02
    start_x = 0.03
    cards = [
        {
            'label': 'Total Revenue', 'value': f'${total_revenue/1e6:.2f}M',
            'subtitle': f'Gross Margin {margin_pct:.1f}%', 'icon': '💰',
            'color': COLORS['accent'],
        },
        {
            'label': 'Gross Margin', 'value': f'${total_margin/1e6:.2f}M',
            'subtitle': f'{margin_pct:.1f}% of Revenue', 'icon': '📈',
            'color': COLORS['success'],
        },
        {
            'label': 'In-Stock Rate', 'value': f'{in_stock_rate:.1f}%',
            'subtitle': f'{oos_count} SKU-locations OOS', 'icon': '📦',
            'color': COLORS['success'] if in_stock_rate >= 85 else COLORS['warning'],
        },
        {
            'label': 'Inventory at Cost', 'value': f'${total_inv_cost/1e6:.2f}M',
            'subtitle': f'Retail: ${total_inv_retail/1e6:.2f}M', 'icon': '🏬',
            'color': COLORS['purple'],
        },
        {
            'label': 'Vendor On-Time %', 'value': f'{overall_otd:.1f}%',
            'subtitle': f'{len(po_df)} POs Tracked', 'icon': '🚚',
            'color': COLORS['teal'] if overall_otd >= 90 else COLORS['warning'],
        },
    ]

    for i, c in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        draw_kpi_card(ax_kpi, cx, 0.08, card_w, card_h,
                      label=c['label'], value_text=c['value'],
                      subtitle=c['subtitle'], accent_color=c['color'],
                      icon_text=c['icon'])

    # ━━━━━━ BOTTOM ROW: THREE CHART PANELS ━━━━━━

    # --- Panel 1: Revenue by Category (horizontal bar) ---
    ax1 = fig.add_axes([0.05, 0.07, 0.27, 0.58])
    ax1.set_facecolor('white')

    cat_sales = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=True)
    bars = ax1.barh(range(len(cat_sales)), cat_sales.values, height=0.65,
                    color=[COLORS['secondary'] if i == len(cat_sales) - 1
                           else COLORS['accent'] for i in range(len(cat_sales))],
                    edgecolor='none', zorder=3)
    ax1.set_yticks(range(len(cat_sales)))
    ax1.set_yticklabels(cat_sales.index, fontsize=8)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    style_barh(ax1, 'Revenue by Category', xlabel='')

    # Data labels on bars
    for bar_item, val in zip(bars, cat_sales.values):
        ax1.text(val + cat_sales.max() * 0.02, bar_item.get_y() + bar_item.get_height() / 2,
                 f'${val/1000:.0f}K', va='center', fontsize=7.5,
                 color=COLORS['text_light'], fontweight='medium')

    # --- Panel 2: Monthly Revenue Trend (area chart) ---
    ax2 = fig.add_axes([0.38, 0.07, 0.27, 0.58])
    ax2.set_facecolor('white')

    sales_df['month'] = sales_df['sale_date'].dt.to_period('M')
    monthly_rev = sales_df.groupby('month')['sale_price'].sum()
    months_str = [str(m) for m in monthly_rev.index]
    x_pos = range(len(monthly_rev))

    # Area fill
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
                 arrowprops=dict(arrowstyle='->', color=COLORS['secondary'],
                                 lw=1.2), zorder=5)

    ax2.set_xticks(list(x_pos))
    ax2.set_xticklabels([m[-3:] for m in months_str], rotation=45, fontsize=7.5)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax2.set_title('Monthly Revenue Trend', fontsize=11, fontweight='bold',
                  color=COLORS['text'], pad=10, loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(COLORS['border'])
    ax2.spines['bottom'].set_color(COLORS['border'])
    ax2.tick_params(colors=COLORS['text_light'], labelsize=8)
    ax2.yaxis.grid(True, color='#EEEEEE', linewidth=0.5)
    ax2.set_axisbelow(True)

    # --- Panel 3: Top 8 Gyms by Revenue ---
    ax3 = fig.add_axes([0.71, 0.07, 0.27, 0.58])
    ax3.set_facecolor('white')

    gym_sales = sales_df.groupby('gym_name')['sale_price'].sum().nlargest(8).sort_values(ascending=True)
    bars3 = ax3.barh(range(len(gym_sales)), gym_sales.values, height=0.65,
                     color=COLORS['teal'], edgecolor='none', zorder=3, alpha=0.85)
    ax3.set_yticks(range(len(gym_sales)))
    ax3.set_yticklabels([n.replace('Movement ', '') for n in gym_sales.index], fontsize=8)
    ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    style_barh(ax3, 'Top 8 Gyms by Revenue', xlabel='')

    for bar_item, val in zip(bars3, gym_sales.values):
        ax3.text(val + gym_sales.max() * 0.02, bar_item.get_y() + bar_item.get_height() / 2,
                 f'${val/1000:.0f}K', va='center', fontsize=7.5,
                 color=COLORS['text_light'], fontweight='medium')

    # ── Footer ──
    fig.text(0.03, 0.015,
             'Data is synthetic — generated for portfolio demonstration purposes only. No real Movement business data was used.',
             fontsize=7.5, color=COLORS['text_light'], style='italic')
    fig.text(0.97, 0.015, 'Peyton Cunningham  ·  Movement Climbing Gyms',
             fontsize=7.5, color=COLORS['text_light'], ha='right', fontweight='medium')

    plt.savefig(os.path.join(CHARTS_DIR, '00_executive_dashboard.png'),
                bbox_inches='tight', facecolor=COLORS['light'], dpi=200)
    plt.close()
    print("   ✅ Chart 00: Executive Dashboard (redesigned)")

create_executive_dashboard()


# ─────────────────────────────────────────────────────────────────────────────
# REMAINING CHARTS (01-12) — preserved with minor style improvements
# ─────────────────────────────────────────────────────────────────────────────

def create_sales_by_category():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Sales Performance by Product Category', fontsize=16, fontweight='bold', color=COLORS['text'])
    cat_revenue = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=False)
    colors_bar = [COLORS['secondary'] if i == 0 else COLORS['accent'] for i in range(len(cat_revenue))]
    cat_revenue.plot(kind='bar', ax=ax1, color=colors_bar, edgecolor='none')
    ax1.set_title('Revenue by Category', fontweight='bold', color=COLORS['text'])
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    cat_units = sales_df.groupby('category')['units_sold'].sum().sort_values(ascending=False)
    colors_bar2 = [COLORS['secondary'] if i == 0 else COLORS['teal'] for i in range(len(cat_units))]
    cat_units.plot(kind='bar', ax=ax2, color=colors_bar2, edgecolor='none')
    ax2.set_title('Units Sold by Category', fontweight='bold', color=COLORS['text'])
    ax2.set_ylabel('Units Sold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    ax2.tick_params(axis='x', rotation=45)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '01_sales_by_category.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 01: Sales by Category")

create_sales_by_category()


def create_sales_by_region():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Regional Sales Performance', fontsize=16, fontweight='bold', color=COLORS['text'])
    region_rev = sales_df.groupby('region')['sale_price'].sum().sort_values(ascending=False)
    region_rev.plot(kind='bar', ax=ax1, color=COLORS['primary'], edgecolor='none')
    ax1.set_title('Revenue by Region', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    region_avg = sales_df.groupby('region')['sale_price'].mean().sort_values(ascending=False)
    region_avg.plot(kind='bar', ax=ax2, color=COLORS['purple'], edgecolor='none')
    ax2.set_title('Average Transaction Value by Region', fontweight='bold')
    ax2.set_ylabel('Avg Sale Price ($)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '02_sales_by_region.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 02: Sales by Region")

create_sales_by_region()


def create_margin_analysis():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Gross Margin Analysis', fontsize=16, fontweight='bold', color=COLORS['text'])
    cat_margin = sales_df.groupby('category').agg(total_revenue=('sale_price', 'sum'), total_cost=('cost', 'sum'))
    cat_margin['margin_pct'] = ((cat_margin['total_revenue'] - cat_margin['total_cost']) / cat_margin['total_revenue'] * 100).round(1)
    cat_margin = cat_margin.sort_values('margin_pct', ascending=True)
    colors_margin = [COLORS['danger'] if v < 40 else COLORS['warning'] if v < 50 else COLORS['success'] for v in cat_margin['margin_pct'].values]
    cat_margin['margin_pct'].plot(kind='barh', ax=ax1, color=colors_margin, edgecolor='none')
    ax1.set_title('Gross Margin % by Category', fontweight='bold')
    ax1.set_xlabel('Margin %')
    ax1.axvline(x=50, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='50% Target')
    ax1.legend()
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    vendor_margin = sales_df.groupby('vendor').agg(total_revenue=('sale_price', 'sum'), total_cost=('cost', 'sum'))
    vendor_margin['margin_dollars'] = vendor_margin['total_revenue'] - vendor_margin['total_cost']
    vendor_margin = vendor_margin.sort_values('margin_dollars', ascending=True)
    vendor_margin['margin_dollars'].plot(kind='barh', ax=ax2, color=COLORS['accent'], edgecolor='none')
    ax2.set_title('Gross Margin $ by Vendor', fontweight='bold')
    ax2.set_xlabel('Margin ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '03_margin_analysis.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 03: Margin Analysis")

create_margin_analysis()


def create_monthly_trend():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), facecolor='white')
    fig.suptitle('Monthly Sales Trends', fontsize=16, fontweight='bold', color=COLORS['text'])
    sales_df['month'] = sales_df['sale_date'].dt.to_period('M')
    monthly_rev = sales_df.groupby('month')['sale_price'].sum()
    monthly_rev.index = monthly_rev.index.astype(str)
    ax1.fill_between(range(len(monthly_rev)), monthly_rev.values, alpha=0.15, color=COLORS['accent'])
    ax1.plot(range(len(monthly_rev)), monthly_rev.values, color=COLORS['accent'], linewidth=2.2, marker='o',
             markersize=5, markerfacecolor='white', markeredgecolor=COLORS['accent'], markeredgewidth=1.8)
    ax1.set_title('Total Monthly Revenue', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.set_xticks(range(len(monthly_rev)))
    ax1.set_xticklabels(monthly_rev.index, rotation=45)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    monthly_cat = sales_df.groupby(['month', 'category'])['units_sold'].sum().unstack(fill_value=0)
    monthly_cat.index = monthly_cat.index.astype(str)
    monthly_cat.plot(kind='bar', stacked=True, ax=ax2, colormap='Set2', edgecolor='none')
    ax2.set_title('Monthly Units Sold by Category', fontweight='bold')
    ax2.set_ylabel('Units Sold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax2.tick_params(axis='x', rotation=45)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '04_monthly_trends.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 04: Monthly Sales Trends")

create_monthly_trend()


def create_instock_by_gym():
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')
    gym_instock = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    ).sort_values(ascending=True)
    colors_is = [COLORS['danger'] if v < 80 else COLORS['warning'] if v < 90 else COLORS['success'] for v in gym_instock.values]
    gym_instock.plot(kind='barh', ax=ax, color=colors_is, edgecolor='none')
    ax.set_title('In-Stock Rate by Gym Location', fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('In-Stock Rate (%)')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=1, alpha=0.7, label='90% Target')
    for i, (v, name) in enumerate(zip(gym_instock.values, gym_instock.index)):
        ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=8)
    legend_elements = [
        mpatches.Patch(color=COLORS['success'], label='≥ 90% (Target)'),
        mpatches.Patch(color=COLORS['warning'], label='80-90% (Needs Attention)'),
        mpatches.Patch(color=COLORS['danger'], label='< 80% (Critical)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '05_instock_by_gym.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 05: In-Stock Rate by Gym")

create_instock_by_gym()


def create_inventory_status():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Inventory Health Overview', fontsize=16, fontweight='bold', color=COLORS['text'])
    status_counts = inventory_df['stock_status'].value_counts()
    status_colors = {
        'In Stock': COLORS['success'], 'Low': COLORS['warning'],
        'Critical Low': '#E67E22', 'Out of Stock': COLORS['danger'],
        'Overstock': COLORS['accent'],
    }
    colors_pie = [status_colors.get(s, 'gray') for s in status_counts.index]
    ax1.pie(status_counts.values, labels=status_counts.index, colors=colors_pie,
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    ax1.set_title('Stock Status Distribution', fontweight='bold')
    wos = inventory_df[inventory_df['on_hand'] > 0]['weeks_of_supply']
    ax2.hist(wos, bins=30, color=COLORS['primary'], edgecolor='white', alpha=0.8)
    ax2.axvline(x=4, color=COLORS['success'], linestyle='--', linewidth=2, label='Min Target (4 wks)')
    ax2.axvline(x=12, color=COLORS['warning'], linestyle='--', linewidth=2, label='Max Target (12 wks)')
    ax2.set_title('Weeks of Supply Distribution', fontweight='bold')
    ax2.set_xlabel('Weeks of Supply')
    ax2.set_ylabel('Number of SKU-Locations')
    ax2.legend()
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '06_inventory_status.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 06: Inventory Status Overview")

create_inventory_status()


def create_aged_inventory():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Aged & Overstock Inventory Analysis', fontsize=16, fontweight='bold', color=COLORS['text'])
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
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '07_aged_inventory.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 07: Aged Inventory Analysis")

create_aged_inventory()


def create_vendor_scorecard():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
    fig.suptitle('Vendor Performance Scorecard', fontsize=16, fontweight='bold', color=COLORS['text'])
    received_pos = po_df[po_df['status'] == 'Received']
    ax = axes[0, 0]
    otd = received_pos.groupby('vendor')['on_time'].mean().sort_values(ascending=True) * 100
    colors_otd = [COLORS['danger'] if v < 85 else COLORS['warning'] if v < 92 else COLORS['success'] for v in otd.values]
    otd.plot(kind='barh', ax=ax, color=colors_otd, edgecolor='none')
    ax.set_title('On-Time Delivery Rate (%)', fontweight='bold')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel('On-Time %')
    ax.set_xlim(0, 105)
    ax = axes[0, 1]
    avg_lead = received_pos.groupby('vendor')['lead_time_days'].mean().sort_values(ascending=True)
    avg_lead.plot(kind='barh', ax=ax, color=COLORS['primary'], edgecolor='none')
    ax.set_title('Average Lead Time (Days)', fontweight='bold')
    ax.set_xlabel('Days')
    ax = axes[1, 0]
    vendor_spend = po_df.groupby('vendor')['total_cost'].sum().sort_values(ascending=True)
    vendor_spend.plot(kind='barh', ax=ax, color=COLORS['accent'], edgecolor='none')
    ax.set_title('Total PO Spend by Vendor', fontweight='bold')
    ax.set_xlabel('Total Cost ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax = axes[1, 1]
    variance = received_pos.groupby('vendor')['delivery_variance_days'].mean().sort_values()
    colors_var = [COLORS['success'] if v <= 0 else COLORS['warning'] if v <= 3 else COLORS['danger'] for v in variance.values]
    variance.plot(kind='barh', ax=ax, color=colors_var, edgecolor='none')
    ax.set_title('Average Delivery Variance (Days)', fontweight='bold')
    ax.set_xlabel('Days (negative = early, positive = late)')
    ax.axvline(x=0, color='black', linewidth=1)
    for ax_item in axes.flat:
        ax_item.spines['top'].set_visible(False)
        ax_item.spines['right'].set_visible(False)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '08_vendor_scorecard.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 08: Vendor Performance Scorecard")

create_vendor_scorecard()


def create_top_bottom_sellers():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Product Performance: Top & Bottom Sellers', fontsize=16, fontweight='bold', color=COLORS['text'])
    product_perf = sales_df.groupby('product_name').agg(
        total_revenue=('sale_price', 'sum'), total_units=('units_sold', 'sum'),
    ).sort_values('total_revenue', ascending=False)
    top10 = product_perf.head(10).sort_values('total_revenue', ascending=True)
    top10['total_revenue'].plot(kind='barh', ax=ax1, color=COLORS['success'], edgecolor='none')
    ax1.set_title('Top 10 Products by Revenue', fontweight='bold')
    ax1.set_xlabel('Revenue ($)')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    bottom10 = product_perf.tail(10).sort_values('total_revenue', ascending=True)
    bottom10['total_revenue'].plot(kind='barh', ax=ax2, color=COLORS['danger'], edgecolor='none')
    ax2.set_title('Bottom 10 Products by Revenue\n(Markdown / discontinue candidates)', fontweight='bold', fontsize=10)
    ax2.set_xlabel('Revenue ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '09_top_bottom_sellers.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 09: Top & Bottom Sellers")

create_top_bottom_sellers()


def create_allocation_analysis():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    fig.suptitle('Allocation Efficiency Analysis', fontsize=16, fontweight='bold', color=COLORS['text'])
    gym_inv = inventory_df.groupby('gym_name')['inventory_value_cost'].sum()
    gym_rev = sales_df.groupby('gym_name')['sale_price'].sum()
    comparison = pd.DataFrame({'inventory': gym_inv, 'revenue': gym_rev}).dropna()
    comparison['inv_to_sales_ratio'] = (comparison['inventory'] / comparison['revenue'] * 100).round(1)
    comparison = comparison.sort_values('inv_to_sales_ratio', ascending=True)
    colors_alloc = [COLORS['danger'] if v > 25 else COLORS['warning'] if v > 18 else COLORS['success'] for v in comparison['inv_to_sales_ratio'].values]
    comparison['inv_to_sales_ratio'].plot(kind='barh', ax=ax1, color=colors_alloc, edgecolor='none')
    ax1.set_title('Inventory-to-Sales Ratio by Gym', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Inventory as % of Revenue')
    region_status = inventory_df.groupby(['region', 'stock_status']).size().unstack(fill_value=0)
    region_status_pct = region_status.div(region_status.sum(axis=1), axis=0) * 100
    status_order = ['Out of Stock', 'Critical Low', 'Low', 'In Stock', 'Overstock']
    available_statuses = [s for s in status_order if s in region_status_pct.columns]
    status_colors_map = {
        'Out of Stock': COLORS['danger'], 'Critical Low': '#E67E22',
        'Low': COLORS['warning'], 'In Stock': COLORS['success'], 'Overstock': COLORS['accent'],
    }
    region_status_pct[available_statuses].plot(
        kind='barh', stacked=True, ax=ax2,
        color=[status_colors_map[s] for s in available_statuses], edgecolor='none'
    )
    ax2.set_title('Stock Status by Region (%)', fontweight='bold')
    ax2.set_xlabel('Percentage')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '10_allocation_analysis.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 10: Allocation Analysis")

create_allocation_analysis()


def create_po_pipeline():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    fig.suptitle('Purchase Order Pipeline', fontsize=16, fontweight='bold', color=COLORS['text'])
    po_status = po_df['status'].value_counts()
    status_colors_po = {'Received': COLORS['success'], 'In Transit': COLORS['warning'], 'Open': COLORS['accent']}
    colors_po = [status_colors_po.get(s, 'gray') for s in po_status.index]
    ax1.pie(po_status.values, labels=po_status.index, colors=colors_po,
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
    ax1.set_title('PO Status Breakdown', fontweight='bold')
    po_df['po_month'] = pd.to_datetime(po_df['po_date']).dt.to_period('M')
    monthly_pos = po_df.groupby('po_month').agg(num_pos=('po_number', 'count'), total_value=('total_cost', 'sum'))
    monthly_pos.index = monthly_pos.index.astype(str)
    ax2_twin = ax2.twinx()
    ax2.bar(range(len(monthly_pos)), monthly_pos['num_pos'], color=COLORS['accent'], alpha=0.7, label='# of POs', edgecolor='none')
    ax2_twin.plot(range(len(monthly_pos)), monthly_pos['total_value'], color=COLORS['secondary'], linewidth=2, marker='o', label='PO Value ($)')
    ax2.set_title('Monthly PO Volume & Value', fontweight='bold')
    ax2.set_ylabel('Number of POs')
    ax2_twin.set_ylabel('PO Value ($)')
    ax2_twin.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2.set_xticks(range(len(monthly_pos)))
    ax2.set_xticklabels(monthly_pos.index, rotation=45)
    ax2.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '11_po_pipeline.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 11: PO Pipeline")

create_po_pipeline()


def create_shoe_deep_dive():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='white')
    fig.suptitle('Category Deep-Dive: Climbing Shoes', fontsize=16, fontweight='bold', color=COLORS['text'])
    shoes_sales = sales_df[sales_df['category'] == 'Climbing Shoes'].copy()
    shoes_inv = inventory_df[inventory_df['category'] == 'Climbing Shoes']
    ax = axes[0, 0]
    shoe_rev = shoes_sales.groupby('product_name')['sale_price'].sum().sort_values(ascending=True)
    shoe_rev.plot(kind='barh', ax=ax, color=COLORS['accent'], edgecolor='none')
    ax.set_title('Revenue by Shoe Model', fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax = axes[0, 1]
    shoes_products = products_df[products_df['category'] == 'Climbing Shoes']
    shoes_with_sub = shoes_sales.merge(shoes_products[['sku', 'subcategory']], on='sku')
    sub_rev = shoes_with_sub.groupby('subcategory')['sale_price'].sum()
    sub_rev.plot(kind='pie', ax=ax, colors=[COLORS['accent'], COLORS['secondary']],
                 autopct='%1.1f%%', textprops={'fontsize': 12})
    ax.set_title('Beginner vs Advanced Shoe Sales', fontweight='bold')
    ax.set_ylabel('')
    ax = axes[1, 0]
    shoe_instock = shoes_inv.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    ).sort_values(ascending=True)
    colors_shoe = [COLORS['danger'] if v < 70 else COLORS['warning'] if v < 85 else COLORS['success'] for v in shoe_instock.values]
    shoe_instock.plot(kind='barh', ax=ax, color=colors_shoe, fontsize=7, edgecolor='none')
    ax.set_title('Shoe In-Stock Rate by Gym', fontweight='bold')
    ax.set_xlabel('In-Stock %')
    ax = axes[1, 1]
    shoes_sales['month'] = shoes_sales['sale_date'].dt.to_period('M')
    monthly_shoes = shoes_sales.groupby('month')['sale_price'].sum()
    monthly_shoes.index = monthly_shoes.index.astype(str)
    ax.fill_between(range(len(monthly_shoes)), monthly_shoes.values, alpha=0.15, color=COLORS['secondary'])
    ax.plot(range(len(monthly_shoes)), monthly_shoes.values, color=COLORS['secondary'], linewidth=2, marker='o',
            markersize=5, markerfacecolor='white', markeredgecolor=COLORS['secondary'], markeredgewidth=1.8)
    ax.set_title('Monthly Shoe Revenue Trend', fontweight='bold')
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.set_xticks(range(len(monthly_shoes)))
    ax.set_xticklabels(monthly_shoes.index, rotation=45)
    for ax_item in axes.flat:
        ax_item.spines['top'].set_visible(False)
        ax_item.spines['right'].set_visible(False)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '12_shoe_deep_dive.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 12: Climbing Shoe Deep-Dive")

create_shoe_deep_dive()


# =============================================================================
# SECTION 4: SUMMARY REPORT
# =============================================================================

def print_summary():
    print("\n" + "=" * 70)
    print("📋 SUMMARY OF KEY FINDINGS")
    print("=" * 70)
    total_rev = sales_df['sale_price'].sum()
    total_cost_sold = sales_df['cost'].sum()
    total_gm = total_rev - total_cost_sold
    print(f"\n💰 REVENUE & MARGIN")
    print(f"   Total Revenue (12 months):      ${total_rev:>12,.2f}")
    print(f"   Total Cost of Goods Sold:        ${total_cost_sold:>12,.2f}")
    print(f"   Gross Margin:                    ${total_gm:>12,.2f} ({total_gm/total_rev*100:.1f}%)")
    top_cat = sales_df.groupby('category')['sale_price'].sum().idxmax()
    top_cat_rev = sales_df.groupby('category')['sale_price'].sum().max()
    print(f"   Top Category:                    {top_cat} (${top_cat_rev:,.2f})")
    print(f"\n📦 INVENTORY HEALTH")
    total_inv = inventory_df['inventory_value_cost'].sum()
    in_stock = (inventory_df['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(inventory_df) * 100)
    oos = (inventory_df['stock_status'] == 'Out of Stock').sum()
    overstock = (inventory_df['stock_status'] == 'Overstock').sum()
    print(f"   Total Inventory Value (at cost): ${total_inv:>12,.2f}")
    print(f"   Overall In-Stock Rate:           {in_stock:>11.1f}%")
    print(f"   Out-of-Stock SKU-Locations:      {oos:>12}")
    print(f"   Overstock SKU-Locations:         {overstock:>12}")
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
    print(f"\n⚡ ACTIONABLE INSIGHTS")
    gym_is = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    )
    low_gyms = gym_is[gym_is < 80]
    if len(low_gyms) > 0:
        print(f"   🔴 {len(low_gyms)} gym(s) below 80% in-stock rate — prioritize in next allocation")
        for gym, rate in low_gyms.items():
            print(f"      → {gym}: {rate:.1f}%")
    overstock_value = inventory_df[inventory_df['stock_status'] == 'Overstock']['inventory_value_cost'].sum()
    if overstock_value > 0:
        print(f"   🟡 ${overstock_value:,.2f} in overstock inventory — review for markdowns or transfers")
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

print_summary()
