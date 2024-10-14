import os

from bs4 import BeautifulSoup
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .. import models

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(TESTS_DIR, "assets")


class DriverTests(TestCase):
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

        cls.driver_1 = models.Driver.objects.create(
            name="Driver 1",
            nationality="Poland",
            phone="+48 662126789",
            available=True,
            image=os.path.join(ASSETS_DIR, "driver_1.jpg"),
        )
        cls.driver_2 = models.Driver.objects.create(
            name="Driver 2",
            nationality="Ukraine",
            phone="38 0445551234",
            available=False,
            image=os.path.join(ASSETS_DIR, "driver_2.jpg"),
        )

        cls.client = Client()

    def test_driver_list_view(self):
        response = self.client.get(reverse("dashboard:driver_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/driver/driver_list.html")

    def test_driver_list_view_drivers(self):
        response = self.client.get(reverse("dashboard:driver_list"))
        soup = BeautifulSoup(response.content, "html.parser")
        drivers = soup.find_all("div", {"class": "driver-card"})
        self.assertEqual(len(drivers), 2)

    def test_modify_driver_button_exists(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("dashboard:driver_list"))
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(
            soup.find(
                "a",
                {"href": reverse("dashboard:driver_update", args=[self.driver_1.pk])},
            )
        )
        self.client.logout()

    def test_can_modify_driver(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(
            reverse("dashboard:driver_update", args=[self.driver_1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/driver/driver_update.html")
        self.client.logout()

    def test_access_denied_modify_driver(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(
            reverse("dashboard:driver_update", args=[self.driver_1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_access_denied_delete_driver(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(
            reverse("dashboard:delete_driver", args=[self.driver_1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()
