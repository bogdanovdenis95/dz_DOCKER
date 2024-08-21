import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_stripe_product(name, description):
    product = stripe.Product.create(
        name=name,
        description=description,
    )
    return product.id

def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  
        currency='usd',
    )
    return price.id

def create_checkout_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
