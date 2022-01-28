from django.http import HttpResponse


class stripe_webhook_handler:
    """ Handle Strip Webhooks"""

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """
        return HttpResponse{
            content='Webhook recieved: {event["type"]}',
            status=200
        }