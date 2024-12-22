from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta,datetime

class Category(models.Model):
    name=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField()

    def __str__(self):
        return f"{self.description}-->{self.amount}"

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now = timezone.now()  # Use timezone-aware current time
        expiration_time = now + timedelta(minutes=5)
        print(f"Current time: {now}, Expiration time: {expiration_time}, Valid: {now <= expiration_time}")  # Debug output
        return now <= expiration_time