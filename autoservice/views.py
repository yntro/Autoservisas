from django.shortcuts import render

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