from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView

from . import forms
from . import models


# Create your views here.
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

    current_page = "menu"


@login_required
def restricted_view(request):
    return render(request, "dashboard/restricted_view.html")
