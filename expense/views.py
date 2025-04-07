from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from expense.forms import ExpenseForm
from expense.models import Category, Expense

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import datetime

# Create your views here.


@login_required
def index(request):
    """
    Displays the dashboard home page with expense summary data.

    Calculates the total expenses and breaks down expenses by category,
    including percentage calculations and color assignments for visualization.
  
    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :returns: HttpResponse object with the rendered home template
    :rtype: HttpResponse
    """
    # Total expenses
    total_expenses = Expense.objects.aggregate(
        total=Sum('amount'))['total'] or 0

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
    # Loops each expense category
    for i, category in enumerate(expenses_category):
        if category.total_amount and total_expenses > 0:
            # Calculate percentage
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

    # Context dictionary to pass data to the template
    context = {
        'total_expenses': total_expenses,
        'categories': percentage_list,
    }
    #
    return render(request, 'expense/home.html', context)


@login_required
def expense_list(request):
    """
    Displays a list of all expenses ordered by paid date (most recent first).

    Retrieves all expense records from the database and calculates the total
    sum of all expenses.

    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :returns: HttpResponse object with the rendered expense list template
    :rtype: HttpResponse
    """
    # Gets all expenses
    expenses_list = Expense.objects.order_by('-paid_date')

    # Calculate the total sum of all expenses
    total_expenses = expenses_list.aggregate(total=Sum('amount'))['total'] or 0

    # Context dictionary to pass data to the template
    context = {'expenses_list': expenses_list,
               'total_expenses': total_expenses}

    # Display expense.html template to user with context data
    return render(request, 'expense/expense.html', context)


@login_required
def add_expense(request):
    """
    Handles the creation of a new expense record.

    Processes the form submission when POST request is received.
    If form is valid, saves the new expense and redirects to the expense list.
    For GET requests, displays an empty expense form.

    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :returns: HttpResponse with form for GET or redirect to expense list for
    valid POST
    :rtype: HttpResponse
    """
    # Checks if request is a POST
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        # Checks if form is valid
        if form.is_valid():
            form.save()
            # Dislay expense list to user
            return HttpResponseRedirect(
                reverse('expense:expense_list')
            )
    else:
        form = ExpenseForm()

    # Display form to user
    return render(request, 'expense/form.html', {
        'form': form,  # Pass the form instance to the template
        'title': 'Add Expense'  # Set Page title
        })


@login_required
def edit_expense(request, expense_id):
    """
    Handles editing of an existing expense record.

    Retrieves the specified expense and processes the form submission
    when POST request is received. If form is valid, updates the expense
    and redirects to the expense list. For GET requests, displays a form
    pre-populated with the expense data.

    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :param expense_id: Primary key of the expense to edit
    :type expense_id: int
    :returns: HttpResponse with form for GET or redirect to expense list for
    valid POST
    :rtype: HttpResponse
    :raises: Http404 if expense with given ID does not exist
    """
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        # Checks if form is valid
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('expense:expense_list')
            )
    else:
        form = ExpenseForm(instance=expense)

    # Display form to user
    return render(request, 'expense/form.html', {
        'form': form,   # Pass the form instance
        'title': 'Edit Expense',  # Set Page title
        'expense': expense  # Pass the existing expense object
        })


@login_required
def delete_expense(request, expense_id):
    """
    Handles deletion of an existing expense record.

    Retrieves the specified expense and deletes it when a POST request
    is received. For GET requests, displays a confirmation form.

    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :param expense_id: Primary key of the expense to delete
    :type expense_id: int
    :returns: HttpResponse with confirmation form for GET or redirect to
    expense list for POST
    :rtype: HttpResponse
    :raises: Http404 if expense with given ID does not exist
    """
    # Get the expense object by primary key
    # If its not found return 404 not found
    expense = get_object_or_404(Expense, pk=expense_id)

    # Checks if request is a POST
    if request.method == 'POST':
        # delete expense object
        expense.delete()
        # Display Expense List Page
        return HttpResponseRedirect(
            reverse('expense:expense_list')
        )
    # Display form to user
    return render(request, 'expense/form.html', {'expense': expense})


def generate_report(request):
    """
    Generates a PDF report of all expenses.

    Creates a PDF document using ReportLab that includes a table of
    all expenses with their details and a calculated total.
    The PDF is returned as an attachment for download.

    :param request: HttpRequest object containing metadata about the request
    :type request: HttpRequest
    :returns: HttpResponse containing the generated PDF as an attachment
    :rtype: HttpResponse
    """
    # Create HttpResponse with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create the PDF object using ReportLab
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Container for elements to be added to the PDF
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']

    # Add report title
    elements.append(Paragraph("Expense Report", title_style))
    elements.append(Spacer(1, 0.5*cm))

    # Add generation date
    date_text = f'''
    Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}'''
    elements.append(Paragraph(date_text, normal_style))
    elements.append(Spacer(1, 0.5*cm))

    # Gets all expenses
    expenses_list = Expense.objects.order_by('-paid_date')

    # Calculate the total sum of all expenses
    total_expenses = expenses_list.aggregate(total=Sum('amount'))['total'] or 0

    # Create data for the table
    data = [['Date', 'Item', 'Category', 'Amount']]  # Header row

    # Add expense data to table
    for expense in expenses_list:
        data.append([
            expense.paid_date.strftime('%Y-%m-%d'),
            expense.title,
            expense.category.name,
            f"R {expense.amount:.2f}",
        ])

    # Add total row
    data.append(['', '', 'Total: ', f"R {total_expenses:.2f}"])

    # https://docs.reportlab.com/reportlab/userguide/ch7_tables/
    # Create table
    table = Table(data, colWidths=[3*cm, 6*cm, 3*cm, 3*cm])

    # Style the table
    table_style = TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Body styling
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Total row styling
        ('BACKGROUND', (0, -1), (-1, -1), colors.darkgreen),  # Dark green
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),       # White text
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

        # All cells
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.black),
    ])

    table.setStyle(table_style)
    elements.append(table)

    # Add footnote
    elements.append(Spacer(1, 1*cm))
    footnote = "This is an automatically generated report."
    elements.append(Paragraph(footnote, normal_style))

    # Build the PDF
    doc.build(elements)
    return response
