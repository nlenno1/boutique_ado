from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """ A view to return the checkout page """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KLUjyEOKmuxWaEDbqpWyqMP9Kvwv59JLov4nKJhXxIwt4aWzRil14wrPTOb6S9CwmP3Vsc8ReD5y7Qnw0sWOdIc00opad7Sy5',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
