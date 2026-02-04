"""
visualizations/ - Individual chart modules

Each file creates one chart. Import all chart functions from here:
    from visualizations import create_executive_dashboard, create_sales_by_category, ...
"""

from .executive_dashboard import create_executive_dashboard
from .sales_by_category import create_sales_by_category
from .sales_by_region import create_sales_by_region
from .margin_analysis import create_margin_analysis
from .monthly_trends import create_monthly_trend
from .top_bottom_sellers import create_top_bottom_sellers
from .instock_by_gym import create_instock_by_gym
from .inventory_status import create_inventory_status
from .aged_inventory import create_aged_inventory
from .allocation_analysis import create_allocation_analysis
from .vendor_scorecard import create_vendor_scorecard
from .po_pipeline import create_po_pipeline
from .shoe_deep_dive import create_shoe_deep_dive
