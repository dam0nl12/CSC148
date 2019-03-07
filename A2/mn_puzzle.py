from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a '*'
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> target_grid = (('1', '2', '3'), ('4', '5', '*'))
        >>> start_grid = (('*', '2', '3'), ('1', '4', '5'))
        >>> target_grid2 = (('4', '5', '*'), ('1', '2', '3'))
        >>> start_grid2 = (('1', '2', '3'), ('4', '5', '*'))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>> mnp2 = MNPuzzle(start_grid2, target_grid2)
        >>> mnp == mnp2
        False
        >>> mnp3 = MNPuzzle(start_grid, target_grid)
        >>> mnp == mnp3
        True
        """
        return (type(self) == type(other) and
                (self.from_grid == other.from_grid) and
                (self.to_grid == other.to_grid))

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (('1', '2', '3'), ('4', '5', '*'))
        >>> start_grid = (('*', '2', '3'), ('1', '4', '5'))
        >>> target_grid2 = (('4', '5', '*'), ('1', '2', '3'))
        >>> start_grid2 = (('1', '2', '3'), ('4', '5', '*'))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>> mnp2 = MNPuzzle(start_grid2, target_grid2)
        >>> print(mnp)
        Current State:
         * 2 3
         1 4 5
        Target State:
         1 2 3
         4 5 *
        <BLANKLINE>
        >>> print(mnp2)
        Current State:
         1 2 3
         4 5 *
        Target State:
         4 5 *
         1 2 3
        <BLANKLINE>
        """
        board = ''
        board_2 = ''

        for row in self.from_grid:
            for space in row:
                board += ' ' + space
            board += '\n'

        for row in self.to_grid:
            for space in row:
                board_2 += ' ' + space
            board_2 += '\n'

        return 'Current State:\n' + board + 'Target State:\n' + board_2

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below '*' with '*'
    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> start_grid = (('1', '2', '3'), ('4', '5', '*'))
        >>> target_grid = (('1', '2', '3'), ('*', '4', '5'))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>> lst = mnp.extensions()
        >>> for x in lst: print(x)
        Current State:
         1 2 *
         4 5 3
        Target State:
         1 2 3
         * 4 5
        <BLANKLINE>
        Current State:
         1 2 3
         4 * 5
        Target State:
         1 2 3
         * 4 5
        <BLANKLINE>
        >>> start_grid = (('*', '1', '2'), ('3', '4', '5'))
        >>> target_grid = (('1', '2', '3'), ('4', '5', '*'))
        >>> mnp2 = MNPuzzle(start_grid, target_grid)
        >>> lst = mnp2.extensions()
        >>> for x in lst: print(x)
        Current State:
         3 1 2
         * 4 5
        Target State:
         1 2 3
         4 5 *
        <BLANKLINE>
        Current State:
         1 * 2
         3 4 5
        Target State:
         1 2 3
         4 5 *
        <BLANKLINE>
        """
        y = 0

        # set y value to row of empty space
        while '*' not in self.from_grid[y]:
            y += 1
        x = self.from_grid[y].index('*')

        lst = []

        # shift piece down, empty space goes up
        if y > 0:
            lst.append(MNPuzzle(swap_up(self.from_grid, y, x),
                                self.to_grid))

        # shift piece up, empty space goes down
        if y < len(self.from_grid) - 1:
            lst.append(MNPuzzle(swap_down(self.from_grid, y, x),
                                self.to_grid))

        # shift piece left, empty space goes right
        if x < len(self.from_grid[0]) - 1:
            lst.append(MNPuzzle(swap_right(self.from_grid, y, x),
                                self.to_grid))

        # shift piece right, empty space goes left
        if x > 0:
            lst.append(MNPuzzle(swap_left(self.from_grid, y, x),
                                self.to_grid))

        return lst

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return True iff MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool

        >>> target_grid = (('1', '2', '3'), ('4', '5', '*'))
        >>> start_grid = (('*', '2', '3'), ('1', '4', '5'))
        >>> mnp = MNPuzzle(target_grid, target_grid)
        >>> mnp2 = MNPuzzle(start_grid, target_grid)
        >>> mnp.is_solved()
        True
        >>> mnp2.is_solved()
        False
        """
        return self.to_grid == self.from_grid


def swap_up(grid, y, x):
    """
    Swap empty space with puzzle symbol above it in the grid. y is the index
    of the tuple containing the empty space in grid, and x is index of empty
    space in it's tuple.

    Precondition:  0 < y < len(grid), 0 <= x < len(grid[0])

    @type grid: tuple[tuple[str]]
    @type y: int
    @type x: int
    @rtype: tuple[tuple[str]]
            A grid for mn puzzle

    >>> start_grid = (('1', '2', '3'), ('4', '5', '*'))
    >>> swap_up(start_grid, 1, 2)
    (('1', '2', '*'), ('4', '5', '3'))
    >>> start_grid = (('1','2','3'), ('4', '5', '6'), \
                        ('7', '8', '*'), ('9', '10', '11'))
    >>> swap_up(start_grid, 2, 2)
    (('1', '2', '3'), ('4', '5', '*'), ('7', '8', '6'), ('9', '10', '11'))
    """
    symbol = grid[y - 1][x]

    # creates new tuples for the rows changed
    new_toprow = grid[y - 1][:x] + tuple('*')
    new_botrow = grid[y][:x] + tuple(symbol)

    # adds the space after the swapped piece for both rows
    if x < len(grid[y]):
        new_toprow += tuple(grid[y - 1][x + 1:])
        new_botrow += tuple(grid[y][x + 1:])

    return grid[:y-1] + (new_toprow, new_botrow) + grid[y+1:]


def swap_down(grid, y, x):
    """
    Swap empty space with puzzle symbol below it in the grid. y is the index
    of the tuple containing the empty space in grid, and x is index of empty
    space in it's tuple.

    Precondition: 0 <= y < len(grid) - 1, 0 <= x < len(grid[0])

    @type grid: tuple[tuple[str]]
    @type y: int
    @type x: int
    @rtype: tuple[tuple[str]]

    >>> start_grid = (('1', '2', '*'), ('4', '5', '3'))
    >>> swap_down(start_grid, 0, 2)
    (('1', '2', '3'), ('4', '5', '*'))
    >>> start_grid = (('1','2','3'), ('4', '5', '*'), \
                        ('7', '8', '6'), ('9', '10', '11'))
    >>> swap_down(start_grid, 1, 2)
    (('1', '2', '3'), ('4', '5', '6'), ('7', '8', '*'), ('9', '10', '11'))
    """
    symbol = grid[y + 1][x]

    new_botrow = grid[y + 1][:x] + ('*',)
    new_toprow = grid[y][:x] + (symbol,)

    if x < len(grid[y]):
        new_toprow += tuple(grid[y][x + 1:])
        new_botrow += tuple(grid[y + 1][x + 1:])

    return grid[:y] + (new_toprow, new_botrow) + grid[y + 2:]


def swap_right(grid, y, x):
    """
    Swap empty space with puzzle symbol to the right of it in the grid. y is
    the index of the tuple containing the empty space in grid, and x is index
    of empty space in it's tuple.

    Precondition: 0 <= x < len(grid[0]) - 1, 0 <= y < len(grid)

    @type grid: tuple[tuple[str]]
    @type y: int
    @type x: int
    @rtype: tuple[tuple[str]]

    >>> start_grid = (('1', '*', '2'), ('3', '4', '5'))
    >>> swap_right(start_grid, 0, 1)
    (('1', '2', '*'), ('3', '4', '5'))
    >>> start_grid = (('1','2','3'), ('4', '*', '5'), \
                        ('6', '7', '8'), ('9', '10', '11'))
    >>> swap_right(start_grid, 1, 1)
    (('1', '2', '3'), ('4', '5', '*'), ('6', '7', '8'), ('9', '10', '11'))
    """
    symbol = grid[y][x + 1]

    # creates a new tuple for the changed row
    new_row = grid[y][:x] + (symbol,) + ('*',)

    # adds the space after the swapped piece for the changed row
    if x < len(grid[y]) - 2:
        new_row += tuple(grid[y][x + 2:])

    return grid[:y] + (new_row,) + grid[y+1:]


def swap_left(grid, y, x):
    """
    Swap empty space with puzzle symbol to the left of it in the grid. y is
    the index of the tuple containing the empty space in grid, and x is index
    of empty space in it's tuple.

    Precondition: 0 < x < len(grid[0]), 0 <= y < len(grid)

    @type grid: tuple[tuple[str]]
    @type y: int
    @type x: int
    @rtype: tuple[tuple[str]]

    >>> start_grid = (('1', '*', '2'), ('3', '4', '5'))
    >>> swap_left(start_grid, 0, 1)
    (('*', '1', '2'), ('3', '4', '5'))
    >>> start_grid = (('1','2','3'), ('4', '5', '*'), \
                        ('6', '7', '8'), ('9', '10', '11'))
    >>> swap_left(start_grid, 1, 2)
    (('1', '2', '3'), ('4', '*', '5'), ('6', '7', '8'), ('9', '10', '11'))
    """
    symbol = grid[y][x - 1]

    new_row = grid[y][:x - 1] + ('*',) + (symbol,)

    if x < len(grid[y]) - 1:
        new_row += grid[y][x + 1:]

    return grid[:y] + (new_row,) + grid[y+1:]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    target_grid = (('1', '2', '3'), ('4', '5', '*'))
    start_grid = (('*', '2', '3'), ('1', '4', '5'))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print('BFS solved: \n\n{} \n\nin {} seconds'.format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print('DFS solved: \n\n{} \n\nin {} seconds'.format(
        solution, end - start))
