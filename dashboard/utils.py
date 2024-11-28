from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from courses.models import Incentive

def get_monthly_earnings(user, months=6):
    """Get monthly earnings data for the last specified number of months."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)
    
    monthly_data = (Incentive.objects
        .filter(
            agent=user,
            created_at__range=(start_date, end_date)
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    
    return monthly_data

def get_downline_stats(user):
    """Get detailed statistics about user's downline."""
    downline = user.get_downline()
    direct_referrals = user.referrals.count()
    
    return {
        'total_members': len(downline),
        'direct_referrals': direct_referrals,
        'indirect_referrals': len(downline) - direct_referrals
    }