from decimal import Decimal
from typing import List, Dict
from .config import get_settings

def calculate_discount(order_total: Decimal) -> Decimal:
    """Calculate discount based on order total using business parameters"""
    settings = get_settings()
    discount_tiers = settings.get_business_param("pricing.discount_tiers", [])
    
    applicable_discount = Decimal('0')
    for tier in sorted(discount_tiers, key=lambda x: x['threshold'], reverse=True):
        if order_total >= tier['threshold']:
            applicable_discount = Decimal(str(tier['percentage']))
            break
            
    return (order_total * applicable_discount) / Decimal('100')

def validate_order(items: List[Dict], total: Decimal) -> bool:
    """Validate order against business rules"""
    settings = get_settings()
    
    # Check minimum order
    if total < Decimal(str(settings.get_business_param("pricing.minimum_order", 0))):
        return False
        
    # Check max items per order
    max_items = settings.get_business_param("inventory.max_items_per_order")
    if sum(item.get('quantity', 0) for item in items) > max_items:
        return False
        
    return True
