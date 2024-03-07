#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

class Config(object):
    LOG_LEVEL = logging.DEBUG  # Set the desired logging level here
    LOG_FILE = "logs/weather.log"
    WEATHER_URL = "https://api.caiyunapp.com/v2.6/6CUJi5yB5S1cpqW7/%s,%s/daily"
    GEO_URL="https://geoapi.qweather.com/v2/city/lookup"
    GEO_PRIVATE_KEY = "8310a8194c2c4ad3bdddee1e27029577"
    IP_LOCATION_URL = "http://api.ip33.com/ip/search"
    HTTP_TIMEOUT = 50
    


class DevelopConfig(Config):
    DEBUG = True  # Set debug mode to True


class TestConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


class ProductConfig(Config):
    DEBUG = True
    TESTING = True

config = {
    "development": DevelopConfig,
    "testing": TestConfig,
    "production": ProductConfig,
}