# pysimplegui_adapter.py
# Version 0.54
# Provides a graphical user interface using PySimpleGUI, allowing dynamic interactions and data presentation based on backend processes.

import PySimpleGUI as sg

def launch_gui():
    """
    Launches a GUI window using PySimpleGUI, which interacts with backend data.
    The GUI is designed to be user-friendly and capable of displaying data dynamically fetched from the backend.
    """
    layout = [
        [sg.Text('Data will be displayed here:', key='data_text')],
        [sg.Button('Refresh'), sg.Button('Exit')]
    ]

    window = sg.Window('Data Display GUI', layout)

    while True:
        event, values = window.read()
        if event == 'Refresh':
            # Simulate fetching data from a backend
            data = fetch_data()
            window['data_text'].update(f'Data: {data}')
        elif event in (sg.WIN_CLOSED, 'Exit'):
            break

    window.close()

def fetch_data():
    """
    Fetch data from the backend. This function is a placeholder to simulate backend interaction.
    Returns:
        str: A string containing data fetched from the backend.
    """
    return "Sample data from backend"

if __name__ == '__main__':
    launch_gui()
