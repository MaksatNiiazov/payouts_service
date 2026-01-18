import pytest
from payouts.models import Payout

pytestmark = pytest.mark.django_db


def test_create_payout_idempotency_key(api_client):
    payload = {
        "amount": "100.00",
        "currency": "USD",
        "recipient_details": "Card ****1234",
    }

    response_1 = api_client.post(
        "/api/payouts/",
        payload,
        format="json",
        HTTP_IDEMPOTENCY_KEY="test-key-123",
    )

    assert response_1.status_code == 201
    assert Payout.objects.count() == 1

    response_2 = api_client.post(
        "/api/payouts/",
        payload,
        format="json",
        HTTP_IDEMPOTENCY_KEY="test-key-123",
    )

    assert response_2.status_code == 201
    assert response_1.json() == response_2.json()
    assert Payout.objects.count() == 1


def test_create_payout_without_idempotency_key_creates_multiple(api_client):
    payload = {
        "amount": "100.00",
        "currency": "USD",
        "recipient_details": "Card ****1234",
    }

    api_client.post("/api/payouts/", payload, format="json")
    api_client.post("/api/payouts/", payload, format="json")

    assert Payout.objects.count() == 2


def test_create_payout_different_idempotency_keys(api_client):
    payload = {
        "amount": "100.00",
        "currency": "USD",
        "recipient_details": "Card ****1234",
    }

    api_client.post(
        "/api/payouts/",
        payload,
        format="json",
        HTTP_IDEMPOTENCY_KEY="key-1",
    )
    api_client.post(
        "/api/payouts/",
        payload,
        format="json",
        HTTP_IDEMPOTENCY_KEY="key-2",
    )

    assert Payout.objects.count() == 2
