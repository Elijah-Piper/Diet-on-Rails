from django import template

register = template.Library()

@register.filter
def value_from_model_field(field, model):
	return field.value_from_object(model)

@register.filter
def underscores_begone(string):
	readable_string = ""
	for char in string:
		if char == "_":
			readable_string += " "
		else:
			readable_string += char

	return readable_string