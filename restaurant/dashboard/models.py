from django.db import models
from django.urls import reverse


# Create your models here.
class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="dishes/")

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_absolute_url(self):
        return reverse("dish_detail", kwargs={"pk": self.pk})


class DishReview(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    stars = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.dish.name}"


class Order(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    items = models.ManyToManyField(Dish, through="OrderItem")

    ORDER_STATUS = (
        ("W", "Waiting for Confirmation"),
        ("P", "Being Prepared"),
        ("T", "In Transit"),
        ("D", "Delivered"),
    )

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default="W",
        help_text="Order Status",
    )

    def __str__(self):
        return f"{self.name} - ${self.total}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.dish.name} - {self.quantity} - ${self.dish.price}"


class Driver(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    vehicle = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name
