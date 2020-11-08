from django.contrib import admin

from .models import SavedFood, FoodGroup, FoodLog

# Register your models here.
admin.site.register(SavedFood)
admin.site.register(FoodGroup)
admin.site.register(FoodLog)