from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            ("dynamic_template.urls", "dynamic_template"), namespace="dynamic_template"
        ),
    ),
]
