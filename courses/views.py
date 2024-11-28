from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import CoursePackage, Purchase, Incentive
from .utils import calculate_incentives

def course_list(request):
    courses = CoursePackage.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(CoursePackage, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
@transaction.atomic
def purchase_course(request, pk):
    course = get_object_or_404(CoursePackage, pk=pk)
    
    if Purchase.objects.filter(user=request.user, package=course).exists():
        messages.error(request, 'You have already purchased this course.')
        return redirect('courses:detail', pk=pk)
    
    purchase = Purchase.objects.create(user=request.user, package=course)
    calculate_incentives(purchase)
    
    messages.success(request, f'Successfully purchased {course.name}!')
    return redirect('dashboard:home')