import time
import traceback
from datetime import datetime

import cv2
import mss
import numpy as np
import psutil
import pyautogui
import pyscreeze
from numpy import ndarray
from pymsgbox import alert

from models.resources import FolderPath


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
        _raise(e)


def show_img(img, window="", delay=0):
    cv2.imshow(winname=window, mat=img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def pop_err(text="", title="Error", button="OK"):
    alert(text=text, title=title, button=button)


def _raise(e: Exception = None, act="raise"):
    if act == "print":
        print(traceback.format_exc())
        return False
    if act == "raise" and e:
        raise e


def click(x: int = 0,
          y: int = 0,
          item_loc: dict = None,
          _click: int = 1,
          _interval=0.0):
    """click to point(x,y) with sleep"""
    if item_loc:
        pyautogui.moveTo(item_loc["x"], item_loc["y"])
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


def click_item(item_path: str):
    try:
        loc = find_item(item_path=item_path)
        click(item_loc=loc)
    except Exception as e:
        _raise(e)


def find_item(item_path: str, region: tuple = None, wait=3):
    """find item given an image then return its central location on screen"""
    item_path = FolderPath.ITEM + item_path
    print(f"Finding: {item_path}")
    item_loc = None
    for _ in range(3):
        time.sleep(wait)
        hayimage = screenshot(region=region)
        needleimage = cv2.imread(item_path)
        item_loc = pyscreeze.locate(needleImage=needleimage,
                                    haystackImage=hayimage, grayscale=False)
        if item_loc:
            break
    if item_loc is None:
        return False
    loc_x, loc_y = pyautogui.center(item_loc)

    return {"x": loc_x / 2, "y": loc_y / 2}
