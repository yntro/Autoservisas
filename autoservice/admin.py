from django.contrib import admin
from .models import Car, Order, Service, OrderLine, CarComments, OrderComments

class CarAdmin(admin.ModelAdmin):
    list_display = ['vin_code', 'make', 'model', 'license_plate', 'client_name', 'has_image', 'description']
    search_fields = ['vin_code', 'license_plate']
    list_filter = ['make', 'model', 'license_plate', 'client_name', 'vin_code']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'due_date', 'order_lines', 'total', 'status', 'client']
    inlines = [OrderLineInline]

    def order_lines(self, obj):
        return ", ".join(f"{order_line.service.name} x {order_line.quantity}" for order_line in obj.orderline_set.all())

    order_lines.short_description = "Order Lines"

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum', 'status']

class CarCommentsAdmin(admin.ModelAdmin):
    list_display = ['car', 'date_created', 'user', 'content']

class OrderCommentsAdmin(admin.ModelAdmin):
    list_display = ['order', 'date_created', 'user', 'content']

admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(CarComments, CarCommentsAdmin)
admin.site.register(OrderComments, OrderCommentsAdmin)