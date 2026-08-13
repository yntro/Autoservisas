from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static, settings
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("autoservice/", include("autoservice.urls")),
    path("",views.home,name="home"),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))