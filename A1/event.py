"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location, Location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF
from container import PriorityQueue


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.

    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> m = Monitor()
        >>> d = Dispatcher()
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> rq = RiderRequest(0, rd)
        >>> rq2 = RiderRequest(1, rd2)
        >>> results = PriorityQueue()
        >>> results.add(rq.do(d, m).pop())
        >>> print(m)
        Monitor (0 drivers, 1 riders)
        >>> print(results.remove())
        100 -- Lola: Cancel the request
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        >>> results.add(rq2.do(d, m).pop())
        >>> print(m)
        Monitor (0 drivers, 2 riders)
        >>> print(results.remove())
        11 -- Godzilla: Cancel the request
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        Godzilla at (10, 10) Patience: 10 Destination: (7, 1) Status: waiting
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.identifier, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)

        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> print(RiderRequest(0, rd))
        0 -- Lola: Request a driver
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> print(RiderRequest(5, rd2))
        5 -- Godzilla: Request a driver
        """
        return "{} -- {}: Request a driver".format(self.timestamp,
                                                   self.rider.identifier)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> m = Monitor()
        >>> d = Dispatcher()
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> d.wait_rd.add(rd)
        >>> dq = DriverRequest(0, dr)
        >>> dq2 = DriverRequest(1, dr2)
        >>> results = PriorityQueue()
        >>> results.add(dq.do(d, m).pop())
        >>> print(m)
        Monitor (1 drivers, 0 riders)
        >>> print(results.remove())
        0 -- Charles: Pick up Lola
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>
        >>> dq2.do(d, m)
        []
        >>> print(m)
        Monitor (2 drivers, 0 riders)
        >>> results.is_empty()
        True
        >>> print(d)
        Available Drivers:
        Bunny at (10, 10) Speed: 2 Is available: True
        Waiting Riders:
        <BLANKLINE>
        """
        events = []

        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.identifier, self.driver.location)

        # Request a rider from the dispatcher.
        rider = dispatcher.request_rider(self.driver)

        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
            return events

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> print(DriverRequest(0, dr))
        0 -- Charles: Request a rider
        >>> print(DriverRequest(1, dr2))
        1 -- Bunny: Request a rider
        """
        return "{} -- {}: Request a rider".format(self.timestamp,
                                                  self.driver.identifier)


class Cancellation(Event):
    """
    A rider cancels their pickup request.

    ===Attributes===
    @type rider: Rider
    """

    def __init__(self, timestamp, rider):
        """Initialize a Pickup event.

        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Cancel rider's request.

        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """
        monitor.notify(self.timestamp, RIDER, CANCEL,
                       self.rider.identifier, self.rider.origin)

        if self.rider.status == WAITING:
            self.rider.status = CANCELLED

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> print(Cancellation(0, rd))
        0 -- Lola: Cancel the request
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> print(Cancellation(5, rd2))
        5 -- Godzilla: Cancel the request
        """
        return "{} -- {}: Cancel the request".format(self.timestamp,
                                                     self.rider.identifier)


class Pickup(Event):
    """
    A driver picks up a rider.

    ===Attributes===
    @type driver: Driver
    @type rider: Rider
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event.

        @type rider: Rider
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver, self.rider = driver, rider

    def do(self, dispatcher, monitor):
        """Sets driver to drive the rider to the rider's destination. If the
        rider cancelled before they arrive then starts new DriverRequest event.

        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> m = Monitor()
        >>> d = Dispatcher()
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> rd2.status = CANCELLED
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr.destination = rd.origin
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> dr2.destination = rd2.origin
        >>> pu = Pickup(0, rd, dr)
        >>> pu2 = Pickup(0, rd2, dr2)
        >>> results = PriorityQueue()
        >>> results.add(pu.do(d, m).pop())
        >>> print(m)
        Monitor (1 drivers, 1 riders)
        >>> print(results.remove())
        3 -- Charles: Drop off Lola
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>
        >>> results.add(pu2.do(d, m).pop())
        >>> print(m)
        Monitor (2 drivers, 2 riders)
        >>> print(results.remove())
        0 -- Bunny: Request a rider
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>
        """
        events = []

        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.identifier, self.driver.destination)

        monitor.notify(self.timestamp, RIDER, PICKUP,
                       self.rider.identifier, self.rider.origin)

        self.driver.end_drive()

        # Rider is picked up successfully.
        if self.rider.status == WAITING:
            travel_time = self.driver.start_ride(self.rider)
            events.append(Dropoff(self.timestamp + travel_time, self.rider,
                                  self.driver))
            return events

        # Rider already cancelled the request.
        elif self.rider.status == CANCELLED:
            events.append(DriverRequest(self.timestamp, self.driver))
            return events

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> print(Pickup(0, rd, dr))
        0 -- Charles: Pick up Lola
        >>> print(Pickup(5, rd2, dr2))
        5 -- Bunny: Pick up Godzilla
        """
        return "{} -- {}: Pick up {}".format(self.timestamp,
                                             self.driver.identifier,
                                             self.rider.identifier)


class Dropoff(Event):
    """
    A driver drops off a rider.

    ===Attributes===
    @type driver: Driver
    @type rider: Rider
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff event.

        @type self: Dropoff
        @type rider: Rider
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver, self.rider = driver, rider

    def do(self, dispatcher, monitor):
        """Sets driver location to the rider's destination. DriverRequest event
        happens immediately.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> m = Monitor()
        >>> d = Dispatcher()
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr.destination = rd.destination
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> dr2.destination = rd2.destination
        >>> dof = Dropoff(0, rd, dr)
        >>> dof2 = Dropoff(0, rd2, dr2)
        >>> results = PriorityQueue()
        >>> results.add(dof.do(d, m).pop())
        >>> print(m)
        Monitor (1 drivers, 0 riders)
        >>> print(results.remove())
        0 -- Charles: Request a rider
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>
        >>> results.add(dof2.do(d, m).pop())
        >>> print(m)
        Monitor (2 drivers, 0 riders)
        >>> print(results.remove())
        0 -- Bunny: Request a rider
        >>> print(d)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>
        """
        events = []

        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.identifier, self.driver.destination)

        self.driver.end_ride()

        # Once a driver drops off a rider, this driver submits a new request.
        events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str

        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> print(Dropoff(0, rd, dr))
        0 -- Charles: Drop off Lola
        >>> print(Dropoff(5, rd2, dr2))
        5 -- Bunny: Drop off Godzilla
        """
        return "{} -- {}: Drop off {}".format(self.timestamp,
                                              self.driver.identifier,
                                              self.rider.identifier)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]

    # Not feasible for examples, because examples need to be extracted
    # from txt file.
    """
    events = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]
            identifier = tokens[2]
            location = deserialize_location(tokens[3])
            # HINT: Use Location.deserialize to convert the location string to
            # a location.
            event = None

            if event_type == "DriverRequest":
                speed = int(tokens[4])
                # Create a DriverRequest event.
                driver = Driver(identifier, location, speed)

                event = DriverRequest(timestamp, driver)

            elif event_type == "RiderRequest":
                destination = deserialize_location(tokens[4])
                patience = int(tokens[-1])
                # Create a RiderRequest event.
                rider = Rider(identifier, location, destination, patience)

                event = RiderRequest(timestamp, rider)

            events.append(event)

    return events
