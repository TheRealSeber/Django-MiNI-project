from bs4 import BeautifulSoup
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .. import models


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = models.CustomUser.objects.create_superuser(
            email="admin@admin.com",
            username="admin",
            password="admin",
            email_is_verified=True,
        )
        cls.base_not_verified_user = models.CustomUser.objects.create(
            email="notverified@admin.com",
            username="notverified",
            password="notverified",
        )
        cls.client = Client()

    def test_dashboard_view(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")

    def test_administrator_button_enabled(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get("/dashboard/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(soup.find("a", {"href": reverse("dashboard:administrator")}))
        self.client.logout()

    def test_administrator_button_disabled(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get("/dashboard/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertFalse(soup.find("a", {"href": reverse("dashboard:administrator")}))
        self.client.logout()

    def test_logout_form_exists(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get("/dashboard/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(soup.find("form", {"action": reverse("dashboard:logout")}))
        self.client.logout()

    def test_verify_email_button_exists(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get("/dashboard/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(soup.find("input", {"name": "verify_email"}))
        self.client.logout()
