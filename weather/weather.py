#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict
from .models import Coordinate


@dataclass
class WeatherQuery(object):
    day_range: int
    coordinate: Coordinate


class WeatherService(object):
    """
    Weather Service, providing weather information of every day.
    """

    def __init__(self, url: str) -> None:
        self.url = url

    def find_weather(self, parameter: WeatherQuery) -> Dict:
        pass
