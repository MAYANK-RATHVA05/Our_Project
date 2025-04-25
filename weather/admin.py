from django.contrib import admin
from .models import UserProfile, FavoriteLocation

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_location')
    search_fields = ('user__username', 'default_location')
    list_filter = ('user',)

class FavoriteLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FavoriteLocation, FavoriteLocationAdmin)
