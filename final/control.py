"""Provide Methods to control"""
import random
import re
from subprocess import Popen, PIPE

from rembg import remove

from models.character import Character
from models.image import upscale
from models.item import *
from models.npc import NPC, npc_reset, npc_master
from models.resources import FolderPath, Screen, Command, Point, ItemLoc
from models.text import extract_text_from
from symetry import superm2, draw
from utils import process_running, screenshot, save_img, _raise, click, \
    chat, pop_err, cal_rotate_n

server_name: str
sub_server_name: str
first_theta = None
last_theta = None


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


def check_screen(screen: Screen = None):
    """check which screen is showed"""
    if (screen == Screen.START or not screen) \
            and click(_loc=ItemLoc.CHAT) \
            and Item(CHAT_SEND).click_item():
        return Screen.IN_GAME
    if (screen == Screen.START or not screen) and \
            Item(START).find_item():
        return Screen.START
    if (screen == Screen.SERVER or not screen) and \
            Item(VIP).find_item():
        return Screen.SERVER
    if (screen == Screen.CHARACTER or not screen) and \
            Item(C_MAGIC).find_item():
        return Screen.CHARACTER
    return False


def log_in():
    if open_app() is False:
        pop_err("Open App Failed")
        return False
    time.sleep(5)
    screen = check_screen()
    match screen:
        case None:
            pop_err("Open App Failed")
            return False
        case Screen.START:
            click(_loc=ItemLoc.START)
            time.sleep(5)
            return Screen.SERVER
        case Screen.SERVER:
            return screen
        case Screen.IN_GAME:
            return screen


def join_server(server="VIP5"):
    if not check_screen(Screen.SERVER):
        return False
    try:
        _type = " ".join(re.findall("[a-zA-Z]+", server)).upper()
        _number = server[-1]
        global server_name, sub_server_name
        server_name = "ItemLoc." + _type
        sub_server_name = server_name + _number
        click(_loc=eval(server_name))
        click(_loc=eval(sub_server_name))
        time.sleep(5)
        select_character()
        time.sleep(5)
        if check_screen(Screen.IN_GAME) == Screen.IN_GAME:
            return True
    except Exception as e:
        _raise(e)
    return False


def select_character(_char=ItemLoc.C_MAGIC):
    try:
        click(_loc=_char)
        click(_loc=ItemLoc.C_ENTER)
        time.sleep(4)
        if check_screen(Screen.IN_GAME) == Screen.IN_GAME:
            return True
    except Exception as e:
        _raise(e)


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


def read_message():
    ss = screenshot()
    chat_window = ss[1500:1645, 800:1495]
    message = extract_text_from(chat_window).replace("\n", "")
    print(message)
    return message


def reset_wait(message):
    if re.search(r'missed the captcha', message):
        wait = re.findall(r'\d{1,2}', message)
        print(wait)
        if len(wait) == 2:
            time.sleep(int(wait[0]) * 60 + int(wait[1]))


def solve_captcha(master=False):
    global first_theta, last_theta
    first_try = True

    # random seed to choose which side to rotate the captcha image
    seed = random.choice([True, False])

    while not re.search("Lorencia", Character().cur_loc()[0]):
        time.sleep(3)

        # crop and upscale the captcha
        crop = screenshot(region=(790, 1070, 1320, 1570))
        captcha_scl = upscale(crop)
        captcha_obj = remove(captcha_scl)
        r, theta = superm2(captcha_obj)
        if not last_theta:
            last_theta = theta
        rotate_n = cal_rotate_n(theta, last_theta)
        print(r, theta)

        # if theta = 0 or 3.14, the captcha is at vertical symetry position
        if 0.00 <= theta <= 0.03 or theta == 3.14 or first_theta == theta:
            click(_loc=ItemLoc.RS_SEND)

            # reset seed and first theta
            seed = random.choice([True, False])
            first_try = True
            first_theta = None

            time.sleep(2)
            if re.search('arena', Character().cur_loc()[0].lower()):
                sym_image = draw(captcha_scl, r, theta)
                save_img(image=sym_image, name="captcha", suffix="-failed",
                         folder_path=FolderPath.SAMPLE)
                if not master:
                    NPC(npc=npc_reset).click_npc()
                else:
                    NPC(npc=npc_master).click_npc()
                # check if reset has been blocked and wait
                reset_wait(read_message())
                time.sleep(3)
                continue
            break
        if first_try:
            first_theta = theta
            first_try = False
        if seed:
            click(_loc=ItemLoc.RS_LEFT, _click=rotate_n)
        else:
            click(_loc=ItemLoc.RS_RIGHT, _click=rotate_n)
    time.sleep(7)
    join_server()
    return True


def train_point():
    click(_loc=ItemLoc.MOVE_LEFT, _click=2, _interval=2)
    time.sleep(1)
    click(_loc=ItemLoc.MOVE_UP)


def train(character: Character, map_command=Command.ARENA11):
    if character.lvl == 600:
        print("Train Complete: Max LvL")
        return True
    chat(map_command)
    map_name = " ".join(re.findall("[a-zA-Z]+", map_command))
    time.sleep(3)
    if character.cur_loc()[0].lower() == map_name:
        train_point()
        while not character.check_max_lvl():
            pyautogui.mouseDown(x=ItemLoc.ATTACK_EVIL["x"],
                                y=ItemLoc.ATTACK_EVIL["y"])
            time.sleep(6)
        print("Train Complete: Max LvL")
        return True
    return False


def train_after_reset(character: Character):
    if character.cur_reset() > 0 or character.energy > 3000:
        return True
    click(_loc=ItemLoc.INVENTORY)
    box = Item(INVENTORY_SLOT)
    box.click_item(find=False, pick_up=True)
    box.click_item()
    click(_loc=ItemLoc.INVENTORY)

    box = Item(INVENTORY_SLOT)
    box.click_item(find=False, pick_up=True)
    box.click_item()

    if character.lvl <= 50:
        click(_loc=ItemLoc.SETTING)
        click(_loc=ItemLoc.CHANGE_SERVER)
        time.sleep(6)
        join_server("SPOT5")
        chat(Command.ARENA11)
        time.sleep(3)
        if character.cur_loc()[0].lower() == "arena":
            train_point()
            while 1 <= character.cur_lvl()["lvl"] <= 50:
                pyautogui.mouseDown(x=ItemLoc.ATTACK_HAND["x"],
                                    y=ItemLoc.ATTACK_HAND["y"])
                time.sleep(5)
            character.add_point(stat=Point.ENERGY)
        click(_loc=ItemLoc.SETTING)
        click(_loc=ItemLoc.CHANGE_SERVER)
    else:
        time.sleep(6)
        join_server("VIP5")
        chat(Command.ARENA11)
        train_point()
        while character.energy < 3000:
            pyautogui.mouseDown(x=ItemLoc.ATTACK_EVIL["x"],
                                y=ItemLoc.ATTACK_EVIL["y"])
            time.sleep(15)
            character.cur_stat()
            if character.agility < character.energy:
                character.add_point(Point.AGILITY)
            else:
                character.add_point(Point.ENERGY)
            time.sleep(0.5)
        return True
    return False
