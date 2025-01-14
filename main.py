import yt_dlp
from tqdm import tqdm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess
import threading
import sys


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ProgressUpdater:
    def __init__(self):
        self.pbar = None

    def hook(self, d):
        if d["status"] == "downloading":
            if self.pbar is None:
                file_size = d.get("total_bytes", 0)
                if file_size > 0:  # Ensure file size is valid
                    self.pbar = tqdm(
                        total=file_size, unit="B", unit_scale=True, desc=d["filename"]
                    )
            if self.pbar is not None:  # Ensure pbar is initialized before using
                downloaded = d.get("downloaded_bytes", 0)
                self.pbar.n = downloaded
                self.pbar.refresh()
        elif d["status"] == "finished":
            if self.pbar:
                self.pbar.close()
                self.pbar = None

def download_youtube(video_url, format_type):
    try:
        progress_updater = ProgressUpdater()

        if format_type == "MP3":
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": "music/%(title)s.%(ext)s",
                "progress_hooks": [progress_updater.hook],
            }
        else:  # MP4
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": "videos/%(title)s.%(ext)s",
                "progress_hooks": [progress_updater.hook],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        if format_type == "MP3":
            file_path = os.path.join(
                "music", f"{os.path.splitext(os.path.basename(filename))[0]}.mp3"
            )
        else:
            file_path = os.path.join(
                "videos", f"{os.path.splitext(os.path.basename(filename))[0]}.mp4"
            )

        def open_file():
            if os.name == "nt":  # For Windows
                os.startfile(file_path)
            elif os.name == "posix":  # For macOS and Linux
                subprocess.call(("open", file_path))

        status_label.config(text="Download completed!")
        root.update()
        messagebox.showinfo(
            "Success",
            f"Video downloaded and converted to {format_type} successfully! Click OK to open the file.",
            icon=messagebox.INFO,
        )
        open_file()

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")


def on_download():
    video_url = url_entry.get()
    format_type = format_var.get()

    # Run the download in a separate thread to prevent UI freezing
    download_thread = threading.Thread(target=download_youtube, args=(video_url, format_type))
    download_thread.start()
    status_label.config(text="Download started...")


# Create the main window
root = tk.Tk()
root.title("MP3 Harvest")
root.geometry("400x580")

# Set the icon using resource_path
root.iconbitmap(resource_path("assets/icon.ico"))

root.configure(bg="#2E2E2E")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", foreground="white", background="#2E2E2E")
style.configure("TEntry", fieldbackground="#3E3E3E", foreground="white")
style.configure("TButton", background="#3E3E3E", foreground="white")
style.configure("TCombobox", fieldbackground="#3E3E3E", foreground="white")

# Create and pack widgets
img = tk.PhotoImage(file=resource_path("assets/does.png"))
img = img.subsample(2, 2)  # Resize the image to half its original size
label = tk.Label(root, image=img, background="#2E2E2E", justify="center")
label.pack()

url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=10)
url_entry = ttk.Entry(root, width=50)
url_entry.pack()

format_label = ttk.Label(root, text="Select format:")
format_label.pack(pady=10)
format_var = tk.StringVar(root)
format_var.set("MP3")  # default value
format_dropdown = ttk.Combobox(root, textvariable=format_var, values=["MP3", "MP4"], state="readonly")
format_dropdown.pack()

download_button = ttk.Button(root, text="Download", command=on_download)
download_button.pack(pady=20)

status_label = ttk.Label(root, text="")
status_label.pack()

img2 = tk.PhotoImage(file=resource_path("assets/ta.png"))
img2 = img2.subsample(2, 2)  # Resize the image to half its original size


def open_link(event):
    import webbrowser

    webbrowser.open("https://www.youtube.com/@TechAchievers-IV/featured")


label2 = tk.Label(
    root,
    image=img2,
    background="#2E2E2E",
    justify="center",
    compound="center",
    cursor="hand2",
)
label2.pack(pady=10)
label2.bind("<Button-1>", open_link)

if __name__ == "__main__":
    root.mainloop()
