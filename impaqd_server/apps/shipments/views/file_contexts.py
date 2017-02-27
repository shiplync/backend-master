from ..serializers.users import FileContextSerializer
from ..utils import json_response, resize_image, create_or_update_remote_file
from ..models import FileContext

from rest_framework import generics
from rest_framework.authentication import (
    TokenAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


import logging
LOG = logging.getLogger('impaqd')


class FileUploadView(generics.GenericAPIView):
    """View to handle upload of a single files.

    Can be used to either upload a new file or update an existing file.
    Every file is maintained by a FileContext object.
    Example use: curl -x POST -F "file=@photo.jpg" host/?path=profile_photo

    TODO: A lot of the logic in this view can probably be moved out to the
    serializer or model. Also, ideally the file processing and uploading should
    be executed as a background job.

    Data:
    path  --  points to a FileContext field on the GenericUser (supports object
    dot notation)
    file -- points to local file on client
    returns: {url : url pointing to resource with 30s TTL}
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = FileContextSerializer

    def post(self, request, format=None):
        file_obj = request.data.get('file')
        # Get path variable
        path = self.request.GET.get('path')
        # Verify that path points to a valid field (or nested field)
        # on the user object.
        # TODO: Ability to assign filecontext to an object of any type.
        # E.g. "?assignee_content_type=shipment&assignee_id=123&attr=bol
        valid_paths = ['profile_photo', 'company.logo']
        if path in valid_paths:
            # Process files according to their path
            url_ttl = 30  # Default url ttl
            if path in ['profile_photo', 'company.logo']:
                try:
                    size = 300, 300
                    file_obj = resize_image(file_obj, size)
                    url_ttl = 99999999  # 3 years
                except Exception, e:
                    import traceback
                    LOG.error(traceback.format_exc())
                    return json_response({
                        'error': 'unable to resize image. ',
                        'detail': str(e)
                    }, status=500)
            # Get FileContext from dotted path (relative to user object)
            file_context = None
            assignee = None
            attr = None
            if path == 'profile_photo':
                assignee = request.user.genericuser
                file_context = assignee.profile_photo
                attr = 'profile_photo'
            elif path == 'company.logo':
                assignee = request.user.genericuser.company
                file_context = assignee.logo
                attr = 'logo'
            # If FileContext doesn't exists, create it
            if not file_context:
                file_context = FileContext.objects.create(
                    path=path, url_ttl=url_ttl)
                setattr(assignee, attr, file_context)
                assignee.save()
            # Update file remotely
            try:
                file_obj.seek(0)
                create_or_update_remote_file(file_context, file_obj)
            except Exception, e:
                import traceback
                LOG.error(traceback.format_exc())
                return json_response({
                    'error': 'unable to update file remotely. ',
                    'detail': str(e)
                }, status=500)

            return json_response({
                'url': file_context.file_url
            }, status=202)
        else:
            return json_response({
                'detail': 'you must supply a valid path variable in the url'
            }, status=406)
