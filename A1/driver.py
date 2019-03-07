from location import Location, manhattan_distance
from rider import Rider, SATISFIED


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type identifier: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        Precondition: speed > 0

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        (self.identifier, self.location, self.speed, self.is_idle,
         self.destination) = (identifier, location, speed, True, None)

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> print(dr)
        Charles at (0, 0) Speed: 3 Is available: True
        >>> print(dr2)
        Bunny at (10, 10) Speed: 2 Is available: True
        """
        return ('{0} at {1} Speed: {2} Is available: {3}'.format(
            self.identifier, self.location, self.speed, self.is_idle))

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> dr3 = Driver('Charles', Location(0, 0), 3)
        >>> dr == dr2
        False
        >>> dr == dr3
        True
        """
        return ((self.identifier == other.identifier) and
                (self.location == other.location) and
                (self.speed == other.speed) and
                (self.is_idle == other.is_idle))

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> dr.get_travel_time(Location(5, 6))
        4
        >>> dr2.get_travel_time(Location(0, 0))
        10
        """
        return round((manhattan_distance(self.location, destination) /
                      self.speed))

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> dr.start_drive(Location(4,3))
        2
        >>> dr.is_idle
        False
        >>> dr2.start_drive(Location(0, 0))
        10
        >>> dr.is_idle
        False
        """
        self.is_idle = False
        self.destination = location
        return self.get_travel_time(location)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> dr.start_ride(rd)
        3
        >>> dr2.start_ride(rd2)
        6
        """
        self.destination = rider.destination
        rider.status = SATISFIED
        return self.get_travel_time(rider.destination)
        # preceding events should guarantee that this is the case:
        # driver's location is same as rider's location.

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None
