class Container:
    """A container that holds objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item):
        """Add <item> to this Container.

        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self):
        """Remove and return a single item from this Container.

        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self):
        """Return True iff this Container is empty.

        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    # @type _items: list
    #     The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self):
        """Initialize an empty PriorityQueue.

        @type self: PriorityQueue
        @rtype: None
        """
        self._items = []

    def remove(self):
        """Remove and return the next item from this PriorityQueue.

        Precondition: <self> should not be empty.

        @type self: PriorityQueue
        @rtype: object

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        assert not self.is_empty(), "Oh dear, empty PriorityQueue!"
        return self._items.pop(0)

    def is_empty(self):
        """Return true iff this PriorityQueue is empty.

        @type self: PriorityQueue
        @rtype: bool

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def add(self, item):
        """Add <item> to this PriorityQueue.

        @type self: PriorityQueue
        @type item: object
        @rtype: None
        """
        i = 0
        while (i < len(self._items)) and (self._items[i] <= item):
            i += 1
        self._items.insert(i, item)

    def __str__(self):
        """Return a string representation.

        @type self: PriorityQueue
        @rtype: str

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> print(pq)
        blue
        yellow
        >>> pq.remove()
        'blue'
        >>> print(pq)
        yellow
        """
        string = ''

        for item in self._items:
            string += (str(item) + '\n')

        return string.strip()

# In normal circumstances we would have redesigned PriorityQueue to be a sub of
# Queue, so that the shared methods between Queue and PriorityQueue would be
# inherited. But, due to PriorityQueue being provided and graded we decided not
# to risk manipulating it's code in case it is tested directly for marks.


class Queue(Container):
    """A queue of items that is first in first out.

    Objects can be of different types.
    """

    # === Private Attributes ===
    # @type _items: list
    #     The items stored in the Queue.
    #
    # === Representation Invariants ===
    # _items is a list that is FIFO.

    def __init__(self):
        """Initialize an empty Queue.

        @type self: Queue
        @rtype: None
        """
        self._items = []

    def add(self, item):
        """Add <item> to this Queue.

        @type item: object
        @rtype: None
        """
        self._items.append(item)

    def __str__(self):
        """Return a string representation.

        @type self: Queue
        @rtype: str

        >>> q = Queue()
        >>> q.add('dr')
        >>> q.add('jd')
        >>> print(q)
        dr
        jd
        >>> q.remove()
        'dr'
        >>> print(q)
        jd
        """
        string = ''

        for item in self._items:
            string += (str(item) + '\n')

        return string.strip()

    def __eq__(self, other):
        """Return if Queue self is equivalent to Queue other, and false
        otherwise.

        @type self: Queue
        @type other: Queue
        @rtype: bool

        >>> r = Queue()
        >>> r2 = Queue()
        >>> r3 = Queue()
        >>> r.add(1)
        >>> r3.add(1)
        >>> r == r2
        False
        >>> r == r3
        True

        """
        return type(self) == type(other) and self._items == other._items

    def first(self):
        """Return first item in Queue.

        Precondition: Queue is not empty.

        @rtype: Object

        >>> q = Queue()
        >>> q.add(1)
        >>> q.add(2)
        >>> q.first()
        1
        >>> q.remove()
        1
        >>> q.first()
        2
        """
        assert not self.is_empty(), 'Empty Queue, oh dear!'

        return self._items[0]

    # breaks traditional usability of Queue, but required for cancelled riders
    # and faster drivers that are later in the Queue.

    def spcl_remove(self, item):
        """Removes <item> from container self.

        @type item: object
        @rtype: None

        >>> q = Queue()
        >>> q.add(1)
        >>> q.add(2)
        >>> q.spcl_remove(2)
        >>> print(q)
        1
        >>> q.spcl_remove(1)
        >>> print(q)
        <BLANKLINE>
        """
        self._items.remove(item)

    def remove(self):
        """Remove and return the first item from this Queue.

        Precondition: <self> should not be empty.

        @type self: Queue
        @rtype: object

        >>> q = Queue()
        >>> q.add("red")
        >>> q.add("blue")
        >>> q.add("yellow")
        >>> q.add("green")
        >>> q.remove()
        'red'
        >>> q.remove()
        'blue'
        >>> q.remove()
        'yellow'
        >>> q.remove()
        'green'
        """
        assert not self.is_empty(), "Oh dear, empty Queue!"
        return self._items.pop(0)

    def is_empty(self):
        """Return true iff this Queue is empty.

        @type self: Queue
        @rtype: bool

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.add("thing")
        >>> q.is_empty()
        False
        """
        return len(self._items) == 0

    def __iter__(self):
        """Return list_iterator to give Queue iterable functionality.

        @type self: Queue
        @rtype: list_iterator

        >>> q = Queue()
        >>> q.add(0)
        >>> type(q.__iter__())
        <class 'list_iterator'>
        """
        return self._items.__iter__()

    def length(self):
        """Return length of Queue self.

        @type self: Queue
        @rtype: int

        >>> q = Queue()
        >>> q.length()
        0
        >>> q.add("red")
        >>> q.length()
        1
        """
        return len(self._items)
