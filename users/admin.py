from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_agent', 'referrer')
    list_filter = ('is_agent', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('MLM Info', {'fields': ('phone_number', 'is_agent', 'referrer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MLM Info', {'fields': ('phone_number', 'is_agent', 'referrer')}),
    )