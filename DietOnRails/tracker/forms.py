from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 


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
		choices=[('0', 'Both'), ('1', 'Brand Name'), ('2', 'USDA Common')]
	)