from django.contrib import admin
from .models import CoursePackage, Purchase, Incentive

@admin.register(CoursePackage)
class CoursePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__username', 'package__name')

@admin.register(Incentive)
class IncentiveAdmin(admin.ModelAdmin):
    list_display = ('agent', 'purchase', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('agent__username',)