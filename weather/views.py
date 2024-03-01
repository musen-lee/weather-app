#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

bp_weather = Blueprint("weather", __name__, template_folder="../templates")


@bp_weather.route("/weather/<city_name>")
def get_weather_by_city(city_name: str):
    return render_template("weather.html")


@bp_weather.route("/weather")
def search_weather():
    return render_template("weather.html")
