"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from sudoku_puzzle import SudokuPuzzle
from grid_peg_solitaire_puzzle import GridPegSolitairePuzzle

# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    # examples unfeasible due to length and unpredictability of solved path
    """
    node = PuzzleNode(puzzle)

    seen = set({})

    # solution is the first node that has a solved state for the puzzle
    solution = depth_search_ans(node, seen)

    # traces back by parents to create a path from start to solved
    path = get_path(solution)

    return path


def get_path(pn):
    """
    Return a PuzzleNode with the only child being the next step towards the
    solution.

    @type pn: PuzzleNode
    @rtype: PuzzleNode

    # examples unfeasible due to length and unpredictability of solved path
    """
    if pn.parent is None:
        return pn

    # creates new node with only one child
    else:
        return get_path(PuzzleNode(pn.parent.puzzle, [pn], pn.parent.parent))


def depth_search_ans(pn, seen=set({})):
    """
    Find and return the first node with the final state. Not following paths
    that contain the same state as previously seen.

    @type pn: PuzzleNode
    @type seen: set
    @rtype: PuzzleNode

    >>> grid = [['*', '*', '*', '*', '*'],\
                ['*', '*', '*', '*', '*'],\
                ['*', '*', '*', '*', '*'],\
                ['*', '*', '.', '*', '*'],\
                ['*', '*', '*', '*', '*']]
    >>> gpsp = GridPegSolitairePuzzle(grid, {'*', '.', '#'})
    >>> seen = set({})
    >>> pn2 = PuzzleNode(gpsp)
    >>> print(depth_search_ans(pn2, seen))
     . . . . .
     . . . . .
     . . . . .
     . . . . .
     . . * . .
    <BLANKLINE>
    <BLANKLINE>
    >>> s = SudokuPuzzle(9, ["*", "*", "*", "7", "*", "8", "*", "1", "*",\
                            "*", "*", "7", "*", "9", "*", "*", "*", "6",\
                            "9", "*", "3", "1", "*", "*", "*", "*", "*",\
                            "3", "5", "*", "8", "*", "*", "6", "*", "1",\
                            "*", "*", "*", "*", "*", "*", "*", "*", "*",\
                            "1", "*", "6", "*", "*", "9", "*", "4", "8",\
                            "*", "*", "*", "*", "*", "1", "2", "*", "7",\
                            "8", "*", "*", "*", "7", "*", "4", "*", "*",\
                            "*", "6", "*", "3", "*", "2", "*", "*", "*"],\
                            {"1", "2", "3", "4", "5", "6", "7", "8", "9"})
    >>> pn = PuzzleNode(s)
    >>> print(depth_search_ans(pn, seen))
    645|738|912
    217|594|836
    983|126|574
    -----------
    352|847|691
    498|613|725
    176|259|348
    -----------
    539|461|287
    821|975|463
    764|382|159
    <BLANKLINE>
    <BLANKLINE>
    """
    if pn.puzzle.is_solved():
        return pn

    elif pn.puzzle.extensions() is None:
        return None

    elif pn.puzzle.fail_fast():
        return None

    elif str(pn.puzzle) in seen:
        return None

    seen.add(str(pn.puzzle))

    extensions = pn.puzzle.extensions()

    # create a node for each next move that hasn't been seen before
    for extension in extensions:
        if str(extension) not in seen:
            node = PuzzleNode(extension, parent=pn)
            pn.children.append(node)

    # recursive call
    else:
        for child in pn.children:
            state = depth_search_ans(child, seen)

            # if it's not None it must be the solution
            if state is not None:
                return state


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    nodes = Queue()
    pn = PuzzleNode(puzzle)
    seen = set({})
    seen.add(str(pn))

    if pn.puzzle.is_solved():
        return pn

    else:
        nodes.add(pn)
        # there are still potential moves left
        while not nodes.is_empty():

            removed = nodes.remove()
            """@type removed: PuzzleNode"""
            pot_ans = removed.puzzle.extensions()

            for state in pot_ans:
                next_node = PuzzleNode(state, parent=removed)

                # found the correct solution, return the path to it
                if state.is_solved():
                    return get_path(next_node)

                # keep looking
                if str(next_node) not in seen:
                    seen.add(str(next_node))
                    nodes.add(next_node)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))


# added Queue class from labs, because we are more familiar with it, as
# opposed to hoping that the deque from collections works how we hope it
# works.
class Queue:
    """
    A first-in, first-out (FIFO) queue.
    """

    def __init__(self):
        """
        Create and initialize new Queue self.

        @param Queue self: this queue
        @rtype: None
        """
        self._contents = []

    def add(self, obj):
        """
        Add object at the back of Queue self.

        @param Queue self: this queue
        @param object obj: object to add
        @rtype: None
        """
        self._contents.append(obj)

    def remove(self):
        """
        Remove and return front object from Queue self.

        Queue self must not be empty.

        @param Queue self: this Queue
        @rtype: object

        >>> q = Queue()
        >>> q.add(3)
        >>> q.add(5)
        >>> q.remove()
        3
        >>> q.remove()
        5
        """
        return self._contents.pop(0)

    def is_empty(self):
        """
        Return whether Queue self is empty

        @param Queue self:
        @rtype: bool

        >>> q = Queue()
        >>> q.add(5)
        >>> q.is_empty()
        False
        >>> q.remove()
        5
        >>> q.is_empty()
        True
        """
        return len(self._contents) == 0
