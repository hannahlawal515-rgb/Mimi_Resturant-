from django.contrib import admin
from django.urls import path

from restaurant import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("order/<int:dish_id>/", views.place_order, name="place_order"),
    path("management/", views.management_dashboard, name="management_dashboard"),
]