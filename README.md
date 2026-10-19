# Mimi's Table

A responsive Django restaurant menu for African and intercontinental dishes. Customers can order a dish and quantity; the order is saved in the database, then WhatsApp opens with the order details pre-filled for **+234 906 540 0858**. The customer sends the message in WhatsApp to complete the handoff.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the menu. The first migration adds sample menu items; edit or replace them in the admin.

## Staff tools

- `http://127.0.0.1:8000/management/` is the staff-only overview for menu and recent order counts.
- `http://127.0.0.1:8000/admin/` is Django's full admin. Staff can add dishes, update prices and availability, create orders, and update order statuses.

## Checks

```bash
python manage.py test
python manage.py check
```

For deployment, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS`; configure HTTPS and a production database before accepting real orders.