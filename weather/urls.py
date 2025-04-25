from django.urls import path
from . import views

urlpatterns = [
    # Weather information views
    path('search/', views.weather_search, name='weather_search'),
    path('location/', views.get_weather, name='get_weather'),
    path('map/', views.map_view, name='map_view'),
    
    # User profile views
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Favorite location management
    path('locations/save/', views.save_location, name='save_location'),
    path('locations/delete/<int:location_id>/', views.delete_location, name='delete_location'),
    path('locations/set-default/<int:location_id>/', views.set_default_location, name='set_default_location'),
    
    # Authentication views (custom ones beyond Django's auth)
    path('register/', views.register, name='register'),
]

