from urllib.parse import urlencode

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Dish, Order


WHATSAPP_NUMBER = "2349065400858"


def home(request):
    dishes = Dish.objects.filter(is_available=True)
    return render(request, "restaurant/home.html", {"dishes": dishes})


def place_order(request, dish_id):
    if request.method != "POST":
        return redirect("home")

    dish = get_object_or_404(Dish, pk=dish_id, is_available=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, min(quantity, 20))

    order = Order.objects.create(
        dish=dish,
        dish_name=dish.name,
        quantity=quantity,
        unit_price=dish.price,
    )
    message = (
        f"Hello Mimi's Table! I'd like to order:\n"
        f"Order #{order.pk}: {order.dish_name} x{order.quantity}\n"
        f"Total: NGN {order.total_price:,.2f}\n"
        "Please confirm availability and delivery details."
    )
    return redirect(f"https://wa.me/{WHATSAPP_NUMBER}?{urlencode({'text': message})}")


@staff_member_required
def management_dashboard(request):
    today = timezone.localdate()
    context = {
        "dish_count": Dish.objects.count(),
        "available_count": Dish.objects.filter(is_available=True).count(),
        "order_count": Order.objects.count(),
        "new_orders": Order.objects.filter(status=Order.Status.NEW).count(),
        "today_orders": Order.objects.filter(created_at__date=today).count(),
        "recent_orders": Order.objects.select_related("dish")[:8],
    }
    return render(request, "restaurant/management.html", context)