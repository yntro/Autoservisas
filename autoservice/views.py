from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View, generic

from autoservice.models import Car, Service, Order, OrderLine


def index(request):
    num_completed_orders = sum(order.status for order in Order.objects.all())
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {"cars": Car.objects.all(),
               "services": Service.objects.all(),
               "orders": Order.objects.all(),
               "order_lines": OrderLine.objects.all(),
               "num_cars": Car.objects.count(),
               "num_services": Service.objects.count(),
               "num_orders": Order.objects.count(),
               "completed_orders": num_completed_orders,
               "num_visits": num_visits,
               }
    return render(request, "autoservice/index.html", context)

def services(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "autoservice/services.html", context)

class CarListView(generic.ListView):
    model = Car
    template_name = "autoservice/car_list.html"
    context_object_name = "car_list"
    paginate_by = 10

class CarDetailView(generic.DetailView):
    model = Car
    template_name = "autoservice/car_details.html"
    context_object_name = "car"

def order_list(request):
    paginator = Paginator(Order.objects.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    completed_orders = sum(order.status for order in Order.objects.all())

    context = {"completed_orders": completed_orders,
               "order_list": page_obj,
               "order_lines": OrderLine.objects.all(),
               "page_obj": page_obj,
    }
    return render(request, "autoservice/order_list.html", context)

def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_lines = order.orderline_set.all()
    context = {"order": order,
               "order_lines": order_lines,
               }
    return render(request, "autoservice/order_details.html", context)

def search(request):
    query = request.GET.get('query')
    if not query:
        return render(request, "autoservice/search.html")
    car_search_results = Car.objects.filter(Q(make__icontains=query) |
                                            Q(vin_code__icontains=query) |
                                            Q(license_plate__icontains=query) |
                                            Q(client_name__icontains=query) |
                                            Q(model__icontains=query)
                                            )
#    order_search_results = Order.objects.filter(Q(car__make__icontains=query) |)
    context = {
        "query": query,
        "car_list": car_search_results,
    }
    return render(request, "autoservice/search.html", context)
