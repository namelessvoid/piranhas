

class CircularList(list):
    """A list which provides a function to iterate through it. If the end is
        reaced, it continues from the beginning. You get a endless repeating
        list so to speak."""

    def __init__(self):
        """Initializes the list."""
        list.__init__(self)
        self._current = 0

    def next(self):
        """Returns the next item in the list.
            Return:
                next object in the list or None if list is empty"""
        if len(self) == 0:
            return None
        else:
            self._current += 1
            self._current %= len(self)
            return self.current()

    def current(self):
        """Returns the current item in the list.
            Return:
                current object in the list or None if list is empty"""
        if len(self) == 0:
            return None
        return self[self._current]
