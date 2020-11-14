from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

from .models import FoodGroup, SavedFood


class CreateUserForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
	email = forms.EmailField(max_length=254, help_text="Required")

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AddSavedFoodForm(forms.Form):
	"""
	Searches the food API for a single food item.
	"""
	query = forms.CharField(
		label='Save a new food', 
		max_length=75, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control mr-sm-2', 
				'type': 'text', 
				'placeholder': 'Search',
				'aria-label': 'Search'
			}
		)
	)

	food_type = forms.ChoiceField(
		label='Food type',
		widget=forms.RadioSelect(),
		choices=[('1', 'Brand Name Only'), ('2', 'USDA Common Foods Only'), ('0', 'Both')],
		required=False
	)


class AddFoodGroupForm(forms.Form):
	"""
	Determines the saved food items/groups and the number of servings of each to
		use in the new food group.
	"""
	name = forms.CharField(
		max_length=60,
		required=True,
		label='name'
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(AddFoodGroupForm, self).__init__(*args, **kwargs)

		# Dynamically creates a field for each food or group the user has
		for food in user.saved_foods.all():
			self.fields[f'serving_{food.pk}'] = forms.FloatField(
				required=True,
				min_value=0,
				label=f'{food.serving_unit} | {food}',
				initial=0,
				widget=forms.NumberInput(attrs={'style': 'width:4em;'})
			)
		for group in user.grouped_foods.all():
			self.fields[f'serving_{group.pk}'] = forms.FloatField(
				required=True,
				min_value=0,
				label=f'serving(s) | {group}',
				initial=0,
				widget=forms.NumberInput(attrs={'style': 'width:4em;'})
			)