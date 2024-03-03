#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import requests
from dataclasses import asdict, dataclass
from typing import Dict, Tuple

from weather.exceptions import WeatherQueryError
from .models import Coordinate, Daily, DailyForecast, WeatherData


@dataclass
class WeatherQuery(object):
    day_range: int
    coordinate: Coordinate


class WeatherService(object):
    """
    Weather Service, providing weather information of every day.
    """

    def __init__(self, cfg: Dict) -> None:
        self.url = cfg["WEATHER_URL"]
        self.timeout = cfg["HTTP_TIMEOUT"]

    def find_weather(self, coordinate: Tuple) -> Dict:
        url = self.url % coordinate
        daily_step = {"dailysteps": 4}
        try:
            resp = requests.get(url=url, params=daily_step, timeout=self.timeout)
            if resp.status_code == 200:
                weather_data = resp.json()
                if weather_data.get("status") == "ok":
                    daiy_data = weather_data.get("result")
                    return daiy_data
            return {}
        except requests.exceptions.Timeout:
            logging.error(
                "Connect to weather service timeout", exc_info=True, stack_info=True
            )
            raise WeatherQueryError("Connect to weather service timeout")
        except requests.exceptions.ConnectionError:
            logging.error(
                "Couldn't connect to weather service", exc_info=True, stack_info=True
            )
            raise WeatherQueryError("Couldn't connect to weather service")
        except requests.exceptions.JSONDecodeError as e:
            logging.error(
                "Find weather by coordinate error, json decoded failed",
                exc_info=True,
                stack_info=True,
            )
            raise WeatherQueryError(
                f"Find weather by coordinate error, json decoded failed: { str(e)}"
            )
        except IOError as ex:
            logging.error(
                "Find weather by coordinate error", exc_info=True, stack_info=True
            )
            raise WeatherQueryError(f"Find weather by coordinate error: {str(ex)}")
