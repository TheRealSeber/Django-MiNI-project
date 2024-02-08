import django_filters
from django import forms
from django.db import models

from . import models as m


class DishFilter(django_filters.FilterSet):
    class Meta:
        model = m.Dish
        fields = {
            "available": ["exact"],
            "price": ["lt", "gt"],
        }

        filter_overrides = {
            models.BooleanField: {
                "filter_class": django_filters.BooleanFilter,
                "extra": lambda f: {
                    "widget": forms.Select(
                        attrs={"class": "form-control"},
                        choices=[("", "---------"), (True, "Yes"), (False, "No")],
                    )
                },
            },
            models.DecimalField: {
                "filter_class": django_filters.NumberFilter,
                "extra": lambda f: {
                    "widget": forms.NumberInput(
                        attrs={"class": "form-control", "placeholder": "Price"}
                    ),
                },
            },
        }


class DriverFilter(django_filters.FilterSet):
    class Meta:
        model = m.Driver
        fields = {
            "nationality": ["contains"],
            "name": ["contains"],
        }

        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "widget": forms.TextInput(attrs={"class": "form-control"}),
                },
            },
        }
