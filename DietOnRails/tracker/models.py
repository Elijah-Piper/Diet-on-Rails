from django.contrib.auth.models import User
from django.db import models


class SavedFood(models.Model):
	"""
	A user-specific cached food item from the food API.
	Goes by a (either default or set) name.
	Encapsulates individual food items nutritional data.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_foods')

	name = models.CharField(max_length=60)
	brand_name = models.CharField(max_length=60, null=True)
	serving_qty = models.FloatField()
	serving_unit = models.CharField(max_length=20)
	serving_weight = models.IntegerField()
	calories = models.IntegerField()
	total_fat = models.IntegerField()
	saturated_fat = models.IntegerField()
	cholesterol = models.IntegerField()
	sodium = models.IntegerField()
	total_carbs = models.IntegerField()
	fiber = models.IntegerField()
	sugars = models.IntegerField()
	protein = models.IntegerField()
	potassium = models.IntegerField()

	class Meta:
		ordering = ['name']

	def __str__(self):
		return name


class FoodGroup(models.Model):
	"""
	A user-specific grouping of (SavedFood instances or other FoodGroup instances).
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grouped_foods')

	# Collection of individual foods encapulated by this group
	grouped_foods = models.ManyToManyField(SavedFood, related_name='foods')
	# Collection of other food groups encapsulated by this group
	grouped_groups = models.ManyToManyField('self', related_name='groups')

	name = models.CharField(max_length=60)
	# Totals evaluted from the ManytoMany relationships
	serving_weight = models.IntegerField()
	calories = models.IntegerField()
	total_fat = models.IntegerField()
	saturated_fat = models.IntegerField()
	cholesterol = models.IntegerField()
	sodium = models.IntegerField()
	total_carbs = models.IntegerField()
	fiber = models.IntegerField()
	sugars = models.IntegerField()
	protein = models.IntegerField()
	potassium = models.IntegerField()

	def __str__(self):
		return name


class FoodLog(FoodGroup):
	"""
	A user-specific, day-specific grouping of FoodGroup and/or SavedFood instances.
	Inherits from FoodGroup model.
	Functions like a food group, but is associated with a specific date
	"""
	date = models.DateField()

	# Is '{date} - {username}'
	# This is a unique identifier; each user has only one log per given day
	identifier = models.CharField(max_length=60, primary_key=True)