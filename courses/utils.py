from decimal import Decimal
from .models import Incentive
from .services import calculate_purchase_incentives

def calculate_incentives(purchase):
    """
    Create incentive records for a purchase based on the MLM structure.
    """
    incentives = calculate_purchase_incentives(purchase)
    
    for incentive_data in incentives:
        Incentive.objects.create(
            agent=incentive_data['agent'],
            purchase=purchase,
            amount=incentive_data['amount']
        )