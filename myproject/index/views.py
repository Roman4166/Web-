import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import openmeteo_requests
import json
from datetime import datetime


load_dotenv()

def list_temperatyre(dictt  ):
    data = dictt["hourly"]["time"]
    temp = dictt["hourly"]["temperature_2m"]
    paired_data = zip(data, temp)  
    return paired_data



def get_weather(city_coords : dict):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": city_coords["latitude"],
	"longitude": city_coords["longitude"],
	'hourly': ['temperature_2m','cloud_cover']
    }   
    responses = requests.get(url, params=params)

    geo_data = responses.json()
        
    print("Ответ геокодинга (JSON):")
    print(json.dumps(geo_data, indent=2, ensure_ascii=False))
    return geo_data
def get_coordinates(city_name):
    """Получаем координаты города по его названию"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city_name,
        'language': 'ru',
        'format': 'json',
        
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    print(data)


    if data.get('results'):
        return {
            'latitude': data['results'][0]['latitude'],
            'longitude': data['results'][0]['longitude']
        }
    return None


def weather_view(request):
    city = request.GET.get('city', '')
    weather_data = None
    time_now = datetime.now().hour 
    time = datetime.now()
    temperature = None
    cloud = None
    list_temperatyre_value = None
    if city:
        weather_coords = get_coordinates(city)
        try:
            weather_data = get_weather(weather_coords)
            temperature = weather_data['hourly']['temperature_2m'][time_now]
            cloud = weather_data['hourly']['cloud_cover'][time_now]
            list_temperatyre_value = list_temperatyre(weather_data)
        except :
            city = None
            weather_data = None
            time_now = datetime.now().hour 
            time = datetime.now()
            temperature = None
            cloud = None
            list_temperatyre_value = None
        
        
    return render(request, 'index/index.html', {
        'city': city,
        'temperature':temperature,
        'time': time,
        'time_now':time_now,
        "cloud": cloud,
        'weather': weather_data,
        "list_temperatyre_value": list_temperatyre_value
    })