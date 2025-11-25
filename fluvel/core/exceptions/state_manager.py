
class FluvelBindingError(ValueError):
    """Exception thrown when the Data Binding syntax is invalid."""
    pass

class FluvelStateError(RuntimeError):
    """Exception thrown due to errors related to the StateManager."""
    pass