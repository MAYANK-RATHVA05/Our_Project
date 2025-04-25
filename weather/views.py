from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from decimal import Decimal
import json

from .models import UserProfile, FavoriteLocation
from .utils import get_weather_data

# Home view
def home(request):
    """
    Display the home page with weather search form and map
    """
    context = {}
    
    # If user is logged in, fetch their favorite locations
    if request.user.is_authenticated:
        favorite_locations = FavoriteLocation.objects.filter(user=request.user).order_by('-created_at')
        context['favorite_locations'] = favorite_locations
        
    return render(request, 'weather/home.html', context)

# Weather search view
def weather_search(request):
    """
    Handle weather search form submission
    """
    if request.method == 'POST':
        location = request.POST.get('location', '')
        
        if location:
            # Get weather data from API
            weather_data = get_weather_data(location=location)
            
            if weather_data.get('error'):
                messages.error(request, weather_data.get('message'))
                return redirect('home')
            
            # Pass weather data to template
            context = {
                'weather_data': weather_data,
            }
            
            # Add favorite locations for logged in users
            if request.user.is_authenticated:
                favorite_locations = FavoriteLocation.objects.filter(user=request.user).order_by('-created_at')
                context['favorite_locations'] = favorite_locations
            
            return render(request, 'weather/home.html', context)
        
        else:
            messages.error(request, 'Please enter a location.')
            return redirect('home')
    
    # If not POST, redirect to home
    return redirect('home')

# Get weather by coordinates (for map clicks)
def get_weather(request):
    """
    Get weather data based on latitude and longitude
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if lat and lon:
        # Get weather data from API
        weather_data = get_weather_data(lat=lat, lon=lon)
        
        if weather_data.get('error'):
            messages.error(request, weather_data.get('message'))
            return redirect('home')
        
        # Pass weather data to template
        context = {
            'weather_data': weather_data,
        }
        
        # Add favorite locations for logged in users
        if request.user.is_authenticated:
            favorite_locations = FavoriteLocation.objects.filter(user=request.user).order_by('-created_at')
            context['favorite_locations'] = favorite_locations
        
        return render(request, 'weather/home.html', context)
    
    messages.error(request, 'Invalid coordinates.')
    return redirect('home')

# Map view 
def map_view(request):
    """
    Display a full page map for selecting locations
    """
    return render(request, 'weather/map.html')

# User registration view
def register(request):
    """
    Handle user registration
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Also save email if provided
            email = request.POST.get('email')
            if email:
                user.email = email
                user.save()
            
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

# User profile view
@login_required
def profile_view(request):
    """
    Display user profile page
    """
    user = request.user
    favorite_locations = FavoriteLocation.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user': user,
        'favorite_locations': favorite_locations,
    }
    
    return render(request, 'authentication/profile.html', context)

# Profile update view
@login_required
def profile_update(request):
    """
    Handle profile update form submission
    """
    if request.method == 'POST':
        user = request.user
        
        # Update email
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update profile
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.default_location = request.POST.get('default_location', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')

# Password change view
@login_required
def change_password(request):
    """
    Handle password change form submission
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'authentication/change_password.html', {'form': form})

# Save location to favorites
@login_required
def save_location(request):
    """
    Save a location to user's favorites
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if name and latitude and longitude:
            # Check if this location already exists for the user
            existing_location = FavoriteLocation.objects.filter(
                user=request.user,
                name=name
            ).first()
            
            if existing_location:
                messages.info(request, f'"{name}" is already in your favorites.')
            else:
                # Create new favorite location
                FavoriteLocation.objects.create(
                    user=request.user,
                    name=name,
                    latitude=Decimal(latitude),
                    longitude=Decimal(longitude)
                )
                messages.success(request, f'"{name}" added to your favorites!')
        
        else:
            messages.error(request, 'Invalid location data.')
    
    return redirect('home')

# Delete location from favorites
@login_required
def delete_location(request, location_id):
    """
    Delete a location from user's favorites
    """
    location = get_object_or_404(FavoriteLocation, id=location_id, user=request.user)
    name = location.name
    location.delete()
    
    messages.success(request, f'"{name}" removed from your favorites.')
    
    # Redirect back to the page that called this view
    referer = request.META.get('HTTP_REFERER')
    if referer and 'profile' in referer:
        return redirect('profile')
    return redirect('home')

# Set default location
@login_required
def set_default_location(request, location_id):
    """
    Set a favorite location as the default location
    """
    location = get_object_or_404(FavoriteLocation, id=location_id, user=request.user)
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    profile.default_location = location.name
    profile.save()
    
    messages.success(request, f'"{location.name}" set as your default location.')
    
    # Redirect back to the page that called this view
    referer = request.META.get('HTTP_REFERER')
    if referer and 'profile' in referer:
        return redirect('profile')
    return redirect('home')
