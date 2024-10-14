---

# Django Restaurant Dashboard

This project is a restaurant management system built using Django. It includes features for managing dishes, drivers, and users, as well as user authentication and permissions.

## Features
- User Registration and Authentication (Signup, Login, Logout, Email Verification, Password)
- Email Verification for User Signup, Password Reset Functionality
- Dish Management (CRUD operations for dishes)
- Driver Management (CRUD operations for drivers)
- Review System for Dishes
- Role-based Access Control (Admin, Manager User Group, Regular Groups)

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [License](#license)

## Requirements

Ensure you have the following installed:
- Python 3.12

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/TheRealSeber/Django-MiNI-project.git
cd Django-MiNI-project
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Create a PostgreSQL database (or the equivalent for your DB of choice). Then, apply the migrations:

```bash
python restaurant/manage.py migrate
```

### 5. Create a Manager group

```bash
python restaurant/manage.py create_manager_group
```

### 6. Create a superuser

```bash
python restaurant/manage.py createsuperuser
```

Follow the prompts to set up the superuser account.

## Running the Project

To start the server:

```bash
python restaurant/manage.py runserver
```

Access the app at [http://localhost:8000/](http://localhost:8000/).

## Running Tests

You can run tests using Django's test framework:

```bash
python restaurant/manage.py test dashboard
```

### Running Tests with Coverage

To check test coverage, install `coverage.py`:

```bash
pip install coverage
```

Then, run tests with coverage:

```bash
coverage run --source='.' restaurant/manage.py test dashboard
coverage report
```

## Deployment

To deploy the application, follow these steps:
1. Set up your environment (ensure the necessary packages are installed and environment variables are configured).
2. Set `DEBUG=False` and configure `ALLOWED_HOSTS` in the settings.
3. Use a production-ready web server like Gunicorn or uWSGI.

---
