import requests
from django.conf import settings
from requests.exceptions import HTTPError
from rest_framework.renderers import JSONRenderer
from celery import shared_task

from .models import ExchangeNode
from .serializers import ExchangeNodeSerializer


@shared_task
def upload_orders():
    try:
        for order in ExchangeNode.objects.all():
            serializer = ExchangeNodeSerializer(order)
            json = JSONRenderer().render(serializer.data)
            response = requests.post(
                settings.HTTP_SERVICE,
                headers={'Content-Type': 'application/json'},
                auth=(settings.HTTP_USER, settings.HTTP_PASSWORD),
                data=json
            )
            if response.status_code >= 300:
                raise HTTPError(response.status_code, response)
            order.delete()
    except HTTPError as err:
        print(f"HTTP error: {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
    else:
        print("OK")
