from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("canvas/", include("api.canvas.urls", namespace="canvas")),
]
