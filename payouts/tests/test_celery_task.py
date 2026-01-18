import pytest
from payouts.models import Payout, PayoutStatus
from payouts.tasks import process_payout

pytestmark = pytest.mark.django_db


def test_process_payout_happy_path():
    payout = Payout.objects.create(
        amount="100.00",
        currency="USD",
        recipient_details="Card ****1234",
    )

    process_payout(payout.id)

    payout.refresh_from_db()
    assert payout.status == PayoutStatus.COMPLETED


def test_process_payout_idempotent():
    payout = Payout.objects.create(
        amount="100.00",
        currency="USD",
        recipient_details="Card ****1234",
        status=PayoutStatus.PROCESSING,
    )

    process_payout(payout.id)

    payout.refresh_from_db()
    assert payout.status == PayoutStatus.PROCESSING
