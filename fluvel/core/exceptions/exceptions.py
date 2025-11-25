class ContentNotFoundError(Exception):
    """
    Exception that is thrown when attempting to access content
    of the GlobalContent class with an incorrect or non-existent id.
    """

    def __init__(self, *args):
        super().__init__(*args)

class ContentLoadingError(Exception):
    """
    Exception thrown when attempting to load .json files via ContentHandler
    """
    def __init__(self, *args):
        super().__init__(*args)