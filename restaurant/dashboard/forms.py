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


class DriverForm(forms.ModelForm):
    class Meta:
        model = models.Driver
        fields = "__all__"
        labels = {
            "name": "Driver Name",
            "email": "Email",
            "phone": "Phone",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Driver Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone",
                }
            ),
        }
