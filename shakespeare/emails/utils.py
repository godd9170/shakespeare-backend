import stripe
from django.conf import settings
from pinax.stripe.models import Customer
stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY

def charge_email(user):
    customer_id = Customer.objects.get(user=user).stripe_id
    amount = user.shakespeareuser.price
    stripe.InvoiceItem.create(
        customer=customer_id,
        amount=amount,
        currency="usd",
        description="Email"
    )
