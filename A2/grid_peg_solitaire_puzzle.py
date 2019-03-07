from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          '#' for unused, '*' for peg, '.' for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == '*' or x == '.' or x == '#' for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @return: bool

        >>> grid1 = [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '.', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {'*', '.', '#'})
        >>> grid2 = [['*', '*', '*', '*', '*']]
        >>> grid2 += [['*', '*', '*', '*', '*']]
        >>> grid2 += [['*', '*', '*', '*', '*']]
        >>> grid2 += [['*', '*', '.', '*', '*']]
        >>> grid2 += [['*', '*', '*', '*', '*']]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {'*', '.', '#'})
        >>> grid3 = [['#', '#', '*', '#', '#']]
        >>> grid3 += [['#', '*', '*', '*', '#']]
        >>> grid3 += [['#', '.', '*', '*', '#']]
        >>> grid3 += [['#', '*', '*', '*', '#']]
        >>> grid3 += [['#', '#', '*', '#', '#']]
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {'*', '.', '#'})
        >>> gpsp1 == gpsp2
        True
        >>> gpsp3 == gpsp2
        False

        """
        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation of
        GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @return: str

        >>> grid1 = [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '.', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {'*', '.', '#'})
        >>> print(gpsp1)
         * * * * *
         * * * * *
         * * * * *
         * * . * *
         * * * * *
        >>> grid2 = [['#', '#', '.', '#', '#']]
        >>> grid2 += [['#', '.', '.', '*', '#']]
        >>> grid2 += [['#', '.', '*', '*', '#']]
        >>> grid2 += [['#', '.', '*', '*', '#']]
        >>> grid2 += [['#', '#', '*', '#', '#']]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {'*', '.', '#'})
        >>> print(gpsp2)
         - - . - -
         - . . * -
         - . * * -
         - . * * -
         - - * - -

        """
        board = ''
        for row in self._marker:
            for space in row:
                if space == '#':
                    board += ' -'
                else:
                    board += ' ' + space
            board += '\n'
        return board[:-1]

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [['*', '*', '.', '.', '.']]
        >>> gpsp = GridPegSolitairePuzzle(grid, {'*', '.', '#'})
        >>> L1 = list(gpsp.extensions())
        >>> grid[0][0] = '.'
        >>> grid[0][1] = '.'
        >>> grid[0][2] = '*'
        >>> L2 = [GridPegSolitairePuzzle(grid, {'*', '.', '#'})]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        >>> grid = [['*', '*', '.', '.', '.']]
        >>> grid += [['*', '*', '.', '.', '.']]
        >>> grid += [['*', '*', '.', '.', '.']]
        >>> gpsp = GridPegSolitairePuzzle(grid, {'*', '.', '#'})
        >>> for puzzle in gpsp.extensions(): print(str(puzzle) + '\\n')
         . . * . .
         * * . . .
         * * . . .
        <BLANKLINE>
         * * . . .
         . . * . .
         * * . . .
        <BLANKLINE>
         * * . . .
         * * . . .
         . . * . .
        <BLANKLINE>
        """
        # no need to go through moves if the puzzle is solved
        if self.is_solved():
            return []

        y = 0
        lst = []

        while y < len(self._marker):
            x = 0
            while x < len(self._marker[y]):

                if self._marker[y][x] == '.':

                    # jump peg on the right of the empty spot
                    if (x + 2 < len(self._marker[y]) and
                            self._marker[y][x + 2] == '*' and
                            self._marker[y][x + 1] == '*'):
                        lst.append(GridPegSolitairePuzzle(
                            jump_left(self._marker, y, x), self._marker_set))

                    # jump peg on the left of the empty spot
                    if (x - 2 >= 0 and
                            self._marker[y][x - 2] == '*' and
                            self._marker[y][x - 1] == '*'):
                        lst.append(GridPegSolitairePuzzle(
                            jump_right(self._marker, y, x), self._marker_set))

                    # jump peg above the empty spot
                    if (y - 2 >= 0 and
                            self._marker[y - 2][x] == '*' and
                            self._marker[y - 1][x] == '*'):
                        lst.append(GridPegSolitairePuzzle(
                            jump_down(self._marker, y, x), self._marker_set))

                    # jump peg below the empty spot
                    if (y + 2 < len(self._marker) and
                            self._marker[y + 2][x] == '*' and
                            self._marker[y + 1][x] == '*'):
                        lst.append(GridPegSolitairePuzzle(
                            jump_up(self._marker, y, x), self._marker_set))

                x += 1
            y += 1

        return lst

    # override is_solved
    # A configuration is solved when there is exactly one '*' left
    def is_solved(self):
        """
        Return True iff GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> grid1 += [['*', '*', '.', '*', '*']]
        >>> grid1 += [['*', '*', '*', '*', '*']]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {'*', '.', '#'})
        >>> gpsp1.is_solved()
        False
        >>> grid2 = [['.', '.', '.', '.', '.']]
        >>> grid2 += [['.', '.', '*', '.', '.']]
        >>> grid2 += [['.', '.', '.', '.', '.']]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {'*', '.', '#'})
        >>> gpsp2.is_solved()
        True
        """
        count = 0

        for row in self._marker:
            for space in row:
                if space == '*':
                    count += 1
                    if count == 2:
                        return False

        return True


def jump_left(board, y, x):
    """
    Jump peg on the right of the empty spot.

    Precondition: 0 <= x < len(grid[0]) - 2, 0 <= y < len(grid)

    @type board: list[list[str]]
    @type y: int
    @type x: int
    @rtype: list[list[str]]

    >>> grid = [['*', '*', '.', '*', '*']]
    >>> print(jump_left(grid, 0, 2))
    [['*', '*', '*', '.', '.']]
    """
    new_board = []

    # create duplicate board to be changed
    for i in range(len(board)):
        new_board.append(board[i].copy())

    # change relevant positions on new_board
    (new_board[y][x], new_board[y][x + 1],
     new_board[y][x + 2]) = ('*', '.', '.')

    return new_board


def jump_right(board, y, x):
    """
    Jump peg on the left of the empty spot.

    Precondition: 2 <= x < len(grid[0]), 0 <= y < len(grid)

    @type board: list[list[str]]
    @type y: int
    @type x: int
    @rtype: list[list[str]]

    >>> grid = [['*', '*', '.', '*', '*']]
    >>> print(jump_right(grid, 0, 2))
    [['.', '.', '*', '*', '*']]
    """
    new_board = []

    for i in range(len(board)):
        new_board.append(board[i].copy())

    (new_board[y][x], new_board[y][x - 1],
     new_board[y][x - 2]) = ('*', '.', '.')

    return new_board


def jump_up(board, y, x):
    """
    Jump peg below the empty spot, return new grid.

    Precondition: 0 <= y < len(grid) - 2, 0 <= x < len(grid[0])

    @type board: list[list[str]]
    @type y: int
    @type x: int
    @rtype: list[list[str]]

    >>> grid = [['.', '*', '.', '.', '.']]
    >>> grid += [['*', '*', '.', '.', '.']]
    >>> grid += [['*', '*', '.', '.', '.']]
    >>> ans = [['*', '*', '.', '.', '.']]
    >>> ans += [['.', '*', '.', '.', '.']]
    >>> ans += [['.', '*', '.', '.', '.']]
    >>> ans == jump_up(grid, 0, 0)
    True
    """
    new_board = []

    for i in range(len(board)):
        new_board.append(board[i].copy())

    (new_board[y][x], new_board[y + 1][x],
     new_board[y + 2][x]) = ('*', '.', '.')

    return new_board


def jump_down(board, y, x):
    """
    Jump peg above the empty spot, return new grid.

    Precondition: 2 <= y < len(grid), 0 <= x < len(grid[0])

    @type board: list[list[str]]
    @type y: int
    @type x: int
    @rtype: list[list[str]]

    >>> grid = [['*', '*', '.', '.', '.']]
    >>> grid += [['*', '*', '.', '.', '.']]
    >>> grid += [['.', '*', '.', '.', '.']]
    >>> ans = [['.', '*', '.', '.', '.']]
    >>> ans += [['.', '*', '.', '.', '.']]
    >>> ans += [['*', '*', '.', '.', '.']]
    >>> ans == jump_down(grid, 2, 0)
    True
    """
    new_board = []

    for i in range(len(board)):
        new_board.append(board[i].copy())

    (new_board[y][x], new_board[y - 1][x],
     new_board[y - 2][x]) = ('*', '.', '.')

    return new_board


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '.', '*', '*'],
            ['*', '*', '*', '*', '*']]
    gpsp = GridPegSolitairePuzzle(grid, {'*', '.', '#'})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print('Solved 5x5 peg solitaire in {} seconds.'.format(end - start))
    print('Using depth-first: \n{}'.format(solution))
