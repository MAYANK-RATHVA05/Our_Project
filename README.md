# Weather App

A Django-based weather application that allows users to check weather conditions for any location on Earth. The app includes user authentication, map-based location selection, and the ability to save favorite locations.

## Features

- **Current Weather Data**: Display temperature, humidity, and wind information
- **Location Selection**:
  - Search for locations by name
  - Select locations using an interactive map
  - Save favorite locations for quick access
- **User Authentication**:
  - User registration and login
  - Profile management
  - Password change functionality
- **Responsive Design**: Works well on both desktop and mobile devices

## Demo

Here's what you can do with Weather App:

1. Check weather for any location using search or map selection
2. Create an account to save your favorite locations
3. View detailed weather information including temperature, humidity, and wind
4. Update your profile and manage your favorite locations

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **APIs**: 
  - OpenWeatherMap API for weather data
  - OpenStreetMap/Nominatim for geocoding and mapping
- **Database**: SQLite (default for development)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Installation

1. **Clone the repository** (or download the source code):
   ```
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```
   pip install django django-bootstrap5 django-crispy-forms requests python-dotenv
   ```

### Configuration

1. **Create a .env file** in the project root directory with the following variables:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

   > **Note**: You need to sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api) to use the weather data feature.

2. **Database setup and migrations**:
   ```
   python manage.py migrate
   ```

3. **Create a superuser** (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

### Running the Application

1. **Start the development server**:
   ```
   python manage.py runserver
   ```

2. **Access the application** in your web browser at:
   ```
   http://127.0.0.1:8000/
   ```

3. **Admin panel** can be accessed at:
   ```
   http://127.0.0.1:8000/admin/
   ```

## API Information

### OpenWeatherMap API

This application uses the [OpenWeatherMap Current Weather API](https://openweathermap.org/current) to fetch weather data. 

- **API Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Documentation**: [OpenWeatherMap API Docs](https://openweathermap.org/api)
- **Rate Limits**: Free plan includes up to 1,000 API calls per day
- **Parameters**:
  - `q`: City name for location search
  - `lat` & `lon`: Coordinates for location-based search
  - `units`: Metric (for Celsius) or Imperial (for Fahrenheit)
  - `appid`: Your API key

## Project Structure

```
weather_app/
├── .env                    # Environment variables
├── manage.py               # Django management script
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── map.js          # Map functionality
├── templates/              # HTML templates
│   ├── authentication/     # User authentication templates
│   └── weather/            # Weather app templates
├── weather/                # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   └── utils.py            # Utility functions
└── weather_app/            # Project settings
    ├── settings.py         # Django settings
    └── urls.py             # Project URL configuration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

#   W P P - P R O J E C T  
 