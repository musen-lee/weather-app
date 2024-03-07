#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pytest
import requests
import requests_mock
from requests_mock import Mocker
from .geo import LocationService, GeoService
from exceptions import LocationQueryError, GeoQueryError

logging.basicConfig(level=logging.ERROR)


class TestLocationService:

    @pytest.fixture
    def location_service(self):
        cfg = {"IP_LOCATION_URL": "http://api.ip33.com/ip/search", "HTTP_TIMEOUT": 5}
        return LocationService(cfg)

    @pytest.fixture
    def mock_requests(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_get_location_success(self, location_service, mock_requests):
        mock_requests.post(location_service.url, json={"area": "广东省广州市 电信"})
        city = location_service.get_location()
        assert city == "广州市"

    def test_get_location_request_exception(self, location_service, mock_requests):
        mock_requests.post(
            location_service.url, exc=requests.exceptions.RequestException
        )
        with pytest.raises(LocationQueryError) as e:
            location_service.get_location()
        assert str(e.value) == "get location based on public IP address failed"

    def test_get_location_other_exception(self, location_service, mock_requests):
        mock_requests.post(location_service.url, exc=Exception("Other exception"))
        with pytest.raises(LocationQueryError) as e:
            location_service.get_location()
        assert (
            str(e.value)
            == "get location based on public IP address failed: Other exception"
        )


class TestGeoService:

    @pytest.fixture
    def geo_service(self) -> GeoService:
        cfg = {
            "GEO_URL": "https://geoapi.qweather.com/v2/city/lookup",
            "GEO_PRIVATE_KEY": "8310a8194c2c4ad3bdddee1e27029577",
            "HTTP_TIMEOUT": 5,
        }
        return GeoService(cfg)

    @pytest.fixture
    def mock_request(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_get_coordinate_success(
        self, geo_service: GeoService, mock_request: Mocker
    ):
        mock_request.get(
            geo_service.url,
            json={
                "code": "200",
                "location": [
                    {
                        "name": "广州",
                        "id": "101280101",
                        "lat": "23.12518",
                        "lon": "113.28064",
                        "adm2": "广州",
                        "adm1": "广东省",
                        "country": "中国",
                        "tz": "Asia/Shanghai",
                        "utcOffset": "+08:00",
                        "isDst": "0",
                        "type": "city",
                        "rank": "11",
                        "fxLink": "https://www.qweather.com/weather/guangzhou-101280101.html",
                    }
                ],
                "refer": {
                    "sources": ["QWeather"],
                    "license": ["QWeather Developers License"],
                },
            },
            status_code=200,
        )
        lon, lat = geo_service.get_coordinate("广州市")
        assert lon == '113.28064'
        assert lat == '23.12518'

    def test_get_coordinate_request_exception(
        self, geo_service: GeoService, mock_request
    ):
        mock_request.get(geo_service.url, exc=requests.exceptions.RequestException)
        with pytest.raises(GeoQueryError) as exc_info:
            geo_service.get_coordinate("广州市")
        assert "Query coordinates by city name failed" in str(exc_info.value)

    def test_get_coordinate_other_exception(
        self, geo_service: GeoService, mock_request: Mocker
    ):
        mock_request.get(geo_service.url, exc=Exception("Other error"))
        with pytest.raises(GeoQueryError) as exc_info:
            geo_service.get_coordinate("广州市")
        assert "Query coordinates by city name error" in str(exc_info.value)
