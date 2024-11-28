from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect
from django.http import JsonResponse
from courses.models import Purchase, Incentive
from django.db.models import Sum
from datetime import datetime, timedelta
from .utils import get_monthly_earnings, get_downline_stats

@login_required
def dashboard_home(request):
    user = request.user
    context = {
        'purchased_courses': Purchase.objects.filter(user=user).select_related('package')
    }
    
    if user.is_agent:
        # Calculate total incentives
        total_incentives = Incentive.objects.filter(agent=user).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Get downline statistics
        downline_stats = get_downline_stats(user)
        
        # Calculate monthly earnings
        thirty_days_ago = datetime.now() - timedelta(days=30)
        monthly_earnings = Incentive.objects.filter(
            agent=user,
            created_at__gte=thirty_days_ago
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        context.update({
            'total_incentives': total_incentives,
            'downline_stats': downline_stats,
            'monthly_earnings': monthly_earnings,
            'recent_incentives': Incentive.objects.filter(agent=user).order_by('-created_at')[:5]
        })
    
    return render(request, 'dashboard/home.html', context)

@login_required
def referrals(request):
    if not request.user.is_agent:
        return redirect('dashboard:home')
    
    downline = request.user.get_downline()
    direct_referrals = request.user.referrals.all()
    
    context = {
        'direct_referrals': direct_referrals,
        'downline': downline,
        'downline_stats': get_downline_stats(request.user)
    }
    return render(request, 'dashboard/referrals.html', context)

@login_required
def earnings(request):
    if not request.user.is_agent:
        return redirect('dashboard:home')
    
    context = {
        'total_earnings': Incentive.objects.filter(agent=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    }
    return render(request, 'dashboard/earnings.html', context)

@login_required
def earnings_data(request):
    if not request.user.is_agent:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    monthly_data = get_monthly_earnings(request.user)
    data = {
        'labels': [],
        'values': []
    }
    
    for entry in monthly_data:
        data['labels'].append(entry['month'].strftime('%B %Y'))
        data['values'].append(float(entry['total']))
    
    return JsonResponse(data)