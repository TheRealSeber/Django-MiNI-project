from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("menu/", views.DishListView.as_view(), name="menu"),
    path("administrator/", views.AdministratorView.as_view(), name="administrator"),
    path(
        "administrator/dish_update/<int:pk>/",
        views.DishUpdateView.as_view(),
        name="dish_update",
    ),
]
