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
    path(
        "add_dish_review/<int:pk>/",
        views.DishReviewCreateView.as_view(),
        name="add_dish_review",
    ),
    path(
        "administrator/delete_dish/<int:pk>/",
        views.DishDeleteView.as_view(),
        name="delete_dish",
    ),
    path("reviews/", views.DishReviewListView.as_view(), name="reviews"),
    path(
        "administrator/delete_review/<int:pk>/",
        views.DishReviewDeleteView.as_view(),
        name="delete_review",
    ),
    path("driver_list/", views.DriverListView.as_view(), name="driver_list"),
    path(
        "administrator/driver_update/<int:pk>/",
        views.DriverUpdateView.as_view(),
        name="driver_update",
    ),
    path(
        "administrator/delete_driver/<int:pk>/",
        views.DriverDeleteView.as_view(),
        name="delete_driver",
    ),
]
