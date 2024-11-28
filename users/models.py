from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    is_agent = models.BooleanField(default=False)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    
    def get_downline(self):
        """Returns all users in the downline (directly and indirectly referred)"""
        downline = set()
        queue = list(self.referrals.all())
        
        while queue:
            referral = queue.pop(0)
            downline.add(referral)
            queue.extend(referral.referrals.all())
            
        return downline