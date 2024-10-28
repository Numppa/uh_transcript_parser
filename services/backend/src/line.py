class Line:
    """
    A class for representing a line in a document.
    """

    def __init__(self, value: str):
        self.value = value
        self.next_line = None
        self.prev_line = None
