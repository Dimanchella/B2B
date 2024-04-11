from rest_framework import response, viewsets, status, pagination
from rest_framework.permissions import BasePermission
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination

from debug import IsDebug, IsDeepDebug, IsTrace, IsPrintExceptions, print_to, print_exception, trace_request

#   ----------------
#   GENERAL RESPONSE
#   ----------------

def general_response(results=None, response_status=status.HTTP_200_OK, headers=None, errors=None):
    trace_request('mixins.general_response', results=results)
    try:
        return response.Response({
            'results': results,
            'error': errors 
        }, response_status, headers)
    except Exception as err:
        if IsPrintExceptions:
            print_exception(stack=True, request=request)


class CreateModelMixin(viewsets.ModelViewSet):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        trace_request('mixins.CreateModelMixin.create', request=request, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return general_response(serializer.data, response_status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(viewsets.ModelViewSet, pagination.PageNumberPagination):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        trace_request('mixins.ListModelMixin.list', request=request)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return general_response(self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return general_response(serializer.data)


class RetrieveModelMixin(viewsets.ModelViewSet):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        trace_request('mixins.RetrieveModelMixin.retrieve', request=request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return general_response(serializer.data)


class UpdateModelMixin(viewsets.ModelViewSet):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        trace_request('mixins.UpdateModelMixin.update', request=request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return general_response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        trace_request('mixins.UpdateModelMixin.update', request=request)
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(viewsets.ModelViewSet):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        trace_request('mixins.DestroyModelMixin.destroy', request=request)
        return general_response(response_status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class IsOwnerOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        trace_request('mixins.IsOwnerOrAdminUser.has_permission', request=request)
        if request.method in ["POST", "PUT", "DELETE"]:
            return request.user and request.user.is_staff
        elif request.method in ['GET']:
            return request.user and request.user.is_authenticated
        else:
            return True


class GeneralModelViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    permission_classes = []


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12

    def get_paginated_response(self, data):
        return general_response({
            "count": self.page.paginator.count,
            "num_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "per_page": self.page.paginator.per_page,
            "results": data,
        })
