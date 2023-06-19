import time

import cv2
import pyautogui

from resources import FolderPath, Item
from utils import process_running


def click(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(2)
    pyautogui.click()
    time.sleep(1)


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


def find_item(item, wait=3):
    item_path = FolderPath.ITEM + item
    item_img = cv2.imread(item_path)
    item_loc = None
    for i in range(3):
        time.sleep(wait)
        item_loc = pyautogui.locateOnScreen(item_img)
        if item_loc: break
    if item_loc is None:
        print(item + "button not found")
        return False
    loc_x, loc_y = pyautogui.center(item_loc)
    return {"x": loc_x / 2, "y": loc_y / 2}


def click_item(item: str, wait=3):
    item_loc = find_item(item, wait)
    click(item_loc["x"], item_loc["y"])
    return True


def first_reset_farm():
    click_item(Item.SPOT)
    click_item(Item.SPOT5)
    return True


def check_screen(screen: str):
    if screen == "start":
        if find_item(Item.START): return True
    if screen == "choose_server":
        if find_item(Item.VIP): return True
    if screen == "choose_character":
        if find_item(Item.C_MAGIC): return True
    return False


def move_character(x=1, y=1):
    if x > 0:
        for i in range(x):
            click(814, 468)
    if x < 0:
        for i in range(abs(x)):
            click(646, 362)
    if y > 0:
        for i in range(x):
            click(803, 348)
    if y < 0:
        for i in range(abs(x)):
            click(642, 643)
