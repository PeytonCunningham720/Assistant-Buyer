"""
config.py - Central configuration for the retail analysis project

All constants, color palettes, plot settings, and data definitions live here.
Import this module anywhere you need access to shared settings.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# DIRECTORY PATHS
# =============================================================================
# Get the project root (one level up from src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')

# Create output directories if they don't exist
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# =============================================================================
# RANDOM SEED - keeps synthetic data reproducible
# =============================================================================
RANDOM_SEED = 42

# =============================================================================
# MATPLOTLIB STYLE CONFIGURATION
# =============================================================================
# Professional typography and clean chart aesthetics
PLOT_STYLE = {
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Helvetica', 'Arial'],
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.labelsize': 10,
    'axes.spines.top': False,      # hide top spine for cleaner look
    'axes.spines.right': False,    # hide right spine
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#CCCCCC',
    'grid.color': '#EEEEEE',
    'grid.linewidth': 0.6,
}

def apply_plot_style():
    """Apply the project's matplotlib style settings."""
    plt.rcParams.update(PLOT_STYLE)
    sns.set_style("whitegrid")

# =============================================================================
# COLOR PALETTE - Movement-inspired professional colors
# =============================================================================
COLORS = {
    'primary':     '#1B2A4A',   # deep navy - main brand color
    'secondary':   "#070707",   # warm red - accent/highlight
    'accent':      '#2E86AB',   # steel blue - charts/data
    'success':     '#28A745',   # green - positive metrics
    'warning':     '#F5A623',   # amber - attention needed
    'danger':      '#DC3545',   # red - critical/negative
    'light':       '#F4F6F9',   # soft gray - backgrounds
    'purple':      '#7B61B8',   # muted purple - variety
    'teal':        '#17A89B',   # rich teal - variety
    'text':        '#2D3436',   # near-black - primary text
    'text_light':  '#6C757D',   # gray - secondary text
    'border':      '#DEE2E6',   # subtle borders
    'card_bg':     '#FFFFFF',   # card backgrounds
    'card_shadow': '#D1D9E6',   # shadow color
}

# Palette for categorical data in charts
CATEGORY_PALETTE = [
    '#2E86AB', '#D94F4F', '#28A745', '#F5A623',
    '#7B61B8', '#17A89B', '#E07C4F', '#5B8C5A', '#3D5A80'
]

# =============================================================================
# GYM LOCATIONS - Movement's network of climbing gyms
# =============================================================================
GYM_LOCATIONS = [
    # California
    {'gym_id': 'MOV-001', 'gym_name': 'Movement Mountain View', 'city': 'Mountain View', 'state': 'CA', 'region': 'California', 'size': 'Large'},
    {'gym_id': 'MOV-002', 'gym_name': 'Movement Belmont', 'city': 'Belmont', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    {'gym_id': 'MOV-003', 'gym_name': 'Movement Fountain Valley', 'city': 'Fountain Valley', 'state': 'CA', 'region': 'California', 'size': 'Large'},
    {'gym_id': 'MOV-004', 'gym_name': 'Movement San Francisco', 'city': 'San Francisco', 'state': 'CA', 'region': 'California', 'size': 'Large'},
    {'gym_id': 'MOV-005', 'gym_name': 'Movement Santa Clara', 'city': 'Santa Clara', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    {'gym_id': 'MOV-006', 'gym_name': 'Movement Sunnyvale', 'city': 'Sunnyvale', 'state': 'CA', 'region': 'California', 'size': 'Medium'},
    # Oregon
    {'gym_id': 'MOV-007', 'gym_name': 'Movement Portland', 'city': 'Portland', 'state': 'OR', 'region': 'Pacific NW', 'size': 'Large'},
    # Colorado
    {'gym_id': 'MOV-008', 'gym_name': 'Movement Baker', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-009', 'gym_name': 'Movement Boulder', 'city': 'Boulder', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    {'gym_id': 'MOV-010', 'gym_name': 'Movement Centennial', 'city': 'Centennial', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-011', 'gym_name': 'Movement Englewood', 'city': 'Englewood', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-012', 'gym_name': 'Movement Golden', 'city': 'Golden', 'state': 'CO', 'region': 'Colorado', 'size': 'Medium'},
    {'gym_id': 'MOV-013', 'gym_name': 'Movement RiNo', 'city': 'Denver', 'state': 'CO', 'region': 'Colorado', 'size': 'Large'},
    # Illinois
    {'gym_id': 'MOV-014', 'gym_name': 'Movement Lincoln Park', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Large'},
    {'gym_id': 'MOV-015', 'gym_name': 'Movement Wrigleyville', 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest', 'size': 'Large'},
    # Texas
    {'gym_id': 'MOV-016', 'gym_name': 'Movement Denton', 'city': 'Denton', 'state': 'TX', 'region': 'Texas', 'size': 'Medium'},
    {'gym_id': 'MOV-017', 'gym_name': 'Movement Design District', 'city': 'Dallas', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-018', 'gym_name': 'Movement Fort Worth', 'city': 'Fort Worth', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    {'gym_id': 'MOV-019', 'gym_name': 'Movement Grapevine', 'city': 'Grapevine', 'state': 'TX', 'region': 'Texas', 'size': 'Medium'},
    {'gym_id': 'MOV-020', 'gym_name': 'Movement The Hill', 'city': 'Dallas', 'state': 'TX', 'region': 'Texas', 'size': 'Medium'},
    {'gym_id': 'MOV-021', 'gym_name': 'Movement Plano', 'city': 'Plano', 'state': 'TX', 'region': 'Texas', 'size': 'Large'},
    # Maryland
    {'gym_id': 'MOV-022', 'gym_name': 'Movement Columbia', 'city': 'Columbia', 'state': 'MD', 'region': 'Mid-Atlantic', 'size': 'Medium'},
    {'gym_id': 'MOV-023', 'gym_name': 'Movement Hampden', 'city': 'Baltimore', 'state': 'MD', 'region': 'Mid-Atlantic', 'size': 'Large'},
    {'gym_id': 'MOV-024', 'gym_name': 'Movement Rockville', 'city': 'Rockville', 'state': 'MD', 'region': 'Mid-Atlantic', 'size': 'Medium'},
    {'gym_id': 'MOV-025', 'gym_name': 'Movement Timonium', 'city': 'Timonium', 'state': 'MD', 'region': 'Mid-Atlantic', 'size': 'Medium'},
    # New York
    {'gym_id': 'MOV-026', 'gym_name': 'Movement Gowanus', 'city': 'Brooklyn', 'state': 'NY', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-027', 'gym_name': 'Movement Harlem', 'city': 'New York', 'state': 'NY', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-028', 'gym_name': 'Movement LIC', 'city': 'Queens', 'state': 'NY', 'region': 'Northeast', 'size': 'Medium'},
    {'gym_id': 'MOV-029', 'gym_name': 'Movement Valhalla', 'city': 'Valhalla', 'state': 'NY', 'region': 'Northeast', 'size': 'Medium'},
    # Pennsylvania
    {'gym_id': 'MOV-030', 'gym_name': 'Movement Callowhill', 'city': 'Philadelphia', 'state': 'PA', 'region': 'Northeast', 'size': 'Large'},
    {'gym_id': 'MOV-031', 'gym_name': 'Movement Fishtown', 'city': 'Philadelphia', 'state': 'PA', 'region': 'Northeast', 'size': 'Medium'},
    # Virginia
    {'gym_id': 'MOV-032', 'gym_name': 'Movement Crystal City', 'city': 'Arlington', 'state': 'VA', 'region': 'Mid-Atlantic', 'size': 'Large'},
    {'gym_id': 'MOV-033', 'gym_name': 'Movement Fairfax', 'city': 'Fairfax', 'state': 'VA', 'region': 'Mid-Atlantic', 'size': 'Medium'},
]

# =============================================================================
# VENDOR DATA - climbing gear suppliers with lead times and reliability
# =============================================================================
VENDORS = {
    'La Sportiva':   {'lead_time_days': 21, 'min_order': 500, 'reliability': 0.92},
    'Petzl':         {'lead_time_days': 18, 'min_order': 400, 'reliability': 0.95},
    'Black Diamond': {'lead_time_days': 14, 'min_order': 300, 'reliability': 0.93},
    'Evolv':         {'lead_time_days': 21, 'min_order': 400, 'reliability': 0.88},
    'Scarpa':        {'lead_time_days': 25, 'min_order': 600, 'reliability': 0.90},
    'Metolius':      {'lead_time_days': 10, 'min_order': 200, 'reliability': 0.94},
    'FrictionLabs':  {'lead_time_days': 7,  'min_order': 150, 'reliability': 0.97},
    'Beal':          {'lead_time_days': 20, 'min_order': 350, 'reliability': 0.91},
    'Mammut':        {'lead_time_days': 22, 'min_order': 500, 'reliability': 0.89},
    'prAna':         {'lead_time_days': 14, 'min_order': 250, 'reliability': 0.93},
}

# =============================================================================
# PRODUCT CATALOG - all SKUs with cost, retail, and categorization
# =============================================================================
PRODUCTS = [
    # Climbing Shoes - the bread and butter
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
    # Chalk - high volume, low margin, always needs restocking
    {'sku': 'CH-001', 'name': 'FrictionLabs Unicorn Dust', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'FrictionLabs', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CH-002', 'name': 'FrictionLabs Gorilla Grip', 'category': 'Chalk', 'subcategory': 'Chunky Chalk', 'vendor': 'FrictionLabs', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'CH-003', 'name': 'Metolius Super Chalk', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Metolius', 'cost': 4.00, 'retail': 9.95, 'size_run': False},
    {'sku': 'CH-004', 'name': 'Black Diamond White Gold', 'category': 'Chalk', 'subcategory': 'Loose Chalk', 'vendor': 'Black Diamond', 'cost': 5.00, 'retail': 11.95, 'size_run': False},
    # Belay Devices
    {'sku': 'BD-001', 'name': 'Petzl GriGri+', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Petzl', 'cost': 55.00, 'retail': 109.95, 'size_run': False},
    {'sku': 'BD-002', 'name': 'Black Diamond ATC-XP', 'category': 'Belay Devices', 'subcategory': 'Tubular', 'vendor': 'Black Diamond', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    {'sku': 'BD-003', 'name': 'Mammut Smart 2.0', 'category': 'Belay Devices', 'subcategory': 'Assisted Braking', 'vendor': 'Mammut', 'cost': 15.00, 'retail': 29.95, 'size_run': False},
    # Carabiners
    {'sku': 'CB-001', 'name': 'Petzl Attache', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Petzl', 'cost': 8.00, 'retail': 16.95, 'size_run': False},
    {'sku': 'CB-002', 'name': 'Black Diamond RockLock', 'category': 'Carabiners', 'subcategory': 'Locking', 'vendor': 'Black Diamond', 'cost': 7.00, 'retail': 14.95, 'size_run': False},
    {'sku': 'CB-003', 'name': 'Petzl Djinn Quickdraw', 'category': 'Carabiners', 'subcategory': 'Quickdraw', 'vendor': 'Petzl', 'cost': 12.00, 'retail': 24.95, 'size_run': False},
    # Chalk Bags
    {'sku': 'CB-101', 'name': 'Metolius Competition Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Metolius', 'cost': 8.00, 'retail': 17.95, 'size_run': False},
    {'sku': 'CB-102', 'name': 'Mammut Gym Print Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Mammut', 'cost': 10.00, 'retail': 21.95, 'size_run': False},
    {'sku': 'CB-103', 'name': 'Black Diamond Mojo Chalk Bag', 'category': 'Chalk Bags', 'subcategory': 'Standard', 'vendor': 'Black Diamond', 'cost': 9.00, 'retail': 19.95, 'size_run': False},
    # Ropes - high ticket items
    {'sku': 'RP-001', 'name': 'Beal Stinger III 9.4mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Beal', 'cost': 95.00, 'retail': 189.95, 'size_run': False},
    {'sku': 'RP-002', 'name': 'Mammut Crag Classic 9.8mm', 'category': 'Ropes', 'subcategory': 'Single Rope', 'vendor': 'Mammut', 'cost': 80.00, 'retail': 159.95, 'size_run': False},
    # Apparel
    {'sku': 'AP-001', 'name': 'prAna Stretch Zion Pant', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 40.00, 'retail': 85.00, 'size_run': False},
    {'sku': 'AP-002', 'name': 'prAna Bridger Jean', 'category': 'Apparel', 'subcategory': 'Pants', 'vendor': 'prAna', 'cost': 35.00, 'retail': 75.00, 'size_run': False},
    {'sku': 'AP-003', 'name': 'Movement Logo Tee', 'category': 'Apparel', 'subcategory': 'Tops', 'vendor': 'prAna', 'cost': 8.00, 'retail': 25.00, 'size_run': False},
    # Training gear
    {'sku': 'TR-001', 'name': 'Metolius Simulator 3D', 'category': 'Training', 'subcategory': 'Hangboard', 'vendor': 'Metolius', 'cost': 20.00, 'retail': 44.95, 'size_run': False},
    {'sku': 'TR-002', 'name': 'Metolius Rock Rings', 'category': 'Training', 'subcategory': 'Grip Trainer', 'vendor': 'Metolius', 'cost': 15.00, 'retail': 34.95, 'size_run': False},
]

# =============================================================================
# DATA GENERATION PARAMETERS
# =============================================================================
# How gym size affects sales volume and inventory capacity
SIZE_MULTIPLIERS = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.6}
SIZE_CAPACITY = {'Large': 1.5, 'Medium': 1.0, 'Small': 0.7}

# How often each category sells (average transactions per month per gym)
CATEGORY_FREQUENCY = {
    'Chalk': 30,           # high volume consumable
    'Chalk Bags': 8,
    'Climbing Shoes': 12,  # main revenue driver
    'Harnesses': 6,
    'Belay Devices': 4,
    'Carabiners': 7,
    'Apparel': 10,
    'Ropes': 2,            # less frequent, high ticket
    'Training': 5,
}

# Seasonal demand multipliers (month number -> multiplier)
SEASONALITY = {
    1: 0.70,   # Jan - post-holiday slump
    2: 0.75,   # Feb
    3: 0.90,   # Mar - spring uptick
    4: 1.10,   # Apr
    5: 1.20,   # May - peak outdoor season
    6: 1.00,   # Jun
    7: 0.85,   # Jul - summer lull (people outside)
    8: 0.90,   # Aug
    9: 1.15,   # Sep - back to gym season
    10: 1.25,  # Oct - peak indoor season
    11: 1.00,  # Nov
    12: 1.10,  # Dec - holiday gifting
}
