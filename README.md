# Recipe App

A Django-based web application for discovering, saving, and analyzing recipes. This application provides a modern, user-friendly interface for managing your recipe collection with advanced search and analytics capabilities.

## Features

### Core Functionality
- User authentication system with login/logout functionality
- Recipe browsing with detailed view support
- Personal recipe collection management
- Advanced recipe search capabilities
- Data visualization and analytics

### Search Features
- Filter recipes by title
- Search by ingredients (comma-separated)
- Filter by difficulty level (1-5 scale)
- Adjustable cooking time range (0-360 minutes)

### Analytics Dashboard
- Most common ingredients analysis
- Difficulty distribution visualization
- Cooking time distribution analysis
- Multiple chart types (Bar, Pie, Line)

### User Features
- Save favorite recipes
- Personal recipe collection view
- Responsive design for all devices

## Technical Stack

- **Backend**: Django 4.2.17
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript
- **Data Visualization**: Matplotlib
- **Image Handling**: Django ImageField
- **Authentication**: Django built-in auth

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd recipe-app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
pip install matplotlib
pip install pandas
pip install Pillow
```

4. Configure the environment:
- Create a `.env` file in the root directory
- Add your secret key and other environment variables

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Create required directories:
```bash
mkdir media
mkdir static
mkdir staticfiles
```

8. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

```
recipe_app/
├── manage.py
├── recipe_app/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── recipes/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils.py
│   └── tests.py
├── static/
│   └── styles.css
├── media/
│   └── recipes/
└── templates/
    ├── auth/
    │   ├── login.html
    │   └── success.html
    └── recipes/
        ├── analytics.html
        ├── detail.html
        ├── main.html
        ├── my_recipes.html
        └── recipes_home.html
```

## Models

### Recipe Model
- `name`: CharField (max_length=120)
- `ingredients`: TextField
- `cooking_time`: IntegerField
- `difficulty`: CharField
- `pic`: ImageField
- `saved_by`: ManyToManyField (User)

## Testing

The application includes comprehensive tests covering:
- Model functionality
- Form validation
- View behavior
- User authentication
- Search functionality
- Analytics features

Run the test suite with:
```bash
python manage.py test
```

## Security Considerations

- CSRF protection enabled
- User authentication required for sensitive operations
- Image upload validation
- Form data validation
- Django security middleware enabled

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.