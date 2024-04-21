# display_factory.py
from ops-display.curses_adapter import CursesAdapter
from ops-display.pysimplegui_adapter import PySimpleGUIAdapter
from ops-display.react_adapter import ReactAdapter  # Assuming React setup is handled differently

def get_display_adapter(display_type):
    """
    Factory method to get the appropriate display adapter based on the display type.
    
    Args:
        display_type (str): The type of display adapter to retrieve.
                            Options are 'curses', 'pysimplegui', 'react'.

    Returns:
        DisplayInterface: An instance of a class implementing DisplayInterface.
    
    Raises:
        ValueError: If an unknown display type is provided.
    """
    if display_type == 'curses':
        return CursesAdapter()
    elif display_type == 'pysimplegui':
        return PySimpleGUIAdapter()
    elif display_type == 'react':
        # React option processed via [app_main.py] flask invoked
        # -See [app_main.py] for more detail 
        # - Generally React adapter not defined here.
        # Uncomment and modify the below line according to your React integration strategy.
        return ReactAdapter()
        raise NotImplementedError("React display adapter is not implemented.")
    else:
        raise ValueError(f"Unknown display type: {display_type}")
