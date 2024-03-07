#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests
from dataclasses import dataclass
from typing import Dict, Tuple
from exceptions import GeoQueryError, LocationQueryError

@dataclass
class Location:
    name: str
    id: str
    lat: float
    lon: float
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


def extract_city(area_string):
    if "省" in area_string:
        province_city = area_string.split("省")
        city_info = province_city[1]
        city = city_info.split(" ")[0]
    elif "市" in area_string:
        city = area_string.split("市")[0]
    elif "自治区" in area_string:
        autonomous_region_city = area_string.split("自治区")
        city_info = autonomous_region_city[1]
        city = city_info.split(" ")[0]
    else:
        city = area_string
    return city.strip()


class LocationService(object):

    def __init__(self, cfg: Dict) -> None:
        self.url = cfg["IP_LOCATION_URL"]
        self.timeout = cfg["HTTP_TIMEOUT"]

    def get_location(self) -> str:
        """
        Automatically obtains the geographic location based on the current public IP address
        """
        try:
            resp = requests.post(self.url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                return extract_city(data.get("area"))
        except requests.exceptions.RequestException:
            logging.error(
                "get location based on public IP address failed",
                exc_info=True,
                stack_info=True,
            )
            raise LocationQueryError("get location based on public IP address failed")
        except Exception as e:
            logging.error(
                f"get location based on public IP address failed: {str(e)}",
                exc_info=True,
                stack_info=True,
            )
            raise LocationQueryError(
                f"get location based on public IP address failed: {str(e)}"
            )


class GeoService(object):

    def __init__(self, cfg: Dict) -> None:
        self.url = cfg["GEO_URL"]
        self.key = cfg["GEO_PRIVATE_KEY"]
        self.timeout = cfg["HTTP_TIMEOUT"]

    def get_coordinate(self, city_name: str) -> Tuple[float, float]:
        parameter = {"location": city_name, "key": self.key}
        try:
            resp = requests.get(self.url, params=parameter, timeout=self.timeout)
            if resp.status_code == 200:
                json_content = resp.json()
                geo_resp = GeoResponse(**json_content)
                if int(geo_resp.code) == 200:
                    location = Location(**geo_resp.location[0])
                    return (location.lon, location.lat)
            return ()
        except requests.exceptions.RequestException:
            logging.error(
                "Query coordinates by city name faile",
                exc_info=True,
                stack_info=True,
            )
            raise GeoQueryError("Query coordinates by city name failed")
        except Exception as ex:
            logging.error(
                "Query coordinates by city name error", exc_info=True, stack_info=True
            )
            raise GeoQueryError(f"Query coordinates by city name error: {str(ex)}")