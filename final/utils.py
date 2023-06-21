import sys
from datetime import datetime

import cv2
import mss
import numpy as np
import psutil
import pyautogui

from resources import FolderPath


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


def screenshot(monitor_number=1):
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


def save_img(image, name="img", suffix="", folder_path=FolderPath.IMAGE):
    cur_time = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    image_path = folder_path + name + suffix + cur_time + ".png"
    try:
        cv2.imwrite(image_path, image)
        return True
    except Exception as e:
        raise e.with_traceback(sys.exc_info()[2])


def show_img(img, window="", delay=0):
    cv2.imshow(winname=window, mat=img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()



