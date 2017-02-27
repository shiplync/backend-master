from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RangeValidator(object):
    def __init__(self, lower=0.0, upper=0.0):
        self.lower = lower
        self.upper = upper
        self.error_message = "Value must be between %s and %s." % (lower, upper)

    def __call__(self, value):
        try:
            val = float(value)
        except ValueError:
            return

        if val < self.lower or val > self.upper:
            raise ValidationError(self.error_message)

    def __eq__(self, other):
        return (
            isinstance(other, RangeValidator) and
            self.lower == other.lower and
            self.upper == other.upper and
            self.error_message == other.error_message
        )

    def __ne__(self, other):
        return not (self == other)


@deconstructible
class LatitudeValidator(RangeValidator):
    def __init__(self):
        super(LatitudeValidator, self).__init__(lower=-90.0, upper=90.0)


@deconstructible
class LongitudeValidator(RangeValidator):
    def __init__(self):
        super(LongitudeValidator, self).__init__(lower=-180, upper=180.0)
