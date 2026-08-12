from django.urls import include, path
from django.contrib import admin
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("autoservice/", include("autoservice.urls")),
    path("",views.home,name="home"),
]