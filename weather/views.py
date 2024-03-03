#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, render_template, current_app

from .models import ok,fail

from .helper import convert2weather
from .weather import WeatherService
from .exceptions import GeoQueryError, WeatherQueryError
from .geo import GeoService

bp_weather = Blueprint("weather", __name__, template_folder="../templates")


@bp_weather.route("/weather/<city_name>")
def get_weather_by_city(city_name: str):
    geo_service = GeoService(current_app.config)
    try:
        coordinate = geo_service.get_location(city_name=city_name)
        if coordinate:
            weather_service = WeatherService(current_app.config)
            weather_data = weather_service.find_weather(coordinate=coordinate)
            resp = ok(convert2weather(weather_data))
            return resp.to_dict()
    except GeoQueryError as e:
        logging.error("get weather by city failed: %s", e)
        resp = fail(f"get weather by city failed:{str(e)}")
        return resp.to_dict()
    except WeatherQueryError as ex:
        logging.error("get weather by city failed: %s", ex)
        resp = fail(f"get weather by city failed:{str(ex)}")
        return resp.to_dict()
    return ok({}).to_dict()


@bp_weather.route("/weather")
def search_weather():
    return render_template("weather.html")
