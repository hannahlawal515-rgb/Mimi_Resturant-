from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Dish, Order


class RestaurantFlowTests(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(
            name="Jollof rice",
            description="Smoky rice with grilled chicken.",
            category=Dish.Category.AFRICAN,
            price="8500.00",
            image_url="https://example.com/jollof.jpg",
        )

    def test_menu_shows_available_dishes_and_order_controls(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Jollof rice")
        self.assertContains(response, "Order now")
        self.assertContains(response, "ADD FOOD")

    def test_order_is_saved_and_whatsapp_message_contains_order_details(self):
        response = self.client.post(reverse("place_order", args=[self.dish.pk]), {"quantity": "2"})

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        self.assertEqual(order.total_price, 17000)
        self.assertIn("https://wa.me/2349065400858", response["Location"])
        message = parse_qs(urlparse(response["Location"]).query)["text"][0]
        self.assertIn(f"Order #{order.pk}", message)
        self.assertIn("Jollof rice x2", message)
        self.assertIn("NGN 17,000.00", message)

    def test_order_uses_price_snapshot(self):
        self.client.post(reverse("place_order", args=[self.dish.pk]), {"quantity": "1"})
        self.dish.price = "9900.00"
        self.dish.save()

        self.assertEqual(Order.objects.get().unit_price, 8500)

    def test_management_dashboard_requires_staff(self):
        response = self.client.get(reverse("management_dashboard"))
        self.assertEqual(response.status_code, 302)

        staff = get_user_model().objects.create_user(username="manager", password="test-password", is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse("management_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RESTAURANT CONTROL")