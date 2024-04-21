import subprocess
import sys
from tkinter import filedialog, messagebox
from config import timelogger

@timelogger
def install_and_import(package):
    """
    Attempts to import a package. If the package is not installed, tries to install it.
    If the package cannot be installed or imported, the application will raise an exception
    and exit with an error message.

    Args:
        package (str): The name of the package to be checked and potentially installed.

    Raises:
        ImportError: If the package cannot be installed or imported.
    """
    try:
        __import__(package)
        print(f"{package} is successfully imported.")
    except ImportError:
        try:
            print(f"Attempting to install {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            __import__(package)
            print(f"{package} has been successfully installed.")
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to install the package {package}. Please install it manually."
            print(error_message)
            messagebox.showerror("Installation Error", error_message)
            sys.exit(f"Exiting due to failure in installing necessary package: {package}")

@timelogger
def open_location(root):
    """
    Opens a dialog for the user to select a directory. Returns the directory path along with a status message and color.
    
    Args:
        root (Tk): The root window of the application for anchoring the file dialog.
    
    Returns:
        tuple: Directory path, message, and message color indicating success or failure.
    """
    folder_name = filedialog.askdirectory(parent=root)
    if folder_name:
        return folder_name, "Directory selected: " + folder_name, "green"
    else:
        return None, "Please choose a directory!", "red"
