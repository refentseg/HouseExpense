from django.db import models

# Create your models here. 
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField('date paid')
    

    def __str__(self):
        return f"{self.amount} on {self.paid_date}"
