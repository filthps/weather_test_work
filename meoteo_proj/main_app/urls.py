from django.urls import include, path
from django.views.generic import TemplateView
from .views import SearchCityView, HistoryView


urlpatterns = [
    path("", SearchCityView.as_view(), name="search"),
    # Все запросы происходят преимущественно на стороне клиента
    path("", save_in_history_from_xhr),
    path("wait/<uuid:task_id>", TemplateView.as_view(template_name="wait.html"),  name="wait"),
    path("error/<uuid:task_id>", TemplateView.as_view(template_name="error.html"), name="error"),
    path("log/", HistoryView.as_view(), name="log"),
]
