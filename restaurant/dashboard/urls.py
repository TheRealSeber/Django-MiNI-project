from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("restricted/", views.restricted_view, name="restricted_view"),
    path("menu/", views.DishListView.as_view(current_page="menu"), name="menu"),
]
