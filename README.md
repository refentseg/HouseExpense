# HouseExpense

A web application for tracking and managing household expenses.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)

## Description
HouseExpense simplifies household expense management through an intuitive web interface. This Django-based application allows users to track spending

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/HouseExpense.git
cd HouseExpense
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
```bash
python manage.py migrate
# Create migration files for your app
python manage.py makemigrations {name} # Can use name of choice e.g expense

# View the SQL that would be executed for the migration
python manage.py sqlmigrate {name} 0001

# Apply the migrations to the database
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at `http://127.0.0.1:8000/`

## Usage
### Getting Started
1. You are asked to login first or register

![Login Page]()

2. From Home Page Dashboard you can view expenses list
3. The dashboard allows you to Add/Edit or Delete expenses

### Dashboard Overview
The dashboard provides a pie chart visualization of your expenses by category (WiFi, Rent, Water).

![Expense Dashboard]()

### Viewing Expenses
The Expenses page displays a table with all your recorded expenses, showing Date, Title, Category, and Price for each entry.

![View Expenses]()

### Adding New Expenses
The Add Expense form lets you enter:
- Category (dropdown selection)
- Title
- Amount
- Date (with calendar picker)

![Add Expense Form]()

### Editing and Deleting Expenses
From the expenses list view:
1. Select any expense to edit its details
2. Use the delete option to remove unwanted expense records
3. Changes are saved immediately to the database


## Credits
- Developer: [Refentse Gaonnwe](https://github.com/refentseg)
