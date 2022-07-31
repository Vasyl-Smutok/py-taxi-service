from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PrivateDriverView(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicDriverView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test___",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        driver1 = Driver.objects.create_user(
            username="Test1 username",
            password="Test1 password",
            license_number="Test1 license number"
        )
        driver1.save()

        driver2 = Driver.objects.create_user(
            username="Test2 username",
            password="Test2 password",
            license_number="Test2 license number"
        )
        driver2.save()

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
