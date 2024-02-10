from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import RedirectView

from .. import forms
from ..tokens import account_activation_token

User = get_user_model()


class VerifyEmailConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.email_is_verified = True
            user.save()
            messages.success(request, "Your email has been verified.")
        else:
            messages.warning(request, "The link is invalid.")

        return redirect(reverse_lazy("dashboard:index"))


class DashboardView(View):
    template_name = "dashboard/dashboard.html"

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest):
        if "verify_email" in request.POST:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string(
                "dashboard/verify_email_message.html",
                {
                    "request": request,
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = "html"
            email.send()
            return render(request, "dashboard/dashboard.html", {"email_sent": True})


class SignUpView(CreateView):
    form_class = forms.RegistrationForm
    success_url = reverse_lazy("dashboard:index")
    template_name = "dashboard/signup.html"


class LoginView(FormView):
    form_class = forms.LoginForm
    success_url = reverse_lazy("dashboard:index")
    template_name = "dashboard/login.html"

    def form_valid(self, form: forms.LoginForm):
        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid Email or password.")
            return self.form_invalid(form)


class LogoutView(RedirectView):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse_lazy("dashboard:index"))


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
