from driver import Driver
from rider import Rider
from container import Queue
from location import Location


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.

    === Attributes ===
    @type avail_dr: Queue of Driver
        A Queue of all drivers without a task.
    @type wait_rd: Queue of Rider
        A Queue of all riders who need to be driven.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        # Used Queue to maintain order by First in First Out, both with Drivers
        # and Riders. Riders get Drivers assigned to them by which is first in
        # the list. Drivers by the first in the list that is also the fastest.

        self.avail_dr, self.wait_rd = Queue(), Queue()

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str

        >>> r = Dispatcher()
        >>> r.avail_dr.add(Driver('Bunny', Location(10, 10), 2))
        >>> r.wait_rd.add(Rider("Lola", Location(0, 0), Location(5, 4), 100))
        >>> print(r)
        Available Drivers:
        Bunny at (10, 10) Speed: 2 Is available: True
        Waiting Riders:
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        """
        dr_str = ''
        for driver in self.avail_dr:
            dr_str += str(driver) + '\n'

        return ('Available Drivers:\n' + dr_str +
                'Waiting Riders:\n' + str(self.wait_rd))

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None

        >>> dr = Driver('Charles', Location(0, 0), 3)
        >>> dr2 = Driver('Bunny', Location(10, 10), 2)
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> dis = Dispatcher()
        >>> dis2 = Dispatcher()
        >>> dis3 = Dispatcher()

        >>> dis.avail_dr = Queue()
        >>> dis.request_driver(rd)
        >>> print(dis)
        Available Drivers:
        Waiting Riders:
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting

        >>> dis2.avail_dr.add(dr)
        >>> print(dis2)
        Available Drivers:
        Charles at (0, 0) Speed: 3 Is available: True
        Waiting Riders:
        <BLANKLINE>
        >>> print(dis2.request_driver(rd))
        Charles at (0, 0) Speed: 3 Is available: True
        >>> print(dis2)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>

        >>> dis3.avail_dr.add(dr)
        >>> dis3.avail_dr.add(dr2)
        >>> print(dis3.request_driver(rd))
        Charles at (0, 0) Speed: 3 Is available: True
        >>> print(dis3)
        Available Drivers:
        Bunny at (10, 10) Speed: 2 Is available: True
        Waiting Riders:
        <BLANKLINE>
        """
        # Case 1: No available driver.
        if self.avail_dr.is_empty():
            self.wait_rd.add(rider)
            return None

        # Case 2: Only 1 available driver.
        elif self.avail_dr.length() == 1:
            return self.avail_dr.remove()

        # Case 3: Compare all available drivers to the fastest one.
        else:
            # Set fastest_dr to be the first driver in the list.
            fastest_dr = self.avail_dr.first()
            shortest_time = fastest_dr.get_travel_time(rider.origin)

            # Replace fast_dr with the other one, if the other one can be
            # faster.
            for driver in self.avail_dr:
                if driver.get_travel_time(rider.origin) < shortest_time:
                    fastest_dr = driver
                    shortest_time = driver.get_travel_time(rider.origin)

            self.avail_dr.spcl_remove(fastest_dr)
            return fastest_dr

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None

        >>> dis = Dispatcher()
        >>> dis2 = Dispatcher()
        >>> dis3 = Dispatcher()
        >>> rd = Rider("Lola", Location(0, 0), Location(5, 4), 100)
        >>> rd2 = Rider("Godzilla", Location(10, 10), Location(7, 1), 10)
        >>> dr = Driver('Charles', Location(0, 0), 3)

        >>> dis.request_rider(dr)
        >>> print(dis)
        Available Drivers:
        Charles at (0, 0) Speed: 3 Is available: True
        Waiting Riders:
        <BLANKLINE>

        >>> dis2.wait_rd.add(rd)
        >>> print(dis2.request_rider(dr))
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        >>> print(dis2)
        Available Drivers:
        Waiting Riders:
        <BLANKLINE>

        >>> dis3.wait_rd.add(rd)
        >>> dis3.wait_rd.add(rd2)
        >>> print(dis3.request_rider(dr))
        Lola at (0, 0) Patience: 100 Destination: (5, 4) Status: waiting
        >>> print(dis3)
        Available Drivers:
        Waiting Riders:
        Godzilla at (10, 10) Patience: 10 Destination: (7, 1) Status: waiting
        """
        # Case 1: No waiting rider.
        if self.wait_rd.is_empty():
            self.avail_dr.add(driver)
            return None

        # Case 2: Return the longest-waiting rider.
        else:
            return self.wait_rd.remove()

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        Precondition: rider is in Queue self.wait_rd.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        self.wait_rd.spcl_remove(rider)
