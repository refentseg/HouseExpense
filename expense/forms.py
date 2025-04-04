# https://docs.djangoproject.com/en/5.1/topics/forms/

from django import forms

from expense.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'title', 'amount', 'paid_date']
        widgets = {
            'paid_date': forms.DateInput(attrs={'class': 'form-control',
                                                'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'placeholder': 'Amount',
                                               'step': '0.01'})
        }
