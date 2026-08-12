from django.shortcuts import render, get_object_or_404
from django.views import View, generic

from autoservice.models import Car, Service, Order, OrderLine


def index(request):
    completed_orders = sum(order.status for order in Order.objects.all())
    context = {"cars": Car.objects.all(),
               "services": Service.objects.all(),
               "orders": Order.objects.all(),
               "order_lines": OrderLine.objects.all(),
               "num_cars": Car.objects.count(),
               "num_services": Service.objects.count(),
               "num_orders": Order.objects.count(),
               "completed_orders": completed_orders
               }
    return render(request, "index.html", context)

def services(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "services.html", context)

class CarListView(generic.ListView):
    model = Car
    template_name = "car_list.html"
    context_object_name = "car_list"

class CarDetailView(generic.DetailView):
    model = Car
    template_name = "car_details.html"
    context_object_name = "car"

def order_list(request):
    completed_orders = sum(order.status for order in Order.objects.all())
    context = {"completed_orders": completed_orders,
               "order_list": Order.objects.all(),
               "order_lines": OrderLine.objects.all(),
    }
    return render(request, "order_list.html", context)

def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_lines = order.orderline_set.all()
    context = {"order": order,
               "order_lines": order_lines,
               }
    return render(request, "order_details.html", context)