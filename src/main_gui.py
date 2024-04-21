# main_gui.py
# Import necessary modules from the project and the standard library.
from tkinter import Tk, Label, Entry, Button, ttk, messagebox

from media_downloads import download_video, download_audio, download_and_combine
from utils import open_location, install_and_import
from config import VIDEO_CHOICES, timelogger

@timelogger
def download_media():
    """Handle the media download process based on user input for URL and selection."""
    url = url_entry.get()
    folder_name, message, color = open_location(root)
    location_error.config(text=message, fg=color)

    if folder_name and url:
        choice = choice_combobox.get()
        try:
            from pytube import YouTube
            yt = YouTube(url)
            if choice == "1080p":
                message, color = download_video(yt, folder_name)
            elif choice == "Audio":
                message, color = download_audio(yt, folder_name)
            elif choice == "Combine":
                message, color = download_and_combine(yt, folder_name)
            download_status.config(text=message, fg=color)
        except Exception as e:
            download_status.config(text=str(e), fg="red")

@timelogger
def setup_window():
    """Set up the main window for the application."""
    root = Tk()
    root.title("YouTube Video and Sound Downloader")
    root.geometry("350x450")
    root.columnconfigure(0, weight=1)

    # Create and place GUI components within the window.
    Label(root, text="Enter YouTube URL:", font=("Arial", 14)).grid(pady=(20, 0))
    global url_entry, download_status, location_error, choice_combobox
    url_entry = Entry(root, width=40, font=("Arial", 12))
    url_entry.grid(pady=5)

    choice_combobox = ttk.Combobox(root, values=VIDEO_CHOICES, font=("Arial", 12), state='readonly')
    choice_combobox.grid(pady=5)
    choice_combobox.set("Select Quality")

    Button(root, text="Choose Download Directory", command=lambda: open_location(root), font=("Arial", 12)).grid(pady=5)
    location_error = Label(root, text="", font=("Arial", 10), fg="red")
    location_error.grid(pady=(0, 5))

    Button(root, text="Download", command=download_media, font=("Arial", 14), bg="blue", fg="white").grid(pady=15)
    download_status = Label(root, text="Waiting for input...", font=("Arial", 12), fg="green")
    download_status.grid(pady=(5, 20))

    return root

@timelogger
def main():
    """Entry point of the application."""
    root = setup_window()
    root.mainloop()

if __name__ == "__main__":
    # Ensure necessary modules are installed before running the main application.
    try:
        install_and_import('pytube')
        install_and_import('moviepy')
        install_and_import('python-slugify')
    except Exception as e:
        messagebox.showerror("Installation Error", str(e))
        sys.exit("Failed to install necessary packages. Please install them manually.")

    main()
