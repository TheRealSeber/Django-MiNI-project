from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic import ListView

from .. import filters
from .. import forms
from .. import models


class DishListView(ListView):
    model = models.Dish
    template_name = "dashboard/dish/dish_list.html"

    def get(self, request: HttpRequest):
        filter = filters.DishFilter(request.GET, queryset=models.Dish.objects.all())
        return render(request, self.template_name, {"filter": filter})


class DishUpdateView(PermissionRequiredMixin, View):
    model = models.Dish
    template_name = "dashboard/dish/dish_update.html"
    permission_required = "dashboard.change_dish"

    def get(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishForm(instance=dish)
        return render(request, self.template_name, {"form": form, "dish": dish})

    def post(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("dashboard:menu"))
        return render(request, self.template_name, {"form": form, "dish": dish})


class DishDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.Dish
    template_name = "dashboard/dish/dish_delete.html"
    permission_required = "dashboard.delete_dish"
    success_url = reverse_lazy("dashboard:menu")

    def get(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        return render(request, self.template_name, {"dish": dish})
