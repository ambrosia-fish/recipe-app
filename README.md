# Gamila Recipe App

A web application for exploring and saving Moroccan recipes.

## About This Version

This version (in the `refresh` branch) has been updated to make the recipe app fully public, with no login requirement to browse recipes. Authentication is still available for users who want to save their favorite recipes.

### Key Features

- Browse all recipes without login requirements
- Search recipes by title, ingredients, difficulty level, and cooking time
- View recipe details with ingredients and cooking information
- Create a user account to save favorite recipes
- Analytics page to visualize recipe data

### Technical Updates

- Removed authentication requirements from recipe browsing views
- Updated templates to handle both authenticated and non-authenticated users
- Modified save functionality to prompt for login when needed
- Improved navigation and user experience
- Responsive design for all screen sizes

## Technical Stack

- Python/Django
- HTML/CSS
- JavaScript
- SQLite database
- Matplotlib for data visualization

## Getting Started

To run this application locally:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python src/manage.py migrate`
6. Start the server: `python src/manage.py runserver`
7. Visit http://127.0.0.1:8000/ in your browser

## License

This project is open source.
