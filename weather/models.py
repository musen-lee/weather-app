#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import dataclasses
import logging
from typing import List, Dict, Any, Type, Tuple
from dataclasses import asdict, dataclass, is_dataclass

from util import to_camel_case


class DictMixin:
    @classmethod
    def from_dict(cls: Type, data: Dict[str, Any]) -> Any:
        """
        Create dataclass object from a dictionary, only match the exist keys
        """
        if not is_dataclass(cls):
            raise ValueError(f"{cls.__name__} is not a dataclass")
        field_names = {field.name for field in dataclasses.fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in field_names}
        return cls(**kwargs)

    def to_dict(self, camel_case: bool = True) -> Dict[str, Any]:
        data = asdict(self)
        if camel_case and is_dataclass(type(self)):
            data = {
                to_camel_case(k): self._convert_value(v, camel_case)
                for k, v in data.items()
            }
        return data

    def _convert_value(self, value: Any, camel_case: bool) -> Any:
        if is_dataclass(type(value)):
            return value.to_dict(camel_case=camel_case)
        elif isinstance(value, (list, tuple)):
            return [self._convert_value(item, camel_case) for item in value]
        elif isinstance(value, dict):
            return {to_camel_case(k): self._convert_value(v, camel_case) for k, v in value.items()}
        else:
            return value


@dataclass
class Coordinate:
    latitude: float
    longitude: float


@dataclass
class APIResponse(DictMixin):
    code: int
    msg: int
    data: Any


def ok(data: Any, msg: str = "success") -> APIResponse:
    return APIResponse(code=200, msg=msg, data=data)


def fail(msg: str, data: Any = {}) -> APIResponse:
    return APIResponse(code=400, msg=msg, data=data)


def error(msg: str, code: int, data: Any = {}) -> APIResponse:
    return APIResponse(code=code, msg=msg, data=code)


@dataclass
class Location:
    name: str
    id: str
    lat: str
    lon: str
    adm2: str
    adm1: str
    country: str
    tz: str
    utcOffset: str
    isDst: str
    type: str
    rank: str
    fxLink: str


@dataclass
class GeoResponse:
    code: int
    location: list[Location]
    refer: Dict


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
class WeatherDisplayData(DictMixin):
    date: str
    sunrise: str
    sunset: str
    temperature: Dict[str, int]
    sky_con: str
    wind: str
    air_quality: str
