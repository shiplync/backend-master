from django.contrib.contenttypes.models import ContentType


def update_object(data, obj):
    for d in data:
        setattr(obj, d, data[d])
    obj.save()
    return obj


def obj_permissions(serializer, obj):
    request = serializer.context.get('request', None)
    if request:
        user = request.user
        ct = ContentType.objects.get_for_model(obj)
        change_name = 'change_%s' % ct.model
        delete_name = 'delete_%s' % ct.model

        return {
            'can_change': user.has_perm(change_name, obj),
            'can_delete': user.has_perm(delete_name, obj)
        }
    else:
        # If data is not being serialized by a view, (e.g. in tests) it will
        # not have a context
        return {}
