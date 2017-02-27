class VehicleType(object):
    FLATBED = 1
    REEFER = 2
    VAN = 3
    POWER_ONLY = 4

    CHOICES = (
        (FLATBED, 'Flatbed'),
        (REEFER, 'Reefer'),
        (VAN, 'Van'),
        (POWER_ONLY, 'Power Only')
    )

    @classmethod
    def valid(cls, vehicle):
        return cls.FLATBED <= vehicle <= cls.POWER_ONLY
