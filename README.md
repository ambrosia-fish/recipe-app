# Recipe App

A Django web application for managing and searching recipes. Users can create, store, and search recipes based on ingredients.

## Features
- Recipe creation and storage
- User authentication
- Search recipes by ingredients
- Automatic difficulty calculation
- Admin dashboard for data management

## Setup
1. Create virtual environment:
- `python3 -m venv venv`
- `source venv/bin/activate`

2. Install requirements:
- `pip install django`

3. Run migrations:
- `python manage.py migrate`

4. Create superuser:
- `python manage.py createsuperuser`

5. Run server:
- `python manage.py runserver`

Visit http://127.0.0.1:8000/admin to access admin panel.

## Models
- User: Handles authentication with username, email and password
- Recipe: Stores recipe information including name, ingredients (comma-separated), cooking time and difficulty level

## Running Tests
`python manage.py test`