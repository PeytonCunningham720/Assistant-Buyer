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
# pandas: The core data manipulation library - similar to Excel but can handle
# much larger datasets and automate repetitive tasks
import pandas as pd

# numpy: Mathematical operations - used for generating realistic random data
# and performing calculations like averages, percentages, etc.
import numpy as np

# matplotlib & seaborn: Visualization libraries that create the charts
# matplotlib is the foundation, seaborn adds statistical chart types
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# os: Handles file paths so the script works on any computer
import os

# datetime/timedelta: For working with dates (order dates, delivery windows, etc.)
from datetime import datetime, timedelta

# warnings: Suppresses non-critical warnings to keep output clean
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================
# These settings control where output files are saved and ensure consistent results.

# Output directories - where charts and data exports will be saved
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')

# Create output directories if they don't exist
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Random seed for reproducibility - ensures the same "random" data is generated
# each time, so results are consistent for review
np.random.seed(42)

# Set the visual style for all charts - clean, professional look
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 10

# Movement brand-inspired color palette
COLORS = {
    'primary': '#2C3E50',      # Dark blue-gray
    'secondary': '#E74C3C',    # Movement red
    'accent': '#3498DB',       # Bright blue
    'success': '#27AE60',      # Green (in-stock)
    'warning': '#F39C12',      # Orange/amber (low stock)
    'danger': '#E74C3C',       # Red (out of stock)
    'light': '#ECF0F1',        # Light gray
    'purple': '#9B59B6',       # Purple accent
    'teal': '#1ABC9C',         # Teal accent
}

# =============================================================================
# SECTION 1: DATA GENERATION
# =============================================================================
"""
This section creates realistic synthetic data that mirrors what you'd see in
retail systems like Business Central and RGP. The data covers:
- 30+ gym locations with realistic geographic distribution
- Product catalog with gear categories (shoes, harnesses, chalk, etc.)
- Purchase orders with vendor information
- Sales transactions across all locations
- Inventory levels and allocation data

WHY SYNTHETIC DATA?
Using fake data lets me demonstrate analytical capabilities without
compromising any real business information. The patterns and distributions
are designed to be realistic based on my experience at Movement Golden.
"""

# -----------------------------------------------------------------------------
# 1.1 GYM LOCATIONS
# -----------------------------------------------------------------------------
# Movement's actual gym locations across the country, used to make the
# analysis feel realistic and relevant.

GYM_LOCATIONS = [
    # Colorado locations
    {'gym_id': 'MOV-001', 'gym_name': 'Movement Baker', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-002', 'gym_name': 'Movement RiNo', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-003', 'gym_name': 'Movement Englewood', 'city': 'Englewood', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-004', 'gym_name': 'Movement Golden', 'city': 'Golden', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-005', 'gym_name': 'Movement Boulder', 'city': 'Boulder', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-006', 'gym_name': 'Movement Fountain', 'city': 'Colorado Springs', 'state': 'CO', 'region': 'Colorado', 'size': 'Small'},
    # Texas locations
    {'gym_id': 'MOV-007', 'gym_name': 'Movement Plano', 'city': 'Plano', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-008', 'gym_name': 'Movement Austin', 'city': 'Austin', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-009', 'gym_name': 'Movement Houston', 'city': 'Houston', 'state': 'TX', 'region': 'Texas', 'size': 'Medium'},
    # California locations
    {'gym_id': 'MOV-010', 'gym_name': 'Movement San Francisco', 'city': 'San Francisco', 'state': 'CA', 'region': 'California', 'size': 'Large'},
    {'gym_id': 'MOV-011', 'gym_name': 'Movement Sunnyvale', 'city': 'Sunnyvale', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    {'gym_id': 'MOV-012', 'gym_name': 'Movement Oakland', 'city': 'Oakland', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    # East Coast locations
    {'gym_id': 'MOV-013', 'gym_name': 'Movement Hampden', 'city': 'Baltimore', 'state': 'MD', 'region': 'East Coast', 'size': 'Large'},
    {'gym_id': 'MOV-014', 'gym_name': 'Movement Timonium', 'city': 'Timonium', 'state': 'MD', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-015', 'gym_name': 'Movement Columbia', 'city': 'Columbia', 'state': 'MD', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-016', 'gym_name': 'Movement Richmond', 'city': 'Richmond', 'state': 'VA', 'region': 'East Coast', 'size': 'Medium'},
    {'gym_id': 'MOV-017', 'gym_name': 'Movement Virginia Beach', 'city': 'Virginia Beach', 'state': 'VA', 'region': 'East Coast', 'size': 'Small'},
    {'gym_id': 'MOV-018', 'gym_name': 'Movement Manassas', 'city': 'Manassas', 'state': 'VA', 'region': 'East Coast', 'size': 'Small'},
    # Mid-Atlantic / Northeast
    {'gym_id': 'MOV-019', 'gym_name': 'Movement Gowanus', 'city': 'Brooklyn', 'state': 'NY', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-020', 'gym_name': 'Movement Harlem', 'city': 'New York', 'state': 'NY', 'region': 'Northeast', 'size': 'Medium'},
    # Pacific Northwest
    {'gym_id': 'MOV-021', 'gym_name': 'Movement Portland', 'city': 'Portland', 'state': 'OR', 'region': 'Pacific NW', 'size': 'Large'},
    {'gym_id': 'MOV-022', 'gym_name': 'Movement Sellwood', 'city': 'Portland', 'state': 'OR', 'region': 'Pacific NW', 'size': 'Medium'},
    # Illinois
    {'gym_id': 'MOV-023', 'gym_name': 'Movement Wrigleyville', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Large'},
    {'gym_id': 'MOV-024', 'gym_name': 'Movement Lincoln Park', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Medium'},
    # Pennsylvania
    {'gym_id': 'MOV-025', 'gym_name': 'Movement Philadelphia', 'city': 'Philadelphia', 'state': 'PA', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-026', 'gym_name': 'Movement King of Prussia', 'city': 'King of Prussia', 'state': 'PA', 'region': 'Northeast', 'size': 'Medium'},
]

gyms_df = pd.DataFrame(GYM_LOCATIONS)

# -----------------------------------------------------------------------------
# 1.2 PRODUCT CATALOG
# -----------------------------------------------------------------------------
# Gear categories typical of a climbing gym pro shop. Each product has a
# vendor, cost, retail price, and category for analysis.

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
    # Climbing Shoes - highest margin category
    {'sku': 'SH-001', 'name': 'La Sportiva Tarantula', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'La Sportiva', 'cost': 45.00, 'retail': 89.95, 'size_run': True},
    {'sku': 'SH-002', 'name': 'La Sportiva Finale', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'La Sportiva', 'cost': 50.00, 'retail': 99.95, 'size_run': True},
    {'sku': 'SH-003', 'name': 'La Sportiva Solution', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'La Sportiva', 'cost': 95.00, 'retail': 189.95, 'size_run': True},
    {'sku': 'SH-004', 'name': 'Evolv Defy', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'Evolv', 'cost': 40.00, 'retail': 79.95, 'size_run': True},
    {'sku': 'SH-005', 'name': 'Evolv Shaman', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'Evolv', 'cost': 85.00, 'retail': 169.95, 'size_run': True},
    {'sku': 'SH-006', 'name': 'Scarpa Instinct VS', 'category': 'Climbing Shoes', 'subcategory': 'Advanced', 'vendor': 'Scarpa', 'cost': 90.00, 'retail': 179.95, 'size_run': True},
    {'sku': 'SH-007', 'name': 'Black Diamond Momentum', 'category': 'Climbing Shoes', 'subcategory': 'Beginner', 'vendor': 'Black Diamond', 'cost': 42.00, 'retail': 84.95, 'size_run': True},

    # Harnesses
    {'sku': 'HR-001', 'name': 'Petzl Corax', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Petzl', 'cost': 32.00, 'retail': 64.95, 'size_run': False},
    {'sku': 'HR-002', 'name': 'Black Diamond Momentum Harness', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Black Diamond', 'cost': 30.00, 'retail': 59.95, 'size_run': False},
    {'sku': 'HR-003', 'name': 'Petzl Sitta', 'category': 'Harnesses', 'subcategory': 'Performance', 'vendor': 'Petzl', 'cost': 70.00, 'retail': 139.95, 'size_run': False},
    {'sku': 'HR-004', 'name': 'Mammut Ophir 4 Slide', 'category': 'Harnesses', 'subcategory': 'All-Around', 'vendor': 'Mammut', 'cost': 35.00, 'retail': 69.95, 'size_run': False},

    # Chalk & Accessories - high volume, lower margin
    {'sku': 'CH-001', 'name': 'FrictionLabs Unicorn Dust', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'FrictionLabs', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CH-002', 'name': 'FrictionLabs Gorilla Grip', 'category': 'Chalk', 'subcategory': 'Chunky Chalk', 'vendor': 'FrictionLabs', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'CH-003', 'name': 'Metolius Super Chalk', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Metolius', 'cost': 4.00, 'retail': 9.95, 'size_run': False},
    {'sku': 'CH-004', 'name': 'Black Diamond White Gold', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Black Diamond', 'cost': 5.00, 'retail': 11.95, 'size_run': False},

    # Belay Devices
    {'sku': 'BD-001', 'name': 'Petzl GriGri+', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Petzl', 'cost': 55.00, 'retail': 109.95, 'size_run': False},
    {'sku': 'BD-002', 'name': 'Black Diamond ATC-XP', 'category': 'Belay Devices', 'subcategory': 'Tubular', 'vendor': 'Black Diamond', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'BD-003', 'name': 'Mammut Smart 2.0', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Mammut', 'cost': 15.00, 'retail': 29.95, 'size_run': False},

    # Carabiners & Quickdraws
    {'sku': 'CB-001', 'name': 'Petzl Attache', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Petzl', 'cost': 8.00, 'retail': 16.95, 'size_run': False},
    {'sku': 'CB-002', 'name': 'Black Diamond RockLock', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Black Diamond', 'cost': 7.00, 'retail': 14.95, 'size_run': False},
    {'sku': 'CB-003', 'name': 'Petzl Djinn Quickdraw', 'category': 'Carabiners', 'subcategory': 'Quickdraw', 'vendor': 'Petzl', 'cost': 12.00, 'retail': 24.95, 'size_run': False},

    # Chalk Bags
    {'sku': 'CB-101', 'name': 'Metolius Competition Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Metolius', 'cost': 8.00, 'retail': 17.95, 'size_run': False},
    {'sku': 'CB-102', 'name': 'Mammut Gym Print Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Mammut', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CB-103', 'name': 'Black Diamond Mojo Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Black Diamond', 'cost': 9.00, 'retail': 19.95, 'size_run': False},

    # Rope & Slings
    {'sku': 'RP-001', 'name': 'Beal Stinger III 9.4mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Beal', 'cost': 95.00, 'retail': 189.95, 'size_run': False},
    {'sku': 'RP-002', 'name': 'Mammut Crag Classic 9.8mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Mammut', 'cost': 80.00, 'retail': 159.95, 'size_run': False},

    # Apparel
    {'sku': 'AP-001', 'name': 'prAna Stretch Zion Pant', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 40.00, 'retail': 85.00, 'size_run': False},
    {'sku': 'AP-002', 'name': 'prAna Bridger Jean', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 35.00, 'retail': 75.00, 'size_run': False},
    {'sku': 'AP-003', 'name': 'Movement Logo Tee', 'category': 'Apparel', 'subcategory': 'Tops', 'vendor': 'prAna', 'cost': 8.00, 'retail': 25.00, 'size_run': False},

    # Crash Pads & Training
    {'sku': 'TR-001', 'name': 'Metolius Simulator 3D', 'category': 'Training', 'subcategory': 'Hangboard', 'vendor': 'Metolius', 'cost': 20.00, 'retail': 44.95, 'size_run': False},
    {'sku': 'TR-002', 'name': 'Metolius Rock Rings', 'category': 'Training', 'subcategory': 'Grip Trainer', 'vendor': 'Metolius', 'cost': 15.00, 'retail': 34.95, 'size_run': False},
]

products_df = pd.DataFrame(PRODUCTS)

# Calculate margin for each product
# Margin % = (Retail - Cost) / Retail * 100
# This is a critical metric for retail buying decisions
products_df['margin_pct'] = ((products_df['retail'] - products_df['cost']) / products_df['retail'] * 100).round(1)
products_df['margin_dollars'] = (products_df['retail'] - products_df['cost']).round(2)


# -----------------------------------------------------------------------------
# 1.3 SALES DATA GENERATION
# -----------------------------------------------------------------------------
# Generate 12 months of realistic sales data across all gyms.
# Sales patterns account for:
# - Seasonality (higher in spring/fall when outdoor climbing season drives interest)
# - Gym size (larger gyms sell more)
# - Product category popularity (chalk sells most, ropes sell least)

def generate_sales_data(gyms, products, months=12):
    """
    Generate realistic sales transaction data across all gym locations.

    Parameters:
        gyms: DataFrame of gym locations
        products: DataFrame of product catalog
        months: Number of months of historical data to generate

    Returns:
        DataFrame with individual sale transactions

    WHY THIS MATTERS:
    Understanding sales velocity by location is critical for allocation decisions.
    A product that sells 10 units/week at Movement Baker might only sell 2/week
    at Movement Fountain. The allocation model must account for this.
    """
    sales_records = []

    # Size multipliers - larger gyms generate more retail sales
    size_multipliers = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.6}

    # Category sales frequency - how often each category sells (relative)
    # Chalk is the #1 seller by volume in any climbing gym pro shop
    category_frequency = {
        'Chalk': 30,
        'Chalk Bags': 8,
        'Climbing Shoes': 12,
        'Harnesses': 6,
        'Belay Devices': 4,
        'Carabiners': 7,
        'Apparel': 10,
        'Ropes': 2,
        'Training': 5,
    }

    # Monthly seasonality factor (1 = January, 12 = December)
    # Higher in spring and fall when people are psyched on climbing
    seasonality = {
        1: 0.7,   # January - post-holiday slump
        2: 0.75,  # February - still slow
        3: 0.9,   # March - spring approaching
        4: 1.1,   # April - outdoor season starting
        5: 1.2,   # May - peak spring
        6: 1.0,   # June - summer heat reduces gym traffic in some areas
        7: 0.85,  # July - summer dip
        8: 0.9,   # August - back to school
        9: 1.15,  # September - fall sending season
        10: 1.25, # October - peak fall
        11: 1.0,  # November - pre-holiday
        12: 1.1,  # December - holiday gift buying
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

                # Calculate expected monthly units for this product at this gym
                # Base rate * gym size * seasonality * some randomness
                expected_units = cat_freq * gym_size_mult * season_factor
                actual_units = max(0, int(np.random.poisson(expected_units)))

                if actual_units > 0:
                    # Generate individual transactions spread across the month
                    days_in_month = 28 if current_month == 2 else (30 if current_month in [4, 6, 9, 11] else 31)
                    for _ in range(actual_units):
                        sale_day = np.random.randint(1, days_in_month + 1)
                        sale_date = datetime(current_year, current_month, min(sale_day, days_in_month))

                        # Occasional discount (10% of sales are discounted 10-20%)
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

    sales_df = pd.DataFrame(sales_records)
    sales_df['gross_margin'] = (sales_df['sale_price'] - sales_df['cost']).round(2)
    sales_df['margin_pct'] = ((sales_df['gross_margin'] / sales_df['sale_price']) * 100).round(1)

    return sales_df


# -----------------------------------------------------------------------------
# 1.4 INVENTORY DATA GENERATION
# -----------------------------------------------------------------------------

def generate_inventory_data(gyms, products):
    """
    Generate current inventory snapshot across all locations.

    This represents what you'd pull from Business Central - the on-hand
    quantity, reorder points, and weeks of supply for every SKU at every gym.

    WHY THIS MATTERS:
    The Assistant Buyer's primary weekly task is gear allocation - ensuring
    each gym has the right amount of each product. Too much = tied-up capital
    and potential markdowns. Too little = lost sales and frustrated members.
    """
    inventory_records = []
    size_capacity = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.7}

    for _, gym in gyms.iterrows():
        cap = size_capacity[gym['size']]
        for _, product in products.iterrows():
            # Set par levels based on category and gym size
            if product['category'] == 'Chalk':
                par_level = int(25 * cap)
            elif product['category'] in ['Climbing Shoes', 'Apparel']:
                par_level = int(10 * cap)
            elif product['category'] in ['Harnesses', 'Chalk Bags']:
                par_level = int(8 * cap)
            else:
                par_level = int(5 * cap)

            # Current on-hand (some randomness - not all gyms are at par)
            on_hand = max(0, int(np.random.normal(par_level * 0.7, par_level * 0.3)))

            # Calculate weeks of supply based on average weekly sales
            avg_weekly_sales = max(0.5, np.random.normal(par_level * 0.15, par_level * 0.05))
            weeks_of_supply = round(on_hand / avg_weekly_sales, 1) if avg_weekly_sales > 0 else 0

            # Determine stock status
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

            # Days since last received
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


# -----------------------------------------------------------------------------
# 1.5 PURCHASE ORDER DATA GENERATION
# -----------------------------------------------------------------------------

def generate_po_data(products, num_pos=120):
    """
    Generate purchase order history with vendor performance tracking.

    This data mirrors what you'd manage in Business Central - PO creation,
    vendor confirmation, expected delivery, and actual delivery dates.

    WHY THIS MATTERS:
    The Assistant Buyer creates and tracks POs and is the primary contact
    for vendors. Understanding vendor reliability and lead times is critical
    for maintaining in-stock levels across 30+ gyms.
    """
    po_records = []
    vendors_list = list(VENDORS.keys())

    for i in range(num_pos):
        vendor = np.random.choice(vendors_list)
        vendor_info = VENDORS[vendor]

        # PO creation date (spread across 12 months)
        days_ago = np.random.randint(1, 365)
        po_date = datetime(2025, 2, 1) + timedelta(days=365 - days_ago)

        # Expected delivery based on vendor lead time
        expected_delivery = po_date + timedelta(days=vendor_info['lead_time_days'])

        # Actual delivery - vendor reliability affects on-time performance
        if np.random.random() < vendor_info['reliability']:
            # On time or early
            delivery_variance = np.random.randint(-3, 2)
        else:
            # Late delivery
            delivery_variance = np.random.randint(3, 15)

        actual_delivery = expected_delivery + timedelta(days=delivery_variance)

        # Only set actual delivery for POs that have been received
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

        # Get vendor's products for this PO
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

# Save raw data exports
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

# -----------------------------------------------------------------------------
# CHART 00: EXECUTIVE DASHBOARD
# -----------------------------------------------------------------------------
# A one-page summary showing the most important KPIs at a glance.
# This is what you'd present to the Gear Buyer or leadership in a weekly standup.

def create_executive_dashboard():
    """Create a high-level KPI dashboard summarizing retail performance."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Movement Retail — Executive Dashboard', fontsize=18, fontweight='bold', y=0.98)

    # KPI 1: Total Revenue (top-left)
    ax = axes[0, 0]
    total_revenue = sales_df['sale_price'].sum()
    total_cost = sales_df['cost'].sum()
    total_margin = total_revenue - total_cost
    ax.text(0.5, 0.6, f'${total_revenue:,.0f}', ha='center', va='center', fontsize=28, fontweight='bold', color=COLORS['primary'])
    ax.text(0.5, 0.35, 'Total Revenue (12 mo)', ha='center', va='center', fontsize=12, color='gray')
    ax.text(0.5, 0.15, f'Gross Margin: ${total_margin:,.0f} ({total_margin/total_revenue*100:.1f}%)', ha='center', va='center', fontsize=10, color=COLORS['success'])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # KPI 2: In-Stock Rate (top-center)
    ax = axes[0, 1]
    in_stock_count = len(inventory_df[inventory_df['stock_status'].isin(['In Stock', 'Overstock'])])
    total_skus_locs = len(inventory_df)
    in_stock_rate = in_stock_count / total_skus_locs * 100
    color = COLORS['success'] if in_stock_rate >= 85 else COLORS['warning'] if in_stock_rate >= 75 else COLORS['danger']
    ax.text(0.5, 0.6, f'{in_stock_rate:.1f}%', ha='center', va='center', fontsize=28, fontweight='bold', color=color)
    ax.text(0.5, 0.35, 'In-Stock Rate', ha='center', va='center', fontsize=12, color='gray')
    oos_count = len(inventory_df[inventory_df['stock_status'] == 'Out of Stock'])
    ax.text(0.5, 0.15, f'{oos_count} SKU-locations out of stock', ha='center', va='center', fontsize=10, color=COLORS['danger'])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # KPI 3: Inventory Value (top-right)
    ax = axes[0, 2]
    total_inv_cost = inventory_df['inventory_value_cost'].sum()
    total_inv_retail = inventory_df['inventory_value_retail'].sum()
    ax.text(0.5, 0.6, f'${total_inv_cost:,.0f}', ha='center', va='center', fontsize=28, fontweight='bold', color=COLORS['primary'])
    ax.text(0.5, 0.35, 'Total Inventory (at Cost)', ha='center', va='center', fontsize=12, color='gray')
    ax.text(0.5, 0.15, f'Retail Value: ${total_inv_retail:,.0f}', ha='center', va='center', fontsize=10, color=COLORS['accent'])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # KPI 4: Sales by Category (bottom-left) - horizontal bar
    ax = axes[1, 0]
    cat_sales = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=True)
    colors_list = [COLORS['accent']] * len(cat_sales)
    colors_list[-1] = COLORS['secondary']  # Highlight top category
    cat_sales.plot(kind='barh', ax=ax, color=colors_list)
    ax.set_title('Revenue by Category', fontweight='bold', fontsize=11)
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # KPI 5: Top 5 Gyms by Revenue (bottom-center)
    ax = axes[1, 1]
    gym_sales = sales_df.groupby('gym_name')['sale_price'].sum().nlargest(10).sort_values(ascending=True)
    gym_sales.plot(kind='barh', ax=ax, color=COLORS['teal'])
    ax.set_title('Top 10 Gyms by Revenue', fontweight='bold', fontsize=11)
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # KPI 6: Vendor PO Summary (bottom-right)
    ax = axes[1, 2]
    received_pos = po_df[po_df['status'] == 'Received']
    if len(received_pos) > 0:
        vendor_otd = received_pos.groupby('vendor')['on_time'].mean().sort_values(ascending=True) * 100
        colors_otd = [COLORS['danger'] if v < 85 else COLORS['warning'] if v < 92 else COLORS['success'] for v in vendor_otd.values]
        vendor_otd.plot(kind='barh', ax=ax, color=colors_otd)
        ax.set_title('Vendor On-Time Delivery %', fontweight='bold', fontsize=11)
        ax.set_xlabel('On-Time %')
        ax.axvline(x=90, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.set_xlim(0, 105)
    else:
        ax.text(0.5, 0.5, 'No received POs', ha='center', va='center')
        ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(CHARTS_DIR, '00_executive_dashboard.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 00: Executive Dashboard")

create_executive_dashboard()


# -----------------------------------------------------------------------------
# CHART 01: SALES BY CATEGORY
# -----------------------------------------------------------------------------

def create_sales_by_category():
    """Revenue and units sold breakdown by product category."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Sales Performance by Product Category', fontsize=16, fontweight='bold')

    # Revenue by category
    cat_revenue = sales_df.groupby('category')['sale_price'].sum().sort_values(ascending=False)
    colors_bar = [COLORS['secondary'] if i == 0 else COLORS['accent'] for i in range(len(cat_revenue))]
    cat_revenue.plot(kind='bar', ax=ax1, color=colors_bar)
    ax1.set_title('Revenue by Category', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)

    # Units by category
    cat_units = sales_df.groupby('category')['units_sold'].sum().sort_values(ascending=False)
    colors_bar2 = [COLORS['secondary'] if i == 0 else COLORS['teal'] for i in range(len(cat_units))]
    cat_units.plot(kind='bar', ax=ax2, color=colors_bar2)
    ax2.set_title('Units Sold by Category', fontweight='bold')
    ax2.set_ylabel('Units Sold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '01_sales_by_category.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 01: Sales by Category")

create_sales_by_category()


# -----------------------------------------------------------------------------
# CHART 02: SALES BY REGION
# -----------------------------------------------------------------------------

def create_sales_by_region():
    """Compare retail performance across Movement's geographic regions."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Regional Sales Performance', fontsize=16, fontweight='bold')

    # Revenue by region
    region_rev = sales_df.groupby('region')['sale_price'].sum().sort_values(ascending=False)
    region_rev.plot(kind='bar', ax=ax1, color=COLORS['primary'])
    ax1.set_title('Revenue by Region', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)

    # Average sale price by region
    region_avg = sales_df.groupby('region')['sale_price'].mean().sort_values(ascending=False)
    region_avg.plot(kind='bar', ax=ax2, color=COLORS['purple'])
    ax2.set_title('Average Transaction Value by Region', fontweight='bold')
    ax2.set_ylabel('Avg Sale Price ($)')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '02_sales_by_region.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 02: Sales by Region")

create_sales_by_region()


# -----------------------------------------------------------------------------
# CHART 03: MARGIN ANALYSIS
# -----------------------------------------------------------------------------

def create_margin_analysis():
    """Analyze gross margins by category - critical for buying decisions."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Gross Margin Analysis', fontsize=16, fontweight='bold')

    # Margin % by category
    cat_margin = sales_df.groupby('category').agg(
        total_revenue=('sale_price', 'sum'),
        total_cost=('cost', 'sum')
    )
    cat_margin['margin_pct'] = ((cat_margin['total_revenue'] - cat_margin['total_cost']) / cat_margin['total_revenue'] * 100).round(1)
    cat_margin = cat_margin.sort_values('margin_pct', ascending=True)

    colors_margin = [COLORS['danger'] if v < 40 else COLORS['warning'] if v < 50 else COLORS['success'] for v in cat_margin['margin_pct'].values]
    cat_margin['margin_pct'].plot(kind='barh', ax=ax1, color=colors_margin)
    ax1.set_title('Gross Margin % by Category', fontweight='bold')
    ax1.set_xlabel('Margin %')
    ax1.axvline(x=50, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='50% Target')
    ax1.legend()

    # Margin dollars by vendor
    vendor_margin = sales_df.groupby('vendor').agg(
        total_revenue=('sale_price', 'sum'),
        total_cost=('cost', 'sum')
    )
    vendor_margin['margin_dollars'] = vendor_margin['total_revenue'] - vendor_margin['total_cost']
    vendor_margin = vendor_margin.sort_values('margin_dollars', ascending=True)
    vendor_margin['margin_dollars'].plot(kind='barh', ax=ax2, color=COLORS['accent'])
    ax2.set_title('Gross Margin $ by Vendor', fontweight='bold')
    ax2.set_xlabel('Margin ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '03_margin_analysis.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 03: Margin Analysis")

create_margin_analysis()


# -----------------------------------------------------------------------------
# CHART 04: MONTHLY SALES TREND
# -----------------------------------------------------------------------------

def create_monthly_trend():
    """Track sales trends over 12 months to identify seasonality."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    fig.suptitle('Monthly Sales Trends', fontsize=16, fontweight='bold')

    sales_df['month'] = sales_df['sale_date'].dt.to_period('M')

    # Total revenue by month
    monthly_rev = sales_df.groupby('month')['sale_price'].sum()
    monthly_rev.index = monthly_rev.index.astype(str)
    ax1.fill_between(range(len(monthly_rev)), monthly_rev.values, alpha=0.3, color=COLORS['accent'])
    ax1.plot(range(len(monthly_rev)), monthly_rev.values, color=COLORS['accent'], linewidth=2, marker='o')
    ax1.set_title('Total Monthly Revenue', fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.set_xticks(range(len(monthly_rev)))
    ax1.set_xticklabels(monthly_rev.index, rotation=45)

    # Units by category over time
    monthly_cat = sales_df.groupby(['month', 'category'])['units_sold'].sum().unstack(fill_value=0)
    monthly_cat.index = monthly_cat.index.astype(str)
    monthly_cat.plot(kind='bar', stacked=True, ax=ax2, colormap='Set2')
    ax2.set_title('Monthly Units Sold by Category', fontweight='bold')
    ax2.set_ylabel('Units Sold')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '04_monthly_trends.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 04: Monthly Sales Trends")

create_monthly_trend()


# -----------------------------------------------------------------------------
# CHART 05: IN-STOCK RATE BY GYM
# -----------------------------------------------------------------------------

def create_instock_by_gym():
    """
    In-stock rate by gym - the single most important allocation KPI.

    WHY THIS MATTERS:
    The job description specifically mentions 'ensuring strong in-stock levels.'
    This chart makes it immediately visible which gyms need attention.
    Color coding: Green = 90%+, Yellow = 80-90%, Red = below 80%.
    """
    fig, ax = plt.subplots(figsize=(16, 8))

    gym_instock = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    ).sort_values(ascending=True)

    colors_is = [COLORS['danger'] if v < 80 else COLORS['warning'] if v < 90 else COLORS['success'] for v in gym_instock.values]
    gym_instock.plot(kind='barh', ax=ax, color=colors_is)

    ax.set_title('In-Stock Rate by Gym Location', fontsize=16, fontweight='bold')
    ax.set_xlabel('In-Stock Rate (%)')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=1, alpha=0.7, label='90% Target')
    ax.legend(fontsize=10)

    # Add value labels
    for i, (v, name) in enumerate(zip(gym_instock.values, gym_instock.index)):
        ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=8)

    # Add legend for color coding
    legend_elements = [
        mpatches.Patch(color=COLORS['success'], label='≥ 90% (Target)'),
        mpatches.Patch(color=COLORS['warning'], label='80-90% (Needs Attention)'),
        mpatches.Patch(color=COLORS['danger'], label='< 80% (Critical)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '05_instock_by_gym.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 05: In-Stock Rate by Gym")

create_instock_by_gym()


# -----------------------------------------------------------------------------
# CHART 06: INVENTORY STATUS OVERVIEW
# -----------------------------------------------------------------------------

def create_inventory_status():
    """Breakdown of inventory health across the entire network."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Inventory Health Overview', fontsize=16, fontweight='bold')

    # Stock status distribution
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
    ax1.set_title('Stock Status Distribution (All SKU-Locations)', fontweight='bold')

    # Weeks of Supply distribution
    wos = inventory_df[inventory_df['on_hand'] > 0]['weeks_of_supply']
    ax2.hist(wos, bins=30, color=COLORS['primary'], edgecolor='white', alpha=0.8)
    ax2.axvline(x=4, color=COLORS['success'], linestyle='--', linewidth=2, label='Min Target (4 wks)')
    ax2.axvline(x=12, color=COLORS['warning'], linestyle='--', linewidth=2, label='Max Target (12 wks)')
    ax2.set_title('Weeks of Supply Distribution', fontweight='bold')
    ax2.set_xlabel('Weeks of Supply')
    ax2.set_ylabel('Number of SKU-Locations')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '06_inventory_status.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 06: Inventory Status Overview")

create_inventory_status()


# -----------------------------------------------------------------------------
# CHART 07: AGED INVENTORY
# -----------------------------------------------------------------------------

def create_aged_inventory():
    """
    Identify overstock and slow-moving inventory.

    WHY THIS MATTERS:
    The job description mentions 'monitoring aged inventory.' Excess inventory
    ties up capital and may require markdowns. This chart helps identify which
    SKUs and locations need attention.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Aged & Overstock Inventory Analysis', fontsize=16, fontweight='bold')

    # Overstock value by category
    overstock = inventory_df[inventory_df['stock_status'] == 'Overstock']
    if len(overstock) > 0:
        overstock_by_cat = overstock.groupby('category')['inventory_value_cost'].sum().sort_values(ascending=True)
        overstock_by_cat.plot(kind='barh', ax=ax1, color=COLORS['warning'])
        ax1.set_title('Overstock Value by Category (at Cost)', fontweight='bold')
        ax1.set_xlabel('Inventory Value ($)')
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    else:
        ax1.text(0.5, 0.5, 'No overstock identified', ha='center', va='center', fontsize=14)
        ax1.axis('off')

    # Slow movers: items with > 12 weeks of supply
    slow_movers = inventory_df[inventory_df['weeks_of_supply'] > 12]
    if len(slow_movers) > 0:
        slow_by_vendor = slow_movers.groupby('vendor')['inventory_value_cost'].sum().sort_values(ascending=True)
        slow_by_vendor.plot(kind='barh', ax=ax2, color=COLORS['danger'])
        ax2.set_title('Slow-Moving Inventory by Vendor (at Cost)', fontweight='bold')
        ax2.set_xlabel('Inventory Value ($)')
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    else:
        ax2.text(0.5, 0.5, 'No slow movers identified', ha='center', va='center', fontsize=14)
        ax2.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '07_aged_inventory.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 07: Aged Inventory Analysis")

create_aged_inventory()


# -----------------------------------------------------------------------------
# CHART 08: VENDOR PERFORMANCE SCORECARD
# -----------------------------------------------------------------------------

def create_vendor_scorecard():
    """
    Comprehensive vendor performance analysis.

    WHY THIS MATTERS:
    The Assistant Buyer is the primary vendor contact. Understanding vendor
    reliability, lead times, and performance helps negotiate better terms
    and ensures product arrives when promised.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Vendor Performance Scorecard', fontsize=16, fontweight='bold')

    received_pos = po_df[po_df['status'] == 'Received']

    # On-Time Delivery Rate
    ax = axes[0, 0]
    otd = received_pos.groupby('vendor')['on_time'].mean().sort_values(ascending=True) * 100
    colors_otd = [COLORS['danger'] if v < 85 else COLORS['warning'] if v < 92 else COLORS['success'] for v in otd.values]
    otd.plot(kind='barh', ax=ax, color=colors_otd)
    ax.set_title('On-Time Delivery Rate (%)', fontweight='bold')
    ax.axvline(x=90, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel('On-Time %')
    ax.set_xlim(0, 105)

    # Average Lead Time
    ax = axes[0, 1]
    avg_lead = received_pos.groupby('vendor')['lead_time_days'].mean().sort_values(ascending=True)
    avg_lead.plot(kind='barh', ax=ax, color=COLORS['primary'])
    ax.set_title('Average Lead Time (Days)', fontweight='bold')
    ax.set_xlabel('Days')

    # Total PO Value by Vendor
    ax = axes[1, 0]
    vendor_spend = po_df.groupby('vendor')['total_cost'].sum().sort_values(ascending=True)
    vendor_spend.plot(kind='barh', ax=ax, color=COLORS['accent'])
    ax.set_title('Total PO Spend by Vendor', fontweight='bold')
    ax.set_xlabel('Total Cost ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Delivery Variance (days late/early)
    ax = axes[1, 1]
    variance = received_pos.groupby('vendor')['delivery_variance_days'].mean().sort_values()
    colors_var = [COLORS['success'] if v <= 0 else COLORS['warning'] if v <= 3 else COLORS['danger'] for v in variance.values]
    variance.plot(kind='barh', ax=ax, color=colors_var)
    ax.set_title('Average Delivery Variance (Days)', fontweight='bold')
    ax.set_xlabel('Days (negative = early, positive = late)')
    ax.axvline(x=0, color='black', linewidth=1)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '08_vendor_scorecard.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 08: Vendor Performance Scorecard")

create_vendor_scorecard()


# -----------------------------------------------------------------------------
# CHART 09: TOP SELLERS & BOTTOM SELLERS
# -----------------------------------------------------------------------------

def create_top_bottom_sellers():
    """Identify best and worst performing products for chase buys and markdowns."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Product Performance: Top & Bottom Sellers', fontsize=16, fontweight='bold')

    product_perf = sales_df.groupby('product_name').agg(
        total_revenue=('sale_price', 'sum'),
        total_units=('units_sold', 'sum'),
    ).sort_values('total_revenue', ascending=False)

    # Top 10 by revenue
    top10 = product_perf.head(10).sort_values('total_revenue', ascending=True)
    top10['total_revenue'].plot(kind='barh', ax=ax1, color=COLORS['success'])
    ax1.set_title('Top 10 Products by Revenue', fontweight='bold')
    ax1.set_xlabel('Revenue ($)')
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Bottom 10 by revenue (potential markdown candidates)
    bottom10 = product_perf.tail(10).sort_values('total_revenue', ascending=True)
    bottom10['total_revenue'].plot(kind='barh', ax=ax2, color=COLORS['danger'])
    ax2.set_title('Bottom 10 Products by Revenue\n(Potential markdown or discontinue candidates)', fontweight='bold', fontsize=10)
    ax2.set_xlabel('Revenue ($)')
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '09_top_bottom_sellers.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 09: Top & Bottom Sellers")

create_top_bottom_sellers()


# -----------------------------------------------------------------------------
# CHART 10: ALLOCATION ANALYSIS
# -----------------------------------------------------------------------------

def create_allocation_analysis():
    """
    Allocation efficiency: are we sending the right amount to each gym?

    WHY THIS MATTERS:
    The #1 responsibility in the job description is 'executing weekly gear
    allocations across 30+ gyms.' This chart shows which gyms are over/under
    allocated relative to their sales velocity.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Allocation Efficiency Analysis', fontsize=16, fontweight='bold')

    # Compare inventory value to sales by gym
    gym_inv = inventory_df.groupby('gym_name')['inventory_value_cost'].sum()
    gym_rev = sales_df.groupby('gym_name')['sale_price'].sum()
    comparison = pd.DataFrame({'inventory': gym_inv, 'revenue': gym_rev}).dropna()
    comparison['inv_to_sales_ratio'] = (comparison['inventory'] / comparison['revenue'] * 100).round(1)
    comparison = comparison.sort_values('inv_to_sales_ratio', ascending=True)

    colors_alloc = [COLORS['danger'] if v > 25 else COLORS['warning'] if v > 18 else COLORS['success'] for v in comparison['inv_to_sales_ratio'].values]
    comparison['inv_to_sales_ratio'].plot(kind='barh', ax=ax1, color=colors_alloc)
    ax1.set_title('Inventory-to-Sales Ratio by Gym\n(Lower = leaner inventory, higher = potential overstock)', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Inventory as % of Revenue')

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
        color=[status_colors_map[s] for s in available_statuses]
    )
    ax2.set_title('Stock Status by Region (%)', fontweight='bold')
    ax2.set_xlabel('Percentage')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '10_allocation_analysis.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 10: Allocation Analysis")

create_allocation_analysis()


# -----------------------------------------------------------------------------
# CHART 11: PO STATUS PIPELINE
# -----------------------------------------------------------------------------

def create_po_pipeline():
    """Track the purchase order pipeline - open, in transit, and received."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Purchase Order Pipeline', fontsize=16, fontweight='bold')

    # PO status breakdown
    po_status = po_df['status'].value_counts()
    status_colors_po = {'Received': COLORS['success'], 'In Transit': COLORS['warning'], 'Open': COLORS['accent']}
    colors_po = [status_colors_po.get(s, 'gray') for s in po_status.index]
    ax1.pie(po_status.values, labels=po_status.index, colors=colors_po,
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
    ax1.set_title('PO Status Breakdown', fontweight='bold')

    # PO volume over time
    po_df['po_month'] = pd.to_datetime(po_df['po_date']).dt.to_period('M')
    monthly_pos = po_df.groupby('po_month').agg(
        num_pos=('po_number', 'count'),
        total_value=('total_cost', 'sum')
    )
    monthly_pos.index = monthly_pos.index.astype(str)

    ax2_twin = ax2.twinx()
    bars = ax2.bar(range(len(monthly_pos)), monthly_pos['num_pos'], color=COLORS['accent'], alpha=0.7, label='# of POs')
    line = ax2_twin.plot(range(len(monthly_pos)), monthly_pos['total_value'], color=COLORS['secondary'], linewidth=2, marker='o', label='PO Value ($)')
    ax2.set_title('Monthly PO Volume & Value', fontweight='bold')
    ax2.set_ylabel('Number of POs')
    ax2_twin.set_ylabel('PO Value ($)')
    ax2_twin.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2.set_xticks(range(len(monthly_pos)))
    ax2.set_xticklabels(monthly_pos.index, rotation=45)

    # Combined legend
    lines_labels = [bars] + line
    labels = ['# of POs', 'PO Value ($)']
    ax2.legend(lines_labels, labels, loc='upper left')

    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, '11_po_pipeline.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 11: PO Pipeline")

create_po_pipeline()


# -----------------------------------------------------------------------------
# CHART 12: CATEGORY DEEP-DIVE (CLIMBING SHOES)
# -----------------------------------------------------------------------------

def create_shoe_deep_dive():
    """
    Deep dive into climbing shoes - the highest-margin gear category.

    Climbing shoes are the most important category for a climbing gym pro shop.
    They have the highest margin and are typically the first purchase a new
    climber makes after they start renting less.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Category Deep-Dive: Climbing Shoes', fontsize=16, fontweight='bold')

    shoes_sales = sales_df[sales_df['category'] == 'Climbing Shoes']
    shoes_inv = inventory_df[inventory_df['category'] == 'Climbing Shoes']

    # Revenue by shoe model
    ax = axes[0, 0]
    shoe_rev = shoes_sales.groupby('product_name')['sale_price'].sum().sort_values(ascending=True)
    shoe_rev.plot(kind='barh', ax=ax, color=COLORS['accent'])
    ax.set_title('Revenue by Shoe Model', fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Beginner vs Advanced split
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
    colors_shoe = [COLORS['danger'] if v < 70 else COLORS['warning'] if v < 85 else COLORS['success'] for v in shoe_instock.values]
    shoe_instock.plot(kind='barh', ax=ax, color=colors_shoe, fontsize=7)
    ax.set_title('Shoe In-Stock Rate by Gym', fontweight='bold')
    ax.set_xlabel('In-Stock %')

    # Monthly shoe trend
    ax = axes[1, 1]
    shoes_sales['month'] = shoes_sales['sale_date'].dt.to_period('M')
    monthly_shoes = shoes_sales.groupby('month')['sale_price'].sum()
    monthly_shoes.index = monthly_shoes.index.astype(str)
    ax.fill_between(range(len(monthly_shoes)), monthly_shoes.values, alpha=0.3, color=COLORS['secondary'])
    ax.plot(range(len(monthly_shoes)), monthly_shoes.values, color=COLORS['secondary'], linewidth=2, marker='o')
    ax.set_title('Monthly Shoe Revenue Trend', fontweight='bold')
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.set_xticks(range(len(monthly_shoes)))
    ax.set_xticklabels(monthly_shoes.index, rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(CHARTS_DIR, '12_shoe_deep_dive.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print("   ✅ Chart 12: Climbing Shoe Deep-Dive")

create_shoe_deep_dive()


# =============================================================================
# SECTION 4: SUMMARY REPORT
# =============================================================================

def print_summary():
    """Print a text-based summary of key findings."""
    print("\n" + "=" * 70)
    print("📋 SUMMARY OF KEY FINDINGS")
    print("=" * 70)

    # Revenue summary
    total_rev = sales_df['sale_price'].sum()
    total_cost_sold = sales_df['cost'].sum()
    total_gm = total_rev - total_cost_sold
    print(f"\n💰 REVENUE & MARGIN")
    print(f"   Total Revenue (12 months):      ${total_rev:>12,.2f}")
    print(f"   Total Cost of Goods Sold:        ${total_cost_sold:>12,.2f}")
    print(f"   Gross Margin:                    ${total_gm:>12,.2f} ({total_gm/total_rev*100:.1f}%)")

    # Top category
    top_cat = sales_df.groupby('category')['sale_price'].sum().idxmax()
    top_cat_rev = sales_df.groupby('category')['sale_price'].sum().max()
    print(f"   Top Category:                    {top_cat} (${top_cat_rev:,.2f})")

    # Inventory summary
    print(f"\n📦 INVENTORY HEALTH")
    total_inv = inventory_df['inventory_value_cost'].sum()
    in_stock = (inventory_df['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(inventory_df) * 100)
    oos = (inventory_df['stock_status'] == 'Out of Stock').sum()
    overstock = (inventory_df['stock_status'] == 'Overstock').sum()
    print(f"   Total Inventory Value (at cost): ${total_inv:>12,.2f}")
    print(f"   Overall In-Stock Rate:           {in_stock:>11.1f}%")
    print(f"   Out-of-Stock SKU-Locations:      {oos:>12}")
    print(f"   Overstock SKU-Locations:         {overstock:>12}")

    # Vendor summary
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

    # Actionable insights
    print(f"\n⚡ ACTIONABLE INSIGHTS")

    # Find gyms with low in-stock
    gym_is = inventory_df.groupby('gym_name').apply(
        lambda x: (x['stock_status'].isin(['In Stock', 'Overstock']).sum() / len(x)) * 100
    )
    low_gyms = gym_is[gym_is < 80]
    if len(low_gyms) > 0:
        print(f"   🔴 {len(low_gyms)} gym(s) below 80% in-stock rate - prioritize in next allocation")
        for gym, rate in low_gyms.items():
            print(f"      → {gym}: {rate:.1f}%")

    # Overstock value
    overstock_value = inventory_df[inventory_df['stock_status'] == 'Overstock']['inventory_value_cost'].sum()
    if overstock_value > 0:
        print(f"   🟡 ${overstock_value:,.2f} in overstock inventory — review for markdowns or transfers")

    # Late vendor
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
