#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, render_template, current_app
from .models import ok, fail
from .helper import convert2weather
from thirdapis.weather import WeatherService
from errors import GeoQueryError, WeatherQueryError
from thirdapis.geo import GeoService

bp_weather = Blueprint("weather", __name__, template_folder="../templates")


@bp_weather.errorhandler(500)
def internal_system_error():
    return render_template("500.html"), 500


@bp_weather.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@bp_weather.route("/weather/<city_name>")
def get_weather_by_city(city_name: str):
    geo_service = GeoService(current_app.config)
    try:
        coordinate = geo_service.get_coordinate(city_name=city_name)
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
