from impaqd_server.apps.shipments import serializers

from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination


def nested_or_flat_serializer(serializer_name, request):
    '''Return nested or flat serializer based on `the nested` url parameter

    serilizer_name -- (string) name of serializer
    request -- request object with an optional `nested` url variable
    nested  -- if true, return nested serializer (if it exists)
    '''
    nested = False
    nested = (request.GET.get('nested', False) == 'true')

    # Using depth is deprecated
    d = request.GET.get('depth', '0')
    nested = nested or (d.isdigit() and int(d) > 0)

    default_serializer = getattr(serializers, serializer_name)
    if nested:
        return getattr(
            serializers, serializer_name + 'Nested', default_serializer)
    else:
        return default_serializer


class ViewValidationError(APIException):
    status_code = 400


class ViewDoesNotExistError(APIException):
    status_code = 404


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'paginate_by'
    max_page_size = 1000
