from itertools import count

from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=6)
    vin_code = models.CharField(max_length=17, unique=True)
    client_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.make} {self.license_plate} {self.client_name}"
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

class Order(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    @property
    def status(self):
        return all(line.status for line in self.orderline_set.all())

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

    def total(self):
        total = 0.0
        for order_line in self.orderline_set.all():
            total += order_line.line_sum()
        return total
    def __str__(self):
        return f"{self.car.vin_code}{self.car.license_plate}{self.date}"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)

    def line_sum(self):
        return self.service.price * self.quantity
    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name_plural = "Order Lines"
        verbose_name = "Order Line"