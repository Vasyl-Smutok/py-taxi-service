from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        self.assertEqual(str(manufacturer),  f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )

        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            password="test password",
            first_name="test first",
            last_name="test last"
        )
        self.assertEqual(str(driver),  f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            password="test password",
            license_number="test license number"
        )

        self.assertEqual(driver.username, "test username")
        self.assertTrue(driver.check_password("test password"))
        self.assertEqual(driver.license_number, "test license number")
