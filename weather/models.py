#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from werkzeug.wrappers import Response

@dataclass
class Coordinate:
    latitude: float
    longitude: float