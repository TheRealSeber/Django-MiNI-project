from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


class RestaurantInfoView(View):
    def get(self, request, *args, **kwargs):
        restaurant_data = {
            "name": "Bottega del Gusto",
            "description": (
                "Bottega del Gusto offers a delightful journey through "
                "authentic Italian cuisine. From handmade pasta to freshly baked bread,"
                " every dish is crafted with the finest ingredients."
            ),
            "address": "1234 Italian Plaza, Food City, Country",
            "phone": "+39 555 678 1234",
            "email": "info@bottegadelgusto.com",
            "hours": "Mon-Sun: 11:00 AM - 10:00 PM",
        }
        return JsonResponse(restaurant_data)


class AboutUsView(TemplateView):
    template_name = "dashboard/about_us.html"
