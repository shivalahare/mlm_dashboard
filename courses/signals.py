from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase, Incentive

@receiver(post_save, sender=Purchase)
def handle_purchase_completion(sender, instance, created, **kwargs):
    """Signal to handle additional tasks after purchase completion"""
    if created:
        # Add any additional purchase completion logic here
        pass

@receiver(post_save, sender=Incentive)
def handle_incentive_creation(sender, instance, created, **kwargs):
    """Signal to handle notifications or tasks after incentive creation"""
    if created:
        # Add notification or other logic for new incentives
        pass