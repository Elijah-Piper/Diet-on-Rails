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
	brand = models.CharField(max_length=60, null=True)
	image_url = models.URLField(null=True)

	# Serving info
	serving_qty = models.IntegerField()
	serving_unit = models.CharField(max_length=20)
	serving_weight_g = models.IntegerField()
	calories = models.FloatField(help_text="kcal", blank=True, null=True)

	# Fats (Macro)
	total_fat = models.FloatField(help_text="g", blank=True, null=True)
	saturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	monounsaturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	polyunsaturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	trans_fat = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_ala = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_epa = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_dpa = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_dha = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_ete = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_la = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_gla = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_ea = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_dgla = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_aa = models.FloatField(help_text="g", blank=True, null=True)
	cholesterol = models.FloatField(help_text="mg", blank=True, null=True)
	phytosterol = models.FloatField(help_text="mg", blank=True, null=True)

	# Carbohydrates (Macro)
	total_carbs = models.FloatField(help_text="g", blank=True, null=True)
	fiber = models.FloatField(help_text="g", blank=True, null=True)
	total_sugar = models.FloatField(help_text="g", blank=True, null=True)
	added_sugar = models.FloatField(help_text="g", blank=True, null=True)
	fructose = models.FloatField(help_text="g", blank=True, null=True)
	galactose = models.FloatField(help_text="g", blank=True, null=True)
	lactose = models.FloatField(help_text="g", blank=True, null=True)
	dextrose = models.FloatField(help_text="g", blank=True, null=True)
	maltose = models.FloatField(help_text="g", blank=True, null=True)
	starch = models.FloatField(help_text="g", blank=True, null=True)
	sucrose = models.FloatField(help_text="g", blank=True, null=True)

	# Protein/amino acids (Macro)
	total_protein = models.FloatField(help_text="g", blank=True, null=True)
	alanine = models.FloatField(help_text="g", blank=True, null=True)
	arginine = models.FloatField(help_text="g", blank=True, null=True)
	aspartic_acid = models.FloatField(help_text="g", blank=True, null=True)
	cystine = models.FloatField(help_text="g", blank=True, null=True)
	glycine = models.FloatField(help_text="g", blank=True, null=True)
	histidine = models.FloatField(help_text="g", blank=True, null=True)
	hydroxyproline = models.FloatField(help_text="g", blank=True, null=True)
	isoleucine = models.FloatField(help_text="g", blank=True, null=True)
	leucine = models.FloatField(help_text="g", blank=True, null=True)
	lysine = models.FloatField(help_text="g", blank=True, null=True)
	phenylalanine = models.FloatField(help_text="g", blank=True, null=True)
	proline = models.FloatField(help_text="g", blank=True, null=True)
	serine = models.FloatField(help_text="g", blank=True, null=True)
	threonine = models.FloatField(help_text="g", blank=True, null=True)
	tryptophan = models.FloatField(help_text="g", blank=True, null=True)

	# Elemental/mineral nutrients (Micro)
	sodium = models.FloatField(help_text="g", blank=True, null=True)
	potassium = models.FloatField(help_text='mg', blank=True, null=True)
	calcium = models.FloatField(help_text="mg", blank=True, null=True)
	iron = models.FloatField(help_text="mg", blank=True, null=True)
	magnesium = models.FloatField(help_text="mg", blank=True, null=True)
	phosphorus = models.FloatField(help_text="mg", blank=True, null=True)
	manganese = models.FloatField(help_text="mg", blank=True, null=True)
	selenium = models.FloatField(help_text="mg", blank=True, null=True)
	zinc = models.FloatField(help_text="mg", blank=True, null=True)
	copper = models.FloatField(help_text="mg", blank=True, null=True)
	fluoride = models.FloatField(help_text="µg", blank=True, null=True)

	# Vitamins/compound nutrients (Micro)
	folate = models.FloatField(help_text="µg", blank=True, null=True)
	folic_acid = models.FloatField(help_text="µg", blank=True, null=True)
	carotene_a = models.FloatField(help_text="µg", blank=True, null=True)
	carotene_b = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d2 = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d3 = models.FloatField(help_text="µg", blank=True, null=True)
	choline = models.FloatField(help_text="mg", blank=True, null=True)
	betaine = models.FloatField(help_text="mg", blank=True, null=True)
	lycopine = models.FloatField(help_text="µg", blank=True, null=True)
	niacin = models.FloatField(help_text="mg", blank=True, null=True)
	menaquinone_4 = models.FloatField(help_text="µg", blank=True, null=True)
	pantothenic_acid = models.FloatField(help_text="mg", blank=True, null=True)
	retinol = models.FloatField(help_text="µg", blank=True, null=True)
	riboflavin = models.FloatField(help_text="mg", blank=True, null=True)
	thiamin = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_e = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_b12 = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_b6 = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_c = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_k = models.FloatField(help_text="µg", blank=True, null=True)

	# Pharmacological
	alcohol = models.FloatField(help_text="g", blank=True, null=True)
	caffeine = models.FloatField(help_text="mg", blank=True, null=True)
	theobromine = models.FloatField(help_text="mg", blank=True, null=True)

	# Biological analysis
	ash = models.FloatField(help_text="g", blank=True, null=True) # Represents mineral content of food
	water = models.FloatField(help_text="g", blank=True, null=True)

	class Meta:
		ordering = ['name']

	@property
	def fields(self):
		return self._meta.fields
	
	
	def __str__(self):
		if self.brand:
			return f'{self.name} - {self.brand}'
		else:
			return f'{self.name} - USDA'


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
	# Serving info
	serving_weight_g = models.IntegerField()
	calories = models.FloatField(help_text="kcal", blank=True, null=True)

	# Fats (Macro)
	total_fat = models.FloatField(help_text="g", blank=True, null=True)
	saturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	monounsaturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	polyunsaturated_fat = models.FloatField(help_text="g", blank=True, null=True)
	trans_fat = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_ala = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_epa = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_dpa = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_dha = models.FloatField(help_text="g", blank=True, null=True)
	omega_3_ete = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_la = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_gla = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_ea = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_dgla = models.FloatField(help_text="g", blank=True, null=True)
	omega_6_aa = models.FloatField(help_text="g", blank=True, null=True)
	cholesterol = models.FloatField(help_text="mg", blank=True, null=True)
	phytosterol = models.FloatField(help_text="mg", blank=True, null=True)

	# Carbohydrates (Macro)
	total_carbs = models.FloatField(help_text="g", blank=True, null=True)
	fiber = models.FloatField(help_text="g", blank=True, null=True)
	total_sugar = models.FloatField(help_text="g", blank=True, null=True)
	added_sugar = models.FloatField(help_text="g", blank=True, null=True)
	fructose = models.FloatField(help_text="g", blank=True, null=True)
	galactose = models.FloatField(help_text="g", blank=True, null=True)
	lactose = models.FloatField(help_text="g", blank=True, null=True)
	dextrose = models.FloatField(help_text="g", blank=True, null=True)
	maltose = models.FloatField(help_text="g", blank=True, null=True)
	starch = models.FloatField(help_text="g", blank=True, null=True)
	sucrose = models.FloatField(help_text="g", blank=True, null=True)

	# Protein/amino acids (Macro)
	total_protein = models.FloatField(help_text="g", blank=True, null=True)
	alanine = models.FloatField(help_text="g", blank=True, null=True)
	arginine = models.FloatField(help_text="g", blank=True, null=True)
	aspartic_acid = models.FloatField(help_text="g", blank=True, null=True)
	cystine = models.FloatField(help_text="g", blank=True, null=True)
	glycine = models.FloatField(help_text="g", blank=True, null=True)
	histidine = models.FloatField(help_text="g", blank=True, null=True)
	hydroxyproline = models.FloatField(help_text="g", blank=True, null=True)
	isoleucine = models.FloatField(help_text="g", blank=True, null=True)
	leucine = models.FloatField(help_text="g", blank=True, null=True)
	lysine = models.FloatField(help_text="g", blank=True, null=True)
	phenylalanine = models.FloatField(help_text="g", blank=True, null=True)
	proline = models.FloatField(help_text="g", blank=True, null=True)
	serine = models.FloatField(help_text="g", blank=True, null=True)
	threonine = models.FloatField(help_text="g", blank=True, null=True)
	tryptophan = models.FloatField(help_text="g", blank=True, null=True)

	# Elemental/mineral nutrients (Micro)
	sodium = models.FloatField(help_text="g", blank=True, null=True)
	potassium = models.FloatField(help_text='mg', blank=True, null=True)
	calcium = models.FloatField(help_text="mg", blank=True, null=True)
	iron = models.FloatField(help_text="mg", blank=True, null=True)
	magnesium = models.FloatField(help_text="mg", blank=True, null=True)
	phosphorus = models.FloatField(help_text="mg", blank=True, null=True)
	manganese = models.FloatField(help_text="mg", blank=True, null=True)
	selenium = models.FloatField(help_text="mg", blank=True, null=True)
	zinc = models.FloatField(help_text="mg", blank=True, null=True)
	copper = models.FloatField(help_text="mg", blank=True, null=True)
	fluoride = models.FloatField(help_text="µg", blank=True, null=True)

	# Vitamins/compound nutrients (Micro)
	folate = models.FloatField(help_text="µg", blank=True, null=True)
	folic_acid = models.FloatField(help_text="µg", blank=True, null=True)
	carotene_a = models.FloatField(help_text="µg", blank=True, null=True)
	carotene_b = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d2 = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_d3 = models.FloatField(help_text="µg", blank=True, null=True)
	choline = models.FloatField(help_text="mg", blank=True, null=True)
	betaine = models.FloatField(help_text="mg", blank=True, null=True)
	lycopine = models.FloatField(help_text="µg", blank=True, null=True)
	niacin = models.FloatField(help_text="mg", blank=True, null=True)
	menaquinone_4 = models.FloatField(help_text="µg", blank=True, null=True)
	pantothenic_acid = models.FloatField(help_text="mg", blank=True, null=True)
	retinol = models.FloatField(help_text="µg", blank=True, null=True)
	riboflavin = models.FloatField(help_text="mg", blank=True, null=True)
	thiamin = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_e = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_b12 = models.FloatField(help_text="µg", blank=True, null=True)
	vitamin_b6 = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_c = models.FloatField(help_text="mg", blank=True, null=True)
	vitamin_k = models.FloatField(help_text="µg", blank=True, null=True)

	# Pharmacological
	alcohol = models.FloatField(help_text="g", blank=True, null=True)
	caffeine = models.FloatField(help_text="mg", blank=True, null=True)
	theobromine = models.FloatField(help_text="mg", blank=True, null=True)

	# Biological analysis
	ash = models.FloatField(help_text="g", blank=True, null=True) # Represents mineral content of food
	water = models.FloatField(help_text="g", blank=True, null=True)

	def __str__(self):
		return self.name


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