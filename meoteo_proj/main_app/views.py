from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import History
from .serializers import Serializer


class SearchCityView(APIView):
    template_name = "stat.html"
    serializer_class = Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"title": "Поиск города/области/населённого пункта"})

    def post(self):
        ...


class HistoryView(ListAPIView):
    pass
