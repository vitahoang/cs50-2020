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
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE,
              universal_newlines=True)
    open_scpt = '''
        tell application "MuAwaY"
            run
            delay 2
            activate
        end tell'''
    stdout, stderr = p.communicate(open_scpt)
    print(p.returncode, stdout, stderr)
    time.sleep(1)

    if process_running("MuAwaY"):
        p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  universal_newlines=True)
        fullscreen_scpt = '''
            tell application "System Events" to tell process "MuAwaY"
                -- Exit full screen and move app to the 1 window
                tell menu bar item "View" of menu bar 1
                    click
                    try
                        tell menu item "Exit Full Screen" of menu 1
                            click
                        end tell
                    end try
                end tell
                delay 2
                
                
                set position of window 1 to {0, 50}
                -- Enter fullscreen
                tell menu bar item "View" of menu bar 1
                    click
                    try
                        tell menu item "Enter Full Screen" of menu 1
                            click
                        end tell
                    end try
                end tell
            end tell'''
        stdout, stderr = p.communicate(fullscreen_scpt)
        print(p.returncode, stdout, stderr)
        return True
    print("Cannot Open App!")
    return False


def first_reset_farm():
    click_item(Item.SPOT)
    click_item(Item.SPOT5)
    return True


def check_screen():
    """check which screen is showed"""
    if find_item(Item.START):
        return Screen.START
    if find_item(Item.VIP):
        return Screen.SERVER
    if find_item(Item.C_MAGIC):
        return Screen.CHARACTER
    if find_item(Item.COLLAPSE):
        return Screen.IN_GAME
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


def join_server(server="VIP5"):
    if check_screen() != Screen.SERVER:
        print("Screen is not at SERVER")
        return False
    try:
        _type = " ".join(re.findall("[a-zA-Z]+", server)).upper()
        _number = server[-1]
        server_name = "ItemLoc." + _type
        sub_server_name = server_name + _number
        click(item_loc=eval(server_name))
        click(item_loc=eval(sub_server_name))
        time.sleep(5)
        select_character()
        time.sleep(5)
    except Exception as e:
        _raise(e)
    return True


def select_character(_char=ItemLoc.C_MAGIC):
    if check_screen() != Screen.CHARACTER:
        print("Screen is not at CHARACTER")
        return False
    try:
        click(item_loc=_char)
        click(item_loc=ItemLoc.C_ENTER)
        time.sleep(5)
        if check_screen() == Screen.IN_GAME:
            return True
    except Exception as e:
        _raise(e)


def solve_captcha():
    while Character().cur_loc()["map_name"] != "Lorencia":
        time.sleep(2)
        # ss = cv2.imread(FolderPath.SAMPLE + "boots.png")
        # show_img(ss)
        crop = screenshot(region=(790, 1070, 1320, 1570))
        show_img(crop)
        captcha_scl = upscale(crop)
        captcha_obj = remove(captcha_scl)
        r, theta = superm2(captcha_obj)
        print(r, theta)
        if 0.00 <= theta <= 0.03 or theta == 3.14:
            click_item(item_path=ItemLoc.RS_SEND)
            time.sleep(2)
            if Character().cur_loc()["map_name"] == "Arena":
                sym_image = draw(crop, r, theta)
                save_img(image=sym_image, name="captcha", suffix="-failed",
                         folder_path=FolderPath.SAMPLE)
                continue
            break
        click_item(item_path=ItemLoc.RS_RIGHT)
    return True


def train(character: Character, _map=Map.arena11):
    MenuChat().move(_map)
    map_name = " ".join(re.findall("[a-zA-Z]+", _map))
    time.sleep(2)
    if character.cur_loc()["map_name"].lower() == map_name:
        click(item_loc=ItemLoc.MOVE_LEFT)
        while not character.check_max_lvl():
            pyautogui.mouseDown(x=ItemLoc.ATTACK_EVIL["x"],
                                y=ItemLoc.ATTACK_EVIL["y"])
            time.sleep(5)
        print("Train Complete: Max LvL")
        return True
    return False


def train_after_reset(character: Character):
    join_server("SPOT5")
    menu = MenuChat()
    menu.move(Map.arena11)
    time.sleep(2)
    if character.cur_loc()["map_name"].lower() == "Arena":
        click(item_loc=ItemLoc.MOVE_LEFT)
        while 1 <= character.cur_lvl()["lvl"] <= 50:
            pyautogui.mouseDown(x=ItemLoc.ATTACK_HAND["x"],
                                y=ItemLoc.ATTACK_HAND["y"])
            time.sleep(5)
        menu.add_point(Point.energy, character.free_point)
        while 51 <= character.cur_lvl()["lvl"] <= 100:
            pyautogui.mouseDown(x=ItemLoc.ATTACK_HAND["x"],
                                y=ItemLoc.ATTACK_HAND["y"])
            time.sleep(5)
        menu.add_point(Point.energy, character.free_point)
        setting = MenuSetting()
        setting.open_menu("1", "server")
        return True
    return False
