#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import logging
import requests
from dataclasses import dataclass
from typing import Dict, Tuple,List

from exceptions import WeatherQueryError
from util import DictMixin

@dataclass
class Astro:
    date: str
    sunrise: Dict[str, str]
    sunset: Dict[str, str]


@dataclass
class Precipitation:
    date: str
    max: float
    min: float
    avg: float
    probability: float


@dataclass
class Temperature:
    date: str
    max: float
    min: float
    avg: float


@dataclass
class WindDirection(DictMixin):
    speed: float
    direction: float


@dataclass
class Wind:
    date: str
    max: WindDirection
    min: WindDirection
    avg: WindDirection


@dataclass
class SkyCon:
    date: str
    value: str


@dataclass
class Humidity:
    date: str
    max: float
    min: float
    avg: float


@dataclass
class CloudRate:
    date: str
    max: float
    min: float
    avg: float


@dataclass
class AirQualityIndexValue(DictMixin):
    chn: int
    usa: int


@dataclass
class AirQualityIndexEntry:
    date: str
    max: AirQualityIndexValue
    avg: AirQualityIndexValue
    min: AirQualityIndexValue


@dataclass
class PM25Entry:
    date: str
    max: int
    avg: int
    min: int


@dataclass
class AirQuality:
    aqi: List[AirQualityIndexEntry]
    pm25: List[PM25Entry]


@dataclass
class Daily:
    daily: DailyForecast
    primary: int


@dataclass
class DailyForecast(DictMixin):
    status: str
    astro: List[Astro]
    precipitation: List[Precipitation]
    temperature: List[Temperature]
    wind: List[Wind]
    humidity: List[Humidity]
    cloudrate: List[CloudRate]
    air_quality: AirQuality
    skycon: List[SkyCon]

@dataclass
class WeatherData:
    status: str
    api_version: str
    api_status: str
    lang: str
    unit: str
    tzshift: int
    timezone: str
    server_time: int
    location: List[float]
    result: Daily

@dataclass
class WeatherQuery(object):
    day_range: int
    coordinate: Tuple[float, float]


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
            logging.info("Find weather resp: %s", resp.text)
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
        except Exception as ex:
            logging.error(
                "Find weather by coordinate error", exc_info=True, stack_info=True
            )
            raise WeatherQueryError(f"Find weather by coordinate error: {str(ex)}")
