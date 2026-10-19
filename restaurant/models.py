from django.db import models


class Dish(models.Model):
    class Category(models.TextChoices):
        AFRICAN = "african", "African"
        INTERCONTINENTAL = "intercontinental", "Intercontinental"
        DRINKS = "drinks", "Drinks"

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=240)
    category = models.CharField(max_length=24, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="orders")
    dish_name = models.CharField(max_length=120)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"Order #{self.pk} - {self.dish_name}"

    def save(self, *args, **kwargs):
        if self.pk is None and self.dish:
            self.dish_name = self.dish.name
            self.unit_price = self.dish.price
        super().save(*args, **kwargs)