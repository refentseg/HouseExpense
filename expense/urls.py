from django.urls import path

from expense import views

app_name = 'expense'
urlpatterns = [
    path('', views.index, name='index'),
    path('expense/', views.expense_list, name='expense_list'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/edit/<int:expense_id>/',
         views.edit_expense, name='edit_expense'),
    path('expense/delete/<int:expense_id>/',
         views.delete_expense, name='delete_expense'),
]