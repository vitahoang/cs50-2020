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
    """
        Opens the MuAwaY app and enters full screen mode.
         Args:
            None
         Returns:
            bool: True if the app was successfully opened and full screen
            mode was entered, False otherwise.
         Raises:
            None
    """
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


def join_server(server="VIP4"):
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
        time.sleep(4)
        select_character()
        time.sleep(3)
        if check_screen(Screen.IN_GAME) == Screen.IN_GAME:
            return True
    except Exception as e:
        _raise(e)
    return False


def select_character(_char=ItemLoc.C_MAGIC):
    try:
        click(_loc=_char)
        click(_loc=ItemLoc.C_ENTER)
        time.sleep(3)
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
    """
    Takes a screenshot of a chat window and extracts the text from it.
     Returns:
        str: The extracted text with newlines removed.
     Raises:
        None
    """
    ss = screenshot()
    chat_window = ss[1500:1645, 800:1495]
    message = extract_text_from(chat_window).replace("\n", "")
    print(message)
    return message


def reset_wait(message):
    """
    Resets the wait time if the message contains 'missed the captcha'.
     Args:
        message (str): The message to check for the presence of 'missed the captcha'.
     Returns:
        None
     Raises:
        None
    """
    if re.search(r'missed the captcha', message):
        wait = re.findall(r'\d{1,2}', message)
        print(wait)
        if len(wait) == 2:
            time.sleep(int(wait[0]) * 60 + int(wait[1]))
            return True
    return False


def solve_captcha(master=False):
    global first_theta, last_theta

    # random seed to choose which side to rotate the captcha image
    seed = random.choice([True, False])

    while not re.search("Lorencia", Character().cur_loc()[0]):
        time.sleep(3)

        # crop and upscale the captcha
        crop = screenshot(region=(780, 1070, 1320, 1570))
        captcha_scl = upscale(crop)
        captcha_obj = remove(captcha_scl)
        r, theta = superm2(captcha_obj)

        # cache theta for the first try
        if not last_theta:
            last_theta = theta

        rotate_n = cal_rotate_n(theta, last_theta)
        last_theta = theta

        # from 2nd check, assign the theta after calculate the n of rotate
        print(r, theta)

        # if theta = 0 or 3.14, the captcha is at vertical symetry position
        if 0.00 <= theta <= 0.06 or theta == 3.14 or first_theta == theta:
            # check if captcha window is open
            if not Item(SUBMIT_CAPTCHA).find_item():
                if master:
                    NPC(npc=npc_master).click_npc()
                else:
                    NPC(npc=npc_reset).click_npc()

                # check if reset has been blocked and wait
                if not Item(SUBMIT_CAPTCHA).find_item():
                    if not reset_wait(read_message()):
                        break
                continue

            # submit captcha
            click(_loc=ItemLoc.RS_SEND)

            # reset seed and theta
            seed = random.choice([True, False])
            first_theta = None
            last_theta = None

            time.sleep(2)
            if not re.search('lorencia', Character().cur_loc()[0].lower()):
                sym_image = draw(captcha_scl, r, theta)
                save_img(image=sym_image, name="captcha", suffix="-failed",
                         folder_path=FolderPath.SAMPLE)
                time.sleep(3)
                continue
            sym_image = draw(captcha_scl, r, theta)
            save_img(image=sym_image, name="captcha", suffix="-success",
                     folder_path=FolderPath.SAMPLE)
            time.sleep(3)
            break
        if not first_theta:
            first_theta = theta
        if seed:
            click(_loc=ItemLoc.RS_LEFT, _click=rotate_n, _interval=0.3)
        else:
            click(_loc=ItemLoc.RS_RIGHT, _click=rotate_n, _interval=0.3)
    time.sleep(7)
    join_server()
    return True


def train_point_1():
    click(_loc=ItemLoc.MOVE_UP)
    time.sleep(1)


def train_point_2():
    click(_loc=ItemLoc.MOVE_LEFT)
    time.sleep(2)
    click(_loc=ItemLoc.MOVE_LEFT)
    time.sleep(2)
    click(_loc=ItemLoc.MOVE_LEFT)
    time.sleep(2)


def combo():
    pyautogui.mouseUp()
    pyautogui.mouseDown(x=ItemLoc.ATTACK_EVIL["x"],
                        y=ItemLoc.ATTACK_EVIL["y"])
    time.sleep(2)
    pyautogui.mouseUp()
    pyautogui.mouseDown(x=ItemLoc.ATTACK_TWISTING["x"],
                        y=ItemLoc.ATTACK_TWISTING["y"])
    time.sleep(5)


def combo_evil():
    pyautogui.mouseUp()
    pyautogui.mouseDown(x=ItemLoc.ATTACK_EVIL["x"],
                        y=ItemLoc.ATTACK_EVIL["y"])
    time.sleep(5)


def train(character: Character, map_command=Command.ARENA7):
    if character.lvl == 600:
        print("Train Complete: Max LvL")
        return True
    chat(map_command)
    map_name = " ".join(re.findall("[a-zA-Z]+", map_command))
    time.sleep(3)
    if character.cur_loc()[0].lower() == map_name:
        train_point_2()
        while not character.check_max_lvl():
            combo_evil()
            character.check_party()
        print("Train Complete: Max LvL")
        return True
    return False


def train_after_reset(character: Character):
    if character.cur_reset() > 0 or character.energy > 2000:
        return False

    # rearrange box after reset
    click(_loc=ItemLoc.INVENTORY)
    box = Item(INVENTORY_SLOT)
    box.click_item(find=False, pick_up=True)
    box.click_item()
    click(_loc=ItemLoc.INVENTORY)

    # first train to lv 50
    if character.lvl <= 50:
        chat(Command.ARENA11)
        time.sleep(3)
        if character.cur_loc()[0].lower() == "arena":
            train_point_1()
            while 1 <= character.cur_lvl()["lvl"] <= 50:
                pyautogui.mouseDown(x=ItemLoc.ATTACK_HAND["x"],
                                    y=ItemLoc.ATTACK_HAND["y"])
                time.sleep(10)
                character.check_party()
            character.add_point(stat=Point.ENERGY, p=400)
            character.add_point(stat=Point.AGILITY)

    # then train to level that has efficient points
    chat(Command.ARENA7)
    train_point_1()
    while character.energy < 2000:
        combo()
        time.sleep(10)
        character.cur_stat()
        if character.agility < 4000:
            character.add_point(Point.AGILITY)
        else:
            character.add_point(Point.ENERGY)
        time.sleep(2)
        character.check_party()
    return True
