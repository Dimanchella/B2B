from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler, Response
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            desc = str(exc)
            response.data.clear()
        else:
            desc = response.data.pop('detail', None)

        response.data['results'] = None
        response.data['error'] = {
            'code': response.status_code,
            'desc': desc,
            'view': str(context['view']),
            'args': str(context['args']),
            'kwargs': str(context['kwargs']),
            'request': str(context['request'])
        }

    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                'results': None,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'desc': str(exc),
                    'view': str(context['view']),
                    'args': str(context['args']),
                    'kwargs': str(context['kwargs']),
                    'request': str(context['request'])
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
