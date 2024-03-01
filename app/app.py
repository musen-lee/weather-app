#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from flask import Flask
from config import config
from logging.handlers import RotatingFileHandler
from weather import bp_weather


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    set_logger_cfg(config_name)
    app.config.from_object(config[config_name])
    app.register_blueprint(bp_weather)
    return app


def set_logger_cfg(config_name):
    config_object = config[config_name]
    logging.basicConfig(level=config_object.LOG_LEVEL)
    file_log_handler = RotatingFileHandler(config_object.LOG_FILE, maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s(%(lineno)s): %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)