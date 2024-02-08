from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                }
            ),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )


class DishForm(forms.ModelForm):
    class Meta:
        model = models.Dish
        fields = "__all__"
        labels = {
            "name": "Dish Name",
            "description": "Description",
            "price": "Price",
            "available": "Available",
            "image": "Image",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dish Name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                    "rows": 4,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price",
                }
            ),
            "available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class DishReviewForm(forms.ModelForm):
    class Meta:
        model = models.DishReview
        fields = "__all__"
        labels = {
            "dish": "Dish",
            "name": "Your Name",
            "stars": "Stars",
            "review": "Review",
        }

        widgets = {
            "dish": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name",
                }
            ),
            "stars": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Stars",
                }
            ),
            "review": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Review",
                }
            ),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = models.Driver
        fields = "__all__"
        labels = {
            "name": "Driver Name",
            "phone": "Phone",
            "image": "Image",
            "nationality": "Nationality",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Driver Name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "nationality": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nationality",
                }
            ),
        }
