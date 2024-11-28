from django.db import models
from django.conf import settings

class CoursePackage(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='course_packages/', blank=True)
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    package = models.ForeignKey(CoursePackage, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'package']
        
    def __str__(self):
        return f"{self.user.username} - {self.package.name}"

class Incentive(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incentives')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.agent.username} - {self.amount}"