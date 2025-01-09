from django import forms

DIFFICULTY_CHOICES = (          
   ('5', '5'),
   ('4', '4'),
   ('3', '3'),
   ('2', '2'),
   ('1', '1')
)

class RecipesSearchForm(forms.Form): 
   recipe_title = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter recipe title'
        }),
        required=False,
    )
   recipe_ingredients = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ingredients separated by commas'
        }),
        help_text='Separate ingredients with commas (e.g., salt, pepper, olive oil)'
    )
   difficulty_level = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        label='Max Difficulty'
    )
   cooking_time = forms.IntegerField(
        min_value=0,
        max_value=360,
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'step': '5',
                'class': 'form-range',
                'oninput': 'this.nextElementSibling.value = this.value + " minutes"',
                'list': 'tickmarks'
            }
        ),
        initial=360
    )
   
   def clean_recipe_ingredients(self):
        ingredients = self.cleaned_data.get('recipe_ingredients', '')
        if ingredients:
            ingredients_list = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
            return ','.join(ingredients_list)
        return ingredients
   
   def clean_recipe_title(self):
        title = self.cleaned_data.get('recipe_title', '')
        if title:  # Only validate if a title was provided
            if len(title.strip()) < 3:
                raise forms.ValidationError("Recipe title must be at least 3 characters long")
            return title.strip()
        return title  # Return empty string if no title provided