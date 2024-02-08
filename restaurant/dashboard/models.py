from django.core.validators import MaxValueValidator
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator
from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]
    )
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="dishes/")

    def __str__(self):
        return f"{self.name} - ${self.price}"


class DishReview(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.dish.name}"


class Driver(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, validators=[MinLengthValidator(6)])
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="drivers/")

    def __str__(self):
        return self.name
