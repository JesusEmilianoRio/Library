from django.contrib.auth.decorators import login_required
from .models import UserPayment
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import stripe

# Initialize stripe in payments app.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request, stripe_product_id):
    if request.method == "POST":
        #Get the product from UserPayment model
        product = UserPayment.objects.get(stripe_product_id =    stripe_product_id)

        YOUR_DOMAIN = f'{request.schema}://{request.get_host()}' #https://  127...

        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
            {
                'price_data': {
                    'currency': 'MXN',
                    'unit_amount': product.price * 100,
                    'product_data': {
                        'name': product.name,
                    },
                },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html', #change is not flask
            cancel_url=YOUR_DOMAIN + '/cancel.html', #change is not flask
        )
        except Exception as e:
            return str(e)

def success(request):
    pass

def cancel(request):
    pass