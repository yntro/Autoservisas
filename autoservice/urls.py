from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="autoservice"),
    path("services/", views.services, name="services"),
    path("cars/", views.CarListView.as_view(), name="car_list"),
    path("cars/<int:pk>/", views.CarDetailView.as_view(), name="car_details"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.order_details, name="order_details"),
    path('search/', views.search, name='search'),
]