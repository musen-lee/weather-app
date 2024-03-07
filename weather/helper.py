#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from typing import Dict, List, Tuple
from thirdapis.weather import (
    Daily,
    DailyForecast,
    SkyCon,
    WindDirection,
    Wind,
    Astro,
    AirQuality,
    Temperature,
    Humidity
)
from .models import WeatherDisplayData

def extrat_sunrise_and_sunset(data: List[Astro]) -> Tuple[str, str, str]:
    for entry in data:
        formatted_date = datetime.fromisoformat(entry["date"][:-6]).strftime("%Y-%m-%d")
        sunrise = entry["sunrise"]["time"]
        sunset = entry["sunset"]["time"]
        yield (formatted_date, sunrise, sunset)


def extract_temperature(data: List[Temperature]) -> Tuple[str, str, str, str]:
    for entry in data:
        formatted_date = datetime.fromisoformat(entry["date"][:-6]).strftime("%Y-%m-%d")
        max_temperature = round(entry["max"])
        avg_temperature = round(entry["avg"])
        min_temperature = round(entry["min"])
        yield (formatted_date, max_temperature, avg_temperature, min_temperature)


def extract_humidity(data: List[Humidity]) -> Tuple[str, str, str, str]:
    for item in data:
        formatted_date = datetime.fromisoformat(item["date"][:-6]).strftime("%Y-%m-%d")
        max_humidity = f"{float(item['max']) * 100:.0f}"
        avg_humidity = f"{float(item['avg']) * 100:.0f}"
        min_humidity = f"{float(item['min']) * 100:.0f}"
        yield (formatted_date, max_humidity, avg_humidity, min_humidity)


def extract_wind(data: List[Wind]) -> Tuple[str, str, str]:
    wind_speed_desc = {
        (0, 1): ("无风", 0),
        (1, 5): ("微风", 1),
        (6, 11): ("轻风", 2),
        (12, 19): ("微风", 3),
        (20, 28): ("和风", 4),
        (29, 38): ("清风", 5),
        (39, 49): ("强风", 6),
        (50, 61): ("劲风", 7),
        (62, 74): ("大风", 8),
        (75, 88): ("烈风", 9),
        (89, 102): ("狂风", 10),
        (103, 117): ("暴风", 11),
        (117, float("inf")): ("台风", 12),
    }

    def get_wind_speed_desc(wind_speed: float) -> Tuple[str, int]:
        for speed, level in wind_speed_desc.items():
            if speed[0] <= int(f"{round(wind_speed):.0f}") <= speed[1]:
                return level
        return ("Unknown", -1)

    """
    Wind direction angle, range 0~360, 0 is due north, 90 is due east, 180 is due south, 270 is due west.
    """
    wind_direction_desc = {
        (0, 0): "北风",
        (90, 90): "东风",
        (180, 180): "南风",
        (270, 270): "西风",
        (0, 90): "东北风",
        (90, 180): "东南风",
        (180, 270): "西南风",
        (270, 360): "西北风",
    }

    def get_wind_direction_desc(direction: float) -> str:
        for dc, desc in wind_direction_desc.items():
            if dc[0] <= direction < dc[1]:
                return desc
        return "Unknown"

    for item in data:
        formatted_date = datetime.fromisoformat(item["date"][:-6]).strftime("%Y-%m-%d")
        wind_dc = WindDirection.from_dict(item["max"])
        wind_speed_info = get_wind_speed_desc(float(wind_dc.speed))
        wind_direction_info = get_wind_direction_desc(float(wind_dc.direction))
        yield (formatted_date, wind_speed_info, wind_direction_info)


def extract_sky_con(data: List[SkyCon]) -> Tuple[str, str]:
    skycon_desc = {
        "CLEAR_DAY": "晴（白天）",
        "CLEAR_NIGHT": "晴（夜间）",
        "PARTLY_CLOUDY_DAY": "多云（白天）",
        "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
        "CLOUDY": "阴",
        "LIGHT_HAZE": "轻度雾霾",
        "MODERATE_HAZE": "中度雾霾",
        "HEAVY_HAZE": "重度雾霾",
        "LIGHT_RAIN": "小雨",
        "MODERATE_RAIN": "中雨",
        "HEAVY_RAIN": "大雨",
        "STORM_RAIN": "暴雨",
        "FOG": "雾",
        "LIGHT_SNOW": "小雪",
        "MODERATE_SNOW": "中雪",
        "HEAVY_SNOW": "大雪",
        "STORM_SNOW": "暴雪",
        "DUST": "浮尘",
        "SAND": "沙尘",
        "WIND": "大风",
    }
    for item in data:
        formatted_date = datetime.fromisoformat(item["date"][:-6]).strftime("%Y-%m-%d")
        desc = skycon_desc.get(item["value"])
        yield (formatted_date, desc)


def get_aqi_desc(aqi: int) -> str:
    ranges = {
        (0, 50): "优",
        (51, 100): "良",
        (101, 150): "轻度污染",
        (151, 200): "中度污染",
        (201, 300): "重度污染",
        (300, float("inf")): "严重污染",
    }
    for range_tuple, description in ranges.items():
        if range_tuple[0] <= aqi < range_tuple[1]:
            return description
    return "未知空气质量情况"


def extract_air_quality(data: AirQuality) -> Tuple[str, str, str]:
    for item in data["aqi"]:
        formatted_date = datetime.fromisoformat(item["date"][:-6]).strftime("%Y-%m-%d")
        aqi = item["max"]["chn"]
        aqi_desc = get_aqi_desc(int(aqi))
        yield (formatted_date, aqi, aqi_desc)


def convert2weather(weather_data: Dict) -> List[WeatherDisplayData]:
    list: List[WeatherDisplayData] = []
    if weather_data:
        daily_weather = Daily(**weather_data)
        daily_forecast = DailyForecast.from_dict(daily_weather.daily)
        sunrise_sunset = {
            date: (sunrise, sunset)
            for date, sunrise, sunset in [
                item for item in extrat_sunrise_and_sunset(daily_forecast.astro)
            ]
        }
        logging.info("sunrise and sunset: %s", sunrise_sunset)
        temperature = {
            date: {"max": max, "min": min}
            for date, max, avg, min in [
                item for item in extract_temperature(daily_forecast.temperature)
            ]
        }
        logging.info("temperature: %s" % temperature)
        humidity = {
            date: min
            for date, max, avg, min in [
                item for item in extract_humidity(daily_forecast.humidity)
            ]
        }
        logging.info("humidity: %s" % humidity)
        air_quality = {
            date: {"aqi": aqi, "level": aqi_desc}
            for date, aqi, aqi_desc in [
                item for item in extract_air_quality(daily_forecast.air_quality)
            ]
        }
        logging.info("air_quality: %s", air_quality)
        wind = {
            date: {"name": wd[0], "level": wd[1], "direction": direction}
            for date, wd, direction in [
                item for item in extract_wind(daily_forecast.wind)
            ]
        }
        logging.info("wind: %s", wind)
        skycon = {
            date: value
            for date, value in [item for item in extract_sky_con(daily_forecast.skycon)]
        }
        logging.info("skycon: %s", skycon)

        for dt in sunrise_sunset.keys():
            sunrise, sunset = sunrise_sunset[dt]
            list.append(
                WeatherDisplayData(
                    date=dt,
                    sunrise=sunrise,
                    sunset=sunset,
                    temperature=temperature[dt],
                    sky_con=skycon[dt],
                    wind=wind[dt],
                    air_quality=air_quality[dt],
                )
            )
    return list
