from decimal import Decimal
from typing import List, Dict, Any
from django.db.models import QuerySet
from .models import CoursePackage, Purchase, Incentive

def get_available_courses() -> QuerySet[CoursePackage]:
    """
    Retrieve all available course packages ordered by creation date.
    """
    return CoursePackage.objects.all().order_by('-created_at')

def get_user_purchases(user_id: int) -> QuerySet[Purchase]:
    """
    Get all purchases for a specific user with related course package data.
    """
    return Purchase.objects.filter(user_id=user_id).select_related('package')

def calculate_purchase_incentives(purchase: Purchase) -> List[Dict[str, Any]]:
    """
    Calculate incentives for a purchase based on MLM structure.
    Returns a list of dictionaries containing incentive details.
    """
    incentives = []
    current_user = purchase.user
    package_price = purchase.package.price
    rates = [
        ('Direct Referral', Decimal('0.10')),
        ('Second Level', Decimal('0.05')),
        ('Third Level', Decimal('0.025'))
    ]
    
    for level, rate in rates:
        if not current_user.referrer:
            break
            
        amount = package_price * rate
        incentives.append({
            'agent': current_user.referrer,
            'amount': amount,
            'level': level
        })
        current_user = current_user.referrer
    
    return incentives