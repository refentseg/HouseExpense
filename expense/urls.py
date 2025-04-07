from django.urls import path

from expense import views

"""
URL configuration for the House Expense app.

This module defines the URL patterns and their corresponding views.

:app_name: Namespace for reversing URLs specific to the House Expense app.
:routes:
    - '' → Home page / index view.
    - 'expense/' → List of all expenses.
    - 'expense/add/' → Form to add a new expense.
    - 'expense/edit/<int:expense_id>/' → Edit an existing expense.
    - 'expense/delete/<int:expense_id>/' → Delete an existing expense.
    - 'expense/report/pdf' → Generate a PDF report of expenses.
"""

app_name = 'expense'
urlpatterns = [
    path('', views.index, name='index'),
    path('expense/', views.expense_list, name='expense_list'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/edit/<int:expense_id>/',
         views.edit_expense, name='edit_expense'),
    path('expense/delete/<int:expense_id>/',
         views.delete_expense, name='delete_expense'),
    path('expense/report/pdf', views.generate_report, name='generate_report'),
]
