from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Represents an expense category.

    :ivar name: The unique name of the category.
    :vartype name: str
    """
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Returns the name of the category.

        :returns: The name of the category.
        :rtype: str
        """
        return self.name


class Expense(models.Model):
    """"
    Represents an individual expense entry.

    :ivar category: The category this expense belongs to.
    :vartype category: Category
    :ivar title: A short description of the expense.
    :vartype title: str
    :ivar amount: The monetary value of the expense.
    :vartype amount: Decimal
    :ivar paid_date: The date the expense was paid.
    :vartype paid_date: datetime.date
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField('date paid')

    def __str__(self):
        """
        Returns a string summarizing the expense.

        :returns: A string in the format "<amount> on <paid_date>".
        :rtype: str
        """
        return f"{self.amount} on {self.paid_date}"
