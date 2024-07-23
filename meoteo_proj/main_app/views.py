import json
from rest_framework.request import HttpRequest, Request
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import History
from .serializers import Serializer


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
        data = json.parse(request.data)
        api_call_type = data["type"]
        return Response(status=HTTP_200_OK)


class TaskChecker(APIView, Tools):
    """ Вьюха через xhr получает id задачи и её тип(найти город, найти координаты города, получить погоду),
     а возвращает статус состояния, и, по возможности, результат выполнения. """
    TASK_TYPES = ("",)

    def post(self, request):
        pass
