from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion


def add_starter_menu(apps, schema_editor):
    Dish = apps.get_model("restaurant", "Dish")
    starter_dishes = [
        ("Jollof rice & grilled chicken", "Smoky party jollof, flame-grilled chicken and a fresh side.", "african", "8500", "photo-1512058564366-18510be2db19", True),
        ("Egusi soup & pounded yam", "Rich melon-seed soup with greens, served with soft pounded yam.", "african", "9500", "photo-1547592180-85f173990554", True),
        ("Suya-spiced beef skewers", "Charred beef, northern suya spice, onion and ripe tomato.", "african", "7000", "photo-1529042410759-befb1204b468", False),
        ("Coconut curry prawns", "Juicy prawns simmered in coconut curry with fragrant rice.", "intercontinental", "12500", "photo-1559847844-5315695dadae", True),
        ("Creamy mushroom pasta", "Silky parmesan cream, sauteed mushrooms and fresh herbs.", "intercontinental", "10500", "photo-1473093295043-cdd812d0e601", False),
        ("Classic beef burger", "A juicy seasoned patty, sharp cheddar, crisp lettuce and house sauce.", "intercontinental", "11000", "photo-1568901346375-23c9450c58cd", False),
        ("Zobo cooler", "A bright, chilled hibiscus drink with ginger and citrus.", "drinks", "2500", "photo-1544145945-f90425340c7e", False),
        ("Fresh pineapple juice", "Pressed pineapple, served cold with a squeeze of lime.", "drinks", "3000", "photo-1600271886742-f049cd451bba", False),
    ]
    for name, description, category, price, photo, featured in starter_dishes:
        Dish.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "category": category,
                "price": Decimal(price),
                "image_url": f"https://images.unsplash.com/{photo}?auto=format&fit=crop&w=900&q=80",
                "is_available": True,
                "is_featured": featured,
            },
        )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dish",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.CharField(max_length=240)),
                ("category", models.CharField(choices=[("african", "African"), ("intercontinental", "Intercontinental"), ("drinks", "Drinks")], max_length=24)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image_url", models.URLField(max_length=500)),
                ("is_available", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["category", "name"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dish_name", models.CharField(max_length=120)),
                ("quantity", models.PositiveSmallIntegerField(default=1)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(choices=[("new", "New"), ("confirmed", "Confirmed"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="new", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("dish", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="restaurant.dish")),
            ],
        ),
        migrations.RunPython(add_starter_menu, migrations.RunPython.noop),
    ]