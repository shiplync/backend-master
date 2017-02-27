class DeliveryStatus(object):
    OPEN = 1
    PENDING_PICKUP = 2
    ENROUTE = 3
    DELIVERED = 4
    PENDING_APPROVAL = 5

    CHOICES = (
        (OPEN, 'Open'),
        (PENDING_PICKUP, 'Pending Pickup'),
        (ENROUTE, 'Enroute'),
        (DELIVERED, 'Delivered'),
        (PENDING_APPROVAL, 'Pending Approval'),
    )

    @classmethod
    def valid(cls, status):
        return cls.OPEN <= status <= cls.PENDING_APPROVAL

    ALL_STATUSES = [OPEN, PENDING_PICKUP, ENROUTE, DELIVERED, PENDING_APPROVAL]
    ACTIVE_STATUSES = [PENDING_PICKUP, ENROUTE]
    HAS_CARRIER_STATUSES = [PENDING_PICKUP, ENROUTE, DELIVERED, PENDING_APPROVAL]
    CARRIER_APPROVED_STATUSES = [PENDING_PICKUP, ENROUTE, DELIVERED]
