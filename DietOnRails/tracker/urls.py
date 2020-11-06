from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('createuser/', views.create_user, name='create-user'),
	path('savedfoods/', views.saved_foods, name='saved-foods'),
]


### For testing API endpoints
urlpatterns += [
	path('nutrients', views.item_lookup_nutrients, name='nutrients'),
	path('search/<query>/', views.item_search, name='search')
]