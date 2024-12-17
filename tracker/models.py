from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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