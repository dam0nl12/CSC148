from location import manhattan_distance, Location

"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
@type RIDER: str
    A constant used for the Rider activity category.
@type DRIVER: str
    A constant used for the Driver activity category.
@type REQUEST: str
    A constant used for the request activity description.
@type CANCEL: str
    A constant used for the cancel activity description.
@type PICKUP: str
    A constant used for the pickup activity description.
@type DROPOFF: str
    A constant used for the dropoff activity description.
"""

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    @type timestamp: int
        The time at which the activity occurred.
    @type description: str
        A description of the activity.
    @type identifier: str
        An identifier for the person doing the activity.
    @type location: Location
        The location at which the activity occurred.
    """

    def __init__(self, timestamp, description, identifier, location):
        """Initialize an Activity.

        @type self: Activity
        @type timestamp: int
        @type description: str
        @type identifier: str
        @type location: Location
        @rtype: None
        """
        self.description = description
        self.time = timestamp
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    # @type _activities: dict[str, dict[str, list[Activity]]]
    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self):
        """Initialize a Monitor.

        @type self: Monitor
        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self):
        """Return a string representation.

        @type self: Monitor
        @rtype: str
        """
        return "Monitor ({} drivers, {} riders)".format(
                len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp, category, description, identifier, location):
        """Notify the monitor of the activity.

        @type self: Monitor
        @type timestamp: int
            The time of the activity.
        @type category: DRIVER | RIDER
            The category for the activity.
        @type description: REQUEST | CANCEL | PICKUP | DROP_OFF
            A description of the activity.
        @type identifier: str
            The identifier for the actor.
        @type location: Location
            The location of the activity.
        @rtype: None
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self):
        """Return a report of the activities that have occurred.

        @type self: Monitor
        @rtype: dict[str, object]
        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self):
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        @type self: Monitor
        @rtype: float

        # Calling on restricted method to show correct results from example.
        >>> m = Monitor()
        >>> from rider import Rider
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> m.notify(1, RIDER, REQUEST, rd.identifier, rd.origin)
        >>> m.notify(101, RIDER, CANCEL, rd.identifier, rd.origin)
        >>> m._average_wait_time()
        100.0
        >>> m.notify(1, RIDER, REQUEST, rd2.identifier, rd2.origin)
        >>> m.notify(5, RIDER, PICKUP, rd2.identifier, rd2.origin)
        >>> m._average_wait_time()
        52.0
        """
        wait_time = 0
        count = 0

        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1

        return wait_time / count

    def _average_total_distance(self):
        """Return the average distance drivers have driven.

        @type self: Monitor
        @rtype: float

        # Calling on restricted method to show correct results from example.
        >>> m = Monitor()
        >>> from driver import Driver
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> m.notify(1, DRIVER, REQUEST, dr.identifier, dr.location)
        >>> m.notify(3, DRIVER, PICKUP, dr.identifier, Location(3, 3))
        >>> m.notify(5, DRIVER, DROPOFF, dr.identifier, Location(6, 6))
        >>> m._average_total_distance()
        12.0
        >>> m.notify(1, DRIVER, REQUEST, dr2.identifier, dr2.location)
        >>> m.notify(3, DRIVER, PICKUP, dr2.identifier, Location(12, 12))
        >>> m.notify(5, DRIVER, DROPOFF, dr2.identifier, Location(14, 14))
        >>> m._average_total_distance()
        10.0
        """
        total_distance = 0
        count = 0

        for activities in self._activities[DRIVER].values():
            # More than two activities implies the driver must have moved.
            if len(activities) >= 2:
                i = 0
                # Sum the difference in location between all adjacent events.
                # Ignore the last activity because it is always a RiderRequest
                # so there is no movement.
                while i < len(activities) - 1:
                    total_distance += (manhattan_distance(
                        activities[i].location, activities[i + 1].location))
                    i += 1

            # Add a driver to the total count of drivers.
            count += 1

        return total_distance / count

    def _average_ride_distance(self):
        """Return the average distance drivers have driven on rides.

        @type self: Monitor
        @rtype: float

        # Calling on restricted method to show correct results from example.
        >>> m = Monitor()
        >>> from driver import Driver
        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> m.notify(1, DRIVER, REQUEST, dr.identifier, dr.location)
        >>> m.notify(3, DRIVER, PICKUP, dr.identifier, Location(3, 3))
        >>> m.notify(5, DRIVER, DROPOFF, dr.identifier, Location(6, 6))
        >>> m._average_ride_distance()
        6.0
        >>> m.notify(1, DRIVER, REQUEST, dr2.identifier, dr2.location)
        >>> m.notify(3, DRIVER, PICKUP, dr2.identifier, Location(12, 12))
        >>> m.notify(5, DRIVER, DROPOFF, dr2.identifier, Location(14, 14))
        >>> m._average_ride_distance()
        5.0
        """
        ride_distance = 0
        count = 0

        for activities in self._activities[DRIVER].values():
            # More than two activities implies the Driver must have moved.
            if len(activities) >= 2:
                i = 0
                while i < len(activities):
                    # Ride movement only happens before a Dropoff event.
                    # Dropoff will never be the first event so it is alright
                    # to index to i-1.
                    if activities[i].description == DROPOFF:
                        ride_distance += (manhattan_distance(
                            activities[i - 1].location, activities[i].location))
                    i += 1

            # Add a driver to the total count of drivers.
            count += 1

        return ride_distance / count
