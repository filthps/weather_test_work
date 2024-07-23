from django.urls import include, path
from django.views.generic import TemplateView
from .views import FormPage, HistoryView, APICall


urlpatterns = [
    path("", FormPage.as_view(), name="search"),
    path("api-call/", APICall.as_view(), name="api_call"),
    # Все запросы происходят преимущественно на стороне клиента
    path("wait/<uuid:task_id>/", TemplateView.as_view(template_name="wait.html"),  name="wait"),  # no-ajax
    path("error/<uuid:task_id>/", TemplateView.as_view(template_name="error.html"), name="error"),  # no-ajax
    #path("load-coordinates/<uuid:task_id>/", ...),  # no-ajax получение географических координат
    #path("show-weather/<uuid:task_id>/"),  # weather no-ajax показ погоды
    path("log/", HistoryView.as_view(), name="log"),
    #path()
]
