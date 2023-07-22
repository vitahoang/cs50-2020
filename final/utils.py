import multiprocessing
import multiprocessing.pool
import sys
import time
import traceback
from datetime import datetime
from functools import wraps

import cv2
import mss
import numpy as np
import psutil
import pyautogui
import pyscreeze
from matplotlib import pyplot as plt
from numpy import ndarray
from pymsgbox import alert

from models.resources import FolderPath, ItemLoc


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
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


def screenshot(monitor_number=1, region: tuple = None) -> ndarray:
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_number]
        # Grab the data
        ss = sct.grab(monitor)
        result = cv2.cvtColor(np.array(ss), cv2.COLOR_BGRA2BGR)
        if region:
            return result[region[0]:region[1], region[2]:region[3]]
    return result


def screen_info(axis=False):
    screen_width, screen_height = pyautogui.size()
    print(screen_width, screen_height)
    mouse_x, mouse_y = pyautogui.position()
    if not axis:
        return {"x": mouse_x, "y": mouse_y}
    return {"x": mouse_x * 2, "y": mouse_y * 2}


def save_img(image, name="img", suffix="", folder_path=FolderPath.IMAGE):
    cur_time = datetime.utcnow().strftime('%Y%m%d-%H%M%S%f')[:-3]
    image_path = folder_path + name + suffix + cur_time + ".png"
    try:
        cv2.imwrite(image_path, image)
        return True
    except Exception as e:
        _raise(e)


def show_img(img, window="", delay=0, axis=False):
    if not axis:
        cv2.imshow(winname=window, mat=img)
        cv2.waitKey(delay)
        cv2.destroyAllWindows()
        return True
    plt.imshow(img, interpolation='nearest')
    plt.show()
    return True


def pop_err(text="", title="Error", button="OK"):
    alert(text=text, title=title, button=button)
    sys.exit()


def _raise(e: Exception = None, act="raise"):
    if act == "print":
        print(traceback.format_exc())
        return False
    if act == "raise" and e:
        raise e


def click(x: int = 0,
          y: int = 0,
          _loc: dict = None,
          _click: int = 1,
          _interval=0.1):
    """click to point(x,y) with sleep"""
    if _loc:
        pyautogui.moveTo(_loc["x"], _loc["y"])
        time.sleep(0.5)
        pyautogui.click(clicks=_click, interval=_interval)
        time.sleep(0.5)
        return True
    if x and y:
        pyautogui.moveTo(x, y)
        time.sleep(0.5)
        pyautogui.click(clicks=_click, interval=_interval)
        time.sleep(0.5)
        return True
    return False


def find_item(item_path: str, region: tuple = None, wait=3):
    """find item given an image then return its central location on screen"""
    item_path = FolderPath.ITEM + item_path
    print(f"Finding: {item_path}")
    item_loc = None
    for _ in range(3):
        time.sleep(wait)
        needleimage = cv2.imread(item_path)
        hayimage = screenshot(region=region)
        item_loc = pyscreeze.locate(needleImage=needleimage,
                                    haystackImage=hayimage, grayscale=False)
        if item_loc:
            break
    if item_loc is None:
        return False
    loc_x, loc_y = pyautogui.center(item_loc)

    return {"x": loc_x / 2, "y": loc_y / 2}


def chat(*args: str):
    try:
        click(_loc=ItemLoc.CHAT)
        time.sleep(0.3)
        chars = []
        for arg in args:
            for c in arg:
                chars.append(c)
        pyautogui.write(chars)
        time.sleep(0.3)
        print(chars)
        pyautogui.press("enter")
        time.sleep(0.5)
    except Exception as e:
        _raise(e)


def cal_rotate_n(new_theta: int, last_theta: int = None):
    """Calculate the number of clicks to the rotate button"""
    change = 0.3
    if not last_theta:
        return 1
    if new_theta - last_theta > 0:
        rotate_n = int((3.14 - new_theta) // change - 1)
        return 1 if rotate_n < 1 else rotate_n
    if new_theta - last_theta < 0:
        rotate_n = int(new_theta // change)
        return 1 if rotate_n < 1 else rotate_n


