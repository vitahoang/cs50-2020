"""Provide Methods to control"""
import re
import time
from subprocess import Popen, PIPE

import pyautogui
from rembg import remove

from models.character import Character
from models.image import upscale
from models.menu import MenuChat, MenuSetting
from models.resources import FolderPath, Item, ItemLoc, Screen, Map, Point
from symetry import superm2, draw
from utils import process_running, screenshot, save_img, _raise, click, \
    click_item, find_item, show_img


def open_app():
    """open MUAway app"""
    pyautogui.click()
    pyautogui.hotkey("command", "space")
    pyautogui.write(["m", "u", "a", "w", "a", "y"])
    pyautogui.press('enter')
    if process_running("MuAwaY"):
        return True
    print("Cannot Open App!")
    return False


def find_item(item, wait=3):
    """find item given its image then return its location on screen"""
    item_path = FolderPath.ITEM + item
    print(f"Finding: {item_path}")
    item_img = cv2.imread(item_path)
    item_loc = None
    for _ in range(3):
        time.sleep(wait)
        item_loc = pyautogui.locateOnScreen(item_img)
        if item_loc:
            break
    if item_loc is None:
        raise_err("button not found")
        return False
    loc_x, loc_y = pyautogui.center(item_loc)
    return {"x": loc_x / 2, "y": loc_y / 2}


def click_item(item="", loc=None, wait=4):
    """click to an item given its image"""
    if item:
        item_loc = find_item(item, wait)
        if item_loc:
            click(item_loc["x"], item_loc["y"])
            return True
    if loc:
        click(loc["x"], loc["y"])
        return True
    return False


def first_reset_farm():
    click_item(Item.SPOT)
    click_item(Item.SPOT5)
    return True


def check_screen(screen: str):
    """check which screen is showed"""
    if screen == "start" and find_item(Item.START):
        return True
    if screen == "choose_server" and find_item(Item.VIP):
        return True
    if screen == "choose_character" and find_item(Item.C_MAGIC):
        return True
    return False


def move_character(x=1, y=1):
    """move the character by x,y point"""
    if x > 0:
        for _ in range(x):
            click(814, 468)
    if x < 0:
        for _ in range(abs(x)):
            click(646, 362)
    if y > 0:
        for _ in range(x):
            click(803, 348)
    if y < 0:
        for _ in range(abs(x)):
            click(642, 643)
