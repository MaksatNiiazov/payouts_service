import time
from celery import shared_task
from django.db import transaction
from .models import Payout, PayoutStatus


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_payout(self, payout_id: int) -> None:
    with transaction.atomic():
        payout = (
            Payout.objects
            .select_for_update()
            .get(id=payout_id)
        )

        if payout.status != PayoutStatus.CREATED:
            return

        payout.status = PayoutStatus.PROCESSING
        payout.save(update_fields=["status", "updated_at"])

    time.sleep(2)

    with transaction.atomic():
        payout = (
            Payout.objects
            .select_for_update()
            .get(id=payout_id)
        )

        if payout.status != PayoutStatus.PROCESSING:
            return

        payout.status = PayoutStatus.COMPLETED
        payout.save(update_fields=["status", "updated_at"])
