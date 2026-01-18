from django.db import transaction
from .models import Payout
from .tasks import process_payout


def create_payout(*, data: dict) -> Payout:
    """
    Создаёт заявку и ставит Celery-задачу ТОЛЬКО после коммита.
    """
    with transaction.atomic():
        payout = Payout.objects.create(**data)

        transaction.on_commit(
            lambda: process_payout.delay(payout.id)
        )

    return payout
