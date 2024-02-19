import os

from bs4 import BeautifulSoup
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .. import models

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(TESTS_DIR, "assets")


class DishTests(TestCase):
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

        cls.dish_1 = models.Dish.objects.create(
            name="Dish 1",
            description="Description 1",
            price=10.00,
            available=True,
            image=os.path.join(ASSETS_DIR, "dish_1.jpg"),
        )
        cls.dish_2 = models.Dish.objects.create(
            name="Dish 2",
            description="Description 2",
            price=15.00,
            available=False,
            image=os.path.join(ASSETS_DIR, "dish_2.jpg"),
        )

        cls.dish_3 = models.Dish.objects.create(
            name="Dish 3",
            description="Description 3",
            price=20.00,
            available=True,
            image=os.path.join(ASSETS_DIR, "dish_3.jpg"),
        )

        cls.client = Client()

    def test_menu_view(self):
        response = self.client.get(reverse("dashboard:menu"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dish/dish_list.html")

    def test_menu_view_dishes(self):
        response = self.client.get(reverse("dashboard:menu"))
        soup = BeautifulSoup(response.content, "html.parser")
        dishes = soup.find_all("div", {"class": "card h-100"})
        self.assertEqual(len(dishes), 3)

    def test_modify_dish_button_exists(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("dashboard:menu"))
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(
            soup.find(
                "a", {"href": reverse("dashboard:dish_update", args=[self.dish_1.pk])}
            )
        )
        self.client.logout()

    def test_add_review_button_exists(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(reverse("dashboard:menu"))
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(
            soup.find(
                "a",
                {"href": reverse("dashboard:add_dish_review", args=[self.dish_1.pk])},
            )
        )
        self.client.logout()

    def test_can_modify_dish(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(
            reverse("dashboard:dish_update", args=[self.dish_1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dish/dish_update.html")
        self.client.logout()

    def test_access_denied_modify_dish(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(
            reverse("dashboard:dish_update", args=[self.dish_1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_access_denied_delete_dish(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(
            reverse("dashboard:delete_dish", args=[self.dish_1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()
