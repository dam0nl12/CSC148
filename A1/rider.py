from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider for a ride-sharing service.

    === Attributes ===
    @type identifier: str
        A unique identifier for the rider.
    @type origin: Location
        The current location of the rider.
    @type status: str
        The current status of the rider.
    """

    def __init__(self, identifier, origin, destination, patience):
        """Initialize a rider.

        @type self: Rider
        @type identifier: str
        @type origin: Location
        @type destination: Location
        @type patience: int
        """
        (self.identifier, self.origin, self.destination, self.patience,
         self.status) = (identifier, origin, destination, patience, WAITING)

    def __str__(self):
        """Return a string representation.

        @type self: Rider
        @rtype: str

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> print(rd)
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        >>> print(rd2)
        Godzilla at (10, 10) Patience: 10 Destination: (7, 1) Status: waiting
        """
        return '{0} at {1} Patience: {2} Destination: {3} Status: {4}'\
            .format(self.identifier, self.origin, self.patience,
                    self.destination, self.status)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Rider
        @rtype: bool

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> rd3 = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd == rd2
        False
        >>> rd == rd3
        True
        """
        return ((self.identifier == other.identifier) and
                (self.origin == other.origin) and
                (self.destination == other.destination) and
                (self.patience == other.patience) and
                (self.status == other.status))
