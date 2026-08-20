from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, reverse
from .forms import CarCommentsForm, OrderCommentsForm
from django.views.generic.edit import FormMixin
from django.views import View, generic
from django.urls import reverse_lazy
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

class CarDetailView(FormMixin, generic.DetailView):
    model = Car
    template_name = "autoservice/car_details.html"
    context_object_name = "car"
    form_class = CarCommentsForm

    def get_success_url(self):
        return reverse("car_details", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.car = self.get_object()
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class OrderDetailsView(FormMixin, generic.DetailView):
    model = Order
    template_name = "autoservice/order_details.html"
    context_object_name = "order"
    form_class = OrderCommentsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_lines"] = self.object.orderline_set.all()
        return context

    def get_success_url(self):
        return reverse("order_details", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

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

class ClientOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "autoservice/myorders.html"
    context_object_name = "client_order_list"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "autoservice/signup.html"
    success_url = reverse_lazy("login")