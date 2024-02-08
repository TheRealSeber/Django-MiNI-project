from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView

from . import filters
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

    def get(self, request: HttpRequest):
        filter = filters.DishFilter(request.GET, queryset=models.Dish.objects.all())
        return render(request, self.template_name, {"filter": filter})


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


class DishDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.Dish
    template_name = "dashboard/dish_delete.html"
    permission_required = "dashboard.delete_dish"
    success_url = reverse_lazy("dashboard:menu")

    def get(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        return render(request, self.template_name, {"dish": dish})


class DishReviewCreateView(LoginRequiredMixin, CreateView):
    model = models.DishReview
    fields = "__all__"
    template_name = "dashboard/dish_review_create.html"
    success_url = reverse_lazy("dashboard:menu")

    def get(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishReviewForm(initial={"dish": dish})
        return render(request, self.template_name, {"form": form, "dish": dish})

    def post(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("dashboard:menu"))
        return render(request, self.template_name, {"form": form, "dish": dish})


class DishReviewListView(ListView):
    model = models.DishReview
    template_name = "dashboard/dish_reviews_list.html"
    context_object_name = "reviews"


class DishReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.DishReview
    template_name = "dashboard/dish_review_delete.html"
    permission_required = "dashboard.delete_dishreview"
    success_url = reverse_lazy("dashboard:reviews")

    def get(self, request: HttpRequest, pk: int):
        review = models.DishReview.objects.get(pk=pk)
        return render(request, self.template_name, {"review": review})


class DriverListView(ListView):
    model = models.Driver
    template_name = "dashboard/driver_list.html"
    context_object_name = "drivers"

    def get(self, request: HttpRequest):
        filter = filters.DriverFilter(request.GET, queryset=models.Driver.objects.all())
        return render(request, self.template_name, {"filter": filter})


class DriverUpdateView(PermissionRequiredMixin, View):
    model = models.Driver
    template_name = "dashboard/driver_update.html"
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
    template_name = "dashboard/driver_delete.html"
    permission_required = "dashboard.delete_driver"
    success_url = reverse_lazy("dashboard:driver_list")

    def get(self, request: HttpRequest, pk: int):
        driver = models.Driver.objects.get(pk=pk)
        return render(request, self.template_name, {"driver": driver})


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
            form = forms.DriverForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect(reverse_lazy("dashboard:driver_list"))
        elif "add_dish" in request.POST:
            form = forms.DishForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect(reverse_lazy("dashboard:menu"))
        return HttpResponseBadRequest("Invalid form submission")
