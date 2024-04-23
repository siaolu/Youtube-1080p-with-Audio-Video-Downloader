# display_factory.py
# Version 0.54
# Factory module for creating display adapters based on configuration or runtime parameters.

from display_interface import DisplayInterface
from curses_adapter import CursesAdapter
from pysimplegui_adapter import PySimpleGUIAdapter
from react_adapter import ReactAdapter

def get_display_adapter(adapter_type):
    """
    Factory method to get the appropriate display adapter based on the specified type.
    
    Args:
        adapter_type (str): The type of adapter to create, which could be 'curses', 'pysimplegui', or 'react'.
    
    Returns:
        DisplayInterface: An instance of a class that implements DisplayInterface.
    
    Raises:
        ValueError: If the adapter type is not recognized.
    """
    if adapter_type == 'curses':
        return CursesAdapter()
    elif adapter_type == 'pysimplegui':
        return PySimpleGUIAdapter()
    elif adapter_type == 'react':
        return ReactAdapter()
    else:
        raise ValueError(f"Unknown adapter type: {adapter_type}")
