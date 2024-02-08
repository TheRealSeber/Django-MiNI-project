from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView

from . import forms
from . import models


def dashboard(request: HttpRequest):
    return render(request, "dashboard/dashboard.html")


class SignUpView(CreateView):
    form_class = forms.RegistrationForm
    success_url = reverse_lazy("dashboard:index")
    template_name = "dashboard/signup.html"


class LoginView(FormView):
    form_class = forms.LoginForm
    success_url = reverse_lazy("dashboard:index")
    template_name = "dashboard/login.html"

    def form_valid(self, form: forms.LoginForm):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)


class LogoutView(RedirectView):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse_lazy("dashboard:index"))


class DishListView(ListView):
    model = models.Dish
    template_name = "dashboard/dish_list.html"
    context_object_name = "dishes"


class DishUpdateView(PermissionRequiredMixin, View):
    model = models.Dish
    template_name = "dashboard/dish_update.html"
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


class AdministratorView(PermissionRequiredMixin, View):
    template_name = "dashboard/administrator.html"
    permission_required = "dashboard.add_dish"

    def get(self, request: HttpRequest):
        context = {}
        context["driver_form"] = forms.DriverForm()
        context["dish_form"] = forms.DishForm()
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        if "add_driver" in request.POST:
            form = forms.DriverForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect(reverse_lazy("dashboard:driver_list"))
        elif "add_dish" in request.POST:
            form = forms.DishForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect(reverse_lazy("dashboard:menu"))
        return HttpResponseBadRequest("Invalid form submission")
