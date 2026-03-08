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



## doesn't work on Ubuntu OS
# def clip_copy(text:str) -> None:
# # 1. Initialize the Tkinter root
#     root = Tk()
#     
#     # 2. Keep the window from appearing on the screen
#     root.withdraw()
#     
#     # 3. Clear the clipboard and append new text
#     root.clipboard_clear()
#     root.clipboard_append(text)
#     
#     # 4. CRITICAL: Update the IDLE tasks
#     # This tells Tkinter to process all pending clipboard events 
#     # before the script continues.
#     root.update() 
#     
#     # 5. Optional: If you still experience hanging, 
#     # uncomment the line below to give the OS a split second.
#     # root.after(100, root.destroy) 
#     
#     root.destroy()    

def clip_copy(text:str) -> None:
    try:
        # Use xclip to "spawn" a selection owner
        process = subprocess.Popen(
            ['xclip', '-selection', 'clipboard'], 
            stdin=subprocess.PIPE, 
            close_fds=True
        )
        process.communicate(input=text.encode('utf-8'))
        # print("Successfully copied to clipboard.")
    except FileNotFoundError:
        print("Error: xclip is not installed. Run 'sudo apt install xclip'")    
