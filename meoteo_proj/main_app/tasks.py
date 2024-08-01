""" Данный модуль отвечает за работу с 2gis api """
import os
import requests
from requests import Request
from dotenv import dotenv_values
from celery import Celery
from celery import Task
from kombu import Queue
from celery.exceptions import Reject
from django.conf import settings


API_KEY = dotenv_values(f"{settings.BASE_DIR}/main_app/api_keys.env")["TGIS_API_KEY"]
REDIS = dotenv_values(f"{settings.BASE_DIR}/main_app/api_keys.env")["REDIS_DB_PATH"]

app = Celery(__name__, broker=REDIS, backend=REDIS)
app.conf.task_queues = (
    Queue("names", routing_key="name"),
    Queue("coordinates", routing_key="coord"),
    Queue("weather", routing_key="get_w"),
)
app.conf.task_track_started = True
app.conf.task_ignore_result = False
app.autodiscover_tasks()


@app.task()
def call_to_api_get_city_coordinates(*a, **kw):
    return 1


@app.task(bind=True, exchange="names")
def call_to_api_search_cities(self: Task, text: str):
    """ Искать города по вводимому тексту """
    if not text:
        raise Reject(ValueError)
    api_path = f"https://catalog.api.2gis.com/2.0/region/search?q=Мо&fields=items.point&key={API_KEY}"
    r = requests.get(api_path, headers={"content-type": "application/json"})
    if r.status_code in range(500, 600):
        self.retry(countdown=3)
    return {"code": r.status_code, "text": r.text}
