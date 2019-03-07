from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type self: WordLadderPuzzle
        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> ws = {"cost", "cast", "case", "cave", "save"}
        >>> ws2 = {"Haha"}
        >>> wl1 = WordLadderPuzzle("cost", "save", ws)
        >>> wl2 = WordLadderPuzzle("cost", "save", ws)
        >>> wl3 = WordLadderPuzzle("cave", "save", ws2)
        >>> wl1 == wl2
        True
        >>> wl1 == wl3
        False
        """

        return (type(self) == type(other) and
                (self._from_word == other._from_word) and
                (self._to_word == other._to_word) and
                (self._word_set == other._word_set))

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle
        self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> ws = {"cost", "cast", "case", "cave", "save"}
        >>> ws2 = {"Haha"}
        >>> wl1 = WordLadderPuzzle("cost", "save", ws)
        >>> wl2 = WordLadderPuzzle("Haha", "Haha", ws2)
        >>> print(wl1)
        cost -> save
        >>> print(wl2)
        Haha -> Haha
        """

        return "{} -> {}".format(self._from_word, self._to_word)

    # override extensions
    # legal extensions are WordPadderPuzzles that have a from_word that
    # can be reached from this one by changing a single letter to one of
    # those in self._chars
    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> ws = {"cost", "cast", "case", "cave", "save"}
        >>> ws2 = {"Haha"}
        >>> wl1 = WordLadderPuzzle("cost", "save", ws)
        >>> wl2 = WordLadderPuzzle("Haha", "Haha", ws2)
        >>> print(wl2.extensions())
        []
        >>> for x in wl1.extensions(): print(x)
        cast -> save

        """
        # check if solved, so no extensions needed
        if self.is_solved():
            return []

        # list all possible one letter changes for self._from_word
        else:
            lst = []
            length = len(self._from_word)

            for word in self._word_set:
                if len(word) == length and valid_swap(self._from_word, word):
                    lst.append(WordLadderPuzzle(word, self._to_word,
                                                self._word_set))

        return lst

    def is_solved(self):
        """
        Return whether self WordLadderPuzzle is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> ws = {"cost", "cast", "case", "cave", "save"}
        >>> ws2 = {"Haha"}
        >>> wl1 = WordLadderPuzzle("fame", "save", ws)
        >>> wl2 = WordLadderPuzzle("Haha", "Haha", ws2)
        >>> wl1.is_solved()
        False
        >>> wl2.is_solved()
        True
        """
        return self._to_word == self._from_word


def valid_swap(word_1, word_2):
    """
    Return True if word_1 and word_2 have only one character different.

    Precondition: len(word_1) == len(word_2)

    @type word_1: str
    @type word_2: str
    @rtype: bool

    >>> valid_swap("Hello", "Apple")
    False
    >>> valid_swap("Save", "Cave")
    True
    """
    assert len(word_1) == len(word_2), \
        "The length of both words is different."

    i = 0
    count = 0

    while i < len(word_1) and count < 2:
        if word_1[i] != word_2[i]:
            count += 1
        i += 1

    return count == 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
