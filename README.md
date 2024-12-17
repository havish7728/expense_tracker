# Expense Tracker

## Overview

The Expense Tracker is a web application built with Django that helps users track their expenses. Users can add, remove, and view expenses categorized under different types. This project also includes user authentication with the ability to register, log in, and log out.

## Features

- **User Registration**: Users can create an account to securely log in and manage their expenses.
- **Login & Logout**: Secure login and logout functionality.
- **Expense Management**: Users can add, view, and remove expenses.
- **Category Management**: Users can create expense categories for better organization.
- **Dashboard**: The dashboard displays all user expenses along with the total expense.

## Technologies Used

- **Backend**: Django (Python web framework)
- **Frontend**: HTML, CSS (Custom styles for better UI)
- **Database**: MySQL
- **Authentication**: Django’s built-in authentication system (login, logout, registration)

## Installation

Follow these steps to run the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin) to access the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to:

   ```
   http://127.0.0.1:8000/
   ```

## Usage

- **Home Page**: The home page allows users to log in or register an account.
- **Login**: Users must log in to access their expense dashboard and manage expenses.
- **Dashboard**: Displays the user's expenses, total expense, and options to add/remove expenses.
- **Add Expense**: Users can add a new expense along with a description, amount, and category.
- **Add Category**: Users can create new categories for their expenses.

## Endpoints

- **`/`**: Redirects to the dashboard if logged in, otherwise shows the home page.
- **`/login/`**: Login page where users can authenticate.
- **`/register/`**: Registration page for creating a new account.
- **`/add-expense/`**: Page to add a new expense.
- **`/add-category/`**: Page to add a new expense category.
- **`/remove-expense/<expense_id>/`**: Removes an expense based on its ID.
- **`/logout/`**: Logs the user out and redirects to the home page.
