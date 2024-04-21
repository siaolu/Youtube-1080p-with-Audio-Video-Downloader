# ops-display/curses_adapter.py
import curses
from display_interface import DisplayInterface

class CursesAdapter(DisplayInterface):
    """
    An adapter for implementing a curses-based textual user interface.
    """

    def __init__(self):
        self.stdscr = None

    def initialize(self):
        """Initialize the curses environment."""
        self.stdscr = curses.initscr()  # Initialize the window system
        curses.noecho()  # Turn off key echoing
        curses.cbreak()  # React to keys instantly without requiring the Enter key
        self.stdscr.keypad(1)  # Enable special keys to be interpreted as themselves

    def update(self, data):
        """
        Update the display with new data.
        :param data: Data to be displayed on the screen
        """
        self.stdscr.clear()  # Clear the screen so we can update it
        try:
            self.stdscr.addstr(0, 0, data)  # Try to add string at the first position
        except curses.error:
            pass  # Handle the exception if the data is too large to fit on screen
        self.stdscr.refresh()  # Refresh the screen to show the update

    def shutdown(self):
        """Clean up and return terminal to previous settings."""
        if self.stdscr is not None:
            self.stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()  # Terminate the window session
            self.stdscr = None

    def __del__(self):
        """Ensure the shutdown process is handled."""
        self.shutdown()
