from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str | int,
        date: datetime = None
) -> Order:

    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
