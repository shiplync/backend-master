from impaqd_server.apps.shipments.tasks import worker_test_task
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
def worker_test(request):
    """
    Test that the messaging and worker setup works
    """
    asyncResult = worker_test_task.delay()
    # Wait for restult
    result = asyncResult.get(timeout=5)
    if result:
        return Response({'success': result})
    else:
        return Response({
            'success': False
            }, status=500)
