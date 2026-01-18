import pytest
from django.db import transaction
from payouts.models import Payout, PayoutStatus

pytestmark = pytest.mark.django_db(transaction=True)


def test_create_payout_triggers_celery(api_client, mocker):
    mock_delay = mocker.patch("payouts.services.process_payout.delay")

    response = api_client.post(
        "/api/payouts/",
        {
            "amount": "100.00",
            "currency": "USD",
            "recipient_details": "Card ****1234",
            "comment": "Test payout",
        },
        format="json",
    )

    assert response.status_code == 201

    payout = Payout.objects.get()
    assert payout.status == PayoutStatus.CREATED

    mock_delay.assert_called_once_with(payout.id)
