import mss
import numpy as np
import psutil
import pyautogui


def process_running(process_name):
    """
    By Sanix darker
    Check if there is any running process that contains the given name
    processName.
    """

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (
                psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


def screenshot(monitor_number: int):
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_number]
        # Grab the data
        ss = sct.grab(monitor)
        np_img = np.array(ss)
    return np_img


def screen_info():
    screen_width, screen_height = pyautogui.size()
    print(screen_width, screen_height)
    mouse_x, mouse_y = pyautogui.position()
    print(mouse_x, mouse_y)
