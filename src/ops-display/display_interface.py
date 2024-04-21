# ops-display/display_interface.py
from abc import ABC, abstractmethod

class DisplayInterface(ABC):
    """
    Abstract base class that defines a common interface for all display adapters.
    This interface includes methods for initializing, updating, and shutting down the display.
    """

    @abstractmethod
    def initialize(self):
        """
        Initialize the display or server settings. This method should prepare any necessary
        configurations and resources for the display or service to start functioning.
        """
        pass

    @abstractmethod
    def update(self, data):
        """
        Update the display with new data. This method is intended for dynamic displays
        where content might change frequently. For server-based displays like React, this
        could be a placeholder unless there's a need to push updates from the server to the client.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Clean up resources and properly close or shutdown the display or service. This method
        ensures that there are no resource leaks and everything is cleanly stopped.
        """
        pass
