""" Данный модуль отвечает за работу с 2gis api """
import requests
from dotenv import dotenv_values
from celery import Celery


API_KEY = dotenv_values("api_keys.env")["TGIS_API_KEY"]
REDIS = dotenv_values("api_keys.env")["REDIS_DB_PATH"]

app = Celery("tasks", broker=REDIS, backend=REDIS)


@app.task()
def call_to_api_get_city_coordinates(*a, **kw):
    return 1

