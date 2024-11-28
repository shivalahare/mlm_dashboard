from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('referrals/', views.referrals, name='referrals'),
    path('earnings/', views.earnings, name='earnings'),
    path('earnings/data/', views.earnings_data, name='earnings_data'),
]