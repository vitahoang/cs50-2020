import sys
import time

import cv2
import pyautogui

from utils import process_running

ITEM_FOLDER = "/Users/vitahoang/Code/cs50-2020/final/item/"
START_ITEM = "start.png"
VIP = "vip.png"
VIP5 = "vip5.png"
C_MAGIC = "character-magic.png"
C_ENTER = "character-enter.png"


def open_app():
    # Open MUAway app
    pyautogui.click()
    pyautogui.hotkey("command", "space")
    pyautogui.write(["m", "u", "a", "w", "a", "y"])
    pyautogui.press('enter')
    if process_running("MuAwaY"):
        return True
    else:
        print("Cannot Open App!")
        return False


def click_item(item: str, wait=3):
    img_path = ITEM_FOLDER + item
    item_img = cv2.imread(img_path)
    item_btn = None
    for i in range(3):
        time.sleep(wait)
        item_btn = pyautogui.locateOnScreen(item_img)
        if item_btn:
            print(item_btn)
            break
    if item_btn is None:
        print(item + " button not found")
        return False
    start_btn_x, start_btn_y = pyautogui.center(item_btn)
    pyautogui.moveTo(start_btn_x / 2, start_btn_y / 2)
    pyautogui.click()
    return True


def choose_map(map: str):
    pass


if open_app() is False:
    sys.exit("Open App Failed")
if click_item(START_ITEM) is False:
    sys.exit("Start Failed")
if click_item(VIP) is False:
    sys.exit("Join Sever Failed")
if click_item(VIP5, 1) is False:
    sys.exit("Join Sever Failed")
if click_item(C_MAGIC) is False:
    sys.exit("Select Character Failed")
if click_item(C_ENTER, 1) is False:
    sys.exit("Select Character Failed")
