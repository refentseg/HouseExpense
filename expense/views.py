from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from expense.forms import ExpenseForm
from expense.models import Category, Expense

# Create your views here.

@login_required
def index(request):
    # Total expenses
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    # Expense per category 
    expenses_category = Category.objects.annotate(
        total_amount=Sum('expense__amount')
    )

    # Adding colors
    COLORS = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#6C757D'
    ]

    percentage_list = []
    # Loopss each expense category
    for i,category in enumerate(expenses_category):
        if category.total_amount and total_expenses > 0:
            percentage = (category.total_amount / total_expenses) * 100
        else:
            percentage = 0

        color = COLORS[i % len(COLORS)]
        
        # Add object to list
        percentage_list.append({
            'name': category.name,
            'total_amount': category.total_amount or 0,
            'percentage': round(percentage, 2),  # rounding of to 2 deceimals
            'color': color
        })

    context = {
        'total_expenses': total_expenses,
        'categories': percentage_list,
    }
    # Get percentage of total expense
    return render(request, 'expense/home.html', context)


@login_required
def expense_list(request):
    # Gets all expenses
    expenses_list = Expense.objects.order_by('-paid_date')

    # total expenses calculation
    total_expenses = expenses_list.aggregate(total=Sum('amount'))['total'] or 0

    context = {'expenses_list': expenses_list, 'total_expenses': total_expenses}
    return render(request, 'expense/expense.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # Checks if form is valid
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(
            reverse('expense:expense_list')         
            )
    else:
        form = ExpenseForm()
    
    return render(request, 'expense/form.html', {
        'form': form,
        'title': 'Add Expense'})


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk = expense_id)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        # Checks if form is valid
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(
            reverse('expense:expense_list')         
            )
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expense/form.html', {
        'form': form,
        'title': 'Edit Expense',
        'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk = expense_id)
    
    if request.method == 'POST':
        expense.delete()
        return  HttpResponseRedirect(
        reverse('expense:expense_list')         
        )
    
    return render(request, 'expense/form.html', {'expense': expense})