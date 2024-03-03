#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests
from typing import Dict

from weather.exceptions import GeoQueryError
from .models import Coordinate, GeoResponse, Location


class GeoService(object):

    def __init__(self, cfg: Dict) -> None:
        self.url = cfg["GEO_URL"]
        self.key = cfg["GEO_PRIVATE_KEY"]
        self.timeout = cfg["HTTP_TIMEOUT"]

    def get_location(self, city_name: str) -> Coordinate:
        parameter = {"location": city_name, "key": self.key}
        try:
            resp = requests.get(self.url, params=parameter, timeout=self.timeout)
            json_content = resp.json()
            geo_resp = GeoResponse(**json_content)
            if int(geo_resp.code) == 200:
                location = Location(**geo_resp.location[0])
                return (location.lon, location.lat)
            return ()
        except requests.exceptions.Timeout:
            logging.error(
                "Query Coordinates by city name timeout", exc_info=True, stack_info=True
            )
            raise GeoQueryError("Query Coordinates by city name timeout")
        except requests.exceptions.InvalidJSONError:
            logging.error(
                "Query coordinates by city name failed,convert response content to json error",
                exc_info=True,
                stack_info=True,
            )
            raise GeoQueryError(
                "Query coordinates by city name failed,convert response content to json error"
            )
        except IOError:
            logging.error(
                "Query coordinates by city name error", exc_info=True, stack_info=True
            )
            raise GeoQueryError("Query coordinates by city name error")
        return ()
