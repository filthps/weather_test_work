""" Данный модуль отвечает за работу с 2gis api """
import requests
from dotenv import dotenv_values
from celery import Celery


API_KEY = dotenv_values("api_keys.env")["TGIS_API_KEY"]
app = Celery("tasks", broker='pyamqp://guest@localhost//')


@app.task()
def get_city_coordinates(city_name: str):
    if not isinstance(city_name, str):
        pass
    if not city_name:
        ...

