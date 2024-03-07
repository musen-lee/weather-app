#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest  
import requests
from requests_mock import Mocker
from exceptions import WeatherQueryError
from .weather import WeatherService
  
@pytest.fixture  
def weather_service():  
    return WeatherService({"WEATHER_URL": "https://api.caiyunapp.com/v2.6/6CUJi5yB5S1cpqW7/%s,%s/daily", "HTTP_TIMEOUT": 5})  
  
@pytest.fixture  
def mock_requests(request):  
    mocker = Mocker()  
    request.addfinalizer(mocker.stop)  
    return mocker  
  
def test_find_weather_success(weather_service, mock_requests):
    coordinate = (123.456, 78.901)
    mock_requests.get(weather_service.url, json={  
        "status": "ok",  
        "result": {  
            "date": "2023-04-01",  
            "temperature": {  
                "min": 10,  
                "max": 20  
            }  
        }  
    })  
  
    daily_weather = weather_service.find_weather(coordinate)
    assert daily_weather["date"] == "2023-04-01"  
    assert daily_weather["temperature"]["min"] == 10  
    assert daily_weather["temperature"]["max"] == 20  
  
def test_find_weather_timeout(weather_service, mock_requests):  
    mock_requests.get("https://api.example.com/weather/coordinates/123.456,78.901", exc=requests.exceptions.Timeout)  
    with pytest.raises(WeatherQueryError) as exc_info:
        weather_service.find_weather((123.456, 78.901))
    assert "Error occurred while connecting to weather service" in str(exc_info.value)  
  
def test_find_weather_connection_error(weather_service, mock_requests):  
    mock_requests.get("https://api.example.com/weather/coordinates/123.456,78.901", exc=requests.exceptions.ConnectionError)  
  
    with pytest.raises(WeatherQueryError) as exc_info:  
        weather_service.find_weather((123.456, 78.901))  
    assert "Error occurred while connecting to weather service" in str(exc_info.value)  
  
def test_find_weather_invalid_response(weather_service, mock_requests):  
    mock_requests.get("https://api.example.com/weather/coordinates/123.456,78.901", json={"status": "error", "message": "Invalid request"})  
  
    daily_weather = weather_service.find_weather((123.456, 78.901))  
    assert daily_weather == {}