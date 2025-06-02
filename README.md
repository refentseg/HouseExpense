# HouseExpense

A web application for tracking and managing household expenses.

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](http://http://13.247.174.69)

## Table of Contents
- [Description](#description)
- [Installation](#installation)
    - [Standard Installation](#standard-installation)
    - [Docker Installation](#docker-installation)
- [Usage](#usage)
- [Credits](#credits)

## Description
HouseExpense simplifies household expense management through an intuitive web interface. This Django-based application allows users to track spending

## Installation

### Standard Installation

1. Clone the repository:
```bash
git clone https://github.com/refentseg/HouseExpense.git
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

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/refentseg/HouseExpense.git
cd HouseExpense
```

2. Create a `.env` file (see [Environment Setup](#environment-setup))

3. Build and run the Docker container:
```bash
docker build -t house-expense .
docker run -p 8080:8080 -d house-expense
```

4. Access the application at `http://localhost:8080`

## Environment Setup

1. Create a `.env` file in the project root
   - Generate a secure SECRET_KEY you can use :
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   - Add the generated key to your .env file
   - Check `.env.example` for reference

2. Make sure to include the `.env` file in your `.gitignore`

## Usage
### Getting Started
1. You are asked to login first or register

![Login Page](https://github.com/user-attachments/assets/0a5f3cee-6dbc-450f-a2ff-0b7e4be320ee)

2. From Home Page Dashboard you can view expenses list
3. The dashboard allows you to Add/Edit or Delete expenses

### Dashboard Overview
The dashboard provides a pie chart visualization of your expenses by category (WiFi, Rent, Water).

![Expense Dashboard](https://github.com/user-attachments/assets/2921faf9-69e4-43bc-9f83-a090ab54dbb9)

### Viewing Expenses
The Expenses page displays a table with all your recorded expenses, showing Date, Title, Category, and Price for each entry.

![View Expenses](https://github.com/user-attachments/assets/d0c4f993-52c5-48fa-be77-70903bc117a9)

### Adding New Expenses
The Add Expense form lets you enter:
- Category (dropdown selection)
- Title
- Amount
- Date (with calendar picker)

![Add Expense Form](https://github.com/user-attachments/assets/2fa3bada-d676-4330-ab2b-729e742013c6)

### Editing and Deleting Expenses
![Edit/Delete](https://github.com/user-attachments/assets/480a960c-33b1-45df-9cc9-58eadc0fd8c8)

From the expenses list view:
1. Select &#x270F; to edit its details

![Edit Expense](https://github.com/user-attachments/assets/891af2ee-5da4-4c3f-ae87-502d7c6cd5b0)

3. Use the &#x1F5D1; delete option to remove expense

![Delete Expense](https://github.com/user-attachments/assets/b872d107-44c7-4ce5-bc4a-31862d414519)

5. Changes are saved immediately to the database


## Credits
- Developer: [Refentse Gaonnwe](https://github.com/refentseg)
