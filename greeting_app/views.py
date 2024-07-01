import requests
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    def get(self, request: HttpRequest):
        visitor_name = request.GET.get('visitor_name', 'Guest')
        client_ip = self.get_client_ip(request)
        location, temperature = self.get_location_and_temperature(client_ip)
        
        response_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}"
        }
        
        return Response(response_data)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_location_and_temperature(self, client_ip):
        # Using ipapi.co for IP geolocation and OpenWeatherMap for temperature
        # You'll need to sign up for a free API key at openweathermap.org
        ip_info = requests.get(f'http://ip-api.com/json/{client_ip}').json()
        city = ip_info.get('city', 'Unknown')
        
        OPENWEATHERMAP_API_KEY = '07bff2a311dbd7c64ca1eeb43cda642f'
        weather_data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric').json()
        temperature = weather_data['main']['temp'] if 'main' in weather_data else 'unknown'
        
        return city, temperature
