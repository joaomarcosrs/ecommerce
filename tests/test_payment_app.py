import pytest

pytestmark = pytest.mark.skip(
    reason='Domínio payment/Stripe ainda não implementado no projeto.'
)


def test_create_payment_intent_for_order():
    raise NotImplementedError


def test_payment_webhook_updates_order_status():
    raise NotImplementedError
