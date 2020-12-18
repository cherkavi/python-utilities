from tkinter import Tk
import subprocess

def copy_to_clipboard(text: str):
    r = Tk()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def open_in_browser(selected_url: str):
    subprocess.call(["x-www-browser", selected_url])
