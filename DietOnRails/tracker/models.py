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

	# Serving info
	serving_qty = models.IntegerField()
	serving_unit = models.CharField(max_length=20)
	serving_weight_g = models.IntegerField()
	calories = models.FloatField(help_text="Units: kcal")

	# Fats (Macro)
	total_fat = models.FloatField(help_text="Units: g")
	saturated_fat = models.FloatField(help_text="Units: g")
	monounsaturated_fat = models.FloatField(help_text="Units: g")
	polyunsaturated_fat = models.FloatField(help_text="Units: g")
	omega_3_ala = models.FloatField(help_text="Units: g")
	omega_3_epa = models.FloatField(help_text="Units: g")
	omega_3_dpa = models.FloatField(help_text="Units: g")
	omega_3_dha = models.FloatField(help_text="Units: g")
	omega_3_ete = models.FloatField(help_text="Units: g")
	omega_6_la = models.FloatField(help_text="Units: g")
	omega_6_gla = models.FloatField(help_text="Units: g")
	omega_6_ea = models.FloatField(help_text="Units: g")
	omega_6_dgla = models.FloatField(help_text="Units: g")
	omega_6_aa = models.FloatField(help_text="Units: g")
	cholesterol = models.FloatField(help_text="Units: mg")
	phytosterol = models.FloatField(help_text="Units: mg")

	# Carbohydrates (Macro)
	total_carbs = models.FloatField(help_text="Units: g")
	fiber = models.FloatField(help_text="Units: g")
	total_sugar = models.FloatField(help_text="Units: g")
	added_sugar = models.FloatField(help_text="Units: g")
	fructose = models.FloatField(help_text="Units: g")
	galactose = models.FloatField(help_text="Units: g")
	lactose = models.FloatField(help_text="Units: g")
	dextrose = models.FloatField(help_text="Units: g")
	maltose = models.FloatField(help_text="Units: g")
	starch = models.FloatField(help_text="Units: g")
	sucrose = models.FloatField(help_text="Units: g")

	# Protein/amino acids (Macro)
	total_protein = models.FloatField(help_text="Units: g")
	alanine = models.FloatField(help_text="Units: g")
	arginine = models.FloatField(help_text="Units: g")
	aspartic_acid = models.FloatField(help_text="Units: g")
	cystine = models.FloatField(help_text="Units: g")
	glycine = models.FloatField(help_text="Units: g")
	histidine = models.FloatField(help_text="Units: g")
	hydroxyproline = models.FloatField(help_text="Units: g")
	isoleucine = models.FloatField(help_text="Units: g")
	leucine = models.FloatField(help_text="Units: g")
	lysine = models.FloatField(help_text="Units: g")
	phenylalanine = models.FloatField(help_text="Units: g")
	proline = models.FloatField(help_text="Units: g")
	serine = models.FloatField(help_text="Units: g")
	threonine = models.FloatField(help_text="Units: g")
	tryptophan = models.FloatField(help_text="Units: g")

	# Elemental/mineral nutrients (Micro)
	sodium = models.FloatField(help_text="Units: g")
	potassium = models.FloatField(help_text='Units: mg')
	calcium = models.FloatField(help_text="Units: mg")
	iron = models.FloatField(help_text="Units: mg")
	magnesium = models.FloatField(help_text="Units: mg")
	phosphorus = models.FloatField(help_text="Units: mg")
	manganese = models.FloatField(help_text="Units: mg")
	selenium = models.FloatField(help_text="Units: mg")
	zinc = models.FloatField(help_text="Units: mg")
	copper = models.FloatField(help_text="Units: mg")
	fluoride = models.FloatField(help_text="Units: µg")

	# Vitamins/compound nutrients (Micro)
	folate = models.FloatField(help_text="Units: µg")
	folic_acid = models.FloatField(help_text="Units: µg")
	carotene_a = models.FloatField(help_text="Units: µg")
	carotene_b = models.FloatField(help_text="Units: µg")
	vitamin_d = models.FloatField(help_text="Units: µg")
	vitamin_d2 = models.FloatField(help_text="Units: µg")
	vitamin_d3 = models.FloatField(help_text="Units: µg")
	choline = models.FloatField(help_text="Units: mg")
	betaine = models.FloatField(help_text="Units: mg")
	lycopine = models.FloatField(help_text="Units: µg")
	niacin = models.FloatField(help_text="Units: mg")
	menaquinone_4 = models.FloatField(help_text="Units: Âµg")
	pantothenic_acid = models.FloatField(help_text="Units: mg")
	retinol = models.FloatField(help_text="Units: µg")
	riboflavin = models.FloatField(help_text="Units: mg")
	thiamin = models.FloatField(help_text="Units: mg")
	vitamin_e = models.FloatField(help_text="Units: mg")
	vitamin_b12 = models.FloatField(help_text="Units: Âµg")
	vitamin_b6 = models.FloatField(help_text="Units: mg")
	vitamin_c = models.FloatField(help_text="Units: mg")
	vitamin_k = models.FloatField(help_text="Units: Âµg")

	# Pharmacological
	alcohol = models.FloatField(help_text="Units: g")
	caffeine = models.FloatField(help_text="Units: mg")
	theobromine = models.FloatField(help_text="Units: mg")

	# Biological analysis
	ash = models.FloatField(help_text="Units: g") # Represents mineral content of food
	water = models.FloatField(help_text="Units: g")

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
	# Serving info
	serving_weight_g = models.IntegerField()
	calories = models.FloatField(help_text="Units: kcal")

	# Fats (Macro)
	total_fat = models.FloatField(help_text="Units: g")
	saturated_fat = models.FloatField(help_text="Units: g")
	monounsaturated_fat = models.FloatField(help_text="Units: g")
	polyunsaturated_fat = models.FloatField(help_text="Units: g")
	omega_3_ala = models.FloatField(help_text="Units: g")
	omega_3_epa = models.FloatField(help_text="Units: g")
	omega_3_dpa = models.FloatField(help_text="Units: g")
	omega_3_dha = models.FloatField(help_text="Units: g")
	omega_3_ete = models.FloatField(help_text="Units: g")
	omega_6_la = models.FloatField(help_text="Units: g")
	omega_6_gla = models.FloatField(help_text="Units: g")
	omega_6_ea = models.FloatField(help_text="Units: g")
	omega_6_dgla = models.FloatField(help_text="Units: g")
	omega_6_aa = models.FloatField(help_text="Units: g")
	cholesterol = models.FloatField(help_text="Units: mg")
	phytosterol = models.FloatField(help_text="Units: mg")

	# Carbohydrates (Macro)
	total_carbs = models.FloatField(help_text="Units: g")
	fiber = models.FloatField(help_text="Units: g")
	total_sugar = models.FloatField(help_text="Units: g")
	added_sugar = models.FloatField(help_text="Units: g")
	fructose = models.FloatField(help_text="Units: g")
	galactose = models.FloatField(help_text="Units: g")
	lactose = models.FloatField(help_text="Units: g")
	dextrose = models.FloatField(help_text="Units: g")
	maltose = models.FloatField(help_text="Units: g")
	starch = models.FloatField(help_text="Units: g")
	sucrose = models.FloatField(help_text="Units: g")

	# Protein/amino acids (Macro)
	total_protein = models.FloatField(help_text="Units: g")
	alanine = models.FloatField(help_text="Units: g")
	arginine = models.FloatField(help_text="Units: g")
	aspartic_acid = models.FloatField(help_text="Units: g")
	cystine = models.FloatField(help_text="Units: g")
	glycine = models.FloatField(help_text="Units: g")
	histidine = models.FloatField(help_text="Units: g")
	hydroxyproline = models.FloatField(help_text="Units: g")
	isoleucine = models.FloatField(help_text="Units: g")
	leucine = models.FloatField(help_text="Units: g")
	lysine = models.FloatField(help_text="Units: g")
	phenylalanine = models.FloatField(help_text="Units: g")
	proline = models.FloatField(help_text="Units: g")
	serine = models.FloatField(help_text="Units: g")
	threonine = models.FloatField(help_text="Units: g")
	tryptophan = models.FloatField(help_text="Units: g")

	# Elemental/mineral nutrients (Micro)
	sodium = models.FloatField(help_text="Units: g")
	potassium = models.FloatField(help_text='Units: mg')
	calcium = models.FloatField(help_text="Units: mg")
	iron = models.FloatField(help_text="Units: mg")
	magnesium = models.FloatField(help_text="Units: mg")
	phosphorus = models.FloatField(help_text="Units: mg")
	manganese = models.FloatField(help_text="Units: mg")
	selenium = models.FloatField(help_text="Units: mg")
	zinc = models.FloatField(help_text="Units: mg")
	copper = models.FloatField(help_text="Units: mg")
	fluoride = models.FloatField(help_text="Units: µg")

	# Vitamins/compound nutrients (Micro)
	folate = models.FloatField(help_text="Units: µg")
	folic_acid = models.FloatField(help_text="Units: µg")
	carotene_a = models.FloatField(help_text="Units: µg")
	carotene_b = models.FloatField(help_text="Units: µg")
	vitamin_d = models.FloatField(help_text="Units: µg")
	vitamin_d2 = models.FloatField(help_text="Units: µg")
	vitamin_d3 = models.FloatField(help_text="Units: µg")
	choline = models.FloatField(help_text="Units: mg")
	betaine = models.FloatField(help_text="Units: mg")
	lycopine = models.FloatField(help_text="Units: µg")
	niacin = models.FloatField(help_text="Units: mg")
	menaquinone_4 = models.FloatField(help_text="Units: Âµg")
	pantothenic_acid = models.FloatField(help_text="Units: mg")
	retinol = models.FloatField(help_text="Units: µg")
	riboflavin = models.FloatField(help_text="Units: mg")
	thiamin = models.FloatField(help_text="Units: mg")
	vitamin_e = models.FloatField(help_text="Units: mg")
	vitamin_b12 = models.FloatField(help_text="Units: Âµg")
	vitamin_b6 = models.FloatField(help_text="Units: mg")
	vitamin_c = models.FloatField(help_text="Units: mg")
	vitamin_k = models.FloatField(help_text="Units: Âµg")

	# Pharmacological
	alcohol = models.FloatField(help_text="Units: g")
	caffeine = models.FloatField(help_text="Units: mg")
	theobromine = models.FloatField(help_text="Units: mg")

	# Biological analysis
	ash = models.FloatField(help_text="Units: g") # Represents mineral content of food
	water = models.FloatField(help_text="Units: g")

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