#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass

from util import DictMixin


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
class WeatherDisplayData(DictMixin):
    date: str
    sunrise: str
    sunset: str
    temperature: Dict[str, int]
    sky_con: str
    wind: str
    air_quality: str
