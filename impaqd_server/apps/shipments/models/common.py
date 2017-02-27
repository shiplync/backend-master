def full_user_name(self):
    # Used by GenericUser and Person models
    return ((self.first_name + ' ' + self.last_name) if self.first_name
            and self.last_name else self.first_name if self.first_name
            else self.email)


def get_empty_required_fields(obj, fields):
    # Get empty required fields on shipment models
    empty_required_fields = []
    for f in fields:
        f_value = getattr(obj, f, None)
        if not f_value or f_value == '' or f_value == 0:
            empty_required_fields.append(f)
    return empty_required_fields


def instance_has_changed(instance):
    # check if instance is different from db row
    if instance.pk is None:
        return True
    db_instance = type(instance).objects.get(pk=instance.pk)
    excluded = ('id', 'created_at', 'updated_at',)
    for v in vars(instance):
        if (v not in excluded and v[0] != '_' and
                getattr(instance, v) != getattr(db_instance, v)):
            return True
    return False


def build_unicode_string(obj, attrs):
    res = ''
    for a in attrs:
        val = getattr(obj, a, None)
        if val:
            res += '%s ' % val
    if res:
        return res
    elif obj.pk:
        return str(obj.pk)
    else:
        return None
