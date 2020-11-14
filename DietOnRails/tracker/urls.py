from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('createuser/', views.create_user, name='create-user'),
	path('savedfoods/', views.saved_foods, name='saved-foods'),
	path('foodsearch/', views.food_search, name='food-search'),
	path('addfood/<food_query_string>/', views.add_food, name='add-food'),
	path('deletefood/<food_name>/', views.delete_saved_food, name='delete-food'),
	path('addfoodgroup/', views.add_food_group, name='add-food-group'),
	path('deletegroup/<group_name>/', views.delete_food_group, name='delete-group'),
]