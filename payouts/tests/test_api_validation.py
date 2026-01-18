import pytest

pytestmark = pytest.mark.django_db


def test_create_payout_negative_amount(api_client):
    response = api_client.post(
        "/api/payouts/",
        {
            "amount": "-10.00",
            "currency": "USD",
            "recipient_details": "Card ****1234",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "amount" in response.data


def test_create_payout_invalid_currency(api_client):
    response = api_client.post(
        "/api/payouts/",
        {
            "amount": "100.00",
            "currency": "BTC",
            "recipient_details": "Card ****1234",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "currency" in response.data


def test_create_payout_short_recipient_details(api_client):
    response = api_client.post(
        "/api/payouts/",
        {
            "amount": "100.00",
            "currency": "USD",
            "recipient_details": "123",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "recipient_details" in response.data
