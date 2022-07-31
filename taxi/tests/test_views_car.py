from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PrivateCarView(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicCarView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        test_manufacturer1 = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        Car.objects.create(
            model="Test1 model",
            manufacturer=test_manufacturer1
        )
        Car.objects.create(
            model="Test2 model",
            manufacturer=test_manufacturer1
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
