# Gamila Recipe App

A Django-powered web application for exploring, saving, and sharing Moroccan recipes.

## About

Gamila is a feature-rich recipe application focused on Moroccan cuisine, providing users with an intuitive platform to discover traditional recipes, save favorites, and explore cooking techniques. The application combines a user-friendly interface with powerful search and filtering capabilities, making it easy for users to find recipes based on ingredients, difficulty level, and cooking time.

## Key Features

- **Public Recipe Access**: Browse all recipes without login requirements
- **User Accounts**: Optional registration for saving favorites and personalization
- **Advanced Search**: Find recipes by title, ingredients, difficulty level, or cooking time
- **Detailed Recipe Pages**: Complete with ingredients, steps, cooking times, and difficulty ratings
- **Favorites System**: Save recipes to your personal collection
- **Responsive Design**: Optimized for all screen sizes and devices
- **Analytics Dashboard**: Visual data representations of recipe metrics

## Project Structure

```
recipe-app/
├── src/                    # Main source code
│   ├── gamila/             # Project settings
│   ├── recipes/            # Recipe app
│   │   ├── migrations/     # Database migrations
│   │   ├── templates/      # HTML templates
│   │   ├── static/         # CSS, JS, images
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View controllers
│   │   ├── urls.py         # URL routing
│   │   ├── forms.py        # Form definitions
│   │   ├── admin.py        # Admin configuration
│   │   └── tests.py        # Unit tests
│   ├── users/              # User authentication app
│   ├── analytics/          # Data visualization app
│   └── manage.py           # Django management script
├── static/                 # Collected static files
├── media/                  # User-uploaded content
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Technical Stack

- **Backend**:
  - Python 3.9+
  - Django 3.2 LTS
  - SQLite (development) / PostgreSQL (production)
  - Django REST Framework for API endpoints

- **Frontend**:
  - HTML5 / CSS3
  - JavaScript
  - Bootstrap 5
  - HTMX for interactive elements

- **Data Visualization**:
  - Matplotlib
  - Pandas for data processing
  - Chart.js for interactive charts

- **Development Tools**:
  - Git for version control
  - Black for code formatting
  - Django Debug Toolbar

## Models

### Recipe Model
```python
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField(help_text="In minutes")
    difficulty = models.CharField(
        max_length=20, 
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    )
    image = models.ImageField(upload_to='recipe_images/')
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    region = models.CharField(max_length=100, blank=True)
    preparation_time = models.IntegerField(help_text="In minutes", default=0)
    servings = models.IntegerField(default=4)
```

### User Profile Model
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    favorite_recipes = models.ManyToManyField(Recipe, blank=True, related_name='favorited_by')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    preferred_cuisine = models.CharField(max_length=100, blank=True)
```

## Features In Detail

### Public Access
- Browse all recipes without login
- View detailed recipe information
- Search and filter recipes
- View analytics and trends

### User Features
- Create and manage personal account
- Save favorite recipes
- Rate and review recipes
- Submit recipe suggestions (pending approval)
- Personalized dashboard

### Admin Features
- Content management system
- User management
- Analytics dashboard
- Recipe approval workflow
- Category and tag management

## Getting Started

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/ambrosia-fish/recipe-app.git
   cd recipe-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python src/manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python src/manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python src/manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

### Using Docker (Optional)

1. Make sure Docker and Docker Compose are installed
2. Run `docker-compose up`
3. Visit http://localhost:8000

## Testing

Run the test suite with:
```bash
python src/manage.py test
```

## Deployment

The application is configured for deployment to:
- Heroku
- PythonAnywhere
- DigitalOcean App Platform

See the `deployment.md` file (if available) for detailed deployment instructions.

## Contributing

We welcome contributions! Please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is open source and available under the [MIT License](LICENSE).

## About Moroccan Cuisine

Moroccan cuisine is known for its diverse flavors, aromatic spices, and unique cooking techniques. The recipes in this application showcase traditional dishes from various regions of Morocco, featuring tagines, couscous, pastries, and more.
