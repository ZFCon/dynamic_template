from django.urls import include, path

from dynamic_template.views import RequestAPIView

urlpatterns = [
    path("requests/<int:pk>/", RequestAPIView.as_view(), name="requests"),
]
