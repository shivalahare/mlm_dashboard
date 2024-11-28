from datetime import datetime, timedelta
from typing import Dict, Any
from django.db.models import Sum, QuerySet
from django.db.models.functions import TruncMonth
from courses.models import Incentive
from users.models import CustomUser

def get_agent_statistics(user: CustomUser) -> Dict[str, Any]:
    """
    Get comprehensive statistics for an agent including earnings and referrals.
    """
    total_incentives = Incentive.objects.filter(agent=user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    monthly_earnings = Incentive.objects.filter(
        agent=user,
        created_at__gte=thirty_days_ago
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    downline_stats = get_downline_statistics(user)
    
    return {
        'total_incentives': total_incentives,
        'monthly_earnings': monthly_earnings,
        'downline_stats': downline_stats,
        'recent_incentives': get_recent_incentives(user)
    }

def get_downline_statistics(user: CustomUser) -> Dict[str, int]:
    """
    Calculate detailed statistics about an agent's downline.
    """
    downline = user.get_downline()
    direct_referrals = user.referrals.count()
    
    return {
        'total_members': len(downline),
        'direct_referrals': direct_referrals,
        'indirect_referrals': len(downline) - direct_referrals
    }

def get_recent_incentives(user: CustomUser, limit: int = 5) -> QuerySet:
    """
    Get the most recent incentives for an agent.
    """
    return Incentive.objects.filter(agent=user).order_by('-created_at')[:limit]

def get_monthly_earnings_data(user: CustomUser, months: int = 6) -> QuerySet:
    """
    Get monthly earnings data for charts.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)
    
    return (Incentive.objects
        .filter(
            agent=user,
            created_at__range=(start_date, end_date)
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )