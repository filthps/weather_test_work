import json
import typing
import uuid
from celery.result import AsyncResult, GroupResult, ResultSet
from rest_framework.request import HttpRequest, Request
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE
from .models import History
from .serializers import Serializer
from .tasks import call_to_api_search_cities


class Tools:
    @staticmethod
    def is_ajax(request: HttpRequest):
        if not isinstance(request, (HttpRequest, Request,)):
            raise TypeError
        if "X-Requested-With" in request.headers:
            if request.headers["X-Requested-With"] == "XMLHttpRequest":
                return True
        return False


class FormPage(APIView, Tools):
    template_name = "form.html"
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"title": "Поиск города/области/населённого пункта", "form": Serializer})

    def post(self, request):
        return Response(template_name=None, data=request.data)


class HistoryView(ListAPIView):
    pass


class APICall(APIView, Tools):
    """ Централизованный вызов на любой из api нашего сервиса.
     Создать задачу, вернут её id """
    parser_classes = (JSONParser,)

    def post(self, request):
        if not self.is_ajax(request):
            return Response(status=HTTP_400_BAD_REQUEST)
        api_call_type = request.data["type"]
        task = ...
        if api_call_type == "search_city":
            task: AsyncResult = call_to_api_search_cities.apply_async(args=[request.data["item"]])
        return Response(status=HTTP_200_OK, data={"task_id": task.id})


class TaskChecker(APIView, Tools):
    """ Вьюха через xhr получает id задачи и её тип(найти город, найти координаты города, получить погоду),
     а возвращает статус состояния, и, по возможности, результат выполнения. """
    TASK_TYPES = ("search_city", "get_city_coordinates", "get_weather",)
    MAX_COUNT = 999

    def post(self, request):
        if not self.is_ajax(request):
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        tasks_info: list[dict] = request.data
        if not self._is_valid(tasks_info):
            return Response(status=HTTP_400_BAD_REQUEST)
        task_data = self.check_task_status(tasks_info)
        return Response(data=json.dumps(task_data), status=HTTP_200_OK)

    @staticmethod
    def check_task_status(id_group) -> typing.Optional[typing.Union[dict, Exception]]:
        group_tasks = ResultSet([AsyncResult(data["id"]) for data in id_group])
        print(group_tasks[0].state)
        if not group_tasks.successful():
            return
        return group_tasks.result

    @staticmethod
    def collect_data_from_results(results: GroupResult) -> list[dict]:
        pass

    @classmethod
    def _is_valid(cls, request_data):
        if type(request_data) is not list:
            return
        if len(request_data) > cls.MAX_COUNT:
            return
        for elem in request_data:
            if not isinstance(elem, dict):
                return
            if not frozenset(["type", "id"]).intersection(frozenset(elem)):
                return
            if type(elem["type"]) is not str:
                return
            if type(elem["id"]) is not str:
                return
            if not cls.__validate_id(elem["id"]):
                return
            if elem["type"] not in cls.TASK_TYPES:
                return
        return True

    @staticmethod
    def __validate_id(id_string):
        """ Попробуем передать строку в __init__ """
        try:
            uuid.UUID(id_string)
        except ValueError:
            return
        return True
