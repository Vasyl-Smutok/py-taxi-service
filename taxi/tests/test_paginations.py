from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver
from django.test import TestCase


DRIVER_URL = reverse("taxi:driver-list")


class PaginationDriver(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test___",
            password="test password"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        number_of_driver = 15
        for driver_num in range(number_of_driver):
            Driver.objects.create(
                username=f"Test username {driver_num}",
                first_name=f"Test first name {driver_num}",
                last_name=f"Test last name {driver_num}",
                license_number=f"ASD1234{driver_num}"
            )

    def test_pagination_is_seven(self):
        response = self.client.get(DRIVER_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["driver_list"]) == 7)

    def test_lists_all_driver(self):
        resp = self.client.get(reverse("taxi:driver-list") + "?page=3")
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] is True)
        self.assertTrue(len(resp.context["driver_list"]) == 2)
