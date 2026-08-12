from django.contrib import admin
from .models import Car, Order, Service, OrderLine

class CarAdmin(admin.ModelAdmin):
    list_display = ['vin_code', 'make', 'model', 'license_plate', 'client_name']
    search_fields = ['vin_code', 'license_plate']
    list_filter = ['make', 'model', 'license_plate', 'client_name', 'vin_code']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date','order_lines', 'total', 'status']
    inlines = [OrderLineInline]

    def order_lines(self, obj):
        return ", ".join(f"{order_line.service.name} x {order_line.quantity}" for order_line in obj.orderline_set.all())

    order_lines.short_description = "Order Lines"

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum', 'status']

admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderLine, OrderLineAdmin)