import pyautogui

current_x, current_y = pyautogui.position()
print(f"Current position: ({current_x}, {current_y})")

pyautogui.moveTo(200, 200, duration=1)
