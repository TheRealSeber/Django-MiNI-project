import os

from bs4 import BeautifulSoup
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .. import models

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(TESTS_DIR, "assets")


class DishReviewTests(TestCase):
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
        cls.dish_review_1 = models.DishReview.objects.create(
            dish=cls.dish_1,
            stars=5,
            review="Comment 1",
        )
        cls.dish_review_2 = models.DishReview.objects.create(
            dish=cls.dish_1,
            stars=4,
            review="Comment 2",
        )

        cls.client = Client()

    def test_dish_review_view(self):
        response = self.client.get(reverse("dashboard:reviews"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "dashboard/dish_review/dish_reviews_list.html"
        )

    def test_dish_review_view_reviews(self):
        response = self.client.get(reverse("dashboard:reviews"))
        soup = BeautifulSoup(response.content, "html.parser")
        reviews = soup.find_all("div", {"class": "card h-100"})
        self.assertEqual(len(reviews), 2)

    def test_dish_review_delete_button_exists(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse("dashboard:reviews"))
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertTrue(
            soup.find(
                "a",
                {
                    "href": reverse(
                        "dashboard:delete_review", args=[self.dish_review_1.pk]
                    )
                },
            )
        )
        self.assertTrue(
            soup.find(
                "a",
                {
                    "href": reverse(
                        "dashboard:delete_review", args=[self.dish_review_2.pk]
                    )
                },
            )
        )
        self.client.logout()

    def test_access_denied_delete_dish_review_user(self):
        self.client.force_login(user=self.base_not_verified_user)
        response = self.client.get(
            reverse("dashboard:delete_review", args=[self.dish_review_1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_can_delete_dish_review(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            reverse("dashboard:delete_review", args=[self.dish_review_1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.DishReview.objects.count(), 1)
        self.client.logout()
