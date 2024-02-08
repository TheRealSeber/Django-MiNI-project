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


class DriverListView(ListView):
    model = models.Driver
    template_name = "dashboard/driver/driver_list.html"
    context_object_name = "drivers"

    def get(self, request: HttpRequest):
        filter = filters.DriverFilter(request.GET, queryset=models.Driver.objects.all())
        return render(request, self.template_name, {"filter": filter})


class DriverUpdateView(PermissionRequiredMixin, View):
    model = models.Driver
    template_name = "dashboard/driver/driver_update.html"
    permission_required = "dashboard.change_driver"

    def get(self, request: HttpRequest, pk: int):
        driver = models.Driver.objects.get(pk=pk)
        form = forms.DriverForm(instance=driver)
        return render(request, self.template_name, {"form": form, "driver": driver})

    def post(self, request: HttpRequest, pk: int):
        driver = models.Driver.objects.get(pk=pk)
        form = forms.DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("dashboard:driver_list"))
        return render(request, self.template_name, {"form": form, "driver": driver})


class DriverDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.Driver
    template_name = "dashboard/driver/driver_delete.html"
    permission_required = "dashboard.delete_driver"
    success_url = reverse_lazy("dashboard:driver_list")

    def get(self, request: HttpRequest, pk: int):
        driver = models.Driver.objects.get(pk=pk)
        return render(request, self.template_name, {"driver": driver})
