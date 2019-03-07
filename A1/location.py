class Location:
    """
    A location in the city.

    === Attributes ===
    @type row: int
        A natural number representing a street that runs left to right; order of
        streets ascends.
    @type column: int
        A natural number representing a street that runs top to bottom; order of
        streets ascends.

    """
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self.row, self.column = row, column

    def __str__(self):
        """Return a string representation.

        @rtype: str

        >>> l = Location(1, 1)
        >>> l2 = Location(3, 2)
        >>> print(l)
        (1, 1)
        >>> print(l2)
        (3, 2)
        """
        return "({0}, {1})".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> l = Location(1, 1)
        >>> l2 = Location(3, 2)
        >>> l3 = Location(1, 1)
        >>> l == l2
        False
        >>> l == l3
        True
        """
        return (type(self) == type(other) and
                self.row == other.row and
                self.column == other.column)


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int

    >>> l = Location(10, 10)
    >>> l2 = Location(13, 24)
    >>> l3 = Location(1, 1)
    >>> manhattan_distance(l,l2)
    17
    >>> manhattan_distance(l3,l2)
    35
    """
    return int((((destination.row - origin.row) ** 2) ** 0.5) +
               (((destination.column - origin.column) ** 2) ** 0.5))


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> print(deserialize_location('1,1'))
    (1, 1)
    >>> print(deserialize_location('2,5674'))
    (2, 5674)
    """
    loc_lst = location_str.split(',')
    return Location(int(loc_lst[0]), int(loc_lst[1]))
