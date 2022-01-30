from django.http import HttpResponse


class stripe_webhook_handler:
    """ Handle Strip Webhooks"""

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook recieved: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded event fron Stripe"""
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )
    
    def handle_payment_intent_failed(self, event):
        """ Handle the payment_intent.succeeded event fron Stripe"""
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )
    