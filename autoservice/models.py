from itertools import count
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db import models
from tinymce.models import HTMLField


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=6)
    vin_code = models.CharField(max_length=17, unique=True)
    client_name = models.CharField(max_length=50)
    image = models.ImageField('image', upload_to="images/", null=True, blank=True)
    description = HTMLField(verbose_name="description", max_length=500, default="")

    def __str__(self):
        return f"{self.make} {self.license_plate} {self.client_name}"
    @property
    def has_image(self):
        return bool(self.image)
    class Meta:
        verbose_name_plural = "Cars"
        verbose_name = "Car"

class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Services"
        verbose_name = "Service"

def default_due_date():
    return timezone.now().date() + timedelta(days=7)

class Order(models.Model):
    date = models.DateField(timezone.now().date())
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(default=default_due_date)

    @property
    def status(self):
        return all(line.status for line in self.orderline_set.all())

    @property
    def is_overdue(self):
        return self.due_date and timezone.now().date() > self.due_date

    def total(self):
        total = 0.0
        for order_line in self.orderline_set.all():
            total += order_line.line_sum()
        return total
    def __str__(self):
        return f"{self.car.vin_code}-{self.car.license_plate}-{self.date}"

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)

    def line_sum(self):
        return self.service.price * self.quantity
    def __str__(self):
        return f"{self.service} x {self.quantity} {self.status}"

    class Meta:
        verbose_name_plural = "Order Lines"
        verbose_name = "Order Line"